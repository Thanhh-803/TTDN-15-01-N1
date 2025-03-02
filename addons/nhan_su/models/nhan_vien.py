from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'
    

    #Thông tin nhân viên
    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_va_ten = fields.Char("Họ và tên", required=True)
    ngay_sinh = fields.Date("Ngày sinh", required=True)
    tuoi = fields.Integer("Tuổi", compute = "_compute_tinh_tuoi", store = True)
    gioi_tinh = fields.Selection(
        [('nam', 'Nam'), ('nu', 'Nữ')],
        string="Giới tính",
        default='Chọn giới tính',
        required=True
    )
    can_cuoc_cong_dan = fields.Char("Số CMND/CCCD/Hộ chiếu", required=True)
    dc_tam_tru = fields.Char("Địa chỉ tạm trú", required=True)
    dc_thuong_tru = fields.Char("Địa chỉ thường trú", required=True)
    so_dien_thoai = fields.Char("Số điện thoại", required=True)
    email = fields.Char("Email cá nhân", required=True)
    tinh_trang_hon_nhan = fields.Selection(
        [
            ('Docthan', 'Độc thân'), 
            ('HenHo', 'Hẹn hò'), 
            ('Dakethon', 'Đã kết hôn'),
        ],
        string="Tình trạng hôn nhân", default='draft'
    )
    hinh_anh = fields.Binary("Hình ảnh")

    # Thông tin khác
    don_vi = fields.Char("Đơn vị")
    chuc_vu = fields.Char("Chức vụ")
    chung_chi = fields.Char("Chứng chỉ")
    



    # Lịch sử công tác của nhân viên
    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac", 
        inverse_name = "nhan_vien_id", 
        string = "Danh sách lịch sử công tác")


    # Liên kết chứng chỉ
    chung_chi_ids = fields.One2many(
        'chung_chi', 
        inverse_name = "nhan_vien_id", 
        string="Chứng chỉ của nhân viên")

    # Liên kết phòng ban
    phong_ban_id = fields.Many2one(
        'phong_ban', 
        inverse_name = "nhan_vien_id", 
        string="Phòng ban") 
   
    # Liên kết với khóa học
    khoa_hoc_id = fields.Many2one(
        'khoa_hoc', 
        inverse_name = "nhan_vien_id", 
        string="Khóa học") 


    # Khóa học tham gia
    khoa_hoc_tham_gia_ids = fields.One2many("tham_gia_khoa_dao_tao", "employee_id", string="Khóa học tham gia")


    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ")

    bang_luong_ids = fields.One2many(
        'bang_luong', 
        inverse_name = "nhan_vien_id", 
        string="Bảng lương") 
    
    


    # Tính tuổi cho nhân viên
    @api.depends("ngay_sinh")
    def _compute_tinh_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                today = date.today()
                record.tuoi = today.year - record.ngay_sinh.year - (
                    (today.month, today.day) < (record.ngay_sinh.month, record.ngay_sinh.day)
                )
            else:
                record.tuoi = 0
    # Kiểm tra điều kiện cho tuổi của nhân viên
    @api.constrains('tuoi')
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Tuổi không được bé hơn 18")