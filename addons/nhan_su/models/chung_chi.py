from odoo import models, fields, api
from datetime import date


class ChungChi(models.Model):
    _name = 'chung_chi'
    _description = 'Bảng chứa thông tin về chứng chỉ của nhân viên'
    _rec_name = 'nhan_vien_id'
    

    ten_chung_chi = fields.Char("Tên chứng chỉ", required=True)
    loai_chung_chi = fields.Selection([
        ("ngoai_ngu", "Chứng chỉ ngoại ngữ"),
        ("tin_hoc", "Chứng chỉ tin học văn phòng"),
        ("nghe_nghiep", "Chứng chỉ nghề nghiệp"),
        ("noi_bo", "Chứng chỉ nội bộ"),
        ("quoc_te", "Chứng chỉ quốc tế")
    ], string="Loại chứng chỉ", required=True)
    ngay_cap = fields.Date("Ngày cấp")
    ngay_het_han = fields.Date("Ngày hết hạn")
    cap_boi = fields.Char("Cấp bởi")
    trang_thai = fields.Selection([
        ("con_hieu_luc", "Còn hiệu lực"),
        ("het_han", "Hết hạn"),
    ], string="Trạng thái", compute='_compute_status', store=True)
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên")

    # Cập nhật trạng thái của chứng chỉ dựa vào ngày hết hạn
    @api.depends('ngay_het_han')
    def _compute_status(self):
        today = fields.Date.today()
        for record in self:
            if record.ngay_het_han and record.ngay_het_han < today:
                record.trang_thai = 'het_han'
            else:
                record.trang_thai = 'con_hieu_luc'