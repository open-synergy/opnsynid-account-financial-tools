import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-open-synergy-opnsynid-account-financial-tools",
    description="Meta package for open-synergy-opnsynid-account-financial-tools Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-account_asset_queue',
        'odoo11-addon-account_bank_statement_analytic_tag_reconcilliation',
        'odoo11-addon-account_bank_statement_reconcilliation_show_journal',
        'odoo11-addon-account_deferred_revenue_extra_move',
        'odoo11-addon-account_deferred_revenue_restrict_deletation',
        'odoo11-addon-account_lock_date_group',
        'odoo11-addon-account_move_line_day_overdue',
        'odoo11-addon-account_move_line_latest_reconcilliation_date',
        'odoo11-addon-account_move_workflow_policy',
        'odoo11-addon-ssi_analytic_account_mass_assign',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)
