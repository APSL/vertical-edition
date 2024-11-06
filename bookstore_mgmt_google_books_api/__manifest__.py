# Copyright 2024 (APSL-Nagarro) - Miquel Alzanillas, Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "Google Books API for Bookstore Management",
    'summary': """Bookstore integration with Google Books API """,
    'author': "APSL-Nagarro, Odoo Community Association (OCA)",
    'website': "https://github.com/miquelalzanillas",
    'category': 'Misc',
    "license": "AGPL-3",
    "maintainers": ["peluko00"],
    'version': '17.0.1.0.0',
    'depends': ['bookstore_mgmt', 'web_notify'],
    'external_dependencies': {
        'python': [
            'google-books-api-wrapper',
        ],
    },
    'data': [
        'views/product.xml',
    ],
}
