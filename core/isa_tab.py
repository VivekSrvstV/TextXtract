import io
import csv
import re
from pdfminer.high_level import extract_text

from isatools.model import Investigation, Study, Assay, Sample
from isatools import isatab

# Convert PDF to text file
with open('../data/miappe.pdf', 'rb') as f:
    pdf_text = extract_text(f)

# Extract ISA-Tab data from text file
metadata = {'Investigation Title': 'Example Investigation'}
studies = [Study()]
assays = [Assay()]
samples = [Sample()]

# Use regular expressions to extract data from text
study_regex = r'Study \d+:\s*(.*)'
assay_regex = r'Assay \d+:\s*(.*)'
sample_regex = r'Sample \d+:\s*(.*)'

for line in pdf_text.split('\n'):
    study_match = re.match(study_regex, line)
    if study_match:
        study = Study(filename='s_study.txt')
        study.title = study_match.group(1)
        studies.append(study)
    assay_match = re.match(assay_regex, line)
    if assay_match:
        assay = Assay(filename='a_assay.txt')
        assay.title = assay_match.group(1)
        assays.append(assay)
    sample_match = re.match(sample_regex, line)
    if sample_match:
        sample = Sample(filename='s_sample.txt')
        sample.name = sample_match.group(1)
        samples.append(sample)

# Create ISA-Tab object
isa_tab = Investigation()
isa_tab.metadata = metadata
isa_tab.studies = studies

for study in studies:
    study.assays = [assay for assay in assays if assay in study]

for assay in assays:
    assay.samples = [sample for sample in samples if sample in assay]

# Validate ISA-Tab object
report = isa_tab.validate()
print(report.to_report_string())

# Save ISA-Tab data to CSV file
with io.StringIO() as output:
    writer = csv.writer(output, delimiter='\t')
    isatab.dump(isa_tab, writer)
    isatab_output = output.getvalue()

with open('isa_tab.csv', 'w') as f:
    f.write(isatab_output)
