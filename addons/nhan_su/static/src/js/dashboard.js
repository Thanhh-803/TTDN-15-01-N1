odoo.define('nhan_su.dashboard_overview', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var viewRegistry = require('web.view_registry');

    var DashboardOverviewController = FormController.extend({
        start: function () {
            this._super.apply(this, arguments);
            this.$el.addClass('o_dashboard_view');
        },
        willStart: function () {
            return Promise.all([
                this._super.apply(this, arguments),
                this._loadDashboardData()
            ]);
        },
        _loadDashboardData: function () {
            const self = this;
            return this._rpc({
                model: 'dashboard',
                method: 'get_overview_data',
                args: [],
            }).then(function (data) {
                self.dashboardData = data;
            });
        },
        renderButtons: function () {
            // Ẩn các nút mặc định của form
            this.$buttons = $();
            return this.$buttons;
        },
        _update: function () {
            const self = this;
            return this._loadDashboardData().then(function () {
                self._updateDashboard();
            });
        },
        _updateDashboard: function () {
            if (!this.dashboardData) return;
            const data = this.dashboardData;
            
            // Cập nhật các số liệu thống kê
            this.$('.total_assets').text(data.tong_employees);
            this.$('.active_assets').text(data.hoat_dong_employees);
            this.$('.thu_viec_assets').text(data.thu_viec_employees);
            this.$('.tam_ngung_assets').text(data.tam_ngung_employees);
            this.$('.nghi_viec_assets').text(data.nghi_viec_employees);

            this.$('.total_luong_value').text(this._formatCurrency(data.total_salary));
            this.$('.total_trung_binh_value').text(this._formatCurrency(data.average_salary));


            this.$('.borrowed_assets').text(data.approved_leaves);
            this.$('.returned_assets').text(data.pending_leaves);
            this.$('.canceled_leaves').text(data.canceled_leaves);

            // Vẽ biểu đồ tròn: Số lượng nhân viên theo phòng ban
            this._renderDepartmentsBarChart(data.department_data);
            // Vẽ biểu đồ đường: Biến động lương theo tháng
            this._renderSalaryTrendChart(data.salary_trend_data);
            this._renderRewardPenaltyChart(data.reward_penalty_ratio);
            this._renderAgeGroupChart(data.age_group_data);
        },
        _formatCurrency: function (amount) {
            return amount.toLocaleString('vi-VN') + ' VNĐ';
        },
        _renderDepartmentsBarChart: function (departmentsData) {
            if (!departmentsData || departmentsData.length === 0) return;
            var canvas = this.$('#departmentBarChart')[0];
            if (!canvas) return;
            var ctx = canvas.getContext('2d');
            var labels = departmentsData.map(function(d) { return d.name; });
            var data = departmentsData.map(function(d) { return d.count; });
            
            if (this.departmentChart) {
                this.departmentChart.destroy();
            }
            
            this.departmentChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Số lượng nhân sự',
                        data: data,
                        backgroundColor: [
                            '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e',
                            '#e74a3b', '#5a5c69', '#858796', '#6f42c1',
                            '#20c9a6', '#3498db'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Số lượng nhân sự'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Phòng ban'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        },
        _renderSalaryTrendChart: function (salaryTrendData) {
            if (!salaryTrendData || salaryTrendData.length === 0) return;
            var canvas = this.$('#salaryTrendChart')[0];
            if (!canvas) return;
            var ctx = canvas.getContext('2d');
            var labels = salaryTrendData.map(item => `Tháng ${item.month}`);
            //var labels = salaryTrendData.map(function(item) { return item.month; });
            var data = salaryTrendData.map(function(item) { return item.salary; });
            
            if (this.salaryTrendChart) {
                this.salaryTrendChart.destroy();
            }
            this.salaryTrendChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Tổng lương theo tháng',
                        data: data,
                        fill: false,
                        borderColor: '#4e73df',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },
        _renderRewardPenaltyChart: function (data) {
            if (!data || data.length === 0) return;
            var canvas = this.$('#rewardPenaltyChart')[0];
            if (!canvas) return;
            var ctx = canvas.getContext('2d');
            var labels = data.map(item => `Tháng ${item.month}`);
            // Nếu tỷ lệ là None, ta chuyển về 0 (hoặc có thể dùng null nếu Chart.js xử lý tốt)
            var ratioData = data.map(item => item.ratio !== null ? item.ratio : 0);
            if (this.rewardPenaltyChart) {
                this.rewardPenaltyChart.destroy();
            }
            this.rewardPenaltyChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Tỷ lệ thưởng/phạt',
                        data: ratioData,
                        fill: false,
                        borderColor: '#f6c23e',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
        },
        _renderAgeGroupChart: function (data) {
            if (!data) return;
            var canvas = this.$('#ageGroupChart')[0];
            if (!canvas) return;
            var ctx = canvas.getContext('2d');
        
            var labels = ['Dưới 25', '25-35', '36-45', '46-55', 'Trên 55'];
            var ageData = [
                data.under_25 || 0,
                data['25_35'] || 0,
                data['36_45'] || 0,
                data['46_55'] || 0,
                data.above_55 || 0
            ];
        
            if (this.ageGroupChart) {
                this.ageGroupChart.destroy();
            }
        
            this.ageGroupChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Phân bố độ tuổi nhân viên',
                        data: ageData,
                        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'],
                        hoverOffset: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
        
        
    });

    var DashboardOverviewView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: DashboardOverviewController
        })
    });

    viewRegistry.add('dashboard_overview_view', DashboardOverviewView);

    return {
        DashboardOverviewController: DashboardOverviewController,
        DashboardOverviewView: DashboardOverviewView,
    };
});
