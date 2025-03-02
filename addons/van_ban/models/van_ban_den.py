from odoo import models, fields

class VanBanDen(models.Model):
    _name = "van_ban_den"
    _description = "Văn bản đến"
    _rec_name = "ten_van_ban"


    so_hieu = fields.Char(string="Số hiệu")
    ten_van_ban = fields.Char(string="Tên văn bản")
    so_van_ban_den = fields.Char(string="Số văn bản đến")
    nam = fields.Char(string="Nam")
    noi_gui_den = fields.Char(string="Nơi gửi đến")
    muc_do = fields.Selection(
    [
        ('hoatoc', 'Hỏa tốc'), 
        ('thuongkhan', 'Thượng Khẩn'), 
        ('khan', 'Khẩn')
    ], string="Mức độ")
    loai_van_ban_id = fields.Many2one("loai_van_ban", string = "Loại văn bản", required = True)