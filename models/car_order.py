from odoo import models, fields

class CarOrder(models.Model):
    _name = 'cars.car.order'
    _description = 'Car Order'

    car_id = fields.Many2one('cars.car', string="Car", required=True)
    lead_id = fields.Many2one('crm.lead', string="Lead")

    quantity = fields.Integer(string="Quantity", default=1)

    lead_name = fields.Char(related='lead_id.contact_name', store=True)
    lead_email = fields.Char(related='lead_id.email_from', store=True)
    car_name = fields.Char(related='car_id.name', store=True)