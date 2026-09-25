# -*- coding: utf-8 -*-
from odoo import fields, models


class HrZone(models.Model):
    _name = 'hr.zone'
    _description = 'HR Zone'
    _order = 'name'

    name = fields.Char(required=True)
    region_id = fields.Many2one('res.country.state', string='Region')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A zone with this name already exists.'),
    ]


class HrBranch(models.Model):
    _name = 'hr.branch'
    _description = 'HR Branch'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char()
    city = fields.Char(required=True)
    zone_id = fields.Many2one('hr.zone', string='Zone', required=True)
    region_id = fields.Many2one(
        'res.country.state', string='Region', related='zone_id.region_id',
        store=True, readonly=True,
    )
    address = fields.Text()
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A branch with this name already exists.'),
    ]


class HrDivision(models.Model):
    _name = 'hr.division'
    _description = 'HR Division'
    _order = 'name'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A division with this name already exists.'),
    ]


class HrSubDepartment(models.Model):
    _name = 'hr.sub.department'
    _description = 'HR Sub-Department'
    _order = 'name'

    name = fields.Char(required=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    active = fields.Boolean(default=True)


class HrManagementLevel(models.Model):
    _name = 'hr.management.level'
    _description = 'HR Management Level'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A management level with this name already exists.'),
    ]


class HrGrade(models.Model):
    _name = 'hr.grade'
    _description = 'HR Grade'
    _order = 'sequence, name'

    name = fields.Char(required=True, string='Grade')
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A grade with this name already exists.'),
    ]
