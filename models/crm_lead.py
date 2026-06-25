from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    car_id = fields.Many2one('cars.car', string="Car")

    car_id = fields.Many2one('cars.car')