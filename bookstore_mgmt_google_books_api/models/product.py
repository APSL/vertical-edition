# Copyright 2024 (APSL-Nagarro) - Miquel Alzanillas, Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import time

from odoo import models, _
from odoo.exceptions import UserError
from google_books_api_wrapper.api import GoogleBooksAPI
import base64
import requests
from datetime import datetime

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_convert_to_base64(self, url):
        return base64.b64encode(requests.get(url).content)
    
    def get_editorial_id(self, editorial_name):
        editorial_id = self.env['product.book.editorial'].search([('name', 'ilike', editorial_name)])
        if not editorial_id:
            editorial_id = self.env['product.book.editorial'].create({'name': editorial_name})
        if len(editorial_id) > 1:
                editorial = editorial_id.filtered(lambda x: x.name==editorial_name)
                return editorial if editorial else editorial_id[0]
        return editorial_id
    
    def get_genre_id(self, genres):
        for genre_name in genres:
            genre_id = self.env['product.book.genre'].search([('name', 'ilike', genre_name)])
            if not genre_id:
                genre_id = self.env['product.book.genre'].create({'name': genre_name})
            if len(genre_id) > 1:
                genre = genre_id.filtered(lambda x: x.name==genre_name)
                return genre if genre else genre_id[0]
            return genre_id
                
    def get_author_id(self, author_name):
        author_id = self.env['product.book.author'].search([('name', 'ilike', author_name)])
        if not author_id:
            author_id = self.env['product.book.author'].create({'name': author_name})
        if len(author_id) > 1:
            author = author_id.filtered(lambda x: x.name==author_name)
            return author if author else author_id[0]
        return author_id
        
    def action_import_from_isbn(self):
        for record in self:
            if record.barcode:       
                client = GoogleBooksAPI()
                isbn = record.barcode.replace("-", "")
                book = client.get_book_by_isbn13(isbn)
                if not book:
                     book = client.get_book_by_isbn10(isbn)
                if book:
                    #Set data to be updated
                    data = {
                        'name': book.title,
                    }
                    
                    if book.published_date:
                        #Convert to year format
                        try:
                            published_year = datetime.strptime(book.published_date, '%Y-%m-%d').year
                        except:
                            published_year = book.published_date
                            
                        data['year_edition'] = published_year
                        
                    if book.authors and not record.author_id:
                        data['author_id'] = record.get_author_id(book.authors[0])
                        
                    if book.publisher and not record.editorial_id:
                        data['editorial_id'] = record.get_editorial_id(book.publisher)
                        
                    if book.subjects:
                        data['genre_id'] = record.get_genre_id(book.subjects)
                        
                    if book.description and not record.description:
                        data['description'] = book.description

                    if book.large_thumbnail and not record.image_1920:
                        data['image_1920'] = record.get_convert_to_base64(book.large_thumbnail)
                    
                    # Update book data in Odoo
                    record.write(data)   
                    
                    # Show success notification                 
                    self.env.user.notify_success(message=_("Book data updated from Google Books API"))
                    
                    # Reload page
                    # return {
                    #     'type': 'ir.actions.client',
                    #     'tag': 'reload',
                    #} 
                else:
                    # Return not found notification
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': _('Warning'),
                            'type': 'warning',
                            'message': _('Not book found with this data'),
                            'sticky': True,
                        }
                    } 
            else:
                raise UserError(_("ISBN code is mandatory. Please, provide one."))
