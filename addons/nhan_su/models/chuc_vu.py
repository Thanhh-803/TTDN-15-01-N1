from odoo import models, fields


class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Bảng chứa thông tin chức vụ của nhân viên'
    _rec_name = 'ten_chuc_vu'
    
    ten_chuc_vu = fields.Char("Tên chức vụ", required=True)
    vi_tri_viec_lam = fields.Char("Vị trí việc làm", required=True)
    
