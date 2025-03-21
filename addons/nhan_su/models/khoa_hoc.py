from odoo import models, fields


class KhoaHoc(models.Model):
    _name = 'khoa_hoc'
    _description = 'Bảng chứa danh sách các khóa học'
    _rec_name = 'ten_khoa_hoc'

    chuong_trinh_dao_tao_id = fields.Many2one('khoa_dao_tao', string="Chương trình đào tạo")
    ma_khoa_hoc = fields.Char("Mã khóa học", required=True)
    ten_khoa_hoc = fields.Char("Tên khóa học", required=True)
    mo_ta_khoa_hoc = fields.Text("Mô tả khóa học", required=True)
    ke_hoach_giang_day = fields.Text("Kế hoạch giảng dạy", required=True)
    loai_khoa_hoc = fields.Selection(
        [
            ("Chuyenmon", "Kỹ năng chuyên môn"),
            ("mem", "Kỹ năng mềm"),
            ("Noibo&Hoinhap", "Đào tạo nội bộ & Hội nhập"),
            ("Lanhdao&Quanly", "Đào tạo lãnh đạo và quản lý")
        ],
        string="Loại khóa học", default="Chuyenmon"
    )
    
    
    
    
    

