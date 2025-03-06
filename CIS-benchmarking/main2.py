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

# Extract Table of Contents (TOC) page mappings
toc_pattern = re.compile(r"(\d+\.\d+(?:\.\d+)?(?:\.\d+)?)\s(.+?)\s+(\d+)")
toc_matches = toc_pattern.findall(full_text)

# Create a mapping of control numbers to their respective page numbers
control_page_map = {match[0]: int(match[2]) for match in toc_matches}

# Function to extract Profile Applicability from a given page
def get_profile_applicability(page_number):
    if page_number < len(doc):
        page_text = doc[page_number].get_text("text")
        profile_match = re.search(r"Profile Applicability:\s*\n?•\s*(Level \d)", page_text)
        if profile_match:
            return profile_match.group(1)
    return "Unknown"

# Convert matches into structured data
data = []
for match in matches:
    control_number, control_name, automation_status = match

    # Determine category based on the first number in the control (e.g., "2.1.1.1" -> "2" -> "Data Protection")
    section_number = control_number.split(".")[0]
    current_category = category_map.get(section_number, "Unknown")

    # Format Inspec Profile Control Name (replace spaces with underscores but keep dashes)
    formatted_name = control_number + "_" + control_name.replace(" ", "_")

    # Get the corresponding page number from the Table of Contents
    page_number = control_page_map.get(control_number, None)

    # Extract Profile Applicability from the respective page
    profile_applicability = get_profile_applicability(page_number) if page_number else "Unknown"

    # Append to data
    data.append({
        "Category": current_category,
        "Control Name": control_name,
        "Automated/Manual": automation_status,
        "Inspec Profile Control Name": formatted_name,
        "Profile Applicability": profile_applicability
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to Excel for easy review
output_path = "CIS-benchmarking/CIS_AIX_Controls_v1.xlsx"
df.to_excel(output_path, index=False)

print(f"Extraction complete. Data saved to '{output_path}'.")
