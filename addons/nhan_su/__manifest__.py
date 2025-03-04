# -*- coding: utf-8 -*-
{
    'name': "nhan_su",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/nhan_vien.xml',
        'views/don_vi.xml',
        'views/chuc_vu.xml',
        'views/lich_su_cong_tac.xml',
        'views/chung_chi.xml',
        'views/phong_ban.xml',
        'views/khoa_hoc.xml',
        'views/khoa_dao_tao.xml',
        'views/tham_gia_khoa_dao_tao.xml',
        'views/hop_dong.xml',
        'views/bang_luong.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
