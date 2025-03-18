from odoo import models , fields, api , _



class MyHospital(models.Model):
    _inherit = 'res.partner'
    birthday = fields.Date()
    age = fields.Integer()
    is_patient = fields.Boolean()

class Doctor(models.Model):
    _inherit = "res.users"

    is_doctor = fields.Boolean(string='IS Doctor')
    is_nurse = fields.Boolean(string='IS Doctor Manager')


class MyAppointments(models.Model):
    _name = 'my.appointments'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Appointment" , required=True,copy=False,
                       readonly=True,index=True,default=lambda self:_('new') )
    patient_id = fields.Many2one('res.partner' ,domain='[("is_patient","=",True)]',string='Patient',required=True)
    app_date = fields.Date(string='App Date'  )
    patients_age = fields.Integer(string='Patients Age' ,related="patient_id.age" )
    notes = fields.Text(string='Notes' )


    @api.model
    def create(self,values):
        if values.get('name',_('new')) == _('new'):
            values['name'] = self.env['ir.sequence'].next_by_code("hospital.appointment.sequence") or _('new')
        result = super(MyAppointments,self).create(values)
        return result