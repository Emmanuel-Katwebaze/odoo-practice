from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = "name"
    
    name = fields.Char(required = True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types. Lower is better.")
    property_ids = fields.One2many("estate.property.property", "property_id", string='Offers')
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Type name must be unique!')
    ]
