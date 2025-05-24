from core.get_outline  import GetOutline
import re
import spacy
class IsaAssay:
    def findAllassay(papers):
        assays = []
        for p in papers:
            assay = GetOutline.getOutLineAndText(p)
            MeasurementType = IsaAssay.findMeasurementType(assay)
            TechnologyType = IsaAssay.findTechnologyType(assay)
            assayProp = IsaAssay.findassayProp(assay)
            print("=================into assay =======================")
            print(p)
            print(MeasurementType)
            print(TechnologyType)
            print(assayProp)
            print("==============exiting assay===================")
            if MeasurementType or assayProp or TechnologyType:
                assays.append({'PMID_as': p, 'mt': MeasurementType,'ttype':TechnologyType,'aProp':assayProp})
        return assays


#example
    ''' 
    
    "Measurement Type",
    "Technology Type",
    "Technology Platform",
    "Materials",
    "Characteristic Categories",
    "Unit Categories"
    Study Assay File Name	"a_gilbert-assay-Gx.txt"	"a_gilbert-assay-Tx.txt"
    Study Assay Measurement Type	"metagenome sequencing"	"transcription profiling"
    Study Assay Measurement Type Term Accession Number	""	""
    Study Assay Measurement Type Term Source REF	"OBI"	"OBI"
    Study Assay Technology Type	"nucleotide sequencing"	"nucleotide sequencing"
    Study Assay Technology Type Term Accession Number	""	""
    Study Assay Technology Type Term Source REF	"OBI"	"OBI"
    Study Assay Technology Platform	"454 GS FLX"	"454 GS FLX"
    '''
    def findMeasurementType(papers):
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
        measurementtyoe = []
        # Iterate through each sentence in the paragraph
        for sentence in doc.sents:
            # Iterate through each category of parameters
            for category, parameter_list in parameters.items():
                # Check if any parameter from the category is present in the sentence
                for parameter in parameter_list:
                    if parameter.lower() in sentence.text.lower():
                        measurementtyoe.append(parameter)

        return measurementtyoe
    def findTechnologyType(papers):
        accession_numbers = ""
        pattern = r"\bCO_\d{6}\b"
        accession_numbers = re.findall(pattern, papers)
        return accession_numbers
        return findTechnologyType
    def findassayProp(paper):
        assayProp = ""

        return assayProp

