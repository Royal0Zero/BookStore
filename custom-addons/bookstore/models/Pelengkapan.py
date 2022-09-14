from odoo import api, fields, models


class Perlengkapan(models.Model):
    _name = 'bookstore.perlengkapan'
    _description = 'New Description'

    name = fields.Char(string='Nama Barang')
    description = fields.Html(string='Description Barang')
    satuan = fields.Selection(string='Jenis Satuan',
                            selection=[('Satuan', 'Satuan'), 
                                       ('Pak', 'Pak')])
    harga_jual = fields.Integer(string='Harga')
    stock = fields.Integer(string='Stocks')
    img_perlengkapan = fields.Binary(string='Gambar Perlengkapan')

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