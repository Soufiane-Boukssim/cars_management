from odoo import models,fields

class CarFeature(models.Model):
    _name = 'cars.car.feature'
    _description = 'Car Feature'

    name = fields.Char(required=True)