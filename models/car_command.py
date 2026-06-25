from odoo import models, fields

class CarCommand(models.Model):
    _name = 'cars.car.command'
    _description = 'Car Command'

    car_id = fields.Many2one('cars.car', string="Car")
    line_ids = fields.One2many('cars.car.command.line', 'command_id')
    description = fields.Text(string="Description")
    quantity = fields.Integer(default=1)