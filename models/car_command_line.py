from odoo import models, fields

class CarCommandLine(models.Model):
    _name = 'cars.car.command.line'
    _description = 'Car Command Line'

    command_id = fields.Many2one('cars.car.command')
    product_name = fields.Char()
    quantity = fields.Integer(default=1)