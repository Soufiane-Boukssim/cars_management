from odoo import http
from odoo.http import request


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

        cars = request.env['cars.car'].search(domain)

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
        })

        return request.redirect('/')