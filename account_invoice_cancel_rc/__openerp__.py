# -*- coding: utf-8 -*-
##############################################################################
#    
#    Author: Alessandro Camilli (alessandrocamilli@openforce.it)
#    Copyright (C) 2016
#    Openforce di Camilli Alessandro (www.openforce.it)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Account Invoice Cancel RC ',
    'version': '0.2',
    'category': 'Sale',
    'description': """
    It cancel the invoice created with reverse charge method.
    It unlinks:
    - refunds
    - auto invoice
""",
    'author': 'Alessandro Camilli - Openforce',
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    "depends" : ['l10n_it_invoice_intra_cee', 'account_invoice_delete_final'],
    "data" : [],
    "demo" : [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
