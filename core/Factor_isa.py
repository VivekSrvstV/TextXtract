from core.get_outline  import GetOutline
import re
import spacy
class IsaFactor:
    def findAllFactor(papers):
        factors = []
        for p in papers:
            factor = GetOutline.getOutLineAndText(p)
            factorName = IsaFactor.findFName(factor)
            FactorType = IsaFactor.findFactorType(factor)
            factorProp = IsaFactor.findFactorProp(factor)
            if factorName or factorProp or FactorType:
                factors.append({'PMID_f': p, 'fname': factorName,'ftype':FactorType,'fProp':factorProp})
        return factors


#example
    ''' 
    Study Factor Name	"dose"	"compound"	"collection time"
Study Factor Type	"dose"	"chemical substance"	"time"
Study Factor Type Term Accession Number	"http://www.ebi.ac.uk/efo/EFO_0000428"	"http://purl.obolibrary.org/obo/CHEBI_59999"	"http://purl.obolibrary.org/obo/PATO_0000165"
Study Factor Type Term Source REF	"EFO"	"CHEBI"	"PATO"
    '''
    def findFName(papers):
        nlp = spacy.load("en_ner_bc5cdr_md")
        fname = []
        # Define the list of protocol names
        protocol_names = [
            "dose","compound","collection time","Concentration Gradient","Stress Conditions","Harvesting Time Points","Biological Replicates","Tissue"
        ]
        doc = nlp(papers)

        # Dictionary to store found protocol names
        found_protocols = {protocol: [] for protocol in protocol_names}

        # Iterate through each sentence in the paragraph
        for sentence in doc.sents:
            # Iterate through each protocol name
            for protocol in protocol_names:
                # Check if the protocol name is present in the sentence
                if protocol.lower() in sentence.text.lower():
                    fname.append(sentence.text.strip())

        return fname


    def findFactorType(papers):
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),\n]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = re.findall(url_pattern, papers)
        urls = [url.replace('\n', '') for url in urls]
        return urls

    def findFactorProp(paper):
        factorProp = ""

        return factorProp

