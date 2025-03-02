from odoo import models, fields, api

class LoaiVanBan(models.Model):
    _name = 'loai_van_ban'
    _rec_name = 'loai_van_ban'

    van_ban_di_id = fields.Many2one("van_ban", string = "Văn bản đi", required = True)
    van_ban_den_id = fields.Many2one("van_ban_den", string = "Văn bản đến", required = True)
    loai_van_ban = fields.Selection(
    [
        ('congvantuvan', 'Công văn - tư văn'), 
        ('nghidinhthongtu', 'Nghị định thông tư'), 
        ('vanbanhanhchinh', 'Văn bản hành chính')
    ], string="Loại văn bản")
    nam = fields.Char("Năm", required=True)