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
            <div>
                <h3>New Car Request</h3>

                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Phone:</b> {phone}</p>
                <p><b>Car:</b> {car_name}</p>
                <p><b>Message:</b><br/>{message}</p>
            </div>
        """

        mail = request.env['mail.mail'].sudo().create({
            'subject': f"New Car Request: {car_name}",
            'body_html': body_html,
            'email_to': email,
            'email_from': "no-reply@test.com",
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