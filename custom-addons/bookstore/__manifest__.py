# -*- coding: utf-8 -*-
{
    'name': "bookstore",

    'summary': """
        Module Project Akhir BookStore""",

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
    'depends': ['base','report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/buku_view.xml',
        'views/type_view.xml',
        'views/perlengkapan_view.xml',      
        'views/publisher_view.xml',
        'views/penjualan_view.xml', 
        'views/member_view.xml',    
        'tools/tool_buku_view.xml',
        'tools/tool_perlengkapan_view.xml',
        'report/report.xml',
        'report/faktur_penjualan_pdf.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
