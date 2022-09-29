from odoo import api, fields, models


class ToolsPerlengkapan(models.TransientModel):
    _name = 'bookstore.toolsperlengkapan'
    _description = 'New Description'

    Perlengkapan_id = fields.Many2one(comodel_name='bookstore.perlengkapan', 
                                      string='Perlengkapan')
    
