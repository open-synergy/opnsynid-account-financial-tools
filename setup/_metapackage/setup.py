import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-account-financial-tools",
    description="Meta package for open-synergy-opnsynid-account-financial-tools Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_analytic_account_mass_assign',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
