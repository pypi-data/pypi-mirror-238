from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    account_group_analytic_id = fields.Many2one('account.analytic.group', string='Analytic Group')
