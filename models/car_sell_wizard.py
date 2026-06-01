from odoo import models, fields

class CarSellWizard(models.TransientModel):
    _name = 'car.sell.wizard'
    _description = 'Sell Car Wizard'

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone Number")
    message = fields.Text(string="Message")

    def confirm_sell(self):
        active_id = self.env.context.get('active_id')
        car = self.env['cars.car'].browse(active_id)

        car.state = 'sold'

        # email + crm + log
        self._send_email(car)
        self._create_crm(car)

        return {'type': 'ir.actions.act_window_close'}
    
    def _send_email(self, car):
        body_html = f"""
            <div>
                <h2>New Car Request</h2>
                <p><b>Name:</b> {self.name}</p>
                <p><b>Email:</b> {self.email}</p>
                <p><b>Phone:</b> {self.phone}</p>
                <p><b>Car:</b> {car.name}</p>
                <p><b>Message:</b> {self.message}</p>
            </div>
        """

        self.env['mail.mail'].sudo().create({
            'subject': f"New Car Request: {car.name}",
            'body_html': body_html,
            'email_to': f"{self.email},sfn@test.com",
            'email_from': "sfn@test.com",
        }).send()    

    def _create_crm(self, car):
        stage = self.env['crm.stage'].sudo().search([
            ('name', '=', 'Accepted')
        ], limit=1)

        self.env['crm.lead'].sudo().create({
            'name': f"Car request - {car.name}",
            'expected_revenue': car.price,
            'partner_name': self.name,
            'email_from': self.email,
            'phone': self.phone,
            'description': self.message,
            'stage_id': stage.id if stage else False,
        })