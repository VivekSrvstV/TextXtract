
import string

import classifier as classifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

class M1:

    #Step 1: Define the categories
    categories = ['politics', 'sports', 'entertainment']

    #Step 2: Preprocess the text
    def preprocess_text(text):
        # Remove punctuations
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Tokenize the text
        tokens = word_tokenize(text.lower())
        # Remove stop words
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        # Join the tokens back into a single string
        text = ' '.join(tokens)
        return text
    #Step 2: Preprocess the text
    def processText(self):
        vectorizer = CountVectorizer()
        return vectorizer

    #Step 4: Build a classifier
    def buildClassifier(self,vectorizer):
        classifier = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', MultinomialNB())
        ])
        return classifier

    #Step 5: Train the classifier
    def trainClassifier(self):
        train_data = [
            {
                'species': 'Arabidopsis thaliana',
                'treatment': 'Control',
                'biomass': 5.7,
                'leaf_area': 7.3,
                'root_depth': 10.2,
                'water_use_efficiency': 0.6
            },
            {
                'species': 'Zea mays',
                'treatment': 'Drought',
                'biomass': 9.1,
                'leaf_area': 11.8,
                'root_depth': 13.5,
                'water_use_efficiency': 0.3
            },
            {
                'species': 'Oryza sativa',
                'treatment': 'Salinity',
                'biomass': 6.5,
                'leaf_area': 8.9,
                'root_depth': 11.1,
                'water_use_efficiency': 0.4
            }
        ]
        texts = [data['text'] for data in train_data]
        categories = [data['category'] for data in train_data]

        classifier.fit(texts, categories)

    #Step 6: Test the classifier
    def testing(self):
        test_data = [
            "The tomato plants showed signs of wilting, despite receiving ample water and fertilizer.",
            "The maize crop had a high yield this year due to favorable weather conditions.",
            "The wheat plants were harvested early due to an outbreak of rust disease.",
            "The soybean plants showed an increase in biomass after being treated with a new growth-promoting hormone.",
            "The potato crop suffered from blight this year, resulting in lower yields than expected."
        ]

       # test_texts = [data in test_data]
        #test_categories = [data['category'] for data in test_data]
        predictions = classifier.predict(test_data)
        for i in range(len(test_data)):
            print(f"Text: {test_data[i]}")
            print(f"Predicted category: {predictions[i]}")
            print()


def main():
    M1.testing('o')


if __name__ == "__main__":
    main()

