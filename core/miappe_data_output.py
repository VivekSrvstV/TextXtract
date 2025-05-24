import json
import re

import nltk
import csv
from core.allinone import ALlSearch
from core.data_miappe import MData
from core.bio_miappe import MBio
from core.env_miappe import MEnv
from core.miappe_study import MStudy
import pandas as pd
import csv
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from core.miappe_event import MEvent
from core.miappe_observation import MObs
from core.miappe_sample import MSample
from core.miappe_observed_variable import MOv

class MiappeData:
    def findEntity(entity):
        print('check 1========================================================')
        print('the entity to find is ', entity)
        papers = ALlSearch.papers
        data = []
        pmid_downloads = ""
        for entites, categories in entity.items():
            if entites == 'Investigation':
                data += MiappeData.findInvestigation(categories,papers)
                pmid_downloads = "PMID_inv"
            if entites == 'Study':
               data +=  MiappeData.findStudy(categories,papers)
               pmid_downloads = "PMID_stud"
            if entites == 'Person':
                data += MiappeData.findPerson(categories,papers)
                pmid_downloads = "PMID_per"
            if entites == 'Data':
                data += MiappeData.findData(categories,papers)
                pmid_downloads = "PMID_data"
            if entites == 'Biological':
                data += MiappeData.findBiological(categories,papers)
                pmid_downloads = "PMID_bio"
            if entites == 'Environment':
                data += MiappeData.findEnvironment(categories,papers)
                pmid_downloads = "PMID_env"
            if entites == 'Event':
                data += MiappeData.findEvent(categories,papers)
                pmid_downloads = "PMID_ev"
            if entites == 'Observation Unit':
                print("into obsearvation unit data")
                data += MiappeData.findObs(categories,papers)
                pmid_downloads = "PMID_o"
            if entites == 'Sample':
                data += MiappeData.findSample(categories,papers)
                pmid_downloads = "PMID_s"
            if entites == 'Observed Variable':
                data += MiappeData.findObservedVariable(categories,papers)
                pmid_downloads = "PMID_ov"
            pmid_downloads = entites
        print(json.dumps(data, indent=4, ensure_ascii=False))

        if(data):MiappeData.outputData(data,papers,pmid_downloads)
        print("&&&&&&&&&&&&& check data ",data)
        return data
    def outputData(data,papers,pmid_downloads):
        print("into output data", pmid_downloads)

        print(data)
        print(papers)

        ALlSearch.deleteFilesFromFolder('miappe_output')
        with open("../miappe_output/miappe_data_output.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        df = pd.DataFrame(data)
        df.to_csv(f"miappe_output/miappe_data_output.csv", index=False)
        df.to_excel(f"miappe_output/miappe_data_output.xlsx", index=False)
        # Save as PDF
        data1 = []
        with open(f'../miappe_output/miappe_data_output.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data1.append(row)

        # Create PDF canvas
        doc = SimpleDocTemplate(f'../miappe_output/miappe_data_output.pdf', pagesize=portrait(letter))
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
        '''
        # Convert the list of JSON data into separate files
        for item in data:
            filename = item[pmid_downloads, "default_filename"]
            with open(f"miappe_output/{filename}.json", "w") as file:
                json.dump(item, file, indent=4, ensure_ascii=False)
                # Create a DataFrame for the current item
            df_item = pd.DataFrame([item])

            # Save as CSV
            df_item.to_csv(f"miappe_output/{filename}.csv", index=False)

            # Save as Excel
            df_item.to_excel(f"miappe_output/{filename}.xlsx", index=False)
            #Save as PDF
            data1 = []
            with open(f'miappe_output/{filename}.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    data1.append(row)



            # Create PDF canvas
            doc = SimpleDocTemplate(f'miappe_output/{filename}.pdf', pagesize=portrait(letter))
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
        #df.to_excel("miappe_output/miappe_data_output.xlsx", index=False)
        df.to_csv("miappe_output/miappe_data_output.csv", index=False)
        data1 = []
        with open('miappe_output/miappe_data_output.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data1.append(row)

        # Create PDF canvas
        doc = SimpleDocTemplate('miappe_output/miappe_data_output.pdf', pagesize=portrait(letter))
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
'''

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

    def findStudy(studyEntity,filtered_publications):
        pmids = []
        #print(json.dumps(filtered_publications, indent=4, ensure_ascii=False))
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in record["MedlineCitation"]["Article"]["PublicationTypeList"]:

                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = MStudy.study_values(results,studyEntity)

        return res
    def findBiological(bEntity,filtered_publications):
        print('into biological method')
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = MBio.find_all_BIo(results)
        return res
    def findEnvironment(env,filtered_publications):
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in \
                    record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = MEnv.findAllEnv(results)
        return res
    def findEvent(eve,filtered_publications):
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in \
                    record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = MEvent.findAllEvent(results)
        return res
    def findObs(obs,filtered_publications):
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in \
                    record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = MObs.findAllObs(results)
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
    def findObservedVariable(obs,filtered_publications):
        pmids = []
        for paper_id, record in filtered_publications.items():
            if "PublicationTypeList" in record["MedlineCitation"]["Article"] and "Journal Article" in \
                    record["MedlineCitation"]["Article"]["PublicationTypeList"]:
                pmids.append(paper_id)
        results = MStudy.listPdfFiles(pmids)
        res = MOv.findAllOv(results)
        return res