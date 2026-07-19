import frappe

from print_designer.client_scripts.quotation_warranty import sync_quotation_warranty_client_script


def execute():
	sync_quotation_warranty_client_script()
	frappe.db.commit()
