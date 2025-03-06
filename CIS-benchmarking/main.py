import pymupdf  # PyMuPDF
import pandas as pd
import re

# Load the PDF file
pdf_path = "CIS-benchmarking\documents\CIS_IBM_AIX_7.1_Benchmark_v2.1.0_ARCHIVE.pdf"  # Update your file path
doc = pymupdf.open(pdf_path)

# Function to extract text from the PDF
def extract_text_from_pdf(doc):
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# Extract full text from PDF
full_text = extract_text_from_pdf(doc)

# Regex pattern to extract CIS controls (e.g., "3.1.1.1 Disable writesrv (Automated)")
control_pattern = re.compile(r"(\d+\.\d+(?:\.\d+)?(?:\.\d+)?)\s(.+?)\s\((Automated|Manual)\)")

# Regex pattern to extract section headers (e.g., "2 Data Protection")
section_pattern = re.compile(r"^(\d+)\s([A-Za-z\s\-]+)$", re.MULTILINE)

# Extract all section headers
sections = section_pattern.findall(full_text)

# Convert extracted sections into a dictionary {section_number: category_name}
category_map = {sec_num: sec_name.strip() for sec_num, sec_name in sections}

# Extract matches (CIS controls)
matches = control_pattern.findall(full_text)

# Convert matches into structured data
data = []
current_category = None  # To track which section each control belongs to

for match in matches:
    control_number, control_name, automation_status = match

    # Determine category based on the first number in the control (e.g., "2.1.1.1" -> "2" -> "Data Protection")
    section_number = control_number.split(".")[0]
    current_category = category_map.get(section_number, "Unknown")

    # Format Inspec Profile Control Name (replace spaces with underscores but keep dashes)
    formatted_name = control_number + "_" + control_name.replace(" ", "_")

    # Append to data
    data.append({
        "Category": current_category,
        "Control Name": control_name,
        "Automated/Manual": automation_status,
        "Inspec Profile Control Name": formatted_name
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to Excel for easy review
df.to_excel("CIS_AIX_Controls_v0.xlsx", index=False)

print("Extraction complete. Data saved to 'CIS_AIX_Controls_v#.xlsx'.")