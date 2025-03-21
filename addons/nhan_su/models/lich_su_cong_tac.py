from odoo import models, fields, api
from datetime import date

class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Bảng chứa thông tin lịch sử công tác'
    _rec_name = 'nhan_vien_id'

    
    # Thông tin công việc của nhân viên
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    # Sử dụng related để lấy thông tin nhân viên
    ma_nhan_vien = fields.Char(
        string="Mã nhân viên",
        related="nhan_vien_id.ma_dinh_danh",
        store=True, readonly=True
    )
    

    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ")
    vi_tri = fields.Char(string="Vị trí việc làm", related="chuc_vu_id.vi_tri_viec_lam", store=True)
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban")
    cong_ty = fields.Char(string="Công ty")
    
    

    ngay_vao_lam = fields.Date(string = "Ngày vào công ty", related = "nhan_vien_id.hop_dong_ids.Ngay_bat_dau", store = True)

    ngay_ket_thuc = fields.Char(string="Ngày kết thúc")
    trang_thai = fields.Selection(
    [
        ("dang_lam_viec", "Đang làm việc"), 
        ("nghi_thai_san", "Nghỉ thai sản"),
        ("thu_viec", "Thử việc"),
        ("tam_ngung_cong_tac", "Tạm ngừng công tác"),
        ("da_nghi_viec", "Đã nghỉ việc"),
    ],
    string="Trạng thái làm việc", default="draft"
    )
    ghi_chu = fields.Text(string="Ghi chú")

    
    
    

    # Kiểm tra trạng thái làm việc
    @api.depends('ngay_ket_thuc')
    def _compute_trang_thai(self):
        for record in self:
            if record.ngay_ket_thuc:
                record.trang_thai = "da_nghi_viec"
            else:
                record.trang_thai = "dang_lam_viec"

   

    

    
