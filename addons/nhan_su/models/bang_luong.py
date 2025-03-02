from odoo import models, fields, api

class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương nhân viên'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    nam_hanh_chinh = fields.Date("Ngày bắt đầu", required=True)
    thang_hanh_chinh = fields.Date("Ngày kết thúc", required=True)
    
    # Lương và phụ cấp
    luong_co_ban = fields.Float("Lương cơ bản", required=True)
    thuong = fields.Float("Thưởng", default=0.0)
    phu_cap_xang_xe = fields.Float("Phụ cấp xăng xe", default=0.0)
    phu_cap_an_trua = fields.Float("Phụ cấp ăn trưa", default=0.0)
    phu_cap_dien_thoai = fields.Float("Phụ cấp điện thoại", default=0.0)
    phu_cap = fields.Float("Phụ cấp khác", default=0.0)

    # Bảo hiểm
    bhxh = fields.Float("Bảo hiểm xã hội", compute="_compute_bao_hiem", store=True)
    bhyt = fields.Float("Bảo hiểm y tế", compute="_compute_bao_hiem", store=True)

    # Khấu trừ & Tổng lương
    khau_tru = fields.Float("Khấu trừ", default=0.0)
    tong_luong = fields.Float("Tổng lương", compute="_compute_tong_luong", store=True)

    # Trạng thái lương
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_thanh_toan', 'Đã thanh toán'),
    ], string="Trạng thái", default='cho_duyet', tracking=True)

    # Tính bảo hiểm dựa trên lương cơ bản
    @api.depends('luong_co_ban')
    def _compute_bao_hiem(self):
        for record in self:
            record.bhxh = record.luong_co_ban * 0.08  # 8% BHXH
            record.bhyt = record.luong_co_ban * 0.015 # 1.5% BHYT

    # Tính tổng lương
    @api.depends('luong_co_ban', 'thuong', 'phu_cap', 'bhxh', 'bhyt', 'khau_tru')
    def _compute_tong_luong(self):
        for record in self:
            record.tong_luong = (
                record.luong_co_ban + record.thuong + record.phu_cap 
                - record.bhxh - record.bhyt - record.khau_tru
            )

    # Hành động xác nhận thanh toán lương
    def action_xac_nhan(self):
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.write({'trang_thai': 'da_thanh_toan'})
