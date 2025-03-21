from odoo import models, fields, api


class TuyenDung(models.Model):
    _name = 'tuyen_dung'
    _description = 'Vị trí tuyển dụng'
    _rec_name = 'ten_vi_tri'

    ma_vi_tri = fields.Char("Mã vị trí tuyển dụng",required=True )
    ten_vi_tri = fields.Char("Vị trí tuyển dụng", required=True)
    mo_ta_cv = fields.Text("Mô tả công việc", required=True)
    yeu_cau = fields.Text("Yêu cầu kỹ năng & kinh nghiệm", required=True)
    muc_luong = fields.Char("Mức lương", required=True)
    dai_ngo = fields.Text("Chế độ đãi ngộ", required=True)
    thoi_han = fields.Date("Thời hạn tuyển dụng đến hết ngày", required=True)
    trang_thai = fields.Selection([
        ('dang_tuyen', 'Đang tuyển'),
        ('da_dong', 'Đã đóng'),
    ], string="Trạng thái", default='dang_tuyen')

    ung_vien_ids = fields.One2many(
        "ung_vien",
        inverse_name="tuyen_dung_id",
        string = "Danh sách ứng viên tham gia ứng tuyển"
    )

    # Tính số ứng viên tham gia ứng tuyển
    so_luong_ung_vien = fields.Integer(string="Số lượng ứng viên", compute="_compute_so_luong_nhan_vien", store=True)

    @api.depends('ung_vien_ids')
    def _compute_so_luong_nhan_vien(self):
        for record in self:
            record.so_luong_ung_vien = len(record.ung_vien_ids) 
    
