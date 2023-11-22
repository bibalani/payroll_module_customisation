# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError



class HrContract(models.Model):
    """
    Employee contract based on the visa, work permits
    allows to configure different Salary structure
    """
    _inherit = ['hr.contract']
    _description = 'Employee Contract'


    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure')
    schedule_pay = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi-annually', 'Semi-annually'),
        ('annually', 'Annually'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('bi-monthly', 'Bi-monthly'),
    ], string='Scheduled Pay', index=True, default='monthly',
    help="Defines the frequency of the wage payment.")
    mission_extra_wage = fields.Float(string='Mission Extra Wage', tracking=True)
    uninsured_wage = fields.Float(string='Uninsured Wage',tracking=True)
    job_allowance = fields.Float(string='Job Allowance', tracking=True)
    management_bonus = fields.Float(string='Management Bonus', tracking=True)
    project_management_bonus = fields.Float(string='Project Management Bonus', tracking=True)
    have_eidi = fields.Boolean(string='Have Eidi')
    have_years_of_service = fields.Boolean(string='Have Years of Service', required=True, default=True,)
    shift_allowance = fields.Boolean(string='Shift Allowance', tracking=True)
    shift_allowance_rate = fields.Float(string='Shift Allowance Rate', tracking=True,)
    on_call = fields.Float(string='On Call', tracking=True)
    child_allowance = fields.Float(string="Child Allowance")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            emp_id = val.get('employee_id')
            contract_date = [val.get('date_start'), val.get('date_end')]
            existing_contract = self.env['hr.contract'].search([('employee_id','=',emp_id),
                                                                ('date_end','>=', contract_date[0]),('date_start','<=', contract_date[1])])
        if not existing_contract:
            return super().create(vals_list)
        else:
            raise ValidationError(_('There is an time overlab between existing contracts and new contract')) 


    @api.constrains('shift_allowance', 'shift_allowance_rate')
    def _check_shift_allowance_rate(self):  
        for rec in self:  
            if (rec.shift_allowance == True) and (rec.shift_allowance_rate == 0):
                raise UserError('Please set a non-zero value for Shift Allowance Rate')





        

    def write(self, vals):
        res = super().write(vals)
        # to return edited object assuming regular write (checking anything)
        fields_to_check = {'employee_id', 'date_start', 'date_end'}
        if not any(field for field in fields_to_check if field in vals):
            return res
        for rec in self:
            emp_id = rec.employee_id.id
            start_date = rec.date_start
            end_date = rec.date_end
            existing_contract_count = self.env['hr.contract'].search_count([('employee_id','=',emp_id),
                                                                ('date_end','>=', start_date),('date_start','<=', end_date)])
            if existing_contract_count> 1:
                raise ValidationError(_('There is an time overlab between existing contracts and editing contract'))
        return res        


                                                      




    def get_all_structures(self):
        """
        @return: the structures linked to the given contracts, ordered by hierachy (parent=False first,
                 then first level children and so on) and without duplicata
        """
        structures = self.mapped('struct_id')
        if not structures:
            return []
        # YTI TODO return browse records
        return list(set(structures._get_parent_structure().ids))

    def get_attribute(self, code, attribute):
        return self.env['hr.contract.advantage.template'].search([('code', '=', code)], limit=1)[attribute]

    def set_attribute_value(self, code, active):
        for contract in self:
            if active:
                value = self.env['hr.contract.advantage.template'].search([('code', '=', code)], limit=1).default_value
                contract[code] = value
            else:
                contract[code] = 0.0


class HrContractAdvandageTemplate(models.Model):
    _name = 'hr.contract.advantage.template'
    _description = "Employee's Advantage on Contract"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    lower_bound = fields.Float('Lower Bound', help="Lower bound authorized by the employer for this advantage")
    upper_bound = fields.Float('Upper Bound', help="Upper bound authorized by the employer for this advantage")
    default_value = fields.Float('Default value for this advantage')



