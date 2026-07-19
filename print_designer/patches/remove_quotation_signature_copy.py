import frappe


def execute():
	_remove_quotation_signature_field()


def _remove_quotation_signature_field():
	name = "Quotation-custom_signature"
	if not frappe.db.exists("Custom Field", name):
		return
	frappe.delete_doc("Custom Field", name, force=True)
	frappe.clear_cache(doctype="Quotation")
