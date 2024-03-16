from odoo import fields, models, api

class Bottle(models.Model):
    _name = 'liquor_store.bottle'
    _description = 'Bottle'
    
    brand = fields.Many2one('liquor_store.brand', 'Brand', required=True)
    serial_number = fields.Char('Serial Number')
    size = fields.Float('Bottle Size', required=True)
    purchase_date = fields.Date('Purchase Date', default=fields.Date.today())
    purchase_cost = fields.Integer('Purchase Cost', required=True)
    selling_price = fields.Integer('Selling Price')
    status = fields.Selection(string = 'Status', selection=[('available', 'Available'), ('sold', 'Sold')], default='available')
