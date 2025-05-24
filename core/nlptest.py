import spacy
from spacy.training.example import Example
from pdfminer.high_level import extract_text
from random import shuffle

# Load the plant dataset
plant_data = [("I saw a beautiful orchid in the park today", {"entities": [(18, 24, "PLANT")]} ),
              ("The roses in my garden are blooming",{"entities": [(4, 9, "PLANT")]}),
              ("I love to drink peppermint tea",  {"entities": [(19, 28, "PLANT")]} )]

# Create a new NLP object and add a blank "ner" pipeline
nlp = spacy.load("en_core_sci_lg")
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Add the plant labels to the NER model
ner.add_label("PLANT")

# Convert the dataset to spaCy's Example format
examples = []
for text, entities in plant_data:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, {"entities": entities})
    examples.append(example)

# Train the NER model
optimizer = nlp.initialize()
for i in range(10):
    shuffle(examples)
    for example in examples:
        nlp.update([example], sgd=optimizer)

# Extract text from the PDF file
text = extract_text('../data/miappe.pdf')

doc = nlp(text)
plants = []
for ent in doc.ents:
    if ent.label_ == "PLANT":
        plants.append(ent.text)
print(plants)
