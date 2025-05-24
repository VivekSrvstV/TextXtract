import spacy
from spacy.matcher import Matcher
from pdfminer.high_level import extract_text
# Load the language model
nlp = spacy.load("en_core_sci_lg")

# Define the patterns to match
method_pattern = [{"LOWER": "Methods"}, {"OP": "?"}]
material_pattern = [{"LOWER": "Materials"}, {"OP": "?"}]
mm_pattern = [{"LOWER": "Methods"}, {"LOWER": "and"}, {"LOWER": "Materials"}]

am_pattern = [{"LOWER": "Materials"}, {"LOWER": "and"}, {"LOWER": "Methods"}]
m_pattern = [{"LOWER": "Material"}, {"LOWER": "and"}, {"LOWER": "Method"}]
ms_pattern = [{"LOWER": "materials"}, {"LOWER": "and"}, {"LOWER": "methods"}]
pattern_list = [method_pattern, material_pattern, mm_pattern, am_pattern, m_pattern, ms_pattern]

# Initialize the Matcher with the patterns
matcher = Matcher(nlp.vocab)
matcher.add("MaterialMethods", pattern_list)

# Extract the text from the PDF file
pdf_text = extract_text("fetched_pdfs/18854043.pdf")

# Create a Doc object from the text
doc = nlp(pdf_text)

# Find the matches in the Doc
matches = matcher(doc)

# Check if any matches were found
if matches:
    # Get the start index of the first match
    match_start = matches[0][1]
    # Find the index of the next non-empty line after the match
    next_line_index = pdf_text.find("\n", match_start)
    while next_line_index < len(pdf_text) - 1 and pdf_text[next_line_index+1] == "\n":
        next_line_index = pdf_text.find("\n", next_line_index + 1)
    if next_line_index != -1:
        # Extract the paragraph that follows the match
        paragraph = pdf_text[next_line_index+1:]
        print(f"The paragraph that follows the match is: {paragraph}")
    else:
        print("No paragraph found following the match.")
else:
    print("No matches found in the PDF file.")