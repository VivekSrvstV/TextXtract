from core.get_outline  import GetOutline
import re
import spacy
class MObs:
    def findAllObs(pdfFiles):
        evt_miappe = []
        print('Check 1 obs', pdfFiles)
        for p in pdfFiles:
            "Observation unit factor value"
            findO = GetOutline.getOutLineAndText(p)
            ou = MObs.findOu(findO)
            ouID = MObs.findOuId(findO)
            outype = MObs.findOutype(findO)
            exid = MObs.findeid(findO)
            oufv = MObs.findoufv(findO)
            spD = MObs.findspd(findO)
            if ou or ouID or outype or exid or oufv or spD:
                evt_miappe.append({'PMID_o': p, 'ou': ou,'ouid':ouID,'outype':outype,'spd':spD,'exid':exid,'oufv':oufv})
        return evt_miappe



    def findOu(self):
        ev = ''
        return ev
    def findOuId(self):
        evt = ''
        return evt
    def findOutype(evText):
        accession_numbers = ""
        pattern = r"\bCO_\d{6}\b"
        accession_numbers = re.findall(pattern, evText)
        return accession_numbers

    def findeid(self):
        evD = ''
        return evD
    def findoufv(self):
        evD = ''
        return evD
    def findspd(texts):
        nlp = spacy.load("en_core_sci_lg")
        doc = nlp(texts)
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["DATE"]:
                entities.append(ent.text)
        return entities