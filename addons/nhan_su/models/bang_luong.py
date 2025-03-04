from odoo import models, fields, api

class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương nhân viên'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    hop_dong_id = fields.Many2one('hop_dong', string="Hợp đồng", readonly=True)
    
    # Lương hợp đồng
    luong_hop_dong = fields.Float(string="Lương hợp đồng",store=True)
    
    # Lương cơ bản = Lương hợp đồng (Khi chọn nhân viên)
    luong_co_ban = fields.Float("Lương cơ bản", required=True)
    ngay_cong_thuc_te = fields.Float("Ngày công thực tế", required=True)
    nam_hanh_chinh = fields.Char("Năm hành chính", default=2025)
    thang_hanh_chinh = fields.Selection([
        ('01', 'Tháng 01'), ('02', 'Tháng 02'), ('03', 'Tháng 03'),
        ('04', 'Tháng 04'), ('05', 'Tháng 05'), ('06', 'Tháng 06'),
        ('07', 'Tháng 07'), ('08', 'Tháng 08'), ('09', 'Tháng 09'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng hành chính", default='01')

    ngay_bat_dau = fields.Date("Ngày bắt đầu hành chính", required=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc hành chính", required=True)

    # Thêm lương làm thêm, ngày nghỉ và ngày công chính thức
    luong_lam_them = fields.Float(string="Lương làm thêm", compute="_compute_luong_lam_them", store=True)
    ngay_nghi = fields.Integer(string="Ngày nghỉ")
    ngay_cong_thuc_te = fields.Integer(string="Ngày công thực tế", compute="_compute_ngay_cong", store=True)

    # Thưởng, phụ cấp
    thuong = fields.Float("Thưởng", default=0.0)
    gio_lam_them = fields.Float("Giờ làm thêm", required=True)
    ngay_nghi = fields.Float("Ngày nghỉ", required=True)
    phu_cap_xang_xe = fields.Float("Phụ cấp xăng xe", default=0.0)
    phu_cap_an_trua = fields.Float("Phụ cấp ăn trưa", default=0.0)
    phu_cap_dien_thoai = fields.Float("Phụ cấp điện thoại", default=0.0)
    phu_cap = fields.Float("Phụ cấp khác", default=0.0)

    # Bảo hiểm
    bhxh = fields.Float("BHXH (8%)", compute="_compute_bao_hiem", store=True)
    bhyt = fields.Float("BHYT (1,5%)", compute="_compute_bao_hiem", store=True)

    # Khấu trừ và Tổng lương
    khau_tru = fields.Float("Khấu trừ khác", default=0.0)
    tong_luong = fields.Float("Tổng lương", compute="_compute_tong_luong", store=True)

    # Trạng thái lương
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_thanh_toan', 'Đã thanh toán'),
    ], string="Trạng thái", default='cho_duyet')


     # lương làm thêm là 100k /giờ
    HE_SO_LAM_THEM = 100000  
    # Tính giờ làm thêm
    @api.depends('gio_lam_them')
    def _compute_luong_lam_them(self):
        for record in self:
            record.luong_lam_them = record.gio_lam_them * self.HE_SO_LAM_THEM

    # Tính số ngày nghỉ
    @api.depends('ngay_nghi')
    def _compute_ngay_cong(self):
        for record in self:
            record.ngay_cong_thuc_te = 25 - record.ngay_nghi  # Ngày công thực tế = 22 - ngày nghỉ


    # Tính tiền bảo hiểm
    @api.depends('luong_co_ban')
    def _compute_bao_hiem(self):
        for record in self:
            record.bhxh = record.luong_co_ban * 0.08  # 8% BHXH
            record.bhyt = record.luong_co_ban * 0.015 # 1.5% BHYT

    # Tính tổng lương cho nhân viên
    @api.depends('luong_co_ban','luong_lam_them', 'thuong', 'phu_cap', 'bhxh', 'bhyt', 'khau_tru')
    def _compute_tong_luong(self):
        for record in self:
            record.tong_luong = (
                record.luong_co_ban + record.thuong + record.phu_cap + record.luong_lam_them
                - record.bhxh - record.bhyt - record.khau_tru
            )

    # Xác nhận thanh toán lương cho nhân viên
    def action_xac_nhan(self):
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.write({'trang_thai': 'da_thanh_toan'})


    # Lấy lương hợp đồng và gán lương cơ bản
    @api.onchange('nhan_vien_id')
    def _onchange_nhan_vien_id(self):
        """ Khi chọn nhân viên, tự động lấy hợp đồng gần nhất và cập nhật lương hợp đồng, lương cơ bản """
        if self.nhan_vien_id:
            hop_dong = self.env['hop_dong'].search([
                ('nhan_vien_id', '=', self.nhan_vien_id.id),
                ('trang_thai', '=', 'DangHieuLuc')  # Chỉ lấy hợp đồng còn hiệu lực
            ], order="Ngay_bat_dau desc", limit=1)  # Lấy hợp đồng mới nhất

            if hop_dong:
                self.hop_dong_id = hop_dong.id
                self.luong_hop_dong = hop_dong.luong_hop_dong
                self.luong_co_ban = hop_dong.luong_hop_dong  # Gán lương cơ bản = lương hợp đồng
            else:
                self.hop_dong_id = False
                self.luong_hop_dong = 0.0
                self.luong_co_ban = 0.0  # Không có hợp đồng thì lương cơ bản = 0
