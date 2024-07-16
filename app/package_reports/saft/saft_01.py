import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom

# Define your sales transactions
sales_transactions = [
    {"transaction_id": "001", "product": "Product A", "quantity": 10, "price": 100.00},
    {"transaction_id": "002", "product": "Product B", "quantity": 5, "price": 50.00},
    # Add more transactions as needed
]

# Define your company details
company_name = "Your Company Name"
file_version = "1.0"
date_time = datetime.now().isoformat()

# Define your customers and suppliers
customers = ["Customer A", "Customer B"]
suppliers = ["Supplier A", "Supplier B"]

# Create the root element
root = ET.Element("AuditFile")

# Add header to the SAFT file
header = ET.SubElement(root, "Header")
ET.SubElement(header, "CompanyName").text = company_name
ET.SubElement(header, "FileVersion").text = file_version
ET.SubElement(header, "DateTime").text = date_time

# Add customers to the SAFT file
for customer in customers:
    customer_element = ET.SubElement(root, "Customer")
    ET.SubElement(customer_element, "Name").text = customer

# Add suppliers to the SAFT file
for supplier in suppliers:
    supplier_element = ET.SubElement(root, "Supplier")
    ET.SubElement(supplier_element, "Name").text = supplier

# Add sales transactions to the SAFT file
for transaction in sales_transactions:
    transaction_element = ET.SubElement(root, "Transaction")
    ET.SubElement(transaction_element, "TransactionID").text = transaction["transaction_id"]
    ET.SubElement(transaction_element, "Product").text = transaction["product"]
    ET.SubElement(transaction_element, "Quantity").text = str(transaction["quantity"])
    ET.SubElement(transaction_element, "Price").text = str(transaction["price"])

# Generate the SAFT file
tree = ET.ElementTree(root)

# Create a new minidom object
xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")

# Write the prettified XML to file
with open("app/static/saft/SAFT.xml", "w") as f:
    f.write(xmlstr)