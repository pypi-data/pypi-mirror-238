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
CORE POS (DB) -> Rattail data importing
"""

import datetime
import decimal
import logging
from collections import OrderedDict

import sqlalchemy as sa
from sqlalchemy import orm

from corepos.db.office_op import model as corepos, Session as CoreSession
from corepos.db.office_trans import model as coretrans, Session as CoreTransSession

from rattail import importing
from rattail.gpc import GPC
from rattail.db.util import normalize_full_name
from rattail_corepos import importing as corepos_importing


log = logging.getLogger(__name__)


class FromCOREPOSToRattail(importing.FromSQLAlchemyHandler, importing.ToRattailHandler):
    """
    Import handler for data coming from a CORE POS database.
    """
    # TODO: these should be changed, it now allows for "trans" DB too..
    generic_host_title = 'CORE Office (DB "op")'
    host_key = 'corepos_db_office_op'
    corepos_dbkey = 'default'

    @property
    def host_title(self):
        return "CORE-POS (DB/{})".format(self.corepos_dbkey)

    def make_host_session(self):

        # session type depends on the --corepos-dbtype arg
        if self.corepos_dbtype == 'office_trans':
            return CoreTransSession(bind=self.config.coretrans_engines[self.corepos_dbkey])

        # assume office_op by default
        return CoreSession(bind=self.config.corepos_engines[self.corepos_dbkey])

    def get_importers(self):
        importers = OrderedDict()
        importers['Store'] = StoreImporter
        importers['Employee'] = EmployeeImporter
        importers['Customer'] = CustomerImporter
        importers['Member'] = MemberImporter
        importers['Tax'] = TaxImporter
        importers['Tender'] = TenderImporter
        importers['Vendor'] = VendorImporter
        importers['Department'] = DepartmentImporter
        importers['Subdepartment'] = SubdepartmentImporter
        importers['Product'] = ProductImporter
        importers['ProductCost'] = ProductCostImporter
        importers['MemberEquityPayment'] = MemberEquityPaymentImporter
        return importers

    def get_default_keys(self):
        keys = super().get_default_keys()

        if 'MemberEquityPayment' in keys:
            keys.remove('MemberEquityPayment')

        return keys


class FromCOREPOS(importing.FromSQLAlchemy):
    """
    Base class for all CORE POS data importers.
    """

    def setup(self):
        super().setup()
        self.ignore_new_members = self.should_ignore_new_members()

    def should_ignore_new_members(self):
        if hasattr(self, 'ignore_new_members'):
            return self.ignore_new_members

        return self.config.getbool('rattail_corepos',
                                   'importing_ignore_new_members',
                                   default=False)

    def is_new_member(self, member):
        if member.customers:
            customer = member.customers[0]
            if customer.last_name == 'NEW MEMBER'and not customer.first_name:
                return True
        return False


class StoreImporter(FromCOREPOS, corepos_importing.model.StoreImporter):
    """
    Importer for store data from CORE POS.
    """
    host_model_class = corepos.Store
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'id',
        'name',
    ]

    def normalize_host_object(self, store):
        return {
            'corepos_id': store.id,
            'id': str(store.id),
            'name': store.description,
        }


class EmployeeImporter(FromCOREPOS, corepos_importing.model.EmployeeImporter):
    """
    Importer for employee data from CORE POS.
    """
    host_model_class = corepos.Employee
    key = 'corepos_number'
    supported_fields = [
        'corepos_number',
        'first_name',
        'last_name',
        'full_name',
        'status',
    ]

    def normalize_host_object(self, employee):
        return {
            'corepos_number': employee.number,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'full_name': normalize_full_name(employee.first_name, employee.last_name),
            'status': self.enum.EMPLOYEE_STATUS_CURRENT if employee.active else self.enum.EMPLOYEE_STATUS_FORMER,
        }


class CustomerImporter(FromCOREPOS, corepos_importing.model.CustomerImporter):
    """
    Importer for customer data from CORE POS.
    """
    host_model_class = corepos.MemberInfo
    key = 'corepos_card_number'
    supported_fields = [
        'corepos_card_number',
        'number',
        'name',
        'account_holder_uuid',
        'account_holder_first_name',
        'account_holder_last_name',
        'email_address',
        'phone_number',
        'address_street',
        'address_street2',
        'address_city',
        'address_state',
        'address_zipcode',
    ]

    def setup(self):
        super().setup()
        model = self.model

        query = self.session.query(model.Person)\
                            .outerjoin(model.Customer,
                                       model.Customer.account_holder_uuid == model.Person.uuid)\
                            .outerjoin(model.CoreCustomer)\
                            .outerjoin(model.Member,
                                       model.Member.person_uuid == model.Person.uuid)\
                            .outerjoin(model.CoreMember)\
                            .filter(sa.or_(
                                model.CoreCustomer.corepos_card_number != None,
                                model.CoreMember.corepos_card_number != None))\
                            .options(orm.joinedload(model.Person.customer_accounts)\
                                     .joinedload(model.Customer._corepos))
        def card_number(person, normal):
            customer = self.app.get_customer(person)
            if customer and customer.corepos_card_number:
                return customer.corepos_card_number
            member = self.app.get_member(person)
            if member and member.corepos_card_number:
                return member.corepos_card_number
        self.people_by_card_number = self.cache_model(model.Person, query=query,
                                                      key=card_number)

    def get_person(self, member):

        if hasattr(self, 'people_by_card_number'):
            return self.people_by_card_number.get(member.card_number)

        model = self.model

        try:
            return self.session.query(model.Person)\
                               .join(model.Customer,
                                     model.Customer.account_holder_uuid == model.Person.uuid)\
                               .join(model.CoreCustomer)\
                               .filter(model.CoreCustomer.corepos_card_number == member.card_number)\
                               .one()
        except orm.exc.NoResultFound:
            pass

        try:
            return self.session.query(model.Person)\
                               .join(model.Member,
                                     model.Member.person_uuid == model.Person.uuid)\
                               .join(model.CoreMember)\
                               .filter(model.CoreMember.corepos_card_number == member.card_number)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def normalize_host_object(self, member):
        card_number = member.card_number

        # maybe ignore NEW MEMBER accounts
        if self.should_ignore_new_members():
            if self.is_new_member(member):
                return

        contact = member
        if member.customers:
            contact = member.customers[0]

        person = self.get_person(member)

        street = (member.street or '').split('\n')

        return {
            'corepos_card_number': card_number,
            'number': card_number,
            'name': normalize_full_name(contact.first_name, contact.last_name),
            'account_holder_uuid': person.uuid if person else None,
            'account_holder_first_name': contact.first_name,
            'account_holder_last_name': contact.last_name,
            'email_address': (member.email or '').strip() or None,
            'phone_number': self.app.format_phone_number((member.phone or '').strip() or None),
            'address_street': street[0] or None,
            'address_street2': (street[1] or None) if len(street) > 1 else None,
            'address_city': member.city or None,
            'address_state': member.state or None,
            'address_zipcode': member.zip or None,
        }


class MemberImporter(FromCOREPOS, corepos_importing.model.MemberImporter):
    """
    Importer for member data from CORE POS.
    """
    host_model_class = corepos.MemberInfo
    # TODO use this key instead
    #key = 'corepos_card_number'
    key = 'number'
    supported_fields = [
        'number',
        'corepos_card_number',
        'customer_uuid',
        'person_uuid',
        'person_first_name',
        'person_last_name',
        'membership_type_number',
        'joined',
        'withdrew',
        'active',
    ]

    def setup(self):
        super().setup()
        model = self.model

        self.customers_by_number = self.app.cache_model(self.session,
                                                        model.Customer,
                                                        key='number')

        query = self.session.query(model.Person)\
                            .outerjoin(model.Customer,
                                       model.Customer.account_holder_uuid == model.Person.uuid)\
                            .outerjoin(model.CoreCustomer)\
                            .outerjoin(model.Member,
                                       model.Member.person_uuid == model.Person.uuid)\
                            .outerjoin(model.CoreMember)\
                            .filter(sa.or_(
                                model.CoreCustomer.corepos_card_number != None,
                                model.CoreMember.corepos_card_number != None))\
                            .options(orm.joinedload(model.Person.customer_accounts)\
                                     .joinedload(model.Customer._corepos))
        def card_number(person, normal):
            customer = self.app.get_customer(person)
            if customer and customer.corepos_card_number:
                return customer.corepos_card_number
            member = self.app.get_member(person)
            if member and member.corepos_card_number:
                return member.corepos_card_number
        self.people_by_card_number = self.cache_model(model.Person, query=query,
                                                      key=card_number)

    def get_person(self, member):
        if hasattr(self, 'people_by_card_number'):
            return self.people_by_card_number.get(member.card_number)

        model = self.model

        try:
            return self.session.query(model.Person)\
                               .join(model.Customer,
                                     model.Customer.account_holder_uuid == model.Person.uuid)\
                               .join(model.CoreCustomer)\
                               .filter(model.CoreCustomer.corepos_card_number == member.card_number)\
                               .one()
        except orm.exc.NoResultFound:
            pass

        try:
            return self.session.query(model.Person)\
                               .join(model.Member,
                                     model.Member.person_uuid == model.Person.uuid)\
                               .join(model.CoreMember)\
                               .filter(model.CoreMember.corepos_card_number == member.card_number)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_customer_by_number(self, number):
        if hasattr(self, 'customers_by_number'):
            return self.customers_by_number.get(number)

        model = self.model
        try:
            return self.session.query(model.Customer)\
                               .filter(model.Customer.number == number)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def normalize_host_object(self, core_member):

        # maybe ignore NEW MEMBER accounts
        if self.should_ignore_new_members():
            if self.is_new_member(core_member):
                return

        core_customer = core_member.customers[0] if core_member.customers else None
        core_contact = core_customer or core_member

        card_number = core_member.card_number
        customer = self.get_customer_by_number(card_number)
        person = self.get_person(core_member)

        typeno = None
        if core_customer and core_customer.member_type:
            typeno = core_customer.member_type.id

        joined = None
        withdrew = None
        if core_member.dates:
            dates = core_member.dates
            joined = dates.start_date.date() if dates.start_date else None
            withdrew = dates.end_date.date() if dates.end_date else None
            if joined and joined == datetime.date(1900, 1, 1):
                joined = None
            if withdrew and withdrew == datetime.date(1900, 1, 1):
                withdrew = None

        return {
            'number': card_number,
            'corepos_card_number': card_number,
            'customer_uuid': customer.uuid if customer else None,
            'person_uuid': person.uuid if person else None,
            'person_first_name': core_contact.first_name,
            'person_last_name': core_contact.last_name,
            'membership_type_number': typeno,
            'joined': joined,
            'withdrew': withdrew,
            'active': not bool(withdrew),
        }


class TaxImporter(FromCOREPOS, corepos_importing.model.TaxImporter):
    """
    Importer for tax data from CORE POS.
    """
    host_model_class = corepos.TaxRate
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'code',
        'description',
        'rate',
    ]

    def normalize_host_object(self, tax):
        return {
            'corepos_id': tax.id,
            'code': str(tax.id),
            'description': tax.description,
            'rate': decimal.Decimal(str(tax.rate * 100)),
        }


class TenderImporter(FromCOREPOS, corepos_importing.model.TenderImporter):
    """
    Importer for tender data from CORE POS.
    """
    host_model_class = corepos.Tender
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'code',
        'name',
    ]

    def normalize_host_object(self, tender):
        return {
            'corepos_id': tender.tender_id,
            'code': tender.tender_code,
            'name': tender.tender_name,
        }


class VendorImporter(FromCOREPOS, corepos_importing.model.VendorImporter):
    """
    Importer for vendor data from CORE POS.
    """
    host_model_class = corepos.Vendor
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'name',
        'abbreviation',
        'special_discount',
        'phone_number',
        'fax_number',
        'email_address',
    ]

    def cache_query(self):
        """
        Return the query to be used when caching "local" data.
        """
        # can't just use rattail.db.model b/c the CoreVendor would normally not
        # be in there!  this still requires custom model to be configured though.
        model = self.config.get_model()

        # first get default query
        query = super().cache_query()

        # maybe filter a bit, to ensure only "relevant" records are involved
        if 'corepos_id' in self.key:
            # note, the filter is probably redundant since we INNER JOIN on the
            # extension table, and it doesn't allow null ID values.  but clarity.
            query = query.join(model.CoreVendor)\
                         .filter(model.CoreVendor.corepos_id != None)

        return query

    def normalize_host_object(self, vendor):

        special_discount = None
        if vendor.discount_rate is not None:
            special_discount = decimal.Decimal('{:0.3f}'.format(vendor.discount_rate))

        return {
            'corepos_id': vendor.id,
            'name': vendor.name,
            'abbreviation': vendor.abbreviation or None,
            'special_discount': special_discount,
            'phone_number': vendor.phone or None,
            'fax_number': vendor.fax or None,
            'email_address': vendor.email or None,
        }


class DepartmentImporter(FromCOREPOS, corepos_importing.model.DepartmentImporter):
    """
    Importer for department data from CORE POS.
    """
    host_model_class = corepos.Department
    key = 'corepos_number'
    supported_fields = [
        'corepos_number',
        'number',
        'name',
        'tax_code',
        'food_stampable',
    ]

    def normalize_host_object(self, department):
        return {
            'corepos_number': department.number,
            'number': department.number,
            'name': department.name,
            'tax_code': str(department.tax_rate.id if department.tax_rate else '') or None,
            'food_stampable': department.food_stampable,
        }


class SubdepartmentImporter(FromCOREPOS, corepos_importing.model.SubdepartmentImporter):
    """
    Importer for subdepartment data from CORE POS.
    """
    host_model_class = corepos.Subdepartment
    key = 'corepos_number'
    supported_fields = [
        'corepos_number',
        'number',
        'name',
        'department_number',
    ]

    def normalize_host_object(self, subdepartment):
        return {
            'corepos_number': subdepartment.number,
            'number': subdepartment.number,
            'name': subdepartment.name,
            'department_number': subdepartment.department_number,
        }


class ProductImporter(FromCOREPOS, corepos_importing.model.ProductImporter):
    """
    Importer for product data from CORE POS.
    """
    host_model_class = corepos.Product
    key = 'corepos_id'
    supported_fields = [
        'corepos_id',
        'item_id',
        'upc',
        'brand_name',
        'description',
        'size',
        'unit_size',
        'unit_of_measure',
        'uom_abbreviation',
        'weighed',
        'department_number',
        'subdepartment_number',
        'regular_price_price',
        'regular_price_multiple',
        'regular_price_type',
        'sale_price_price',
        'sale_price_starts',
        'sale_price_ends',
        'sale_price_current',
        'food_stampable',
        'discountable',
        # 'tax1',
        'tax_code',
        'not_for_sale',
    ]

    def setup(self):
        super().setup()

        if self.fields_active(self.sale_price_fields):
            self.core_batch_items = {}

            # TODO: it seems possible for CORE to have more than one
            # batch item for a given product.  sort order will
            # determine which would "win" but not clear what sort
            # order should be used, e.g. CORE does not seem to use one
            today = self.app.today()
            batches = self.host_session.query(corepos.Batch)\
                                       .filter(corepos.Batch.start_date <= today)\
                                       .filter(corepos.Batch.end_date >= today)\
                                       .filter(corepos.Batch.discount_type > 0)\
                                       .options(orm.joinedload(corepos.Batch.items))\
                                       .all()

            def cache(batch, i):
                for item in batch.items:
                    self.core_batch_items.setdefault(item.upc, []).append(item)

            self.progress_loop(cache, batches,
                               message="Caching CORE-POS batch items")

    def get_core_batch_item(self, upc):
        if hasattr(self, 'core_batch_items'):
            items = self.core_batch_items.get(upc)
            if not items:
                return

            sale_price = items[0].sale_price
            if any([item.sale_price != sale_price
                    for item in items[1:]]):
                log.warning("ambiguous batch items for upc: %s", upc)

            return items[0]

        raise NotImplementedError("TODO: fetch batch items in real-time")

    def normalize_host_object(self, product):

        try:
            upc = GPC(product.upc, calc_check_digit='upc')
        except (TypeError, ValueError):
            log.debug("CORE POS product has invalid UPC: %s", product.upc)
            if len(self.key) == 1 and self.key[0] == 'upc':
                return
            upc = None

        price = None
        if product.normal_price is not None:
            price = decimal.Decimal('{:03f}'.format(product.normal_price))

        data = {
            'corepos_id': product.id,
            'item_id': product.upc,
            'upc': upc,
            'brand_name': (product.brand or '').strip() or None,
            'description': (product.description or '').strip(),

            'department_number': product.department_number or None,
            'subdepartment_number': product.subdepartment_number or None,

            'weighed': bool(product.scale),
            'food_stampable': product.foodstamp,
            # 'tax1': bool(product.tax), # TODO: is this right?

            'regular_price_price': price,
            'regular_price_multiple': 1 if price is not None else None,
            'regular_price_type': self.enum.PRICE_TYPE_REGULAR if price is not None else None,

            # nb. these may get set below
            'sale_price_price': None,
            'sale_price_starts': None,
            'sale_price_ends': None,
            'sale_price_current': False,

            'discountable': bool(product.line_item_discountable),

            'not_for_sale': not product.in_use,
        }

        if 'tax_code' in self.fields:
            data['tax_code'] = str(product.tax_rate.id) if product.tax_rate else None

        if self.fields_active(self.size_fields):
            size_info = self.normalize_size_info(product)
            data.update({
                'size': size_info['size'],
                'unit_size': size_info['unit_size'],
                'unit_of_measure': size_info['uom_code'],
                'uom_abbreviation': size_info['uom_abbrev'],
            })

        # sale price
        # nb. CORE discount_type indicates if item is on sale "now"
        if self.fields_active(self.sale_price_fields) and product.discount_type:
            item = self.get_core_batch_item(product.upc)
            if item:
                data.update({
                    'sale_price_price': item.sale_price,
                    'sale_price_starts': self.app.make_utc(self.app.localtime(item.batch.start_date)),
                    'sale_price_ends': self.app.make_utc(self.app.localtime(item.batch.end_date)),
                    'sale_price_current': True,
                })

        return data


class ProductCostImporter(FromCOREPOS, corepos_importing.model.ProductCostImporter):
    """
    Importer for product cost data from CORE POS API.
    """
    host_model_class = corepos.VendorItem
    key = ('corepos_vendor_id', 'corepos_sku')
    supported_fields = [
        'corepos_vendor_id',
        'corepos_sku',
        'product_uuid',
        'vendor_uuid',
        'code',
        'case_size',
        'case_cost',
        'unit_cost',
        'preferred',
    ]

    def setup(self):
        super().setup()
        model = self.model

        query = self.session.query(model.Vendor)\
                            .join(model.CoreVendor)\
                            .filter(model.CoreVendor.corepos_id != None)
        self.vendors_by_corepos_id = self.cache_model(model.Vendor,
                                                      query=query,
                                                      key='corepos_id')

        self.products_by_item_id = self.cache_model(model.Product, key='item_id')

    def query(self):
        query = super().query()

        query = query.options(orm.joinedload(corepos.VendorItem.product))

        return query

    def get_vendor(self, item):
        corepos_id = item.vendor_id

        if hasattr(self, 'vendors_by_corepos_id'):
            return self.vendors_by_corepos_id.get(corepos_id)

        model = self.config.get_model()
        try:
            return self.session.query(model.Vendor)\
                               .join(model.CoreVendor)\
                               .filter(model.CoreVendor.corepos_id == corepos_id)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_product(self, item):
        item_id = item.upc

        if hasattr(self, 'products_by_item_id'):
            return self.products_by_item_id.get(item_id)

        model = self.model
        try:
            return self.session.query(model.Product)\
                               .filter(model.Product.item_id == item_id)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def normalize_host_object(self, item):

        vendor = self.get_vendor(item)
        if not vendor:
            log.warning("CORE POS vendor not found for item: %s", item)
            return

        product = self.get_product(item)
        if not product:
            # just debug logging since this is a common scenario; the
            # CORE table is for items "available from vendor" but not
            # necssarily items carried by store
            log.debug("product not found for CORE vendor item: %s", item)
            return

        core_product = item.product

        preferred = False
        if core_product and core_product.default_vendor_id == item.vendor_id:
            preferred = True

        case_size = decimal.Decimal(str(item.units))
        unit_cost = item.cost
        case_cost = None
        if unit_cost is not None:
            case_cost = unit_cost * case_size

        return {
            'corepos_vendor_id': item.vendor_id,
            'corepos_sku': item.sku,
            'product_uuid': product.uuid,
            'vendor_uuid': vendor.uuid,
            'code': item.sku,
            'case_size': case_size,
            'case_cost': case_cost,
            'unit_cost': unit_cost,
            'preferred': preferred,
        }


class MemberEquityPaymentImporter(FromCOREPOS, corepos_importing.model.MemberEquityPaymentImporter):
    """
    Imports equity payment data from CORE-POS
    """
    host_model_class = coretrans.StockPurchase
    key = 'uuid'
    supported_fields = [
        'uuid',
        'member_uuid',
        'amount',
        'received',
        'transaction_identifier',
        'corepos_card_number',
        'corepos_transaction_number',
        'corepos_transaction_id',
        'corepos_department_number',
        'corepos_datetime',
    ]

    def setup(self):
        super().setup()
        model = self.model

        query = self.session.query(model.Member)\
                            .join(model.Customer)\
                            .join(model.CoreCustomer)\
                            .options(orm.joinedload(model.Member.customer)\
                                     .joinedload(model.Customer._corepos))
        self.members_by_card_number = self.cache_model(
            model.Member, query=query,
            key=lambda member, normal: member.customer.corepos_card_number)

        payments = self.session.query(model.MemberEquityPayment)\
                               .join(model.CoreMemberEquityPayment)\
                               .filter(model.CoreMemberEquityPayment.corepos_transaction_number != None)\
                               .filter(model.CoreMemberEquityPayment.corepos_transaction_id != None)\
                               .all()
        self.payments_by_card_number = {}
        def add(payment, i):
            self.payments_by_card_number.setdefault(payment.corepos_card_number, []).append(payment)
        self.progress_loop(add, payments, message="Grouping payments by card number")

    def cache_query(self):
        query = super().cache_query()
        model = self.model

        # ignore existing payments not known to be in CORE
        # TODO: is this in fact a good idea?
        query = query.join(model.CoreMemberEquityPayment)\
                     .filter(model.CoreMemberEquityPayment.corepos_transaction_number != None)

        return query

    def get_member(self, card_number):
        if hasattr(self, 'members_by_card_number'):
            return self.members_by_card_number.get(card_number)

        model = self.model
        try:
            return self.session.query(model.Member)\
                               .join(model.Customer)\
                               .join(model.CoreCustomer)\
                               .filter(model.CoreCustomer.corepos_card_number == card_number)\
                               .one()
        except orm.exc.NoResultFound:
            pass

    def get_payment(self, stock_purchase):
        payments = self.payments_by_card_number.get(stock_purchase.card_number)
        if not payments:
            return

        # first look for exact match
        dt = self.app.localtime(stock_purchase.datetime)
        match = [payment for payment in payments
                 if payment.corepos_transaction_number == stock_purchase.transaction_number
                 and payment.corepos_transaction_id == stock_purchase.transaction_id
                 and payment.amount == stock_purchase.amount
                 and payment.corepos_department_number == stock_purchase.department_number
                 and self.app.localtime(payment.corepos_datetime, from_utc=True) == dt]
        if len(match) == 1:
            return match[0]

        # nb. avoid datetime for this one
        matches = [payment for payment in payments
                   if payment.corepos_transaction_number == stock_purchase.transaction_number
                   and payment.corepos_transaction_id == stock_purchase.transaction_id
                   and payment.amount == stock_purchase.amount
                   and payment.corepos_department_number == stock_purchase.department_number]
        if len(matches) == 1:
            log.warning("found 'loose' match for card #%s, txn %s, for $%0.2f: %s",
                        stock_purchase.card_number,
                        stock_purchase.transaction_number,
                        stock_purchase.amount,
                        stock_purchase.datetime)

            # so there is one match, but its timestamp may be way off,
            # so let's also make sure at least date matches
            payment = matches[0]
            if self.app.localtime(payment.corepos_datetime, from_utc=True).date() == dt.date():
                return payment

            # do not assume any match, if dates were off
            return

        # TODO: not sure how to handle yet, if last check found more
        # than one match.  presumably if none were found then it is
        # safe to just return none though..
        if matches:
            raise NotImplementedError(f"{len(matches)} payments matched for CORE equity: {stock_purchase}")

    def normalize_host_object(self, stock_purchase):

        card_number = stock_purchase.card_number
        member = self.get_member(card_number)
        if not member:
            log.warning("member not found for card number %s: %s",
                        card_number, stock_purchase)
            return

        dt = stock_purchase.datetime
        if dt:
            dt = self.app.make_utc(self.app.localtime(dt))
        corepos_datetime = dt
        received = dt

        payment = self.get_payment(stock_purchase)
        if payment and payment.source != 'corepos':
            received = payment.received

        return {
            'uuid': payment.uuid if payment else self.app.make_uuid(),
            'member_uuid': member.uuid,
            'amount': stock_purchase.amount,
            'received': received,
            'transaction_identifier': stock_purchase.transaction_number,
            'corepos_card_number': stock_purchase.card_number,
            'corepos_transaction_number': stock_purchase.transaction_number,
            'corepos_transaction_id': stock_purchase.transaction_id,
            'corepos_department_number': stock_purchase.department_number,
            'corepos_datetime': corepos_datetime,
        }

    def create_object(self, key, host_data):
        payment = super().create_object(key, host_data)
        if payment:

            # track where each payment comes from!
            payment.source = 'corepos'

            return payment
