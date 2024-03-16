# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'liquor_store',
    'depends' : ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/liquor_store_brand.xml',
        'views/liquor_store_bottles.xml',
        'views/liquor_store_shots.xml',
        'views/liquor_store_supplier.xml',
        'views/liquor_store_supplier_transaction.xml',
        'views/liquor_store_menus.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}