from core.get_outline  import GetOutline
import re
import spacy
from textblob import TextBlob
class MSample:
    def findAllSamples(pdfFiles):
        evt_miappe = []
        print('Check 1 env', pdfFiles)
        for p in pdfFiles:

            findO = GetOutline.getOutLineAndText(p)
            s = MSample.findS(findO)
            sid = MSample.findSID(findO)
            psds = MSample.findPSDS(findO)
            pae = MSample.findPAE(findO)
            sd = MSample.findSD(findO)
            cd = MSample.findCD(findO)
            eid = MSample.findEID(findO)
            if s or sid or psds or pae or sd or cd or eid:
                evt_miappe.append({'PMID_s': p, 's': s, 'sid': sid, 'psds': psds, 'pae': pae, 'sd': sd, 'cd': cd, 'eid': eid})
        return evt_miappe
    def findS(self):
        ev = ''
        return ev
    def findSID(self):
        evt = ''
        return evt
    def findPSDS(evText):
        accession_numbers = ""
        pattern = r"\bPO\d{6}\b"
        accession_numbers = re.findall(pattern, evText)
        return accession_numbers
    def findPAE(evText):
        accession_numbers = ""
        pattern = r"\bPO\d{6}\b"
        accession_numbers = re.findall(pattern, evText)
        return accession_numbers
    def findSD(pdfFiles):
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
        return evD
    def findEID(self):
        evD = ''
        return evD

    def findCD(texts):
        nlp = spacy.load("en_core_sci_lg")
        doc = nlp(texts)
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["DATE"]:
                entities.append(ent.text)
        return entities