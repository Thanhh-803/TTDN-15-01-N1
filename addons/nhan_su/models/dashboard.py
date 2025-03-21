from odoo import models, api


class Dashboard(models.Model):
    _name = 'dashboard'
    _description = 'Bảng tin chung của quản lý nhân sự'
    _auto = False
    
    @api.model
    def name_get(self):
        return [(record.id, "HR Dashboard") for record in self]


    @api.model
    def get_overview_data(self):
        #Dashboard Tổng Quan Nhân Sự
        # Tổng số nhân viên
        tong_employees = self.env['nhan_vien'].search_count([])
        hoat_dong_employees = self.env['nhan_vien'].search_count([('trang_thai', '=', 'dang_lam_viec')])
        thu_viec_employees = self.env['nhan_vien'].search_count([('trang_thai', '=', 'thu_viec')])
        tam_ngung_employees = self.env['nhan_vien'].search_count([('trang_thai', '=', 'tam_ngung_cong_tac')])
        nghi_viec_employees = self.env['nhan_vien'].search_count([('trang_thai', '=', 'da_nghi_viec')])
        
        # Số lượng nhân viên theo phòng ban
        departments = self.env['phong_ban'].search([])
        department_data = []
        for dept in departments:
            employee_count = self.env['cong_viec'].search_count([('phong_ban_id', '=', dept.id)])
            if employee_count > 0:
                department_data.append({
                    'name': dept.ten_phong_ban or dept.ma_phong_ban,
                    'count': employee_count,
                })

        bang_luong_records = self.env['bang_luong'].search([])
        # 1. Tổng quỹ lương
        total_salary = sum(bang_luong_records.mapped('luong_co_ban'))

        # 2. Lương trung bình
        employee_count = len(bang_luong_records.mapped('nhan_vien_id'))
        average_salary = total_salary / employee_count if employee_count > 0 else 0.0


        # Tính tổng lương từ bảng lương theo từng tháng
        salary_trend_data = []
        current_year = '2025'
        for m in range(1, 13):
            month_str = f"{m:02d}"
            records = self.env['bang_luong'].search([
                ('thang_hanh_chinh', '=', month_str),
                ('nam_hanh_chinh', '=', current_year)
            ])
            month_total = sum(records.mapped('luong_co_ban'))
            salary_trend_data.append({
                'month': month_str,
                'salary': month_total,
            })
        
        approved_leaves = self.env['ngay_nghi'].search_count([('phe_duyet', '=', 'da_duyet')])
        pending_leaves = self.env['ngay_nghi'].search_count([('phe_duyet', '=', 'cho_duyet')])
        canceled_leaves = self.env['ngay_nghi'].search_count([('phe_duyet', '=', 'huy')])

        # Thống kê tỷ lệ thưởng phạt (dưới dạng phần trăm)
        current_year = '2025'
        result_data = []
        for m in range(1, 13):
            month_str = f"{m:02d}"
            decisions = self.env['khen_thuong_ky_luat'].search([
                ('thang_quyet_dinh', '=', month_str),
                ('nam_quyet_dinh', '=', current_year),
                ('trang_thai', '=', 'xac_nhan')
            ])
            total_reward = sum(dec.so_tien_thuong for dec in decisions if dec.loai == 'khen_thuong')
            total_penalty = sum(dec.so_tien_phat for dec in decisions if dec.loai == 'ky_luat')
            ratio = round((total_reward / total_penalty) * 100, 2) if total_penalty > 0 else 0
            result_data.append({
                'month': month_str,
                'total_reward': total_reward,
                'total_penalty': total_penalty,
                'ratio': ratio,
            })

        # Thống kê độ tuổi nhân viên
        age_groups = {
            'under_25': 0,
            '25_35': 0,
            '36_45': 0,
            '46_55': 0,
            'above_55': 0
        }
        employees = self.env['nhan_vien'].search([])
        current_year = int(self.env["ir.config_parameter"].sudo().get_param("current_year", default="2025"))
        
        for emp in employees:
            if emp.ngay_sinh:
                age = current_year - emp.ngay_sinh.year
                if age < 25:
                    age_groups['under_25'] += 1
                elif 25 <= age <= 35:
                    age_groups['25_35'] += 1
                elif 36 <= age <= 45:
                    age_groups['36_45'] += 1
                elif 46 <= age <= 55:
                    age_groups['46_55'] += 1
                else:
                    age_groups['above_55'] += 1

        
       
        
        return {
            'tong_employees': tong_employees,
            'hoat_dong_employees': hoat_dong_employees,
            'thu_viec_employees': thu_viec_employees,
            'tam_ngung_employees': tam_ngung_employees,
            'nghi_viec_employees': nghi_viec_employees,

            'total_salary': total_salary,
            'average_salary': average_salary,

            'department_data': department_data,
            'salary_trend_data': salary_trend_data,  


            'approved_leaves': approved_leaves,
            'pending_leaves': pending_leaves,
            'canceled_leaves': canceled_leaves, 

            'reward_penalty_ratio': result_data,
            'age_group_data': age_groups,
        }
    
    
