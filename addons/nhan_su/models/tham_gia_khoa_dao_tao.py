from odoo import models, fields, api

class ThamGiaKhoaDaoTao(models.Model):
    _name = 'tham_gia_khoa_dao_tao'
    _description = 'Danh sách tham gia khóa đào tạo'
    _rec_name = "employee_id"
  
    ma_dao_tao = fields.Many2one('khoa_dao_tao', string="Chương trình đào tạo", required=True)
    ten_khoa_hoc = fields.Many2one(
        'khoa_hoc', 
        string="Khóa học", 
        domain="[('chuong_trinh_dao_tao_id', '=', ma_dao_tao)]", 
        required=True
    )

    @api.onchange('ma_dao_tao')
    def _onchange_ma_dao_tao(self):
        self.ten_khoa_hoc = False  # Reset danh sách khóa học khi đổi chương trình đào tạo

    employee_id = fields.Many2one("nhan_vien", string="Nhân viên tham gia", required=True)
    chuc_vu_id = fields.Many2one(related="employee_id.lich_su_cong_tac_ids.chuc_vu_id", string="Chức vụ")
    phong_ban_id = fields.Many2one(related="employee_id.lich_su_cong_tac_ids.phong_ban_id", string="Phòng ban")

    nguoi_tham_gia_khoa_hoc = fields.Selection(
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