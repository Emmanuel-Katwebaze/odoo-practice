from odoo import fields, models

class Brand(models.Model):
    _name = 'liquor_store.brand'
    _description = 'Brand'
    
    name = fields.Char('Brand Name', required=True)
    description = fields.Text('Description', required=True)
    quantity = fields.Integer('Quantity', required=True)
