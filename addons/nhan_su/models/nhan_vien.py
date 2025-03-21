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
    # Thông tin căn cước
    can_cuoc_cong_dan = fields.Char("Số CMND/CCCD/Hộ chiếu", required=True)
    cap_tai = fields.Char("Cấp tại", required=True)
    ngay_cap = fields.Date("Ngày cấp", required=True)

    # Địa chỉ
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

    dan_toc = fields.Char("Dân tộc", required=True)
    ton_giao = fields.Char("Tôn giáo")
    quoc_tich= fields.Char("Quốc tịch", required=True)
    thanh_phan_ban_than = fields.Char("Thành phần bản thân hiện tại")
    van_hoa = fields.Char("Trình độ văn hóa")
    hoc_van = fields.Char("Trình độ học vấn")
    suc_khoe = fields.Char("Tình trạng sức khỏe")

    # Thông tin khác
    tinh_cach = fields.Char("Tính cách")
    so_thich = fields.Char("Sở thích")
    nang_khieu = fields.Char("Năng khiếu/Sở trường")
    ngoai_ngu = fields.Char("Ngoại ngữ")

    # Thêm
    ngay_het_han = fields.Date("Ngày hết hạn")
    

    # Thông tin ngân hàng
    ten_ngan_hàng = fields.Char("Tên ngân hàng")
    so_tai_khoan = fields.Char("Số tài khoản")
    chu_the = fields.Char("Tên chủ thẻ")
    chi_nhanh = fields.Char("Chi nhánh")    



    # Lịch sử công tác của nhân viên
    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac", 
        inverse_name = "nhan_vien_id", 
        string = "Danh sách lịch sử công tác")

    cong_viec_ids = fields.One2many(
        "cong_viec", 
        inverse_name = "nhan_vien_id", 
        string = "Thông tin công việc")

    # Trạng thái làm việc của nhân viên (lấy từ lịch sử công tác)
    trang_thai = fields.Selection(
        [
        ("dang_lam_viec", "Đang làm việc"), 
        ("nghi_thai_san", "Nghỉ thai sản"),
        ("thu_viec", "Thử việc"),
        ("tam_ngung_cong_tac", "Tạm ngừng công tác"),
        ("da_nghi_viec", "Đã nghỉ việc"),
        ],
        string="Trạng thái làm việc",
        compute="_compute_trang_thai",
        store=True
    )

    # Quan hệ gia đình
    # Thông tin bố
    ho_ten_bo =  fields.Char("Họ tên Bố")
    ng_sinh_bo =  fields.Char("Ngày sinh")
    phone_bo =  fields.Char("Số điện thoại")
    nghe_nghiep_bo =  fields.Char("Nghề nghiệp")
    address_bo =  fields.Char("Địa chỉ")
    # Thông tin Mẹ
    ho_ten_me =  fields.Char("Họ tên Mẹ")
    ng_sinh_me =  fields.Char("Ngày sinh")
    phone_me =  fields.Char("Số điện thoại")
    nghe_nghiep_me =  fields.Char("Nghề nghiệp")
    address_me =  fields.Char("Địa chỉ")

    # Thông tin Vợ/Chồng (Nếu có)
    ho_ten_vc =  fields.Char("Họ tên Vợ/Chồng (Nếu có)")
    ng_sinh_vc =  fields.Char("Ngày sinh (Nếu có)")
    phone_vc =  fields.Char("Số điện thoại (Nếu có)")
    nghe_nghiep_vc =  fields.Char("Nghề nghiệp(Nếu có)")
    address_vc =  fields.Char("Địa chỉ (Nếu có)")
    
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
    khoa_hoc_tham_gia_ids = fields.One2many(
        "tham_gia_khoa_dao_tao", 
        inverse_name = "employee_id", 
        string="Khóa học tham gia"
    )

    # Hợp đồng nhân viên
    hop_dong_ids = fields.One2many(
        "hop_dong", 
        inverse_name = "nhan_vien_id", 
        string="Thông tin hợp đồng"
    )


    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ")

    bang_luong_ids = fields.One2many(
        'bang_luong', 
        inverse_name = "nhan_vien_id", 
        string="Bảng lương") 

    trinh_do_hoc_van_ids = fields.One2many(
        'trinh_do_hoc_van', 
        inverse_name = "nhan_vien_id", 
        string="Trình độ học vấn"
    )
    ngay_nghi_ids = fields.One2many(
        'ngay_nghi', 
        inverse_name = "nhan_vien_id", 
        string="Ngày nghỉ"
    )
    khen_thuong_ids = fields.One2many(
        'khen_thuong_ky_luat', 
        inverse_name = "nhan_vien_id", 
        string="Khen thưởng & Kỷ luật"
    )

    
    
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

    @api.depends('cong_viec_ids.trang_thai', 'cong_viec_ids.ngay_vao_lam')
    def _compute_trang_thai(self):
        for record in self:
            if record.cong_viec_ids:
                # Lấy lịch sử công tác gần nhất (theo ngày vào làm mới nhất)
                latest_record = record.cong_viec_ids.sorted(lambda r: r.ngay_vao_lam, reverse=True)[0]
                record.trang_thai = latest_record.trang_thai
            else:
                record.trang_thai = "tam_ngung_cong_tac"  # Mặc định nếu chưa có lịch sử công tác