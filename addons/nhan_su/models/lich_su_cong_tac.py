from odoo import models, fields, api

class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Bảng chứa thông tin lịch sử công tác'
    _rec_name = 'nhan_vien_id'

    # Thông tin công việc của nhân viên
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    # Sử dụng related để lấy thông tin nhân viên
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

    ngay_vao_lam = fields.Date("Ngày vào làm")
    trang_thai = fields.Selection(
        [
            ("DanghoatDong", "Đang làm việc"), 
            ("TamNgung", "Tạm nghỉ"),
            ("GiaiThe", "Đã nghỉ")
        ],
        string="Trạng thái làm việc", default="DanghoatDong"
    )

    # Trường thông tin người quản lý trực tiếp
    quan_ly_truc_tiep = fields.Many2one(
        'nhan_vien', 
        string="Người quản lý", 
        compute="_compute_quan_ly_truc_tiep", 
        store=True
    )
    

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
