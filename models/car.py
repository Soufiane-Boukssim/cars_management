from odoo import models, fields


class Car(models.Model):
    _name = 'cars.car'
    _description = 'Car'
    _inherit = ['mail.thread', 'mail.activity.mixin']
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
        string="Status",
        tracking=True
    )

    date_start = fields.Datetime(string="Start Date")
    date_end = fields.Datetime(string="End Date")

    lead_count = fields.Integer(compute="_compute_lead_count")

    def _compute_lead_count(self):
        stage = self.env['crm.stage'].sudo().search([
            ('name', '=', 'Accepted')
        ], limit=1)

        leads = self.env['crm.lead'].sudo().search([
            ('car_id', 'in', self.ids)
        ])

        grouped = {}
        accepted_grouped = {}

        for lead in leads:
            grouped[lead.car_id.id] = grouped.get(lead.car_id.id, 0) + 1

            if stage and lead.stage_id.id == stage.id:
                accepted_grouped[lead.car_id.id] = accepted_grouped.get(lead.car_id.id, 0) + 1

        for car in self:
            car.lead_count = grouped.get(car.id, 0)

    def action_view_leads(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Leads',
            'res_model': 'crm.lead',
            'view_mode': 'list,form',
            'domain': [('car_id', '=', self.id)],
        }

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
    
    has_accepted_lead = fields.Boolean(
        compute='_compute_has_accepted_lead',
        store=False
    )


    def _compute_has_accepted_lead(self):
        stage = self.env['crm.stage'].sudo().search([
            ('name', '=', 'Accepted')
        ], limit=1)

        if not stage:
            for car in self:
                car.has_accepted_lead = False
            return

        lead_map = {}

        leads = self.env['crm.lead'].sudo().search([
            ('car_id', 'in', self.ids),
            ('stage_id', '=', stage.id)
        ])

        for lead in leads:
            lead_map[lead.car_id.id] = True

        for car in self:
            car.has_accepted_lead = lead_map.get(car.id, False)

    def action_export_pdf(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/cars/export/pdf',
            'target': 'new',
        }
