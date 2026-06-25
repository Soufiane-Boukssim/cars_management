import io
import base64
from odoo import http
from odoo.http import request, Response
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


class CarWebsite(http.Controller):

    @http.route('/', auth='public', website=True)
    def homepage(self, **kw):
        cars = request.env['cars.car'].sudo().search([], limit=6)
        return request.render('cars_management.homepage_template', {
            'cars': cars
        })
    
    # @http.route('/cars', auth='public', website=True)
    # def car_list(self, **kw):
    #     cars = request.env['cars.car'].sudo().search([])
    #     return request.render('cars_management.car_list_template', {
    #         'cars': cars
    #     })
    
    @http.route('/cars', type='http', auth='public', website=True)
    def car_list(self, **kwargs):

        domain = []

        # FILTER BY BRAND
        if kwargs.get('brand'):
            domain.append(('brand', 'ilike', kwargs.get('brand')))

        # FILTER BY NAME
        if kwargs.get('name'):
            domain.append(('name', 'ilike', kwargs.get('name')))

        # FILTER BY PRICE
        if kwargs.get('max_price'):
            domain.append(('price', '<=', float(kwargs.get('max_price'))))

        cars = request.env['cars.car'].sudo().search(domain)

        return request.render('cars_management.car_list_template', {
            'cars': cars
        })

    @http.route('/cars/<int:car_id>', auth='public', website=True)
    def car_detail(self, car_id, **kw):

        car = request.env['cars.car'].sudo().browse(car_id)

        if not car.exists():
            return request.not_found()

        return request.render('cars_management.car_detail_template', {
            'car': car
        })
    
    @http.route('/contact', auth='public', website=True)
    def contact(self, **kw):

        car = False

        if kw.get('car_id'):
            car = request.env['cars.car'].sudo().browse(int(kw['car_id']))

        return request.render('cars_management.contact_template', {
            'car': car
        })
    

    @http.route('/contact/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def contact_submit(self, **post):

        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        message = post.get('message')
        car_id = post.get('car_id')
        price = post.get('')
        car_name = ""

        if car_id:
            car = request.env['cars.car'].sudo().browse(int(car_id))
            if car.exists():
                car_name = car.name

        body_html = f"""
            
            <div style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">

                <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f8; padding:20px 0;">
                    <tr>
                    <td align="center">

                ```
                    <!-- Card -->
                    <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:10px; overflow:hidden; box-shadow:0 4px 10px rgba(0,0,0,0.08);">

                    <!-- Header -->
                    <tr>
                        <td style="background:#0d47a1; padding:20px; color:white;">
                        <h2 style="margin:0; font-size:20px;"> New Car Request</h2>
                        <p style="margin:5px 0 0; font-size:13px; opacity:0.8;">A new customer submitted a request</p>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td style="padding:20px;">

                            <!-- Info Table -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse; font-size:14px;">
                                <tr>
                                <td style="padding:10px; font-weight:bold; color:#555;">Name</td>
                                <td style="padding:10px;">{name}</td>
                                </tr>
                                <tr style="background:#f9fafb;">
                                <td style="padding:10px; font-weight:bold; color:#555;">Email</td>
                                <td style="padding:10px;">{email}</td>
                                </tr>
                                <tr>
                                <td style="padding:10px; font-weight:bold; color:#555;">Phone</td>
                                <td style="padding:10px;">{phone}</td>
                                </tr>
                                <tr style="background:#f9fafb;">
                                <td style="padding:10px; font-weight:bold; color:#555;">Car</td>
                                <td style="padding:10px;">{car_name}</td>
                                </tr>
                            </table>

                            <!-- Message -->
                            <div style="margin-top:20px;">
                                <p style="margin-bottom:8px; font-weight:bold; color:#333;">Message</p>
                                <div style="background:#f1f5f9; padding:12px; border-radius:6px; color:#444; line-height:1.5;">
                                {message}
                                </div>
                            </div>

                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background:#f9fafb; padding:15px; text-align:center; font-size:12px; color:#888;">
                        Sent from your website • Car Request System
                        </td>
                    </tr>

                    </table>

                    </td>
                </tr>
                ```

                </table>

            </div>


        """

        mail = request.env['mail.mail'].sudo().create({
            'subject': f"New Car Request: {car_name}",
            'body_html': body_html,
            'email_to': f"{email},soufianeboukssim41@gmail.com",
            'email_from': "sfn@test.com",
        })

        mail.send()

    # 🟢 CRM LEAD (NOUVEAU)
        request.env['crm.lead'].sudo().create({
            'name': f"Car request - {car_name or 'No car'}",
            'expected_revenue': car.price if car else 0,
            'partner_name': name,
            'email_from': email,
            'phone': phone,
            'description': message,
            'car_id': car.id if car else False,
        })

        if car:
            quantity = int(post.get('quantity', 1))
            lead = request.env['crm.lead'].sudo().create({
                'name': "Website Car Request",
                'contact_name': post.get('name'),
                'email_from': post.get('email'),
                'phone': post.get('phone'),
                'description': message or "Website request",
            })
            command= request.env['cars.car.command'].sudo().create({
                'car_id': car.id,
                'description': message or "Website request",
                'quantity': quantity,
            })
            request.env['cars.car.command.line'].sudo().create({
                    'command_id': command.id,
                    'product_name': "Website request",
                    'quantity': 1,
                })
            request.env['cars.car.order'].sudo().create({
                    'car_id': car.id,
                    'lead_id': lead.id,
                    'quantity': quantity,
                })
        return request.redirect('/')
    

    @http.route('/cars/export/pdf', auth='public', website=True, type='http')
    def export_cars_pdf(self, **kw):

        # Voitures sans lead "Accepted"
        stage = request.env['crm.stage'].sudo().search([('name', '=', 'Accepted')], limit=1)

        if stage:
            accepted_car_ids = request.env['crm.lead'].sudo().search([
                ('stage_id', '=', stage.id),
                ('car_id', '!=', False),
            ]).mapped('car_id.id')

            cars = request.env['cars.car'].sudo().search([
                ('id', 'not in', accepted_car_ids)
            ])
        else:
            cars = request.env['cars.car'].sudo().search([])

        # Générer le PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1*cm, rightMargin=1*cm)
        styles = getSampleStyleSheet()
        story = []

        # Titre
        story.append(Paragraph("Available Cars", styles['Title']))
        story.append(Spacer(1, 20))

        # En-têtes
        data = [['Image', 'Brand', 'Name', 'Body Type', 'Fuel', 'Year', 'Color', 'Price ($)']]

        for car in cars:
            # ✅ Image: décoder le base64 stocké dans Odoo
            if car.image:
                try:
                    img_data = base64.b64decode(car.image)
                    img_buffer = io.BytesIO(img_data)
                    img = RLImage(img_buffer, width=2.5*cm, height=2*cm)
                except Exception:
                    img = Paragraph('No image', styles['Normal'])
            else:
                img = Paragraph('No image', styles['Normal'])

            data.append([
                img,
                car.brand or 'N/A',
                car.name or 'N/A',
                car.body_type or 'N/A',
                car.fuel_type or 'N/A',
                str(car.model_year) if car.model_year else 'N/A',
                car.color or 'N/A',
                str(car.price),
            ])

        col_widths = [3*cm, 2.5*cm, 3.5*cm, 2.5*cm, 2*cm, 1.8*cm, 2*cm, 2.2*cm]

        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, 0),  colors.HexColor('#0d47a1')),
            ('TEXTCOLOR',     (0, 0), (-1, 0),  colors.white),
            ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
            ('FONTSIZE',      (0, 0), (-1, 0),  10),
            ('ROWBACKGROUNDS',(0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
            ('FONTSIZE',      (0, 1), (-1, -1), 8),
            ('GRID',          (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING',       (0, 0), (-1, -1), 5),
            # Hauteur de ligne pour les images
            ('ROWHEIGHT',     (0, 1), (-1, -1), 2.2*cm),
        ]))

        story.append(table)
        doc.build(story)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        return Response(
            pdf_bytes,
            content_type='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename="available_cars.pdf"',
                'Content-Length': str(len(pdf_bytes)),
            }
        )

