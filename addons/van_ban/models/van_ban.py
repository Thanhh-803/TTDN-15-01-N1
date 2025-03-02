from odoo import models, fields

class VanBan(models.Model):
    _name = "van_ban"
    _description = "Văn bản đi"
    _rec_name = "ten_van_ban"


    so_hieu = fields.Char(string="Số hiệu")
    ten_van_ban = fields.Char(string="Tên văn bản")
    so_van_ban_di = fields.Char(string="Số văn bản đi")
    nam = fields.Char(string="Nam")
    noi_den = fields.Char(string="Nơi đến")
    loai_van_ban_id = fields.Many2one("loai_van_ban", string = "Loại văn bản", required = True)