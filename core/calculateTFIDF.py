import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import csv

class TFIDF:
    def calc(self,processed_text):
        print('processed text from tfid class is :***************************************************************')
        print(processed_text)
        print('*********************************************************end of processed text from tfid class is *')
        # Join the list of sentences into a single string
        text = [' '.join(sent) for sent in processed_text]
        # Define the TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
        # Create the document-term matrix
        dtm = vectorizer.fit_transform(text)
        # Calculate TF-IDF scores
        tfidf_scores = dtm.toarray()
        # Step 4: Apply topic modeling
        num_topics = 10
        lda_model = LatentDirichletAllocation(n_components=num_topics)
        lda_model.fit(dtm)

        # Step 5: Assign topics to sentences
        topic_assignments = lda_model.transform(dtm)
        sentence_topics = np.argmax(topic_assignments, axis=1)

        # Step 6: Calculate topic-based TF-IDF scores
        topic_based_tfidf_scores = []
        for i in range(len(processed_text)):
            doc_scores = []
            for j in range(num_topics):
                topic_words = lda_model.components_[j]
                top_words_idx = topic_words.argsort()[-10:]
                doc_words_idx = tfidf_scores[i].argsort()[-50:]
                common_words_idx = list(set(top_words_idx) & set(doc_words_idx))
                if len(common_words_idx) > 0:
                    topic_score = tfidf_scores[i][common_words_idx].sum()
                    doc_scores.append(topic_score)
                else:
                    doc_scores.append(0)
            topic_based_tfidf_scores.append(doc_scores)

        # Print the topic-based TF-IDF scores for each sentence
        tfidf_result = []
        for i in range(len(processed_text)):
            tfidf_result.append({"Sentence": processed_text[i],"Topic scores":topic_based_tfidf_scores[i],
                                 "Assigned topic":sentence_topics[i]})


            print("Sentence {}: {}".format(i + 1, processed_text[i]))
            print("Topic scores: {}".format(topic_based_tfidf_scores[i]))
            print("Assigned topic: {}".format(sentence_topics[i]))


        return tfidf_result

