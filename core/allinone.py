import json
import os
import shutil
import csv
import pandas as pd
from Bio import Entrez
from flask import Flask, render_template, request
from concurrent.futures import ThreadPoolExecutor
from Bio.Medline import parse
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from urllib.parse import quote
from urllib.parse import urlparse as url_parse
from urllib.parse import quote as url_quote


app = Flask(__name__)
executor = ThreadPoolExecutor(4) # 4 threads for parallel search

class ALlSearch:
    pubmed_search_results = []
    pubmed_total_results = []
    table = {}
    papers = {}
    @staticmethod
    def search_publications(title, retstart, end,args):
        print("check 5")
        print(end)
        print(title)
        print(args)
        Entrez.email = 'viveksriv19@gmail.com'
        handle = Entrez.esearch(db='pubmed',
                                sort='relevance',
                                retmax=end,
                                retstart=retstart,
                                retmode='xml',
                                term=title + args) # use [Title] to search in the title field
                                #term="genotypic traits in maize plants roots[Title]")
        results = Entrez.read(handle)
        #print('check 2.1',results)
        print(results['Count'])

        handle.close()
        return results

    @staticmethod
    def fetch_details(id_list):
        Entrez.email = 'viveksriv19@gmail.com'
        handle = Entrez.esummary(db='pubmed',
                                 retmode='xml',
                                 id=','.join(id_list))


        handle = Entrez.efetch(db='pubmed', retmode='xml', id=id_list)
        records = Entrez.read(handle)['PubmedArticle']
        ALlSearch.pubmed_search_results.clear()
        ALlSearch.pubmed_total_results.clear()
        ALlSearch.table.clear()
        ALlSearch.papers.clear()
        for record in records:
            paper_id = record['MedlineCitation']['PMID']
            ALlSearch.papers[paper_id] = record
        print('check 3 ',ALlSearch.papers)
        handle.close()
        return ALlSearch.papers

    @staticmethod
    def search_pubmed(title, page=1):
        retstart = (page - 1) * 100
        end = retstart + 100

        id_list = ALlSearch.search_publications(title, retstart, end)
        papers = ALlSearch.fetch_details(id_list)
        return papers

    @staticmethod
    def search_pubmed_parallel(title, page=1):
        retstart = (page - 1) * 100
        end = retstart + 100

        id_lists = []
        with executor as ex:
            futures = [ex.submit(ALlSearch.search_publications, title, i, min(i+99, end)) for i in range(retstart, end, 100)]
            for future in futures:
                id_lists.append(future.result())

        id_list = [paper_id for paper_ids in id_lists for paper_id in paper_ids]
        papers = ALlSearch.fetch_details(id_list)
        return papers

    def extract_result_to_table(query):
        ALlSearch.pubmed_search_results.clear()
        ALlSearch.pubmed_total_results.clear()
        ALlSearch.table.clear()
        ALlSearch.papers.clear()
        print(query)
        id_list = ALlSearch.search_publications(query, 0, 10000,'[Title]')['IdList']
        print('all results ', id_list)
        paper_records = ALlSearch.fetch_details(id_list)
        print(json.dumps(paper_records, indent=4, ensure_ascii=False))
        for paper_id, record in paper_records.items():
            title = record['MedlineCitation']['Article']['ArticleTitle']
            pubmed_id = paper_id
            authors_list = record['MedlineCitation']['Article'].get('AuthorList', [])
            authors = ', '.join(
                [f"{author.get('LastName', '')} {author.get('Initials', '')}" for author in authors_list])
            citation = record['MedlineCitation']['Article']['Journal']['ISOAbbreviation']
            pubdate = f"{record['PubmedData']['History'][0]['Year']}-{record['PubmedData']['History'][0]['Month']}-{record['PubmedData']['History'][0]['Day']}"
            ALlSearch.table[paper_id] = {
                'Title': title,
                'PMID': pubmed_id,
                'Authors': authors,
                'Citation': citation,
                'Publication Date': pubdate
            }
            df = pd.DataFrame.from_records(ALlSearch.table)
            print('dataframe done')
            ALlSearch.deleteFilesFromFolder('/home/vivek/InterText/csv_results')
            df.to_csv("/home/vivek/InterText/csv_results/pubmed_results.csv", index=False)
            df1 = pd.DataFrame.from_dict(ALlSearch.table, orient='index')
            ALlSearch.deleteFilesFromFolder('/var/www/html/InterText/data_results')
            df1.to_csv('/var/www/html/InterText/data_results/data.csv')
            df1.to_json('/var/www/html/InterText/data_results/data.json')
            # Save as PDF
            data1 = []
            with open(f'/var/www/html/InterText/data_results/data.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    data1.append(row)
                    # Create PDF canvas
                    doc = SimpleDocTemplate(f'/var/www/html/InterText/data_results/data.pdf', pagesize=portrait(letter))
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

        return ALlSearch.table

    def save_data_in_csv(texts):
        print('saving data in csv')
        print('in csv print', texts)
        id_list = ALlSearch.search_publications(texts, 0, 10000)
        print('all results ',id_list)
        papers = ALlSearch.fetch_details(id_list['IdList'])
        paper_records = ALlSearch.fetch_details(id_list)

        for paper_id, record in paper_records.items():
            title = record['MedlineCitation']['Article']['ArticleTitle']
            pubmed_id = paper_id
            authors_list = record['MedlineCitation']['Article'].get('AuthorList', [])
            authors = ', '.join(
                [f"{author.get('LastName', '')} {author.get('Initials', '')}" for author in authors_list])
            citation = record['MedlineCitation']['Article']['Journal']['ISOAbbreviation']
            pubdate = f"{record['PubmedData']['History'][0]['Year']}-{record['PubmedData']['History'][0]['Month']}-{record['PubmedData']['History'][0]['Day']}"
            ALlSearch.table[paper_id] = {
                'Title': title,
                'PMID': pubmed_id,
                'Authors': authors,
                'Citation': citation,
                'Publication Date': pubdate
            }
        df = pd.DataFrame.from_records(ALlSearch.table)
        # Convert dictionary to DataFrame
        df1 = pd.DataFrame.from_dict(ALlSearch.table, orient='index')
        print('df done')
        df.to_csv("pubmed_results.csv", index=False)
        df1.to_csv('/home/vivek/InterText/data_results/data.csv')

        return df
    def write_to_pmf(self):
        print('into pmf')
        ALlSearch.deleteFilesFromFolder("fetched_pdfs")
        dict_data = ALlSearch.table
        print('the value in table data is ')
        print(json.dumps(dict_data, indent=4, ensure_ascii=False))
        try:
            with open("PMF", 'a') as file:
                file.seek(0)
                file.truncate()
                for d in dict_data:
                    print(d)
                    file.write(d+"\n")
        except IOError:
            print("I/O error")

    def deleteFilesFromFolder(folder):
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                   if os.path.isfile(file_path):
                      os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        else:
            print(f"The folder {folder} does not exist.")

    def listFileWithTitle(self):
        folder = os.path.abspath('fetched_pdfs')
        pdfFiles = []
        dict_data = ALlSearch.table
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                pdfFiles.append(filename)
                print(filename)
        print(pdfFiles)
        pmidlist = [x[:-4] for x in pdfFiles]
        result = []
        for i in pmidlist:
            print("inside pdf lists")
            print(i)
            j_values = ALlSearch.table[i]
            title = j_values['Title']
            pubmed_id = j_values['PMID']
            print(f"Paper ID: {i}\nTitle: {title}\nPMID: {pubmed_id}\n")
            result.append({"pmid": pubmed_id, "title": title})

        return result

