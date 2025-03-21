from odoo import models, fields



class TrinhDoHocVan(models.Model):
    _name = 'trinh_do_hoc_van'
    _description = 'Trình độ học vấn của nhân viên'
    _rec_name = 'nhan_vien_id'
    
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên")
    nam_tot_nghiep = fields.Char("Năm tốt nghiệp", required=True)
    trinh_do_hoc_van = fields.Selection([
        ('highschool', '12/12'),
        ('college', 'Cao đẳng'),
        ('bachelor', 'Đại học'),
        ('master', 'Thạc sĩ'),
        ('phd', 'Tiến sĩ')
    ], string="Trình độ học vấn", required=True)
    chuyen_nganh = fields.Char("Chuyên ngành", required=True)
    bang_cap = fields.Selection([
        ("cunhan", "Cử nhân"),
        ("caodang", "Bằng cao đẳng"),
        ("thacsi", "Thạc sĩ"),
        ("tiensi", "Tiến sĩ")
    ], string="Bằng cấp", required=True)
    truong_dao_tao = fields.Char("Trường đào tạo", required=True)

    
   

    