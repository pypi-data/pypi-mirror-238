from odoo import models, fields, api


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    # Temporary override to allow one account to be held by multiple partners
    _sql_constraints = [
        ('unique_number', 'unique(sanitized_acc_number, company_id, partner_id)',
         'Account Number must be unique'),
    ]
