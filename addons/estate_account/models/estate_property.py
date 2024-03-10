from odoo import fields, models

class EstatePropertyAccount(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        # Create an empty account.move
        move = self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice'
        })
        
        # Add invoice lines
        move.write({
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Selling Price',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00
                })
            ]
        })
        
        return super().action_sold()
    
    
    