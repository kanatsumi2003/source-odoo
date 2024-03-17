from odoo import http
from odoo.http import request
import odoo.tools.config
import datetime
import logging
import os
import re
import tempfile

from lxml import html

import odoo
import odoo.modules.registry
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, Response
from odoo.service import db
from odoo.tools.misc import file_open, str2bool
from odoo.tools.translate import _

from odoo.addons.base.models.ir_qweb import render as qweb_render

from odoo import http
from odoo.http import request


class AutoCreateDB(http.Controller):
    @http.route('/<subdomain>/', type='http', auth="none", csrf=False)
    def check_and_create_db(self, subdomain, **kwargs):
        if not self._database_exists(subdomain):
            self._create_database(subdomain)

        return request.redirect('/web/database/selector', subdomain=subdomain)

    def _database_exists(self, subdomain):
        # Sử dụng API của Odoo để kiểm tra xem cơ sở dữ liệu có tồn tại không
        db_exist = request.env['ir.config_parameter'].sudo().get_param('database.existing_db_names')
        return subdomain in db_exist.split(',')

    def _create_database(self, subdomain):
        # Tạo cơ sở dữ liệu mới
        try:
            request.env.cr.create_empty_db(subdomain)
        except Exception as e:
            # Xử lý các trường hợp ngoại lệ, ví dụ: cơ sở dữ liệu không thể được tạo
            pass

    # @http.route('/web/database/create', type='http', auth="none", methods=['POST'], csrf=False)
    # def create(self, master_pwd, name, lang, password, **post):
    #     try:
    #         # Ensure the master password is correct and change it if insecure
    #         insecure = config.verify_admin_password('admin')
    #         if insecure and master_pwd:
    #             admin_user = request.env['res.users'].sudo().search([('login', '=', 'admin')], limit=1)
    #             if admin_user:
    #                 admin_user.write({'password': master_pwd})
    #
    #         # Validate the database name
    #         if not re.match('^[a-zA-Z0-9_-]+$', name):
    #             raise ValidationError(
    #                 'Invalid database name. Only alphanumerical characters, underscore, hyphen, and dot are allowed.')
    #
    #         # Create the database
    #         db_manager = request.env['ir.http']
    #         db_manager.db_create(master_pwd, name, demo=bool(post.get('demo')), lang=lang, user_password=password,
    #                              login=post['login'], country_code=post.get('country_code'), phone=post['phone'])
    #
    #         # Authenticate the user and set session
    #         request.session.authenticate(name, post['login'], password)
    #         request.session.db = name
    #
    #         # Redirect to the Odoo web interface
    #         return request.redirect('/web')
    #     except Exception as e:
    #         # Log the exception
    #         _logger.exception("Database creation error: %s", e)
    #         error = "Database creation error: %s" % (str(e) or repr(e))
    #         return request.render('your_module_name.error_template', {'error': error})


# @http.route('/web/database/create', type='json', auth="public", methods=['POST'])
# def create_database(self, **kwargs):
#     try:
#         # Extract parameters from the request
#         master_pwd = kwargs.get('master_pwd')
#         name = kwargs.get('name')
#         lang = kwargs.get('lang')
#         password = kwargs.get('password')
#         demo = kwargs.get('demo', True)
#         login = kwargs.get('login')
#         country_code = kwargs.get('country_code')
#         phone = kwargs.get('phone')
#
#         # Ensure all required parameters are provided
#         if not all([master_pwd, name, lang, password, login]):
#             raise ValidationError('Missing required parameters')
#
#         # Validate the database name
#         if not re.match('^[a-zA-Z0-9_-]+$', name):
#             raise ValidationError(
#                 'Invalid database name. Only alphanumerical characters, underscore, hyphen, and dot are allowed.')
#
#         # Create the database
#         db_manager = request.env['ir.http']
#         db_manager.db_create(master_pwd, name, demo=demo, lang=lang, user_password=password, login=login,
#                              country_code=country_code, phone=phone)
#
#         # Authenticate the user and set session
#         request.session.authenticate(name, login, password)
#         request.session.db = name
#
#         # Return success response
#         return {"status": "success", "message": "Database created successfully"}
#     except Exception as e:
#         # Log the exception
#         _logger.exception("Database creation error: %s", e)
#         error = "Database creation error: %s" % (str(e) or repr(e))
#         return {"status": "error", "message": error}