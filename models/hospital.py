from odoo import models , fields, api , _
from odoo.tools.populate import compute


class MyHospital(models.Model):
    _inherit = 'res.partner'
    birthday = fields.Date()
    age = fields.Integer()
    is_patient = fields.Boolean()
    appointments_count =fields.Integer(compute="compute_appointments_count",string='Appointments Count')

    def compute_appointments_count(self):
        count = self.env["my.appointments"].search_count([("patient_id",'=',self.id)])
        self.appointments_count = count


    def get_patient_appointments(self):
        action = {
            'name':'appointment button action',
            'type':"ir.actions.act_window",
            "res_model":"my.appointments",
            "view_mode":"tree,form",
            "view_id":False,
            "domain":[("patient_id", "=",self.id)]
        }
        return action


class Doctor(models.Model):
    _inherit = "res.users"

    is_doctor = fields.Boolean(string='IS Doctor')
    is_nurse = fields.Boolean(string='IS Doctor Manager')


class MyAppointments(models.Model):
    _name = 'my.appointments'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    status = fields.Selection([("draft","Draft"),("confirm","Confirm"),("done","Done"),("canceled","Canceled")],
                              string="Status" , default='draft')
    name = fields.Char(string="Appointment" , required=True,copy=False,
                       readonly=True,index=True,default=lambda self:_('new') )
    patient_id = fields.Many2one('res.partner' ,domain='[("is_patient","=",True)]',string='Patient',required=True)
    app_date = fields.Date(string='App Date'  )
    patients_age = fields.Integer(string='Patients Age' ,related="patient_id.age" )
    notes = fields.Text(string='Notes' )
    doctor_notes = fields.Text()
    doctor_id = fields.Many2one('res.users',domain="[('is_doctor','=',True)]", required=True)
    prescription_ids = fields.One2many("prescription","appointment_id",
                                       string="prescription")

    @api.model
    def create(self,values):
        if values.get('name',_('new')) == _('new'):
            values['name'] = self.env['ir.sequence'].next_by_code("hospital.appointment.sequence") or _('new')
        result = super(MyAppointments,self).create(values)
        return result

    def confirm_action(self):
        for r in self:
            r.status = "confirm"

    def done_action(self):
        for r in self:
            r.status = "done"

    def back_action(self):
        back_step = {
            "done" : "confirm",
            "confirm" : "draft",
            "canceled" : "draft",
        }
        for r in self:
            r.status = back_step[r.status]
    def canceled_action(self):
        for r in self:
            r.status = "canceled"

class Prescription(models.Model):
    _name = "prescription"

    name = fields.Char(string="Medicine Name")
    notes = fields.Text(string="Notes")
    appointment_id = fields.Many2one("my.appointments")
    medicine_id = fields.Many2one("the.medicine")

class Medicine(models.Model):
    _name = "the.medicine"

    name =fields.Char()
    effective_material = fields.Char()
    prescription_ids = fields.One2many('prescription','medicine_id')