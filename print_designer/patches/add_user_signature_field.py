import json

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

from print_designer.custom_fields import CUSTOM_FIELDS

PRINT_FORMATS = ("NB-QUOTATION", "NB-SALES-ORDER")


def execute():
	create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
	_migrate_banner_images_to_signature()
	_update_print_formats()


def _migrate_banner_images_to_signature():
	for user in frappe.get_all(
		"User",
		filters={"banner_image": ["is", "set"]},
		fields=["name", "banner_image", "custom_signature"],
	):
		if user.custom_signature:
			continue
		frappe.db.set_value("User", user.name, "custom_signature", user.banner_image, update_modified=False)


def _update_print_formats():
	for name in PRINT_FORMATS:
		if not frappe.db.exists("Print Format", name):
			continue
		pf = frappe.get_doc("Print Format", name)
		changed = False
		for fieldname in (
			"print_designer_body",
			"print_designer_footer",
			"print_designer_header",
			"print_designer_after_table",
			"print_designer_print_format",
		):
			raw = pf.get(fieldname)
			if not raw:
				continue
			if isinstance(raw, (dict, list)):
				text = json.dumps(raw)
			else:
				text = raw
			if "banner_image" not in text:
				continue
			updated = text.replace("banner_image", "custom_signature").replace(
				"Banner Image", "Signature"
			)
			if isinstance(raw, (dict, list)):
				pf.set(fieldname, json.loads(updated))
			else:
				pf.set(fieldname, updated)
			changed = True
		if changed:
			pf.save(ignore_permissions=True)
