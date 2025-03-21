from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
    thuong = fields.Float("Thưởng", default=0.0, compute="_compute_thuong_phat", store=True)
    phat = fields.Float("Phạt", default=0.0, compute="_compute_thuong_phat", store=True)


    gio_lam_them = fields.Float("Giờ làm thêm", required=True)
    ngay_nghi = fields.Integer("Ngày nghỉ",compute="_compute_ngay_nghi", store = True)
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
        ('huy', 'Hủy'),
    ], string="Trạng thái", default='cho_duyet')

    ty_le_thuong_phat = fields.Float(string="Tỷ Lệ Thưởng/Phạt (%)", compute="_compute_tyle_thuong_phat", store=True)

    @api.depends("thuong", "phat")
    def _compute_tyle_thuong_phat(self):
        for record in self:
            total = record.thuong + record.phat
            record.ty_le_thuong_phat = (record.thuong / total * 100) if total > 0 else 0


    # Lấy số tiền thưởng và số tiền phạt từ model khen thưởng/kỷ luật
    @api.depends('nhan_vien_id', 'thang_hanh_chinh', 'nam_hanh_chinh')
    def _compute_thuong_phat(self):
        for record in self:
            if record.nhan_vien_id:
                # Lọc các quyết định khen thưởng/kỷ luật của nhân viên theo tháng và năm
                decisions = self.env['khen_thuong_ky_luat'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('thang_quyet_dinh', '=', record.thang_hanh_chinh),
                    ('nam_quyet_dinh', '=', record.nam_hanh_chinh),
                    ('trang_thai', '=', 'xac_nhan')
                ])

                # Tính tổng tiền thưởng và tiền phạt
                thuong = sum(dec.so_tien_thuong for dec in decisions if dec.loai == 'khen_thuong')
                tien_phat = sum(dec.so_tien_phat for dec in decisions if dec.loai == 'ky_luat')

                record.thuong = thuong
                record.phat = tien_phat
            else:
                record.thuong = 0.0
                record.phat = 0.0


    @api.depends('nhan_vien_id', 'thang_hanh_chinh', 'nam_hanh_chinh')
    def _compute_ngay_nghi(self):
        """Tính số ngày nghỉ dựa trên dữ liệu trong bảng ngày nghỉ"""
        for record in self:
            if record.nhan_vien_id and record.thang_hanh_chinh:
                ngay_nghi_count = self.env['ngay_nghi'].search_count([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('thang_hanh_chinh', '=', record.thang_hanh_chinh),
                    ('nam', '=', record.nam_hanh_chinh),
                    ('phe_duyet', '=', 'da_duyet') 
                ])
                record.ngay_nghi = ngay_nghi_count
            else:
                record.ngay_nghi = 0


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
    @api.depends('luong_co_ban', 'luong_lam_them', 'thuong', 'phat', 'phu_cap', 
             'phu_cap_an_trua', 'phu_cap_dien_thoai', 'phu_cap_xang_xe', 
             'bhxh', 'bhyt', 'khau_tru')
    def _compute_tong_luong(self):
        for record in self:
            record.tong_luong = (
                (record.luong_co_ban or 0.0) + (record.luong_lam_them or 0.0) 
                + (record.thuong or 0.0) + (record.phu_cap or 0.0) 
                + (record.phu_cap_an_trua or 0.0) + (record.phu_cap_dien_thoai or 0.0) 
                + (record.phu_cap_xang_xe or 0.0)
                - (record.phat or 0.0) - (record.bhxh or 0.0) 
                - (record.bhyt or 0.0) - (record.khau_tru or 0.0)
            )

    def action_xac_nhan(self):
        # Xác nhận thanh toán lương
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.write({'trang_thai': 'da_thanh_toan'})
            else:
                raise ValidationError("Xác nhận khi trạng thái là 'Chờ duyệt'!")

    def action_cho_duyet(self):
        # Chuyển trạng thái về 'Chờ duyệt'
        self.write({'trang_thai': 'cho_duyet'})

    def action_huy(self):
        """Hủy quyết định"""
        self.write({'trang_thai': 'huy'})

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
