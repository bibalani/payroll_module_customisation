# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError


class HrPayslipEmployees(models.TransientModel):
    _name = 'hr.payslip.employees'
    _description = 'Generate payslips for all selected employees'

    employee_ids = fields.Many2many('hr.employee', 'hr_employee_group_rel', 'payslip_id', 'employee_id', 'Employees',
                                    compute='_compute_employee_ids')

    # def _compute_payslip_batch_id(self):
    #     latest_rec = self.env['hr.payslip.run'].search([], limit=1, order='create_date desc')
    #     self.payslip_batch_id = latest_rec

    
    def _compute_employee_ids(self):
        active_id = self.env.context.get('active_id')
        payslip_batch_obj = self.env['hr.payslip.run'].browse(active_id)
        struct_ids = payslip_batch_obj.struct_ids
        if struct_ids:
            contract_objs = self.env['hr.contract'].search(['&','&','&','&',('employee_company_id','=',payslip_batch_obj.employee_company_id.id),
                                                            ('date_end','>=',payslip_batch_obj.date_start),('date_start','<=',payslip_batch_obj.date_end),
                                                            ('state','in',('open', 'onleave')),('struct_id','in',struct_ids.ids)])
        else:
            contract_objs = self.env['hr.contract'].search(['&','&','&',('employee_company_id','=',payslip_batch_obj.employee_company_id.id),
                                                            ('date_end','>=',payslip_batch_obj.date_start),('date_start','<=',payslip_batch_obj.date_end),
                                                            ('state','in',('open', 'onleave'))])
        self.employee_ids =  [contract.employee_id.id for contract in contract_objs]


    def compute_sheet(self):
        payslips = self.env['hr.payslip']
        [data] = self.read()
        active_id = self.env.context.get('active_id')
        if active_id:
            [run_data] = self.env['hr.payslip.run'].browse(active_id).read(['date_start', 'date_end', 'credit_note','pay_period_id'])
        print('pay_priod_id.....................', run_data.get('pay_period_id'))    
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        if not data['employee_ids']:
            raise UserError(_("There is NOT any feasible payslip to create given pay period and contract!."))
        for employee in self.env['hr.employee'].browse(data['employee_ids']):
            slip_data = self.env['hr.payslip'].onchange_employee_id(from_date, to_date, employee.id, contract_id=False)
            res = {
                'employee_id': employee.id,
                'name': slip_data['value'].get('name'),
                'struct_id': slip_data['value'].get('struct_id'),
                'contract_id': slip_data['value'].get('contract_id'),
                'payslip_run_id': active_id,
                'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
                'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
                'date_from': from_date,
                'date_to': to_date,
                'credit_note': run_data.get('credit_note'),
                'employee_company_id': employee.employee_company_id.id,
                'pay_period_id': run_data.get('pay_period_id')[0],
            }
            payslips += self.env['hr.payslip'].create(res)
        payslips.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}
