from core.get_outline  import GetOutline
import re
import spacy
from textblob import TextBlob
class MEvent:
    def findAllEvent(pdfFiles):
        evt_miappe = []
        print('Check 1 env', pdfFiles)
        for p in pdfFiles:
            findEv = GetOutline.getOutLineAndText(p)
            event = MEvent.findEvent(findEv)
            eventType = MEvent.findEventType(findEv)
            eventAN = MEvent.findEventAn(findEv)
            eventDesc = MEvent.findEventDesc(findEv)
            eventDate = MEvent.findEventDate(findEv)
            if event or eventType or eventAN or eventDesc or eventDate:
                evt_miappe.append({'PMID_ev': p, 'eventAN': eventAN,'eventType':eventType,'eventDesc':eventDesc,'eventDate':eventDate})
        return evt_miappe



    def findEvent(self):
        ev = ''
        return ev
    def findEventType(self):
        evt = ''
        return evt
    def findEventAn(evText):
        accession_numbers = ""
        pattern = r"\bCO_\d{6}\b"
        accession_numbers = re.findall(pattern, evText)
        return accession_numbers

    def findEventDesc(pdfFiles):
        evD = ''
        blob = TextBlob(pdfFiles)
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

    def findEventDate(texts):
        nlp = spacy.load("en_core_sci_lg")
        doc = nlp(texts)
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["DATE"]:
                entities.append(ent.text)
        return entities