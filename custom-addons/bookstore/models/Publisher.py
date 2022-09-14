from odoo import api, fields, models


class Publisher(models.Model):
    _name = 'bookstore.publisher'
    _description = 'New Description'

    name = fields.Char(string='Name')
    alamat = fields.Char(string='Alamat')
    no_telp = fields.Char(string='No Telphone')
    no_tax = fields.Char(string='No Tax')
    email = fields.Char(string='Email')  

    Buku_id = fields.One2many(comodel_name='bookstore.book', 
                                inverse_name='Publisher_id', 
                                string='Daftar Buku')
