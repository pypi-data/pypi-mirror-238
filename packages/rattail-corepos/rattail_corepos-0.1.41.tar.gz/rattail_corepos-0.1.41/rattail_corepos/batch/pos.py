# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
POS batch handler, for CORE-POS integration
"""

import logging

from rattail.batch import pos as base


log = logging.getLogger(__name__)


class POSBatchHandler(base.POSBatchHandler):
    """
    Handler for POS batches
    """

    def describe_execution(self, batch, **kwargs):
        return ("A new transaction will be created in CORE Office, directly "
                "in `dtransactions`, to mirror this batch.")

    def execute(self, batch, progress=None, **kwargs):
        rows = self.get_effective_rows(batch)
        if not rows:
            return True

        self.corepos_handler = self.app.get_corepos_handler()
        self.coretrans = self.corepos_handler.get_model_office_trans()
        self.maxlen_upc = self.app.maxlen(self.coretrans.TransactionDetail.upc)
        self.maxlen_description = self.app.maxlen(self.coretrans.TransactionDetail.description)

        # convert batch rows to `dtransactions` records
        dtransactions = self.normalize_dtransactions(batch, rows, progress)
        if not dtransactions:
            return True

        # commit all to `dtransactions`
        coretrans_session = self.corepos_handler.make_session_office_trans()
        coretrans_session.add_all(dtransactions)
        coretrans_session.commit()
        coretrans_session.close()
        return True

    def normalize_dtransactions(self, batch, rows, progress=None):
        dtransactions = []
        self.made_subtotal = False

        def add(row, i):

            if row.row_type == self.enum.POS_ROW_TYPE_SELL:
                d = self.make_d_item(row)
                dtransactions.append(d)

            elif row.row_type == self.enum.POS_ROW_TYPE_BADSCAN:
                d = self.make_d_badscan(row)
                dtransactions.append(d)

            elif row.row_type in (self.enum.POS_ROW_TYPE_SET_CUSTOMER,
                                  self.enum.POS_ROW_TYPE_SWAP_CUSTOMER):
                d = self.make_d_customer(row)
                dtransactions.append(d)

            elif row.row_type == self.enum.POS_ROW_TYPE_TENDER:

                if not self.made_subtotal:
                    d = self.make_d_subtotal(row, dtransactions)
                    dtransactions.append(d)
                    self.made_subtotal = True

                d = self.make_d_tender(row)
                dtransactions.append(d)

            elif row.row_type == self.enum.POS_ROW_TYPE_CHANGE_BACK:

                d = self.make_d_change(row)
                dtransactions.append(d)

                d = self.make_d_discount(batch, dtransactions)
                dtransactions.append(d)

                d = self.make_d_tax(batch, dtransactions)
                dtransactions.append(d)

        self.progress_loop(add, rows, progress,
                           message="Normalizing items for CORE-POS transaction")

        # now that we have all records, fill in some more values
        session = self.app.get_session(batch)
        store = self.config.get_store(session)
        store_id = store.corepos_id if store else None
        register_number = int(batch.terminal_id)
        employee_number = batch.cashier.corepos_number
        member = self.app.get_member(batch.customer)
        member_type = member.membership_type.number if member else None
        pos_row_id = f'corepos_pos_row_id_term_{batch.terminal_id}'
        self.app.make_counter(session, pos_row_id)
        for i, d in enumerate(dtransactions, 1):
            d.store_id = store_id
            d.register_number = register_number
            d.employee_number = employee_number
            d.card_number = batch.customer.number
            d.member_type = member_type
            d.staff = batch.customer_is_employee
            d.transaction_id = i
            d.pos_row_id = self.app.next_counter_value(session, pos_row_id)

        return dtransactions

    def make_d_basic(self, batch=None, row=None):
        if not batch and not row:
            raise ValueError("must specify either batch or row")
        
        if not batch:
            batch = row.batch

        d = self.coretrans.TransactionDetail()

        d.transaction_number = batch.id

        if row and row.timestamp:
            d.date_time = self.app.localtime(row.timestamp, from_utc=True)
        else:
            # nb. batch.created *should* have a value..if not this would be "now"
            d.date_time = self.app.localtime(batch.created, from_utc=True)

        # TODO: i *think* all these are safe defaults, and can
        # override per line item as needed
        d.transaction_status = ''
        d.department_number = 0
        d.unit_price = 0
        d.reg_price = 0
        d.tax_rate_id = 0
        d.food_stamp = False
        d.member_discount = 0
        d.discount_type = 0
        d.percent_discount = 0
        d.quantity = 0
        d.item_quantity = 0
        d.volume_discount_type = 0
        d.volume_special = 0
        d.mix_match = 0
        d.upc = '0'
        d.num_flag = 0
        d.char_flag = ''
        d.cost = 0
        d.discount = 0
        d.discountable = False
        d.total = 0
        d.voided = 0
        d.volume = 0
        d.matched = False

        return d

    def make_d_badscan(self, row):
        d = self.make_d_basic(row=row)

        d.description = 'BADSCAN'

        d.upc = row.item_entry
        if d.upc and len(d.upc) > self.maxlen_upc:
            log.debug("have to truncate this upc to %s chars (it has %s): %s",
                      self.maxlen_upc, len(d.upc), d.upc)
            d.upc = d.upc[:self.maxlen_upc]
            d.description += " (TRUNCATED)"

        return d

    def make_d_customer(self, row):
        batch = row.batch
        d = self.make_d_basic(row=row)

        d.upc = 'MEMENTRY'
        d.description = 'CARDNO IN NUMFLAG'

        # TODO: what do these mean? are they correct?
        d.transaction_type = 'L'
        d.transaction_subtype = 'OG'
        d.transaction_status = 'D'
        d.num_flag = batch.customer.number
        d.char_flag = '1'

        return d

    def make_d_item(self, row):
        batch = row.batch
        session = self.app.get_session(batch)
        d = self.make_d_basic(batch, row)

        d.transaction_type = 'I'
        d.transaction_subtype = 'NA'
        d.upc = row.product.item_id
        d.department_number = row.department_number
        d.food_stamp = row.foodstamp_eligible

        d.description = row.product.description
        if d.description and len(d.description) > self.maxlen_description:
            log.debug("have to truncate this description to %s chars (it has %s): %s",
                      self.maxlen_description, len(d.description), d.description)
            d.description = d.description[:self.maxlen_description]

        # TODO: should item_quantity ever differ?  see also
        # https://github.com/CORE-POS/IS4C/wiki/Office-Transaction-Database#dtransactions
        d.quantity = row.quantity
        d.item_quantity = row.quantity

        if row.product.cost:
            d.cost = row.product.cost.unit_cost

        d.unit_price = row.txn_price
        d.reg_price = row.reg_price
        d.discountable = row.product.discountable

        d.tax_rate_id = 0
        if row.tax_code:
            tax = self.get_tax(session, row.tax_code)
            d.tax_rate_id = tax.corepos_id
            if not d.tax_rate_id:
                log.error("tax not found in CORE-POS: %s", row.tax_code)
                d.tax_rate_id = 0

        d.total = row.sales_total
        # TODO: if void, should the above change too?
        d.voided = 1 if row.void else 0

        return d

    def make_d_subtotal(self, row, dtransactions):
        batch = row.batch
        d = self.make_d_basic(batch, row)

        d.transaction_type = 'C'
        d.transaction_status = 'D'
        d.voided = 3            # TODO (?)

        d.unit_price = sum([detail.total
                            for detail in dtransactions])

        # TODO
        tax = 0

        d.description = f"Subtotal {d.unit_price:0.2f}, Tax{tax:0.2f} #{batch.customer.number}"

        return d

    def make_d_tender(self, row):
        batch = row.batch
        d = self.make_d_basic(batch, row)

        d.transaction_type = 'T'
        d.transaction_subtype = row.item_entry
        d.description = row.description
        d.total = row.tender_total

        return d

    def make_d_change(self, row):
        batch = row.batch
        d = self.make_d_basic(batch, row)

        d.transaction_type = 'T'
        d.transaction_subtype = row.item_entry
        d.description = "Change"
        d.total = row.tender_total

        if not d.total:
            d.voided = 8        # TODO (?)

        return d

    def make_d_discount(self, batch, dtransactions):
        d = self.make_d_basic(batch)

        d.transaction_type = 'S'
        d.upc = 'DISCOUNT'
        d.quantity = 1
        d.item_quantity = 1
        d.description = "Discount"

        return d

    def make_d_tax(self, batch, dtransactions):
        d = self.make_d_basic(batch)

        d.transaction_type = 'A'
        d.upc = 'TAX'
        d.description = "Tax"

        return d
