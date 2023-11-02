import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        'depends_override': {
            'auto_setup_bank_account_number': "odoo12-addon-auto-setup-bank-account-number==12.0.1.0.1",
        }
    },
)
