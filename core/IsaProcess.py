
import spacy
from pdfminer.high_level import extract_text

from core.get_outline  import GetOutline
import re

from textblob import TextBlob

import nltk
import torch
from transformers import BertForQuestionAnswering, BertTokenizer

class IsaProcess:
    def findAllProcess(papers):
        Processs = []
        for p in papers:
            Process = GetOutline.getOutLineAndText(p)
            values = IsaProcess.findValues(Process)
            performer = IsaProcess.findperformer(Process)
            Date = IsaProcess.findDate(Process)
            PreviousProces = IsaProcess.findPreviousProces(Process)
            NextProces = IsaProcess.findNextProces(Process)
            Inputs = IsaProcess.findInputs(Process)
            Outputs = IsaProcess.findProcessOutputs(Process)
            comments = IsaProcess.findProcessComments(Process)
            if values or Date or performer or Date or PreviousProces or NextProces or Inputs:
                Processs.append({'PMID_pro': p, 'values': values,'perf':performer,'date':Date,
                                  'preproc':PreviousProces,'nxtproc':NextProces,'Outputs':Outputs,'Inputs':Inputs,'comments':comments})
        return Processs


    def findValues(papers):
        #sample
        values = []
        #dose, compound, tree traits like that values
        nlp = spacy.load("en_ner_bc5cdr_md")
        parameters = {
            "Growth Parameters": [
                "Height", "Leaf area", "Biomass", "Stem diameter",
                "Root length", "Shoot fresh weight", "Shoot dry weight"
            ],
            "Physiological Parameters": [
                "Photosynthetic rate", "Transpiration rate", "Stomatal conductance",
                "Chlorophyll content", "Water use efficiency", "CO2 assimilation rate"
            ],
            "Morphological Parameters": [
                "Number of leaves", "Leaf size", "Flowering time",
                "Fruit size", "Fruit weight", "Seed germination rate", "Root/shoot ratio"
            ],
            "Biochemical Parameters": [
                "Enzyme activity", "Catalase", "Peroxidase", "Total protein content",
                "Soluble sugar content", "Starch content", "Lipid content",
                "Carotenoids concentration", "Anthocyanins concentration"
            ],
            "Nutrient Parameters": [
                "Nitrogen content", "Phosphorus content", "Potassium content",
                "Macronutrient concentrations", "Micronutrient concentrations", "Nutrient uptake rates"
            ],
            "Environmental Parameters": [
                "Light intensity", "Temperature", "Humidity",
                "Soil moisture content", "pH levels", "CO2 concentration"
            ],
            "Response to Stress Parameters": [
                "Tolerance to drought", "Tolerance to salinity",
                "Oxidative stress markers", "Pathogen resistance", "Pathogen susceptibility",
                "Heat tolerance", "Cold tolerance"
            ],
            "Gene Expression Parameters": [
                "Expression levels of specific genes", "qPCR", "RNA-seq",
                "Transcription factor activity", "Promoter activity", "Enhancer activity"
            ]
        }
        found_parameters = {key: [] for key in parameters.keys()}

        # Process the paragraph with spaCy
        doc = nlp(papers)

        # Iterate through each sentence in the paragraph
        for sentence in doc.sents:
            # Iterate through each category of parameters
            for category, parameter_list in parameters.items():
                # Check if any parameter from the category is present in the sentence
                for parameter in parameter_list:
                    if parameter.lower() in sentence.text.lower():
                        values.append(parameter)

        return values
    def findperformer(papers):
        #name of person
        nlp = spacy.load("en_ner_bc5cdr_md")
        performer = []
        doc = nlp(papers)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                performer.append(ent.text)
        return performer
    def findProcessComments(paper):
        evD = ''
        blob = TextBlob(paper)
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
        print(summary_text)

        return summary_text
    def findPreviousProces(papers):
        urls = ""
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),\n]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

        urls = re.findall(url_pattern, papers)
        # Remove newline characters from URLs
        urls = [url.replace('\n', '') for url in urls]
        print('chekc 4 =================================================', urls)
        return urls
    def findNextProces(self):
        ver = ""
        return ver
    def findInputs(self):
        par = ""
        return par
    def findProcessOutputs(self):
        com = ""
        return com
    def findDate(text):

        DATE = []
        nlp = spacy.load("en_core_sci_lg")
        x = " , ".join(text)
        # print(x)
        doc = nlp(x)
        for ent in doc.ents:
            print('text:', ent.text)
            print('label:', ent.label_)
        for ent in doc.ents:
            if ent.label_ =="DATE":
                DATE.append(ent.text)
        return DATE
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

