from odoo import models, fields, api


class KhenThuongKyLuat(models.Model):
    _name = 'khen_thuong_ky_luat'
    _description = 'Khen thưởng kỷ luật'
    _rec_name = 'nhan_vien_id'

    ten_quyet_dinh = fields.Char("Tên quyết định", required=True)
    loai = fields.Selection([
        ('khen_thuong', 'Khen thưởng'),
        ('ky_luat', 'Kỷ luật')
    ], string="Loại", default='draft')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    nam_quyet_dinh = fields.Char("Năm", default=2025)
    thang_quyet_dinh = fields.Selection([
        ('01', 'Tháng 01'), ('02', 'Tháng 02'), ('03', 'Tháng 03'),
        ('04', 'Tháng 04'), ('05', 'Tháng 05'), ('06', 'Tháng 06'),
        ('07', 'Tháng 07'), ('08', 'Tháng 08'), ('09', 'Tháng 09'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng hành chính", default='01')
    ngay_quyet_dinh = fields.Date("Ngày quyết định", required=True)
    ly_do = fields.Text("Lý do", required=True)
    hinh_thuc = fields.Selection([
        ('tang_luong', 'Tăng lương'),
        ('thuong', 'Thưởng tiền mặt'),
        ('giam_luong', 'Giảm lương'),
        ('canh_cao', 'Cảnh cáo'),
        ('sa_thai', 'Sa thải'),
        ('khac', 'Khác')
    ], string="Hình thức", required=True)
    so_tien_thuong = fields.Float("Tiền thưởng")
    so_tien_phat = fields.Float("Tiền Phạt")
    trang_thai = fields.Selection([
        ('xac_nhan', 'Xác nhận'),
        ('huy', 'Hủy')
    ], string="Trạng thái", default='xac_nhan', store = True)

    def action_xac_nhan(self):
        # Xác nhận quyết định 
        self.write({'trang_thai': 'xac_nhan'})

    def action_huy(self):
        # Hủy quyết định
        self.write({'trang_thai': 'huy'})

    @api.onchange('loai')
    def _onchange_loai(self):
        if self.loai == 'khen_thuong':
            self.so_tien_phat = False  # Xóa giá trị số tiền phạt
        elif self.loai == 'ky_luat':
            self.so_tien_thuong = False  # Xóa giá trị số tiền thưởng
   
    
