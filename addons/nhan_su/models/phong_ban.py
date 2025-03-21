from odoo import models, fields, api

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa danh sách các phòng ban'
    _rec_name = 'ten_phong_ban'

    ma_phong_ban = fields.Char("Mã phòng ban", required=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    mo_ta = fields.Text("Mô tả")

    nhan_vien_id = fields.Many2one('nhan_vien', string="Người quản lý")  # Người quản lý phòng ban
    email = fields.Char("Email liên hệ")

    trang_thai = fields.Selection(
        [
            ("DanghoatDong", "Đang hoạt động"), 
            ("TamNgung", "Tạm ngừng"),
            ("GiaiThe", "Giải thể")
        ],
        string="Trạng thái", default="DanghoatDong"
    )

    
    danh_sach_nhan_vien = fields.One2many(
        'cong_viec', 
        'phong_ban_id', 
        string="Danh sách nhân viên"
    )

   # Tính số lượng nhân viên trong phòng ban
    so_luong_nhan_vien = fields.Integer(string="Số lượng nhân viên", compute="_compute_so_luong_nhan_vien", store=True)

    @api.depends('danh_sach_nhan_vien')
    def _compute_so_luong_nhan_vien(self):
        for record in self:
            record.so_luong_nhan_vien = len(record.danh_sach_nhan_vien)
