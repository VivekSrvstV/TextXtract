import spacy
from nltk.corpus import stopwords

from core.get_outline  import GetOutline
import re

from textblob import TextBlob

import nltk
import torch
from transformers import BertForQuestionAnswering, BertTokenizer
import json
from core.extrtext import NLPProject
from nltk import WordNetLemmatizer
nltk.download("stopwords")
nltk.download('wordnet') #for lemmatizing
class MEnv:

    def findAllEnv(pdfFiles):
        env_miappe = []
        data = {}
        print('Check 1 env', pdfFiles)
        for p in pdfFiles:
            findEnv = GetOutline.getOutLineAndText(p)
            data[p] = findEnv

        json_data = json.dumps(data, indent=4)
        # Create a new dictionary with non-empty values
        filtered_data = {key: value for key, value in data.items() if value}

        for key,value in filtered_data.items():
            qa = MEnv.initializeBert(value)
            ec = ecUnit = ecValue = ecFactor = ""
            for name,dictionary in qa.items():
                print(dictionary)
                if name == "d1":
                    enc = dictionary['what are the environment condition ?']
                    # Remove all occurrences of "what are the environment condition?"
                    filtered_text = [item.replace('what are the environment condition?', '') for item in enc]
                    # Join the filtered text back into a single string
                    filtered_text = ' '.join(filtered_text)
                    #tokens = nltk.sent_tokenize(filtered_text)
                    words = nltk.word_tokenize(filtered_text)
                    stop_words = set(stopwords.words('english'))
                    filtered_words = [word for word in words if word.lower() not in stop_words]
                    sentenses  = ' '.join([str(elem) for elem in filtered_words])

                    #text = [' '.join(sent) for sent in filtered_words]
                    blob = TextBlob(sentenses)
                    # Split the text into sentences
                    sentences = blob.sentences

                    # Calculate the polarity (sentiment) of each sentence
                    # You can use sentiment analysis to identify important sentences
                    sentence_scores = [(sentence, sentence.sentiment.polarity) for sentence in sentences]

                    # Sort sentences by polarity in descending order (most positive first)
                    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)

                    # Extract the top N sentences as the summary
                    N = 3  # You can adjust N based on your desired summary length
                    summary_sentences = [sentence[0] for sentence in sorted_sentences[:N]]

                    # Combine the summary sentences into a summary text
                    summary_text = " ".join(str(sentence) for sentence in summary_sentences)

                    # Print or use the generated summary
                    #print(summary_text)

                    ec = summary_text
                if name == "d2":
                    ecUnit = dictionary['what are the environmental condition unit ?']

                    # Remove all occurrences of "what are the environment condition?"
                    filtered_text = [item.replace('what are the environmental condition unit ?', '') for item in ecUnit]
                    # Join the filtered text back into a single string
                    filtered_text = ' '.join(filtered_text)
                    # tokens = nltk.sent_tokenize(filtered_text)
                    words = nltk.word_tokenize(filtered_text)
                    stop_words = set(stopwords.words('english'))
                    filtered_words = [word for word in words if word.lower() not in stop_words]
                    sentenses = ' '.join([str(elem) for elem in filtered_words])

                    # text = [' '.join(sent) for sent in filtered_words]
                    blob = TextBlob(sentenses)
                    # Split the text into sentences
                    sentences = blob.sentences

                    # Calculate the polarity (sentiment) of each sentence
                    # You can use sentiment analysis to identify important sentences
                    sentence_scores = [(sentence, sentence.sentiment.polarity) for sentence in sentences]

                    # Sort sentences by polarity in descending order (most positive first)
                    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)

                    # Extract the top N sentences as the summary
                    N = 3  # You can adjust N based on your desired summary length
                    summary_sentences = [sentence[0] for sentence in sorted_sentences[:N]]

                    # Combine the summary sentences into a summary text
                    summary_text = " ".join(str(sentence) for sentence in summary_sentences)

                    # Print or use the generated summary
                    # print(summary_text)

                    ecUnit = summary_text

                if name == "d3":
                    ecvalue = dictionary['what are the environmental condition value? ']
                    # Remove all occurrences of "what are the environment condition?"
                    filtered_text = [item.replace('what are the environmental condition value? ', '') for item in ecvalue]
                    # Join the filtered text back into a single string
                    filtered_text = ' '.join(filtered_text)
                    # tokens = nltk.sent_tokenize(filtered_text)
                    words = nltk.word_tokenize(filtered_text)
                    stop_words = set(stopwords.words('english'))
                    filtered_words = [word for word in words if word.lower() not in stop_words]
                    sentenses = ' '.join([str(elem) for elem in filtered_words])

                    # text = [' '.join(sent) for sent in filtered_words]
                    blob = TextBlob(sentenses)
                    # Split the text into sentences
                    sentences = blob.sentences

                    # Calculate the polarity (sentiment) of each sentence
                    # You can use sentiment analysis to identify important sentences
                    sentence_scores = [(sentence, sentence.sentiment.polarity) for sentence in sentences]

                    # Sort sentences by polarity in descending order (most positive first)
                    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)

                    # Extract the top N sentences as the summary
                    N = 3  # You can adjust N based on your desired summary length
                    summary_sentences = [sentence[0] for sentence in sorted_sentences[:N]]

                    # Combine the summary sentences into a summary text
                    summary_text = " ".join(str(sentence) for sentence in summary_sentences)
                    ecValue = summary_text
                if name == "d4":
                    ecF = dictionary['what are the environmental condition factor? ']

                    filtered_text = [item.replace('what are the environmental condition value? ', '') for item in ecF]
                    # Join the filtered text back into a single string
                    filtered_text = ' '.join(filtered_text)
                    # tokens = nltk.sent_tokenize(filtered_text)
                    words = nltk.word_tokenize(filtered_text)
                    stop_words = set(stopwords.words('english'))
                    filtered_words = [word for word in words if word.lower() not in stop_words]
                    sentenses = ' '.join([str(elem) for elem in filtered_words])

                    # text = [' '.join(sent) for sent in filtered_words]
                    blob = TextBlob(sentenses)
                    # Split the text into sentences
                    sentences = blob.sentences

                    # Calculate the polarity (sentiment) of each sentence
                    # You can use sentiment analysis to identify important sentences
                    sentence_scores = [(sentence, sentence.sentiment.polarity) for sentence in sentences]

                    # Sort sentences by polarity in descending order (most positive first)
                    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)

                    # Extract the top N sentences as the summary
                    N = 3  # You can adjust N based on your desired summary length
                    summary_sentences = [sentence[0] for sentence in sorted_sentences[:N]]

                    # Combine the summary sentences into a summary text
                    summary_text = " ".join(str(sentence) for sentence in summary_sentences)
                    ecFactor = summary_text
            #ec = MEnv.findEnvCondition(findEnv)

            ecOID = MEnv.findEcOntID(value)
            #ecUnit = MEnv.findEcUnit(findEnv)
            #ecValue = MEnv.findEcValue(findEnv)
            ecDesc =  MEnv.findEcDesc(value)
            #ecFactor = MEnv.findEcFactor(findEnv)
            if ec or ecOID or ecUnit or ecOID or ecOID or ecFactor or ecDesc or ecValue:
                env_miappe.append({'PMID_env': key, 'ec': ec,'ecOID':ecOID,'ecUnit':ecUnit,'ecValue':ecValue,'ecDesc':ecDesc,'ecFactor':ecFactor})

        return env_miappe



    def initializeBert(text):
        nltk.download('punkt')
        sentences = nltk.sent_tokenize(text)

        questions = [
            'what are the environment condition ?',
            'what are the environmental condition unit ?',
            'what are the environmental condition value? ',
            'what are the environmental condition factor? '
        ]

        model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        tokenizer_for_bert = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

        max_len = 512
        batch_size = 8

        answers = []

        for question in questions:
            question_input_ids = tokenizer_for_bert.encode(question, add_special_tokens=False)

            for batch_start in range(0, len(sentences), batch_size):
                batch_sentences = sentences[batch_start:batch_start + batch_size]

                input_ids = []
                segment_ids = []

                for sentence in batch_sentences:
                    sentence_input_ids = tokenizer_for_bert.encode(sentence, add_special_tokens=False)
                    combined_input = [tokenizer_for_bert.cls_token_id] + question_input_ids + [
                        tokenizer_for_bert.sep_token_id] + sentence_input_ids + [tokenizer_for_bert.sep_token_id]
                    input_ids.append(combined_input)
                    segment_ids.append([0] * (len(question_input_ids) + 2) + [1] * (len(sentence_input_ids) + 1))

                max_batch_len = max(len(ids) for ids in input_ids)
                input_ids = [ids + [tokenizer_for_bert.pad_token_id] * (max_batch_len - len(ids)) for ids in input_ids]
                segment_ids = [ids + [0] * (max_batch_len - len(ids)) for ids in segment_ids]

                input_ids_tensor = torch.tensor(input_ids)
                segment_ids_tensor = torch.tensor(segment_ids)

                with torch.no_grad():
                    start_scores, end_scores = model(input_ids_tensor, token_type_ids=segment_ids_tensor,
                                                     return_dict=False)

                for i, (start_score, end_score) in enumerate(zip(start_scores, end_scores)):
                    start_idx = torch.argmax(start_score).item()
                    end_idx = torch.argmax(end_score).item()

                    if start_idx > end_idx:
                        start_idx, end_idx = end_idx, start_idx

                    answer = tokenizer_for_bert.decode(input_ids[i][start_idx:end_idx + 1], skip_special_tokens=True)
                    answers.append([question, answer])

        combined_answers = {}
        for question, answer in answers:
            if question not in combined_answers:
                combined_answers[question] = []
            combined_answers[question].append(answer)
        meaningful_answers = {}
        min_answer_length = 10
        for question, answers in combined_answers.items():
            filtered_answers = [answer for answer in answers if len(answer) >= min_answer_length]
            if filtered_answers:
                meaningful_answers[question] = filtered_answers

        dictionaries = {}
        for i, (question, answers) in enumerate(meaningful_answers.items(), start=1):
            dictionary_name = f"d{i}"
            dictionaries[dictionary_name] = {question: answers}

        return dictionaries



    def findEnvCondition(envText):
            print('environtionment parameter')
            ec = ''

            nlp = spacy.load("en_core_sci_lg")
            doc = nlp(envText)
            #for entity in doc.ents:
                #print("Entity:", entity.text)
                #print("Label:", entity.label_)
            return ec
    def findEcOntID(envText):
        ecOID = ''
        pattern = r"\b(?:CO|EO|XEO)[:,]?\d{6}\b"
        ecOID = re.findall(pattern, envText)
        return ecOID
    def findEcUnit(self):
        ecUnit = ''
        return ecUnit
    def findEcValue(envText):
        ecValue = ''
        return ecValue
    def findEcDesc(pdfFiles):
        blob = TextBlob(pdfFiles)
        noun_phrases = blob.noun_phrases
        top_noun_phrases = sorted(set(noun_phrases), key=noun_phrases.count, reverse=True)[:25]

        # Create a title by joining the most important noun phrases with appropriate punctuation
        ecDesc = ' '.join([phrase.capitalize() for phrase in top_noun_phrases]) + '.'

        return ecDesc
    def findEcFactor(self):
        ecFactor = ''
        return ecFactor

