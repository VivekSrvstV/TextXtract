import pandas as pd
import re
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load the crop ontology terms from the CSV file
crop_ontology_df = pd.read_csv('crop_ontology.csv', delimiter='\t')

# Create a bag-of-words vectorizer
vectorizer = CountVectorizer()

# Fit a Naive Bayes classifier on the crop ontology terms
X_train = vectorizer.fit_transform(crop_ontology_df['label'])
y_train = crop_ontology_df['id']
clf = MultinomialNB().fit(X_train, y_train)

# Define a function to extract named entities from text
nlp = spacy.load('en_core_sci_lg')

def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append(ent.text)
    return entities

# Define a function to classify text
def classify_text(text):
    # Vectorize the text
    X = vectorizer.transform([text])

    # Predict the crop ontology terms
    y_pred = clf.predict(X)

    # Get the predicted labels
    labels = crop_ontology_df.loc[crop_ontology_df['id'].isin(y_pred), 'label'].tolist()

    return labels

# Example usage
text = "I planted some durum wheat and bread wheat in my field last week."
entities = extract_entities(text)

# Extract crop ontology terms from entities
terms = []
for entity in entities:
    matches = classify_text(entity)
    if matches:
        terms += matches

# Remove duplicates from the list of terms
terms = list(set(terms))

# Display the crop ontology terms
print("Crop ontology terms found in text:")
print(terms)
