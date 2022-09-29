from odoo import api, fields, models


class ReportXlsx(models.AbstractModel):
    _name = 'report.bookstore.report_buku_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    Tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, barang):
        sheet = workbook.add_worksheet('Daftar Buku')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Tanggal : ' + str(self.Tgl_lap), bold)
        sheet.write(2, 1, 'Judul Buku', bold)
        sheet.write(2, 2, 'Nama Pengarang', bold)
        sheet.write(2, 3, 'Tahun', bold)
        sheet.write(2, 4, 'Publisher', bold)
        sheet.write(2, 5, 'Stock', bold)
        row = 4
        col = 1
        for obj in barang:
            sheet.write(row, col, obj.name, bold)
            sheet.write(row, col+1, str(obj.nama_pengarang))
            sheet.write(row, col+2, str(obj.tahun))
            sheet.write(row, col+3, str(obj.Publisher_id.name))
            sheet.write(row, col+4, str(obj.stock))            
            row += 1
