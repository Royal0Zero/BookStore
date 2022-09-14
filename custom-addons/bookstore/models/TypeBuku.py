from odoo import api, fields, models

class TypeBuku(models.Model):
    _name = 'bookstore.booktype'
    _description = 'New Description'

    name = fields.Selection(string='Jenis Buku',
                            selection=[('Cerpen', 'Cerpen'), 
                                       ('Novel', 'Novel'), 
                                       ('Sekolah', 'Sekolah')])

    Kode_Type = fields.Char(string='Kode Type Buku')
    @api.onchange('name')
    def _compute_field_name(self):
        if (self.name == 'Cerpen'):
            self.Kode_Type = 'CP0001'
        elif (self.name == 'Novel'):
            self.Kode_Type = 'NV0002'
        elif (self.name == 'Sekolah'):
            self.Kode_Type = 'SK0003'

    Buku_id = fields.One2many(comodel_name='bookstore.book', 
                                inverse_name='TypeBuku_id', 
                                string='Daftar Buku')

    Jumlah_Item = fields.Char(compute='_compute_jumlah_item', string='Jumlah Produk')
    @api.depends('Buku_id')
    def _compute_jumlah_item(self):
        for rec in self:
            a = self.env['bookstore.book'].search([('TypeBuku_id', '=' , rec.id)]).mapped('name')
            b = len(a)
            rec.Jumlah_Item = b