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


from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import time
import openerp.netsvc
import logging


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    def _unreconcile_lines(self, cr, uid, move_id, unlink=False):
        reconcile_obj = self.pool['account.move.reconcile']
        move_obj = self.pool['account.move']

        if not move_id:
            return False
        move = move_obj.browse(cr, uid, move_id)
        recs = []
        for ml in move.line_id:
            if ml.reconcile_id:
                recs += [ml.reconcile_id.id]
            if ml.reconcile_partial_id:
                recs += [ml.reconcile_partial_id.id]
        if recs:
            reconcile_obj.unlink(cr, uid, recs)
        if unlink:
            # If posted move, reset to draft
            if move.state not in ['draft']:
                move_obj.button_cancel(cr, uid, [move.id])
            move_obj.unlink(cr, uid, move.id)
        return True

    def _get_moves_chained(self, cr, uid, move_id):
        move_obj = self.pool['account.move']
        move_line_obj = self.pool['account.move.line']
        res = []
        move = move_obj.browse(cr, uid, move_id)
        for ml in move.line_id:
            rec_line_ids = []
            if ml.reconcile_id:
                domain = [('reconcile_id', '=', ml.reconcile_id.id)]
                rec_line_ids = move_line_obj.search(cr, uid, domain)
            if ml.reconcile_partial_id:
                domain = [('reconcile_partial_id', '=',
                           ml.reconcile_partial_id.id)]
                rec_line_ids = move_line_obj.search(cr, uid, domain)
            for rl in move_line_obj.browse(cr, uid, rec_line_ids):
                if not rl.move_id.id in res:
                    res.append(rl.move_id.id)
        return res

    def action_cancel(self, cr, uid, ids, context=None):
        _logger = logging.getLogger(__name__)
        for inv in self.browse(cr, uid, ids):
            # Unlink and delete autoinvoice
            if inv.auto_invoice_id:
                #
                # All moves chained to invoice by reconcile
                #
                all_moves = []
                # All moves chained to invoice supplier
                moves = self._get_moves_chained(cr, uid, inv.move_id.id)
                for m in moves:
                    if not m in all_moves:
                        all_moves.append(m)
                # All moves chained to transfer
                if inv.transfer_entry_id:
                    moves = self._get_moves_chained(
                        cr, uid, inv.transfer_entry_id.id)
                    for m in moves:
                        if not m in all_moves:
                            all_moves.append(m)
                # All moves chained to autoinvoice
                moves = self._get_moves_chained(
                    cr, uid, inv.auto_invoice_id.move_id.id)
                for m in moves:
                    if not m in all_moves:
                        all_moves.append(m)

                # Remove reconcile
                for move_id in all_moves:
                    self._unreconcile_lines(cr, uid, move_id)
                # Remove moves of invoices (I'll delete with standard workflow)
                i = all_moves.index(inv.auto_invoice_id.move_id.id)
                del all_moves[i]
                if inv.move_id.id in all_moves:
                    i = all_moves.index(inv.move_id.id)
                    del all_moves[i]
                # Unlink auto invoice
                self.action_cancel(cr, uid, [inv.auto_invoice_id.id], context)
                self.action_final_delete(cr, uid, [inv.auto_invoice_id.id],
                                         context)
                self.unlink(cr, uid, [inv.auto_invoice_id.id])

                # Unlink moves.
                for move_id in all_moves:
                    unlink = True
                    self._unreconcile_lines(cr, uid, move_id, unlink)

        return super(account_invoice, self).action_cancel(cr, uid, ids,
                                                          context=context)
