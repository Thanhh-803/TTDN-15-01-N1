from odoo import models, fields


class ThamGiaKhoaDaoTao(models.Model):
    _name = 'tham_gia_khoa_dao_tao'
    _description = 'Danh sách tham gia khóa đào tạo'
    
    
    ma_khoa_hoc = fields.Many2one("khoa_hoc", string="Khóa học", required=True, ondelete="cascade")
    employee_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True, ondelete="cascade")
    role = fields.Selection(
        [("trainer", "Giảng viên"), ("student", "Học viên")],
        string="Vai trò",
        required=True
    )