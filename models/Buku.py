import re
from time import sleep
from odoo import api, fields, models


class Buku(models.Model):
    _name = 'bookstore.book'
    _description = 'New Description'

    
    name = fields.Char(string='Judul Buku')
    nama_pengarang = fields.Char(string='Nama Pengarang')
    tahun = fields.Char(string='Tahun')
    sinopsis = fields.Html(string='Sinopsis Buku')
    img_buku = fields.Image('Gambar Buku')
    harga_jual = fields.Integer(string='Harga')

    stock = fields.Integer(string='Stock')

    Publisher_id = fields.Many2one(comodel_name='bookstore.publisher', string='Publisher')

    TypeBuku_id = fields.Many2one(comodel_name='bookstore.booktype', 
                                        string='Type Buku', 
                                        ondelete='cascade')
    state = fields.Selection(
        string='Status',
        selection=[('pemesanan', 'PEMESANAN'),
                   ('ready', 'READY'),
                   ('sold_out', 'SOLD OUT'),
                   ],
        required=True, readonly=True, default='sold_out')

    def action_pemesanan(self):
        self.write({ 'state': 'pemesanan'})

    def action_ready(self):
        self.write({ 'state': 'ready'})

    def action_sold(self):
        self.write({ 'state': 'sold_out'})