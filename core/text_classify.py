# Import the necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
class ClassifyText:
    def classify(self):
        # Load the dataset
        data = pd.read_csv('../data/tfidf_result.csv')
        #data2 = open('tfidf_result.csv', 'r+')
        #yourResult = [data2.readlines()]
        datas = pd.DataFrame(data, columns=['Sentence','Topic Scores', 'Assigned topic'])

        # Split the dataset into training and testing sets
        train_data = datas[:8000]
        test_data = datas[8000:]

        # Convert text data into numerical data using TfidfVectorizer
        vectorizer = TfidfVectorizer()
        train_x = vectorizer.fit_transform(train_data['Sentence'].apply(lambda x: ' '.join(x)))
        test_x = vectorizer.transform(test_data['Sentence'].apply(lambda x: ' '.join(x)))

        # Create a Multinomial Naive Bayes classifier
        clf = MultinomialNB()

        # Train the classifier
        clf.fit(train_x, train_data['Assigned topic'])

        # Make predictions on the testing set
        pred_y = clf.predict(test_x)

        # Calculate the accuracy of the classifier
        accuracy = accuracy_score(test_data['Assigned topic'], pred_y)
        print("Accuracy: ", accuracy)

