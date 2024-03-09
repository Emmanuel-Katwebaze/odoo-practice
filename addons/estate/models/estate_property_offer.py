from datetime import timedelta
from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "id price"
    
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive'),
    ]    
    
    price = fields.Float()
    status = fields.Selection(string = 'Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string = 'Partner', required = True)
    property_id = fields.Many2one('estate.property', string = 'Property', required = True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
                
    def action_accept(self):
        for record in self:
            if record.status != 'accepted':
                record.status = 'accepted'
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
                
    def action_refuse(self):
        for record in self:
            if record.status != 'refused':
                record.status = 'refused'
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
    
    
    
    
