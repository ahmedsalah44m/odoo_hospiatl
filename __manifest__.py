{
    'name':'hospital',
    'description':"hospital app for mangment hospitals",
    'author':'Ahmed_Salah',
    'description':'app to mange hospitals',
    'version':'0.1',
    'depends':['shopping_app_odoo_16','base'],

    'data':[
        'view/hospital_patients_view.xml',
        'view/doctors_view.xml',
        'view/templates.xml',
        'security/ir.model.access.csv',
        'view/appointments.xml',
        'view/menuitems.xml'
    ],
    'category':'uncategorized',

}