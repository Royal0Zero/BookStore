from odoo import api, fields, models


class ToolsBuku(models.TransientModel):
    _name = 'bookstore.toolsbuku'

    Buku_id = fields.Many2one(comodel_name='bookstore.book', 
                                        string='Daftar Buku')
