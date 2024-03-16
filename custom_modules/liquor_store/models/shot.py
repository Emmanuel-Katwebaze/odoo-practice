from odoo import fields, models, api

class Shot(models.Model):
    _name = 'liquor_store.shot'
    _description = 'Shot'
    
    bottle = fields.Many2one('liquor_store.bottle', 'Bottle', required=True)
    bottle_brand = fields.Char(compute='_compute_bottle_brand')
    size = fields.Integer('Shot Size', required=True)
    unit_price = fields.Integer('Unit Price', required=True)
    quantity = fields.Integer('Quantity', required=True)
    bottle_serial_number = fields.Char(related='bottle.serial_number', string='Bottle Serial Number', readonly=True)
    
    @api.depends('bottle')
    def _compute_bottle_brand(self):
        for record in self:
            record.bottle_brand = record.bottle.brand.name
            
