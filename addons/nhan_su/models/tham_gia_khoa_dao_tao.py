from odoo import models, fields


class ThamGiaKhoaDaoTao(models.Model):
    _name = 'tham_gia_khoa_dao_tao'
    _description = 'Danh sách tham gia khóa đào tạo'
  
    
    ma_dao_tao = fields.Many2one("khoa_dao_tao", string="Chương trình đào tạo", required=True)
    ma_khoa_hoc = fields.Many2one("khoa_hoc", string="Khóa học", required=True)
    employee_id = fields.Many2one("nhan_vien", string="Nhân viên tham gia", required=True)

    nguoi_tham_gia_khoa_hoc= fields.Selection(
        [
            ("trainer", "Giảng viên"), 
            ("student", "Học viên"),
            ("intern", "Nhân viên thử việc"),
            ("employee", "Nhân viên chính thức"),
        ],
        string="Tham gia với vai trò",
        required=True
    )

    trang_thai = fields.Selection(
        [
            ("completed", " ✅ Đã hoàn thành"), 
            ("studying", " ⏳ Đang thực hiện"),
            ("nostart", " ⏺️ Chưa bắt đầu"),
            ("cancel", "❌ Đã hủy"),
        ],
        string="Trạng thái",
        required=True
    )

    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ")
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban")





