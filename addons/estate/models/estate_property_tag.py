from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = "name"

    name = fields.Char(required=True, unique=True)   
    color = fields.Integer()
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Tag name must be unique!')
    ]
    
    
