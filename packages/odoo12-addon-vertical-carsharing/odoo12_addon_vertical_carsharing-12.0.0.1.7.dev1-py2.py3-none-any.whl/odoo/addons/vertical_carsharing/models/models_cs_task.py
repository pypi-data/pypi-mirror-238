# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class cs_task(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    cs_task_type = fields.Selection(selection=[
        ('none', 'None'),
        ('car', 'Car'),
        ('carconfig', 'CarConfig'),
        ('pu', 'Production unit'),
        ('community', 'Community'),
        ('cs_user_request', 'CsUser Request'),
        ('cs_update_data', 'Update data - Registration'),
        ('cs_reward', 'Reward'),
        ('cs_invoicing', 'Cs Invoicing')
    ], default='none', string=_("CS Task Type"))
