import csv
import frappe
import os

def import_csv_to_doctype(file_path, doctype_name, field_mapping):
    """
    Import rows from a CSV file into a specified DocType.

    Args:
        file_path (str): Path to the CSV file.
        doctype_name (str): Target DocType.
        field_mapping (dict): Mapping of CSV columns to DocType fields.
    """
    if not os.path.exists(file_path):
        frappe.throw(f"File not found: {file_path}")

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Prepare the document data based on field mapping
            doc_data = {"doctype": doctype_name}
            for csv_field, doctype_field in field_mapping.items():
                doc_data[doctype_field] = row.get(csv_field, "")

            try:
                # Create and insert the document
                doc = frappe.get_doc(doc_data)
                doc.insert(ignore_permissions=True)
                frappe.msgprint(f"Inserted: {doc.name} into {doctype_name}")
            except Exception as e:
                frappe.log_error(message=str(e), title="Error Importing CSV")
                frappe.msgprint(f"Failed to insert record: {row}")

    frappe.db.commit()
    frappe.msgprint(f"All records from {file_path} inserted successfully into {doctype_name}.")

# Example usage for multiple files and DocTypes
files_and_mappings = [
    {
        "file_path": frappe.get_module_path("frappe_insight", "sajha_menu/sinsighQueryforerp.csv"),
        "doctype_name": "Insight Query",
        "field_mapping": {
            "name": "name",
            "title": "title",
            "limit": "limit",
            "json": "json",
            "sql": "sql",
            "filters": "filters",
            "docstatus": "docstatus",
            "idx": "idx",
            "status": "status",
            "is_native_query": "is_native_query",
            "is_assisted_query": "is_assisted_query",
            "is_script_query": "is_script_query",
            "data_source": "data_source",
            "chart": "chart",
            "is_stored": "is_stored"
        }
    },
    {
        "file_path": frappe.get_module_path("frappe_insight", "sajha_menu/sinsightdashboard.csv"),
        "doctype_name": "Insight Dashboard",
        "field_mapping": {
            "name": "name",
            "title": "title",
            "docstatus": "docstatus",
            "idx": "idx",
            "is_public": "is_public",
            "public_key": "public_key"
        }
    },
    {
        "file_path": frappe.get_module_path("frappe_insight", "sajha_menu/sinsightdashboarditem.csv"),
        "doctype_name": "Insight Dashboard Item",
        "field_mapping": {
            "name": "name",
            "dashboard": "dashboard",
            "item_name": "item_name",
            "item_type": "item_type",
            "parenttype": "parenttype",
            "parentfield": "parentfield",
            "parent": "parent",
            "layout": "layout",
            "options": "options",
            "item_id": "item_id",
            "idx": "idx",
            "docstatus": "docstatus"
        }
    },
    {
        "file_path": frappe.get_module_path("frappe_insight", "sajha_menu/sinsightchart.csv"),
        "doctype_name": "Insight Chart",
        "field_mapping": {
            "name": "name",
            "docstatus": "docstatus",
            "idx": "idx",
            "query": "query",
            "chart_type": "chart_type",
            "options": "options",
            "is_public": "is_public"
        }
    }
]

# Run the import for each file
for config in files_and_mappings:
    import_csv_to_doctype(
        config["file_path"],
        config["doctype_name"],
        config["field_mapping"]
    )
