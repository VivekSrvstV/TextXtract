import json
import re

import nltk
import csv

from core.IsaProcess import IsaProcess
from core.Factor_isa import IsaFactor
from core.allinone import ALlSearch
from core.data_miappe import MData
from core.bio_miappe import MBio
from core.isa_protocol import IsaProtocol
from core.miappe_study import MStudy
import pandas as pd
import csv
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from core.miappe_sample import MSample
from core.assay_isa import IsaAssay
class IsaTab:
    def findEntity(entity):
        print('check 1========================================================')
        print('the entity to find is ', entity)
        papers = ALlSearch.papers
        data = []
        pmid_downloads = ""
        for entites, categories in entity.items():
            if entites == 'Investigation':
                data += IsaTab.findInvestigation(categories,papers)
                pmid_downloads = "PMID_inv"
            if entites == 'Study':
               data +=  IsaTab.findStudy(categories,papers)
               pmid_downloads = "PMID_stud"
            if entites == 'Person':
                data += IsaTab.findPerson(categories,papers)
                pmid_downloads = "PMID_per"
            if entites == 'Data':
                data += IsaTab.findData(categories,papers)
                pmid_downloads = "PMID_data"
            if entites == 'Biological Material':
                data += IsaTab.findBiological(categories,papers)
                pmid_downloads = "PMID_bio"
            if entites == 'Assay':
                data += IsaTab.findAssay(categories,papers)
                pmid_downloads = "PMID_asy"
            if entites == 'Factor':
                data += IsaTab.findFactor(categories,papers)
                pmid_downloads = "PMID_fc"
            if entites == 'Protocol':
                print("into obsearvation unit data")
                data += IsaTab.findProtocol(categories,papers)
                pmid_downloads = "PMID_p"
            if entites == 'Sample':
                data += IsaTab.findSample(categories,papers)
                pmid_downloads = "PMID_s"
            if entites == 'Process':
                data += IsaTab.findProcess(categories,papers)
                pmid_downloads = "PMID_pr"
        #print(json.dumps(data, indent=4, ensure_ascii=False))

       # if(data):IsaTab.outputData(data,papers,pmid_downloads)
        return data
    def outputData(data,papers,pmid_downloads):
        print("into output data",pmid_downloads)
        ALlSearch.deleteFilesFromFolder('isa_output')
        with open("../isa_output/miappe_data_output.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        #df = pd.DataFrame(data)
        # Convert the list of JSON data into separate files
        for item in data:
            filename = item[pmid_downloads]
            with open(f"isa_output/{filename}.json", "w") as file:
                json.dump(item, file, indent=4, ensure_ascii=False)
                # Create a DataFrame for the current item
            df_item = pd.DataFrame([item])

            # Save as CSV
            df_item.to_csv(f"isa_output/{filename}.csv", index=False)

            # Save as Excel
            df_item.to_excel(f"isa_output/{filename}.xlsx", index=False)
            #Save as PDF
            data1 = []
            with open(f'isa_output/{filename}.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    data1.append(row)



            # Create PDF canvas
            doc = SimpleDocTemplate(f'isa_output/{filename}.pdf', pagesize=portrait(letter))
            elements = []
            # Create table
            table = Table(data1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
                ('TEXTCOLOR', (0, 0), (-1, 0), 'whitesmoke'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), 'beige'),
                ('GRID', (0, 0), (-1, -1), 1, 'black')
            ]))

            elements.append(table)

            # Build PDF
            doc.build(elements)
        # Create a DataFrame from the JSON data
        df = pd.DataFrame(data)
        #df.to_excel("isa_output/miappe_data_output.xlsx", index=False)
        df.to_csv("isa_output/miappe_data_output.csv", index=False)
        data1 = []
        with open('isa_output/miappe_data_output.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data1.append(row)

        # Create PDF canvas
        doc = SimpleDocTemplate('isa_output/miappe_data_output.pdf', pagesize=portrait(letter))
        elements = []

        # Create table
        table = Table(data1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'whitesmoke'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'beige'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        elements.append(table)

        # Build PDF
        doc.build(elements)
    def findInvestigation(investigationEntity,papers):
        print('into investigation method')
        tables = []

        for paper_id, record in papers.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                title = record['MedlineCitation']['Article']['ArticleTitle']
                first_sentence = ''
                CopyRightInformation = ''
                if 'Abstract' in record['MedlineCitation']['Article']:
                    AbstractText = record['MedlineCitation']['Article']['Abstract']['AbstractText']
                    if AbstractText != '':
                        first_sentence = nltk.sent_tokenize(AbstractText[0])
                        first_sentence = first_sentence[0]
                    else:
                        first_sentence = ''
                    if 'CopyrightInformation' in record['MedlineCitation']['Article']['Abstract']:
                        CopyRightInformation = record['MedlineCitation']['Article']['Abstract']['CopyrightInformation']
                    else:
                        CopyRightInformation = ''
                DateCompleted =record['MedlineCitation']['DateCompleted'] if 'DateCompleted' in record['MedlineCitation'] else ''
                if(DateCompleted):
                    if "Month" in DateCompleted and "Day" in DateCompleted:
                        date_str = "-".join([DateCompleted["Year"], DateCompleted["Month"], DateCompleted["Day"]])
                    elif "Month" in DateCompleted:
                        date_str = "-".join([DateCompleted["Year"], DateCompleted["Month"]])
                    else:
                        date_str = DateCompleted["Year"]
                else:
                    date_str = ''
                PubDate = f"{record['PubmedData']['History'][0]['Year']}-{record['PubmedData']['History'][0]['Month']}-{record['PubmedData']['History'][0]['Day']}"
                eid = record['MedlineCitation']['Article']['ELocationID']
                if len(eid) > 1:
                    doi = eid[1]
                else:
                    doi = eid
                DOI =doi
                if title or first_sentence or date_str or PubDate or CopyRightInformation or DOI :
                    tables.append({
                        'PMID_inv':paper_id,
                        'Title': title,
                        'AbstractText': first_sentence,
                        'DateCompleted': date_str,
                        'PubDate': PubDate,
                        'CopyRightInformation': CopyRightInformation,
                        'DOI': DOI
                    })
        print('the table data is ',tables)

        return tables
    def findStudy(studyEntity,filtered_publications):
        pmids = []
        #print(json.dumps(filtered_publications, indent=4, ensure_ascii=False))
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in record["MedlineCitation"]["Article"]["PublicationTypeList"]:

                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = MStudy.study_values(results,studyEntity)

        return res
    def findData(dataEntity,filtered_publications):
        print('into data method')
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        ##print('reserach articles are ',pmids)
        results = MStudy.listPdfFiles(pmids)
        res = MData.find_all_data(results)
        return res
    def findPerson(personEntity,filtered_publications):
        #print('into person entity')
        ptables = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and record["MedlineCitation"]["Article"][
                "PublicationTypeList"] == ["Journal Article"]:
                authors_list = record['MedlineCitation']['Article'].get('AuthorList', [])
                authors = ', '.join(
                    [f"{author.get('LastName', '')} {author.get('Initials', '')}" for author in authors_list])
                affiliations = []
                identifiers = []
                for author in authors_list:
                    affiliation_info = author.get('AffiliationInfo', [])
                    if affiliation_info:
                        affiliation = affiliation_info[0].get('Affiliation', '')
                        affiliations.append(affiliation)
                    identifier = author.get('Identifier', [])
                    if identifier:
                        identifier = identifier[0]
                        identifiers.append(identifier)
                author_affiliation = ', '.join(affiliations)
                identifier = ', '.join(identifiers)
                role = 'Author'
                if authors or author_affiliation or identifier or role :
                    ptables.append({
                        'PMID_per': paper_id,
                        'PersonName': authors,
                        'PersonAffliation': author_affiliation,
                        'PersonID': identifier,
                        'PersonRole': role,
                        'PersonEmail': ''

                    })

        return ptables

    def findBiological(bEntity,filtered_publications):
        print('into biological method')
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = MBio.find_all_BIo(results)
        return res
    def findAssay(env,filtered_publications):
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in \
                    record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = IsaAssay.findAllassay(results)
        return res
    def findFactor(eve,filtered_publications):
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in \
                    record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = IsaFactor.findAllFactor(results)
        return res
    def findProtocol(obs,filtered_publications):
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in \
                    record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = IsaProtocol.findAllProtocol(results)
        return res
    def findSample(obs,filtered_publications):
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in \
                    record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = MSample.findAllSamples(results)
        return res
    def findProcess(obs,filtered_publications):
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in \
                    record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = IsaProcess.findAllProcess(results)
        return res
