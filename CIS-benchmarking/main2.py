import pdfplumber
import pandas as pd
import re

# Load the PDF file
pdf_path = "CIS-benchmarking/documents/CIS_IBM_AIX_7.1_Benchmark_v2.1.0_ARCHIVE.pdf"  # Update with your actual file path

# Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text

# Extract full text from the PDF
full_text = extract_text_from_pdf(pdf_path)

# Regex pattern to extract CIS controls (e.g., "3.1.1.1 Disable writesrv (Automated)")
control_pattern = re.compile(r"(\d+\.\d+(?:\.\d+)?(?:\.\d+)?)\s(.+?)\s\((Automated|Manual)\)")

# Regex pattern to extract Profile Applicability (e.g., "Profile Applicability: • Level 2")
profile_pattern = re.compile(r"Profile Applicability:\s*(?:•\s*Level\s*(\d))?", re.MULTILINE)

# Extract matches (CIS controls)
matches = control_pattern.findall(full_text)

# Convert matches into structured data
data = []
for match in matches:
    control_number, control_name, automation_status = match

    # Locate the Profile Applicability section after the control's mention
    control_index = full_text.find(control_number)
    profile_section = full_text[control_index:control_index + 500]  # Limit search to 500 chars after

    # Extract Profile Applicability level
    profile_match = profile_pattern.search(profile_section)
    profile_level = profile_match.group(1) if profile_match else "Unknown"

    # Append to data
    data.append({
        "Control Number": control_number,
        "Control Name": control_name,
        "Automated/Manual": automation_status,
        "Profile Applicability": f"Level {profile_level}" if profile_level != "Unknown" else "Unknown"
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to Excel for easy review
df.to_excel("CIS_AIX_Profile_App.xlsx", index=False)

# Display the first few rows
print(df.head())

print("Extraction complete. Data saved to 'CIS_AIX_Profile_App.xlsx'.")
