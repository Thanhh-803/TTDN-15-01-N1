from odoo import models, fields, api
from datetime import date

class CongViec(models.Model):
    _name = 'cong_viec'
    _description = 'Thông tin công việc của nhân viên'
    _rec_name = "nhan_vien_id"

    # Thông tin công việc của nhân viên
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    # Sử dụng related để lấy thông tin nhân viên
    ma_nhan_vien = fields.Char(
        string="Mã nhân viên",
        related="nhan_vien_id.ma_dinh_danh",
        store=True, readonly=True
    )
    ngay_sinh = fields.Date(
        string="Ngày sinh",
        related="nhan_vien_id.ngay_sinh",
        store=True, readonly=True
    )
    gioi_tinh = fields.Selection(
        string="Giới tính",
        related="nhan_vien_id.gioi_tinh",
        store=True, readonly=True
    )
    so_dien_thoai = fields.Char(
        string="Số điện thoại",
        related="nhan_vien_id.so_dien_thoai",
        store=True, readonly=True
    )
    email = fields.Char(
        string="Email liên hệ",
        related="nhan_vien_id.email",
        store=True, readonly=True
    )
    dia_chi = fields.Char(
        string="Địa chỉ",
        related="nhan_vien_id.dc_tam_tru",
        store=True, readonly=True
    )


    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ")
    vi_tri = fields.Char(string="Vị trí việc làm", related="chuc_vu_id.vi_tri_viec_lam", store=True)
    loai_chuc_vu = fields.Selection(
        [
            ("Chính", "Chính"), 
            ("Kiêm nhiệm", "Kiêm nhiệm")
        ],
        string="Loại chức vụ", default="Chính"
    )
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban")

    # Lấy thông tin hợp đồng của nhân viên
    loai_hop_dong = fields.Selection(
        string="Loại hợp đồng",
        related="nhan_vien_id.hop_dong_ids.loai_hop_dong",
        store=True,
        readonly=True
    )

    
    # Lấy thông tin hợp đồng của nhân viên
    ngay_vao_lam = fields.Date(
        string="Ngày vào công ty",
        related="nhan_vien_id.hop_dong_ids.Ngay_bat_dau",
        store=True,
        readonly=True
    )
    muc_luong = fields.Float(
        string="Mức lương",
        related="nhan_vien_id.hop_dong_ids.luong_hop_dong",
        store=True,
        readonly=True
    )
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

    # Trường thông tin người quản lý trực tiếp
    quan_ly_truc_tiep = fields.Many2one(
        'nhan_vien', 
        string="Người quản lý", 
        compute="_compute_quan_ly_truc_tiep", 
        store=True
    )
    
    

    # Kiểm tra trạng thái làm việc
    @api.depends('ngay_ket_thuc')
    def _compute_trang_thai(self):
        for record in self:
            if record.ngay_ket_thuc:
                record.trang_thai = "da_nghi_viec"
            else:
                record.trang_thai = "dang_lam_viec"


    # Tránh  một nhân viên chọn chính mình làm quản lý
    @api.depends('phong_ban_id', 'phong_ban_id.nhan_vien_id', 'nhan_vien_id')
    def _compute_quan_ly_truc_tiep(self):
        for record in self:
            if record.phong_ban_id and record.phong_ban_id.nhan_vien_id:
                # Nếu nhân viên đó chính là người quản lý thì để false
                if record.nhan_vien_id == record.phong_ban_id.nhan_vien_id:
                    record.quan_ly_truc_tiep = False
                else:
                    record.quan_ly_truc_tiep = record.phong_ban_id.nhan_vien_id
            else:
                record.quan_ly_truc_tiep = False
