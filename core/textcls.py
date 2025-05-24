import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Tc:
    def textCl(self):
        # Read in the CSV file
        df = pd.read_csv('../data/tfidf_result.csv')

        # Define the keys to compare against
        miappe_guidelines = {
            'Experimental design': ['Plant material', 'Growing conditions', 'Experimental design'],
            'Phenotyping methods': ['Imaging methods', 'Data extraction and analysis', 'Trait ontology'],
            'Environmental conditions': ['Climate data', 'Soil data', 'Nutrient data'],
            'Metadata': ['Experiment metadata', 'Plant metadata', 'Imaging metadata'],
            'Data availability': ['Data sharing', 'Data archiving'],
            'Standards compliance': ['MIAPPE compliance', 'Ontology compliance', 'Standards compliance']
        }

        # Get the values of the "Sentence" column as a list
        sentences = df['Sentence'].values.tolist()
        print(sentences)
        # Create a dictionary to store the MIAPPE data
        miappe_data = {key: [] for key in miappe_guidelines.keys()}

        # Define a function to calculate the cosine similarity between two sentences
        def calculate_cosine_similarity(sentence, item):
            vectorizer = TfidfVectorizer(stop_words='english', min_df=1, max_df=0.5)
            vectors = vectorizer.fit_transform([sentence, item]).toarray()
            return cosine_similarity(vectors)[0][1]

        # Loop through the sentences in the text
        for sentence in sentences:
            # Loop through the MIAPPE checklist items
            for item, values in miappe_guidelines.items():
                # Loop through the values for each item
                for value in values:
                    # Calculate cosine similarity between sentence and item value
                    similarity = calculate_cosine_similarity(str(sentence), value)
                    print(similarity)
                    # If similarity is above a certain threshold, add the sentence to the MIAPPE data for that item
                    if similarity > 0.1:
                        miappe_data[item].append({'sentence': str(sentence), 'key': value})

        return miappe_data

def main():
    print('running')
    print(Tc().textCl())
    print('completed')
if __name__ == "__main__":
    main()
