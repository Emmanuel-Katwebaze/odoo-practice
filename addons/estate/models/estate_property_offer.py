from datetime import timedelta
from odoo import fields, models, api, exceptions

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "id,price"
    
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive'),
    ]    
    
    price = fields.Float()
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', related='property_id.estate_property_id', store=True)
    
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
                record.property_id.state = 'offer_accepted'
                
    def action_refuse(self):
        for record in self:
            if record.status != 'refused':
                record.status = 'refused'
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'new'
                
    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        price = vals.get('price')
        
        existing_offer = self.search([('property_id', '=', property_id), ('price', '>', price)], limit=1)
        if existing_offer:
            raise exceptions.ValidationError("Cannot create offer with lower amount than existing offer.")
        
        property_obj = self.env['estate.property'].browse(property_id)
        property_obj.state = 'offer_received'
        
        return super().create(vals)
    
    def write(self, vals):
        property_id = vals.get('property_id')
        price = vals.get('price')
        
        existing_offer = self.search([('property_id', '=', property_id), ('price', '>', price)], limit=1)
        if existing_offer:
            raise exceptions.ValidationError("Cannot update offer with lower amount than existing offer.")
        
        return super().write(vals)
    
    
    
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
                record.property_id.state = 'offer_accepted'
                
    def action_refuse(self):
        for record in self:
            if record.status != 'refused':
                record.status = 'refused'
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'new'
    
    
    
    
