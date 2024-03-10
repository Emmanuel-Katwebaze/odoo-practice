from odoo import fields, models, api, exceptions

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = "name"
    
    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types. Lower is better.")
    property_ids = fields.One2many("estate.property", "estate_property_id", string='Property')
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)            
        
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Type name must be unique!')
    ]
