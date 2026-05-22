from odoo import models,fields

class CarImage(models.Model):
    _name = 'cars.car.image'
    _description = 'Car Images'

    car_id = fields.Many2one('cars.car', string="Car")
    image = fields.Image(string="Image")
