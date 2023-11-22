from odoo import api, fields, models


class HRPayPeriod(models.Model):
    _name = "hr.pay.period"
    _description = 'Pay Period'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Name')
    start_date = fields.Date(string='Start', tracking=True)
    end_date = fields.Date(string='End',tracking=True)
    ins_start_date = fields.Date(string='Insurance Period Start', tracking=True)
    ins_end_date = fields.Date(string='Insurance Period End',tracking=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('open', 'Open'),
                              ('manager', 'Manager Approval'),
                              ('payroll', 'Payroll Processing'),
                              ('closed', 'Closed'),
                              ('removed', 'Removed')
                              ], string='Status', tracking=True)
    description = fields.Char(string='Description')

    defaults = {
        'state': 'draft'
    }
