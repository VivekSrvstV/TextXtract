from core.get_outline  import GetOutline
import re
import spacy

from textblob import TextBlob
class IsaProtocol:
    def findAllProtocol(papers):
        Protocols = []
        for p in papers:
            Protocol = GetOutline.getOutLineAndText(p)
            ProtocolName = IsaProtocol.findFName(Protocol)
            ProtocolType = IsaProtocol.findProtocolType(Protocol)
            ProtocolDesc = IsaProtocol.findProtocolDesc(Protocol)
            ProtocolURI = IsaProtocol.findProtocolURI(Protocol)
            ProtocolVersion = IsaProtocol.findProtocolVersion(Protocol)
            ProtocolParameter = IsaProtocol.findProtocolParameter(Protocol)
            ProtocolComponents = IsaProtocol.findProtocolComp(Protocol)
            if ProtocolName or ProtocolDesc or ProtocolType:
                Protocols.append({'PMID_p': p, 'pname': ProtocolName,'ptype':ProtocolType,'pdesc':ProtocolDesc,
                                  'puri':ProtocolURI,'pver':ProtocolVersion,'pcom':ProtocolComponents,'ppar':ProtocolParameter})
        return Protocols


#example
    ''' 
     Study Protocol Name	"environmental material collection - standard procedure 1"	"nucleic acid extraction - standard procedure 2"	"mRNA extraction - standard procedure 3"	"genomic DNA extraction - standard procedure 4"	"reverse transcription - standard procedure 5"	"library construction"	"pyrosequencing - standard procedure 6"	"sequence analysis - standard procedure 7"
Study Protocol Type	"sample collection"	"nucleic acid extraction"	"nucleic acid extraction"	"nucleic acid extraction"	"reverse transcription"	"library construction"	"nucleic acid sequencing"	"data transformation"
Study Protocol Type Term Accession Number	""	""	""	""	""	""	""	""
Study Protocol Type Term Source REF	""	""	""	""	""	""	""	""
Study Protocol Description	"Waters samples were prefiltered through a 1.6 um GF/A glass fibre filter to reduce Eukaryotic contamination. Filtrate was then collected on a 0.2 um Sterivex (millipore) filter which was frozen in liquid nitrogen until nucelic acid extraction. CO2 bubbled through 11000 L mesocosm to simulate ocean acidification predicted conditions. Then phosphate and nitrate were added to induce a phytoplankton bloom."	"Total nucleic acid extraction was done as quickly as possible using the method of Neufeld et al, 2007."	"RNA MinElute + substrative Hybridization + MEGAclear For transcriptomics, total RNA was separated from the columns using the RNA MinElute clean-up kit (Qiagen) and checked for integrity of rRNA using an Agilent bioanalyser (RNA nano6000 chip). High integrity rRNA is essential for subtractive hybridization. Samples were treated with Turbo DNA-free enzyme (Ambion) to remove contaminating DNA. The rRNA was removed from mRNA by subtractive hybridization (Microbe Express Kit, Ambion), and absence of rRNA and DNA contamination was confirmed using the Agilent bioanalyser. The mRNA was further purified with the MEGAclearTM kit (Ambion). Reverse transcription of mRNA was performed using the SuperScript III enzyme (Invitrogen) with random hexamer primers (Promega). The cDNA was treated with RiboShredderTM RNase Blend (Epicentre) to remove trace RNA contaminants. To improve the yield of cDNA, samples were subjected to random amplification using the GenomiPhi V2 method (GE Healthcare). GenomiPhi technology produces branched DNA molecules that are recalcitrant to the pyrosequencing methodology. Therefore amplified samples were treated with S1 nuclease using the method of Zhang et al.2006."	""	"superscript+random hexamer primer"	""	"1. Sample Input and Fragmentation: The Genome Sequencer FLX System supports the sequencing of samples from a wide variety of starting materials including genomic DNA, PCR products, BACs, and cDNA. Samples such as genomic DNA and BACs are fractionated into small, 300- to 800-base pair fragments. For smaller samples, such as small non-coding RNA or PCR amplicons, fragmentation is not required. Instead, short PCR products amplified using Genome Sequencer fusion primers can be used for immobilization onto DNA capture beads as shown below."	""
Study Protocol URI	""	""	""	""	""	""	""	""
Study Protocol Version	""	""	""	""	""	""	""	""
Study Protocol Parameters Name	"filter pore size"	""	""	""	""	"library strategy;library layout;library selection"	"sequencing instrument"	""
Study Protocol Parameters Name Term Accession Number	""	""	""	""	""	";;"	""	""
Study Protocol Parameters Name Term Source REF	""	""	""	""	""	";;"	""	""
Study Protocol Components Name	""	""	""	""	""	""	""	""
Study Protocol Components Type	""	""	""	""	""	""	""	""
Study Protocol Components Type Term Accession Number	""	""	""	""	""	""	""	""
Study Protocol Components Type Term Source REF	""	""	""	""	""	""	""	""
    Study Protocol Name	"dose"	"compound"	"collection time"
Study Protocol Type	"dose"	"chemical substance"	"time"
Study Protocol Type Term Accession Number	"http://www.ebi.ac.uk/efo/EFO_0000428"	"http://purl.obolibrary.org/obo/CHEBI_59999"	"http://purl.obolibrary.org/obo/PATO_0000165"
Study Protocol Type Term Source REF	"EFO"	"CHEBI"	"PATO"
    '''
    def findFName(papers):
        ProtocolName = []
        nlp = spacy.load("en_ner_bc5cdr_md")

        # Define the list of protocol names
        protocol_names = [
            "environmental material collection", "nucleic acid extraction", "mRNA extraction",
            "genomic DNA extraction", "reverse transcription", "library construction",
            "pyrosequencing", "sequence analysis", "PCR (Polymerase Chain Reaction)",
            "Gel Electrophoresis", "Western Blotting", "ELISA","Enzyme-Linked Immunosorbent Assay",
            "Immunoprecipitation", "Chromatography", "RNA-seq Library Preparation",
            "ChIP-seq","Chromatin Immunoprecipitation Sequencing", "Flow Cytometry",
            "Immunohistochemistry", "CRISPR/Cas9 Editing", "Proteomics Analysis",
            "Metagenomic Sequencing", "Single-Cell Sequencing", "Microarray Hybridization",
            "Mass Spectrometry", "Protein Purification", "RNA Interference","RNAi",
            "PCR","Polymerase Chain Reaction","Plant DNA Amplification",
            "Gel Electrophoresis", "Western Blotting","Plant Protein Analysis",
            "ELISA","Enzyme-Linked Immunosorbent Assay","Plant Pathogen Detection",
            "Immunoprecipitation","Plant Proteomics",
            "Chromatography","HPLC", "Gas Chromatography","Plant Metabolite Analysis",
            "RNA-seq",
            "ChIP-seq","Chromatin Immunoprecipitation Sequencing",
            "Flow Cytometry","Plant Cell Analysis", "Immunohistochemistry",
            "CRISPR/Cas9",
            "Proteomics Analysis",
            "Metagenomic Sequencing",
            "Single-Cell Sequencing", "Microarray Hybridization",
            "RNAi","RNA Interference"
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
                    ProtocolName.append(sentence.text.strip())

        return ProtocolName
    def findProtocolType(papers):
        ProtocolType = []

        nlp = spacy.load("en_ner_bc5cdr_md")

        # Define the list of protocol names
        protocol_names = [
            "sample collection", "nucleic acid extraction", "reverse transcription", "library construction",
            "nucleic acid sequencing", "data transformation", "Plant Tissue Culture", "PCR",
            "Polymerase Chain Reaction", "Plant Transformation", "Metabolomics", "Proteomics", "RNA Interference",
            "Chromatin Immunoprecipitation", "Microscopy Techniques", "Plant Phenotyping","Genome Editing"
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
                    ProtocolType.append(sentence.text.strip())

        return ProtocolType

    def findProtocolDesc(paper):
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
    def findProtocolURI(papers):
        urls = ""
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),\n]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

        urls = re.findall(url_pattern, papers)
        # Remove newline characters from URLs
        urls = [url.replace('\n', '') for url in urls]
        print('chekc 4 =================================================', urls)
        return urls
    def findProtocolVersion(self):
        ver = ""
        return ver
    def findProtocolParameter(papers):

        nlp = spacy.load("en_ner_bc5cdr_md")
        pp = []
        # Define the list of protocol names
        protocol_names = [
            "filter pore size", "library strategy", "library layout", "library selection", "sequencing instrument",
            "Sequencing Depth", "Read Length", "Insert Size", "Quality Scores", "Indexing Strategy",
            "Mapping Algorithm", "Plant Genome Size", "Transcriptome Complexity", "Sequencing Platform Compatibility",
            "Specific Plant Transcript Isoforms", "Genomic Variations in Plant Populations",
            "Plant-Specific Reference Genome", "Plant-Specific Bioinformatics Tools", "Functional Annotation",
            "Plant Pathogen Identification", "Plant-Specific Gene Expression Signatures"
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
                    pp.append(sentence.text.strip())

        return pp

    def findProtocolComp(self):
        com = ""
        return com