from odoo import models, fields


class UngVien(models.Model):
    _name = 'ung_vien'
    _description = 'Thông tin về ứng viên'
    _rec_name = 'ten_ung_vien'

    ma_ung_vien = fields.Char("Mã ứng viên", required=True)
    ten_ung_vien = fields.Char("Ứng viên", required=True)
    phone = fields.Char("Số điện thoại", required=True)
    email = fields.Char("Email", required=True)
    ho_so = fields.Binary("Hồ sơ (CV)", required=True, attachment=True)
    tuyen_dung_id = fields.Many2one("tuyen_dung", string="Vị trí tuyển dụng")
    kinh_nghiem = fields.Text("Kinh nghiệm làm việc", required=True)
    ky_nang = fields.Text("Kỹ năng & Trình độ chuyên môn", required=True)
    tham_chieu = fields.Char("Thông tin tham chiếu", required=True)
    ket_qua = fields.Selection([
        ('dat', 'Đạt'),
        ('khong_dat', 'Không đạt'),
    ], string="Kết quả ứng tuyển", default='draft')
    trang_thai = fields.Selection([
        ('dang_xet_duyet', 'Đang xét duyệt'),
        ('loai', 'Loại'),
        ('da_nhan_viec', 'Đã nhận việc'),
    ], string="Tình trạng ứng tuyển", default='draft')


    

    

    
    
