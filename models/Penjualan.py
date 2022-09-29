from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models


class Penjualan(models.Model):
    _name = 'bookstore.penjualan'
    _description = 'New Description'

    name = fields.Char(string='Kode nota', readonly=True, required=True, copy=False, default='New')
    tanggal_pembelian = fields.Date(string='Tanggal Pembelian', default=fields.Datetime.now())
    total_pembayaran = fields.Integer(compute='_compute_totalbayar', string='Total Pembayaran')

    DetailsPenjualanBuku_id = fields.One2many( string='Details Penjualan',
                                               comodel_name='bookstore.detailpenjualanbuku',
                                               inverse_name='PenjualanBuku_id')
    
    DetailsPenjualanPerlengkapan_id = fields.One2many( string='Details Penjualan',
                                               comodel_name='bookstore.detailpenjualanperlengkapan',
                                               inverse_name='PenjualanPerlengkapan_id')

    
    state = fields.Selection(
        string='Status',
        selection=[('draft', 'DRAFT'),
                   ('done', 'DONE'),
                   ('cancelled', 'CANCELLED'),
                   ],
        required=True, readonly=True, default='draft')
    
    id_member = fields.Char(string='ID Member', compute="_compute_id_member", required=False)
    diskon = fields.Char(string='Diskon')

    def action_draft(self):
        self.write({ 'state': 'draft'})

    def action_done(self):
        self.write({ 'state': 'done'})

    def action_cancelled(self):
        self.write({ 'state': 'cancelled'})

    def _compute_totalbayar(self):
        for rec in self:
            a = sum(self.env['bookstore.detailpenjualanbuku'].search([('PenjualanBuku_id', '=', rec.id)]).mapped('Subtotal'))
            b = sum(self.env['bookstore.detailpenjualanperlengkapan'].search([('PenjualanPerlengkapan_id', '=', rec.id)]).mapped('Subtotal'))
            rec.total_pembayaran = a + b
    #--------------------------------------------------------- BUKU ---------------------------------------------------------#   
    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise UserError("Tidak dapat menghapus jika status BUKAN DRAFT")
        else:
            if self.DetailsPenjualanBuku_id:
                a = []
                for rec in self:
                    a = self.env['bookstore.detailpenjualanbuku'].search([('PenjualanBuku_id', '=', rec.id)])
                    print(a)
                for ob in a:
                    print(str(ob.Buku_id.name) + ' ' + str(ob.qty))
                    ob.Buku_id.stock += ob.qty
            record = super(Penjualan, self).unlink()        

    def write(self, vals):
        for rec in self:
            a = self.env['bookstore.detailpenjualanbuku'].search([('PenjualanBuku_id', '=', rec.id)])
            for data in a:
                data.Buku_id.stock += data.qty
        record = super(Penjualan,self).write(vals)
        for rec in self: 
            b = self.env['bookstore.detailpenjualanbuku'].search([('PenjualanBuku_id', '=', rec.id)])
            for databaru in b:
                if databaru in a:
                    databaru.Buku_id.stock -= databaru.qty
                else:
                    pass
        return record

    @api.onchange('state')
    def onchange_state(self):     
        if (self.state == 'cancelled'):
            a = []
            for rec in self:
                a = self.env['bookstore.detailpenjualanbuku'].search([('PenjualanBuku_id', '=', rec.id)])
                print(a)
            for ob in a:
                print(str(ob.Buku_id.name) + ' ' + str(ob.qty))
                ob.Buku_id.stock += ob.qty
    #------------------------------------------------------ PERLENGKAPAN ------------------------------------------------------#
    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise UserError("Tidak dapat menghapus jika status BUKAN DRAFT")
        elif self.filtered(lambda line: line.state != 'cancelled'):
            if self.DetailsPenjualanPerlengkapan_id:
                a = []
                for rec in self:
                    a = self.env['bookstore.detailpenjualanperlengkapan'].search([('PenjualanPerlengkapan_id', '=', rec.id)])
                    print(a)
                for ob in a:
                    print(str(ob.Perlengkapan_id.name) + ' ' + str(ob.qty))
                    ob.Perlengkapan_id.stock += ob.qty
            record = super(Penjualan, self).unlink()
        else:
            if self.DetailsPenjualanPerlengkapan_id:
                a = []
                for rec in self:
                    a = self.env['bookstore.detailpenjualanperlengkapan'].search([('PenjualanPerlengkapan_id', '=', rec.id)])
                    print(a)
                for ob in a:
                    print(str(ob.Perlengkapan_id.name) + ' ' + str(ob.qty))
                    ob.Perlengkapan_id.stock += ob.qty
            record = super(Penjualan, self).unlink()
    
    def write(self, vals):
        for rec in self:
            a = self.env['bookstore.detailpenjualanperlengkapan'].search([('PenjualanPerlengkapan_id', '=', rec.id)])
            for data in a:
                data.Perlengkapan_id.stock += data.qty
        record = super(Penjualan,self).write(vals)
        for rec in self: 
            b = self.env['bookstore.detailpenjualanperlengkapan'].search([('PenjualanPerlengkapan_id', '=', rec.id)])
            for databaru in b:
                if databaru in a:
                    databaru.Perlengkapan_id.stock -= databaru.qty
                else:
                    pass
        return record

    @api.constrains('name')
    def check (self):
        for rec in self:
            if not rec.name:
                raise ValidationError("No.Nota tidak boleh kosong")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'bookstore.penjualan') or 'New'
        result = super(Penjualan,self).create(vals)
        return result    

    _sql_constraints = [
        ('unique_no_nota', 'unique (name)', 'No.Nota tidak boleh sama !!!!')
    ]

class DetailsPenjualanBuku_id(models.Model):
    _name = 'bookstore.detailpenjualanbuku'
    _description = 'Detail trasaksi penjualan buku dan perlengkapan'

    harga = fields.Integer(string='Harga')
    qty = fields.Integer(string='Jumlah')
    
    PenjualanBuku_id = fields.Many2one(comodel_name='bookstore.penjualan', string='Details Penjualan Buku')
    Buku_id = fields.Many2one(comodel_name='bookstore.book', string='Judul Buku')
    
    Subtotal = fields.Integer(compute='_compute_Subtotal', string='Subtotal')    
    @api.depends('harga','qty')
    def _compute_Subtotal(self):
        for rec in self:
            rec.Subtotal = rec.qty * rec.harga

    @api.onchange('Buku_id')
    def onchange_Buku_id(self):
        if (self.Buku_id.harga_jual):
            self.harga = self.Buku_id.harga_jual

    @api.model
    def create(self, vals):
        record = super(DetailsPenjualanBuku_id,self).create(vals)
        if record.qty:
            self.env['bookstore.book'].search([('id', '=', record.Buku_id.id)]).write({'stock' : record.Buku_id.stock - record.qty})
        if record.Buku_id.stock < 1:
            self.env['bookstore.book'].search([('id', '=', record.Buku_id.id)]).write({'state' : 'sold_out'})
        if record.Buku_id.stock > 1:
            self.env['bookstore.book'].search([('id', '=', record.Buku_id.id)]).write({'state' : 'ready'})
        return record

    @api.constrains('qty')
    def check(self):
        for rec in self:
            if (rec.Buku_id.stock < 1):
                raise ValidationError("Maaf stock Untuk {} sedang tidak tersedia !!".format(rec.Buku_id.name))
            elif (rec.Buku_id.stock < rec.qty):
                raise ValidationError("Stock Untuk {} hanya tersedia {}".format(rec.Buku_id.name,rec.Buku_id.stock))
            elif (rec.Buku_id.state == 'pemesanan'):
                raise ValidationError("Maaf untuk Buku {} belum tersedia di toko kami !!".format(rec.Buku_id.name))

class DetailsPenjualanPerlengkapan_id(models.Model):
    _name = 'bookstore.detailpenjualanperlengkapan'
    _description = 'Detail trasaksi penjualan buku dan perlengkapan'

    harga = fields.Integer(string='Harga')
    qty = fields.Integer(string='Jumlah')
    
    PenjualanPerlengkapan_id = fields.Many2one(comodel_name='bookstore.penjualan', string='Details Penjualan Buku')
    Perlengkapan_id = fields.Many2one(comodel_name='bookstore.perlengkapan', string='Nama Barang')
    
    Subtotal = fields.Integer(compute='_compute_Subtotal', string='Subtotal')    
    @api.depends('harga','qty')
    def _compute_Subtotal(self):
        for rec in self:
            rec.Subtotal = rec.qty * rec.harga

    @api.onchange('Perlengkapan_id')
    def onchange_Buku_id(self):
        if (self.Perlengkapan_id.harga_jual):
            self.harga = self.Perlengkapan_id.harga_jual

    @api.model
    def create(self, vals):
        record = super(DetailsPenjualanPerlengkapan_id,self).create(vals)
        if record.qty:
            self.env['bookstore.perlengkapan'].search([('id', '=', record.Perlengkapan_id.id)]).write({'stock' : record.Perlengkapan_id.stock - record.qty})
        if record.Perlenkapan_id.stock < 1:
            self.env['bookstore.perlengkapan'].search([('id', '=', record.Perlengkapan_id.id)]).write({'state' : 'sold_out'})
        if record.Perlengkapan_id.stock > 1:
            self.env['bookstore.perlengkapan'].search([('id', '=', record.Perlengkapan_id.id)]).write({'state' : 'ready'})
        return record

    @api.constrains('qty')
    def check(self):
        for rec in self:
            if (rec.Perlengkapan_id.stock < 1):
                raise ValidationError("Maaf stock Untuk {} sedang tidak tersedia !!".format(rec.Perlengkapan_id.name))
            elif (rec.Perlengkapan_id.stock < rec.qty):
                raise ValidationError("Stock Untuk {} hanya tersedia {}".format(rec.Perlengkapan_id.name,rec.Perlengkapan_id.stock))
            elif (rec.Perlengkapan_id.state == 'pemesanan'):
                raise ValidationError("Maaf untuk Buku {} belum tersedia di toko kami !!".format(rec.Perlengkapan_id.name))