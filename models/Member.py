from odoo import api, fields, models


class Member(models.Model):
    _name = 'bookstore.member'
    _description = 'New Description'

    id_member = fields.Char(string='ID Member', readonly=True, required=True, copy=False, default='New')    
    @api.model
    def create(self, vals):
        if vals.get('id_member', 'New') == 'New':
            vals['id_member'] = self.env['ir.sequence'].next_by_code(
                'bookstore.member') or 'New'
        result = super(Member,self).create(vals)
        return result  
    
    name = fields.Char(string='Nama Member')
    alamat = fields.Char(string='Alamat')
    kode_pos = fields.Char(string='Kode Pos')
    no_telp = fields.Integer(string='Phone number')
    email = fields.Char(string='Email')
    img_profile = fields.Binary(string='Gambar Profile')
    
    
