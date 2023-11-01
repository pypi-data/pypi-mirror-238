from odoo import models, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        """
        Overridden method to search for Account Analytic Accounts with an additional filter.
        This method extends the standard name search behavior for Account Analytic Accounts by adding a filter based on
        the account group of invoice line products when certain conditions are met.

         When the 'filter_invoice_line_account_analytic' context key is set, this method checks for the presence of
         'filter_invoice_line_account_analytic_product_id'. If this context key is provided,
          it filters the search results based on the associated product's account group.

        The purpose of this method is to enhance the standard name search functionality by considering the account
        group of products in invoice lines when searching for Account Analytic Accounts.

        """
        if self.env.context.get("filter_invoice_line_account_analytic"):
            product_id = self.env.context.get('filter_invoice_line_account_analytic')
            if product_id:
                product_ids = self.env['product.product'].search([('id', '=', product_id)])
                if product_ids:
                    args.append(['group_id', '=', product_ids[0].account_group_analytic_id.id])

        res = super(AccountAnalyticAccount, self)._name_search(name, args=args, operator=operator, limit=limit,
                                                                name_get_uid=name_get_uid)
        return ressss
