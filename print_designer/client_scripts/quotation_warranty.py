import frappe

SCRIPT_NAME = "Quotation Item - Warranty on Scan"

SCRIPT = """frappe.ui.form.on('Quotation Item', {
\tprice_list_rate(frm, cdt, cdn) {
\t\tconst row = locals[cdt][cdn];
\t\tif (!row.item_code) {
\t\t\treturn;
\t\t}
\t\tfrappe.db.get_value('Item', row.item_code, 'custom_warranty', (value) => {
\t\t\tconst warranty = value && value.custom_warranty;
\t\t\tif (warranty) {
\t\t\t\tfrappe.model.set_value(cdt, cdn, 'custom_warranty', warranty);
\t\t\t}
\t\t});
\t},
});"""


def sync_quotation_warranty_client_script():
	"""Standard Client Script: copy Item warranty after get_item_details (manual + barcode)."""
	if frappe.db.exists("Client Script", SCRIPT_NAME):
		doc = frappe.get_doc("Client Script", SCRIPT_NAME)
	else:
		doc = frappe.new_doc("Client Script")
		doc.dt = "Quotation"
		doc.view = "Form"
		doc.module = "Selling"

	doc.enabled = 1
	doc.script = SCRIPT
	doc.save(ignore_permissions=True)
