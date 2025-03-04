from odoo import models, fields


class HopDong(models.Model):
    _name = 'hop_dong'
    _description = 'Bảng chứa danh sách các khoa học'
    _rec_name = 'ma_hop_dong'
    
    ma_hop_dong = fields.Char("Mã hợp đồng", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Tên nhân viên")  
    loai_hop_dong = fields.Selection(
        [
            ("ngan_han", "Hợp đồng ngắn hạn"),
            ("toan_thoi_gian", "Hợp đồng toàn thời gian"),
            ("thoi_vu", "Hợp đồng thời vụ"),
            ("thu_viec", "Hợp đồng thử việc"),
            ("cong_tac_vien", "Cộng tác viên")
        ],
        string="Loại hợp đồng",
        default="draft" 
    )
    Ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True)
    Ngay_ket_thuc = fields.Date("Ngày kết thúc", required=True)
    luong_hop_dong = fields.Float("Lương hợp đồng", required=True)
    trang_thai = fields.Selection(
        [
            ("DangHieuLuc", "Đang hiệu lực"),
            ("DaHetHan", "Đã hết hạn"),
            ("DaChamDut", "Đã chấm dứt"),
            ("GiaHan", "Gia hạn hợp đồng")
        ],
        string="Trạng thái hợp đồng", default="draft"
    )
    
    
    
    
    

