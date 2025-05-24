import re

import spacy

from core.get_outline import GetOutline

from summarizer import Summarizer
from textblob import TextBlob

class MBio:
    nlp = spacy.load("en_ner_bionlp13cg_md")
    def find_all_BIo(pdfFiles):
        BIo_miappe = []
        print('Check 1 BIo ',pdfFiles)
        for p in pdfFiles:
            findBIo = GetOutline.getOutLineAndText(p)
            bmid = MBio.findBMID(findBIo)
            organism = MBio.findOrganism(findBIo)
            genus = MBio.findGenus(findBIo)
            species = MBio.findSpecies(findBIo)
            infraspecific  = MBio.findInfra(findBIo)
            lng = MBio.findLong(findBIo)
            lat = MBio.findLat(findBIo)
            alt = MBio.findAlt(findBIo)
            bmp = MBio.findBMP(findBIo)
            msid = MBio.findMSID(findBIo)
            msdoi = MBio.findMsDOI(findBIo)
            msd = MBio.findMSD(findBIo)
            if bmid or organism or genus or species or infraspecific or lng or lat or alt or bmp or msid or msdoi or msd:
                BIo_miappe.append({'PMID_bio': p, 'bmid': bmid, 'organism': organism, 'genus': genus,
                                   'species':species ,'infra':infraspecific,'lng':lng,'lat':lat,
                                   'alt':alt,'bmp':bmp,'msid':msid,'msdoi':msdoi,'msd':msd})
        return BIo_miappe
    def findBMID(BIo):
        bmid = []
        print('into BMID')
        return bmid
    def findOrganism(bIo):
       print('into organism')
       organisms = []
       pattern = re.compile(r"NCBITAXON\d+", re.IGNORECASE)
       matches = re.findall(pattern, bIo)
       if len(matches) > 0:
           ncbi_taxon = matches[0]
           organisms.append(ncbi_taxon)
       else:
           print("No match found.")
       return organisms

    def findGenus(bIo):
        print('into genus')
        doc = MBio.nlp(bIo)
        genes = []
        #species = []
        for ent in doc.ents:
            if ent.label_ == "GENUS":
                genes.append(ent.text)
        '''for ent in doc.ents:
            if ent.label_ == "ORG":
                genus = ent.text.split()[0]
                species = ent.text.split()[1]
                print("Genus:", genus)
                print("Species:", species)
                genes.append(genus)

                break
        else:
            print("No match found.")'''
        return genes

    def findSpecies(bIo):
        print('into species')
        doc = MBio.nlp(bIo)
        specis = []
        for ent in doc.ents:
            if ent.label_ == "ORGANISM" or ent.label_ == "ORGANISM_SUBDIVISION" or ent.label_ == "ORGANISM_SUBSTANCE" or ent.label_ =="SPEC":
                specis.append(ent.text)

        '''for ent in doc.ents:
            if ent.label_ == "ORG":
                species = ent.text.split()[1]
                print("Species:", species)
                specis.append(species)
                break
        else:
            print("No match found.")'''

        return specis
    def findInfra(bIo):
        infra = []
        return infra

    def findLong(p):
        longitude = ""
        pattern = r"\b\d{1,3}\.\d{1,6}\b°?\s?[WwEe]\b"
        longitude = re.findall(pattern, p)
        return longitude
    def findLat(p):
        lat = ""
        pattern = r"\b\d{1,3}\.\d{1,6}\b°?\s?[NnSs]\b"
        lat = re.findall(pattern, p)
        return lat
    def findAlt(p):
        alt = ""
        pattern = r"\b\d{1,5}(\.\d+)?\s?(meters?|m)\b"
        alt = re.findall(pattern, p)
        return alt
    def findBMP(p):
        accession_numbers = ""
        pattern = r"\bEO\d{6}\b"
        accession_numbers = re.findall(pattern, p)
        return accession_numbers
    def findMSID(p):
        msid = ''
        #TODO : complete this
        return msid
    def findMsDOI(s):
        doi = ''
        doi_pattern = r"\b(10[.][0-9]{4,}(?:[.][0-9]+)*\/(?:(?![#$%&'()*+,./:;<=>?@[\]^`{|}~\s])\S)+)\b"
        doi = re.findall(doi_pattern, s)

        return doi
    def findMSD(s):

        blob = TextBlob(s)
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




