from odoo import models, fields


class Car(models.Model):
    _name = 'cars.car'
    _description = 'Car'

    name = fields.Char(string="Car Name", required=True)

    # FIX: default='' prevents False being returned when field is empty
    brand = fields.Char(string="Brand", default='')

    body_type = fields.Selection(
        [
            ('sedan', 'Sedan'),
            ('coupe', 'Coupe'),
            ('suv', 'SUV'),
            ('cabriolet', 'Cabriolet'),
        ],
        string="Body Type"
    )

    fuel_type = fields.Selection(
        [
            ('petrol', 'Petrol'),
            ('diesel', 'Diesel'),
            ('electric', 'Electric'),
            ('hybrid', 'Hybrid'),
        ],
        string="Fuel Type"
    )

    feature_ids = fields.Many2many('cars.car.feature', string="Features")

    brand_country = fields.Selection(
        [
            ("US", "United States"),
            ("JP", "Japan"),
            ("DE", "Germany"),
            ("FR", "France"),
            ("ES", "Spain"),
            ("IT", "Italy"),
            ("GB", "United Kingdom"),
            ("CN", "China"),
            ("KR", "South Korea"),
        ],
        string="Brand Country"
    )

    model_year = fields.Integer(string="Model Year")

    color = fields.Selection(
        [
            ("red", "Red"),
            ("blue", "Blue"),
            ("black", "Black"),
            ("white", "White"),
            ("gray", "Gray"),
        ],
        string="Color"
    )

    price = fields.Integer(string="Price ($)")

    distance = fields.Integer(string="Distance Driven (km)")

    owners_count = fields.Integer(string="Number Of Owners")

    cylinders = fields.Integer(string="Number Of Cylinders")

    is_damaged = fields.Boolean(string="Is Damaged")

    # Main image
    image = fields.Image(string="Main Image")

    # Gallery
    image_ids = fields.One2many(
        'cars.car.image',
        'car_id',
        string="Images"
    )

    state = fields.Selection(
        [
            ('available', 'Available'),
            ('sold', 'Sold'),
        ],
        default='available',
        string="Status"
    )

    def action_sell(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sell Car',
            'res_model': 'car.sell.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,
            }
        }

    def action_confirm(self):
        return True