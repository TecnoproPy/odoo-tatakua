#!/usr/bin/env bash
# run test suite for odoo-paraguay

oe -Q l10n_py_invoice_document -c test13e -d test13e_test
oe -Q l10n_py_reports -c test13e -d test13e_test
oe -Q l10n_py_vat_book -c test13e -d test13e_test
oe -Q partner_ruc_unique -c test13e -d test13e_test
