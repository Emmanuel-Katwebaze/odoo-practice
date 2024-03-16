from odoo import fields, models

class Supplier(models.Model):
    _name = 'liquor_store.supplier'
    _description = 'Supplier'
    
    name = fields.Char('Supplier Name')
    phone_number = fields.Char('Phone Number')
    address = fields.Char('Location')
    
class SupplierTransaction(models.Model):
    _name = 'liquor_store.supplier_transaction'
    _description = 'Supplier Transaction'
    
    supplier = fields.Many2one('liquor_store.supplier', 'Supplier', required=True)
    brand = fields.Char('Brand', required=True)
    #brand = fields.Many2one('liquor_store.brand', 'Brand', required=True)
    order_date = fields.Datetime('Order Date', default=fields.Datetime.now, required=True)
    delivery_date = fields.Datetime('Delivery Date')
    unit_price = fields.Float('Unit Price', required=True)
    amount = fields.Float('Amount', required=True)
    date_received = fields.Date('Date Received')
    status = fields.Selection([('completed', 'Completed'), ('pending', 'Pending')], 'Status', required=True)
    