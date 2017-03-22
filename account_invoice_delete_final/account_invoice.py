# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2013 Alessandro Camilli
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
from openerp.osv import fields, orm
from openerp.tools.translate import _
import time

class account_invoice(orm.Model):
    _inherit = "account.invoice"
 
    def action_final_delete(self, cr, uid, ids, *args):
        
        for inv in self.browse(cr, uid, ids):
            
            if inv.number:
                raise orm.except_orm(_('Error !'),
                    _('You can not delete invoice with number !'))
                continue
            # Clear internal number to allow cancellation
            if inv.internal_number:
                self.write(cr, uid, [inv.id], {'internal_number': False})
            
            # Unlink
            self.action_cancel(cr, uid, [inv.id])
            # TO DO!!!
            #self.unlink(cr, uid, [inv.id])
        
        return True