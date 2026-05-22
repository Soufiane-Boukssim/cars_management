from odoo import models,fields

class Car(models.Model):
    _name = 'cars.car'
    _description = 'Car'
    name = fields.Char(string= "Car Name", required= True)

    brand = fields.Char(string="Brand")
    
    body_type = fields.Selection(
        [
            ('sedan', 'Sedan'),
            ('coupe', 'Coupe'),
            ('suv', 'SUV')
        ]
        , string="Body Type"
    )   
    
    fuel_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ], string="Fuel Type") 
    
    feature_ids = fields.Many2many('cars.car.feature',string="Features")
    
    brand_country = fields.Selection(
        [
            ("US","United States"),
            ("JP","Japan"),
            ("DE","Germany"),
            ("FR","France"),
            ("ES","Spain"),
            ("IT","Italy"),
            ("GB","United Kingdom"),
            ("CN","China"),
            ("KR","South Korea"),
        ]
        ,string="Brand Country")
    
    model_year = fields.Integer(string="Model Year")
    
    color = fields.Selection(
        [
            ("red","Red"),
            ("blue","Blue"),
            ("black","Black"),
            ("white","White"),
            ("gray","Gray"),
        ]
        ,string="Color")
    
    price = fields.Integer(string="Price (mad)")

    distance = fields.Integer(string="Distance Driven (km)")

    owners_count = fields.Integer(string="Number Of Owners")

    cylinders = fields.Integer(string="Number Of Cylinders")

    is_damaged = fields.Boolean(string="Is Damaged")

    # 🖼️ MAIN IMAGE
    image = fields.Image(string="Main Image")

    # 📸 GALLERY
    image_ids = fields.One2many( # que One2many dépend toujours de Many2one
        'cars.car.image',
        'car_id',
        string="Images"
    )

