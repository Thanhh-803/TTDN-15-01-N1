from odoo import models, fields, api


class NgayNghi(models.Model):
    _name = 'ngay_nghi'
    _description = 'Ngày nghỉ của nhân viên'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    nam = fields.Char("Năm", default=2025)
    thang_hanh_chinh = fields.Selection([
        ('01', 'Tháng 01'), ('02', 'Tháng 02'), ('03', 'Tháng 03'),
        ('04', 'Tháng 04'), ('05', 'Tháng 05'), ('06', 'Tháng 06'),
        ('07', 'Tháng 07'), ('08', 'Tháng 08'), ('09', 'Tháng 09'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng hành chính", default='01')
    
    ngay_nghi = fields.Date(string="Ngày nghỉ", required=True)
    ly_do_nghi = fields.Char("Lý do nghỉ", required=True)
    loai_nghi = fields.Selection([
        ('nghi_le', 'Nghỉ lễ/Tết'),
        ('nghi_phep_nam', 'Nghỉ phép năm'),
        ('nghi_benh', 'Nghỉ bệnh'),
        ('nghi_thai_san', 'Nghỉ thai sản'),
    ], string="Loại nghỉ phép", required=True)

    phe_duyet = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('huy', 'Hủy'),
    ], string="Phê duyệt", default='cho_duyet')

    def action_xac_nhan(self):
        # Chờ duyệt
        self.write({'phe_duyet': 'cho_duyet'})

    def action_da_duyet(self):
        # Đã duyệt
        self.write({'phe_duyet': 'da_duyet'})

    def action_huy(self):
        # Hủy 
        self.write({'phe_duyet': 'huy'})

    
    
