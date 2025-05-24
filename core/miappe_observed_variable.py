from core.get_outline  import GetOutline
import re
import spacy

from textblob import TextBlob
class MOv:
    def findAllOv(pdfFiles):
        evt_miappe = []
        print('Check 1 env', pdfFiles)
        for p in pdfFiles:
            findO = GetOutline.getOutLineAndText(p)

            mD = MOv.findMethodD(findO)
            ram = MOv.findRAM(findO)
            scale = MOv.findScale(findO)
            scalean = MOv.findScaleAn(findO)
            tscale = MOv.findTScale(findO)
            if mD or ram or scale or scalean or tscale:
                evt_miappe.append({'PMID_ov': p, 'mD': mD, 'ram': ram, 'scale': scale,
                                   'scalean': scalean, 'tscale': tscale})
        return evt_miappe



    def findMethodD(pdfFiles):
        evD = ''
        blob = TextBlob(pdfFiles)
        noun_phrases = blob.noun_phrases
        top_noun_phrases = sorted(set(noun_phrases), key=noun_phrases.count, reverse=True)[:25]

        # Create a title by joining the most important noun phrases with appropriate punctuation
        evDesc = ' '.join([phrase.capitalize() for phrase in top_noun_phrases]) + '.'

        return evDesc
    def findRAM(findData):

        urls = ""

        url_pattern = re.compile(r'http://doi\.org/[a-zA-Z0-9.]+')

        urls = re.findall(url_pattern, findData)

        urls = [url.replace('\n', '') for url in urls]

        return urls

    def findScale(self):
        evD = ''
        return evD
    def findScaleAn(p):

        accession_numbers = ""
        pattern = r"\bCO\d{6}\b"
        accession_numbers = re.findall(pattern, p)
        return accession_numbers

    def findTScale(self):
        evD = ''
        return evD