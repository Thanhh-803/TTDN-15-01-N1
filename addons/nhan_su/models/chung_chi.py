from odoo import models, fields, api


class ChungChi(models.Model):
    _name = 'chung_chi'
    _description = 'Bảng chứa thông tin về chứng chỉ của nhân viên'
    _rec_name = 'loai_chung_chi'
    
    loai_chung_chi = fields.Selection([
        ("dai_hoc", "Bằng đại học"),
        ("cao_dang", "Bằng cao đẳng"),
        ("trung_cap", "Bằng trung cấp"),
        ("chung_chi", "Chứng chỉ")
    ], string="Loại chứng chỉ", required=True)
    ngay_cap = fields.Date("Ngày cấp")
    noi_cap = fields.Char("Nơi cấp")
    ngay_het_han = fields.Date("Ngày hết hạn")
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên")