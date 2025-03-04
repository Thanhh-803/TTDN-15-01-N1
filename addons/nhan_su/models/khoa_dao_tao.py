from odoo import models, fields, api


class KhoaDaoTao(models.Model):
    _name = 'khoa_dao_tao'
    _description = 'Danh sách khóa đào tạo'
    _rec_name ="ten_khoa_dao_tao"
    
    ma_khoa_dao_tao = fields.Char("Mã khóa đào tạo", required=True)
    ten_khoa_dao_tao = fields.Char("Chương trình đào tạo", required=True)
    noi_dung_dao_tao = fields.Char("Nội dung đào tạo", required=True)
    
    hinh_thuc_dao_tao = fields.Selection(
        [
            ("online", "Online"),
            ("off", "Offline")
        ],
        string="Hình thức đào tạo", default="online"
    )
    
    doi_tuong_tham_gia = fields.Char("Đối tượng tham gia")
    thoi_gian = fields.Date("Thời gian đào tạo")
    # Người hướng hẫn
    employee_id = fields.Many2one("nhan_vien", string="Giảng viên/Người hướng dẫn")

    khoa_hoc_ids = fields.Many2many(
        "khoa_hoc", 
        "khoa_dao_tao_khoa_hoc_rel", 
        "khoa_dao_tao_id", 
        "khoa_hoc_id", 
        string="Danh sách khóa học"
    )

    
    


    
