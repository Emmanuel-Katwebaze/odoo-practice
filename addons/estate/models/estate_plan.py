from odoo import fields, models, api, tools
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id desc"
    
    name = fields.Char(required=True)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string='Offers')
    active = fields.Boolean(default=False)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=True, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer(compute="_compute_best_price")
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West'),])
    state = fields.Selection(string='State', selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], required=True, copy=False, default='new')
    estate_property_id = fields.Many2one("estate.property.type")
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends('expected_price', 'offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = record.expected_price
            for offer in record.offer_ids:
                if offer.price > record.best_price:
                    record.best_price = offer.price
                    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and record.selling_price < (record.expected_price * 0.9):
                raise ValidationError("Selling price must be at least than 90% of the expected price. You must reduce the accepted price if you want to accept this offer")
                
    def action_cancel(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Property is already canceled")
            else:
                record.state = "canceled"
                
    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled Properties cannot be sold")
            else:
                record.state = "sold"
