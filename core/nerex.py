import os

import pandas as pd

import re

import spacy
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfparser import PDFParser
nlp = spacy.load('en_core_sci_lg')

# Define a function to extract named entities from text
def extract_entities(text):
    doc = nlp(text)
    # Extract named entities
    entities = []
    for ent in doc.ents:
        #print('labels in files = ',ent.label_)
        if ent.label_ in ["PERSON", "ORG", "GPE", "EMAIL","LOC","WORK_OF_ART","CARDINAL","DATE","PERCENT","NORP",
                          "PRODUCT","TIME"]:
            entities.append((ent.text, ent.label_))

    # Convert named entities to a DataFrame
    df = pd.DataFrame(entities, columns=["entity", "type"])

    # Print the DataFrame
    #print('the data frame is :')
    #print(df)
    return entities

# Extract text from the PDF file
text = extract_text('../data/miappe.pdf')


body = '''
The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price.
The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal.
Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008.
Real estate firm Tishman Speyer had owned the other 10%.
The buyer is RFR Holding, a New York real estate company.
Officials with Tishman and RFR did not immediately respond to a request for comments.
It's unclear when the deal will close.
The building sold fairly quickly after being publicly placed on the market only two months ago.
The sale was handled by CBRE Group.
The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building.
The rent is rising from $7.75 million last year to $32.5 million this year to $41 million in 2028.
Meantime, rents in the building itself are not rising nearly that fast.
While the building is an iconic landmark in the New York skyline, it is competing against newer office towers with large floor-to-ceiling windows and all the modern amenities.
Still the building is among the best known in the city, even to people who have never been to New York.
It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top.
It has been featured prominently in many films, including Men in Black 3, Spider-Man, Armageddon, Two Weeks Notice and Independence Day.
The previous sale took place just before the 2008 financial meltdown led to a plunge in real estate prices.
Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which was formerly known as Sears Tower, once the world's tallest.
Blackstone Group (BX) bought it for $1.3 billion 2015.
The Chrysler Building was the headquarters of the American automaker until 1953, but it was named for and owned by Chrysler chief Walter Chrysler, not the company itself.
Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete.
Once the competitor could rise no higher, the spire of the Chrysler building was raised into view, giving it the title.
'''

#model = Summarizer()
#result = model(body, min_length=6,max_length=20)
#full = ''.join(result)
#print('000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
#print(full)
# Extract named entities from the text



'''pdf_text = extract_text("fetched_pdfs/29695866.pdf")
a = ['Methods','Methodology','Methods','Materials','Material and Method','Materials and Methods']

for method in a:
    index = pdf_text.find(method)
    if index != -1:
        whitespace_len = 0
        for char in pdf_text[index + len(method):]:
            if char == "\n":
                whitespace_len += 1
            else:
                break

        # Extract the paragraph that follows the method section
        start_index = index + len(method) + whitespace_len
        end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
        paragraph = pdf_text[start_index:end_index]
        #print(f"The paragraph that follows '{method}' is: {paragraph}")
    else:
        print(f"The word '{method}' was not found in the PDF file.")
'''
print('#########################################################################################')


def getOutLineAndText():
    print('Check 8.2 ==============================================')
    folder = os.path.abspath('../fetched_pdfs')
    filenames = os.listdir(folder)
    outline_found = False
    tofind = ''
    print(outline_found)
    textOutput = ''
    mLevel = ''
    titles = ''
    dictin = []
    for p in filenames:
        print(p)
        try:
            with open('fetched_pdfs/32265447.pdf', 'rb') as file:
                parser = PDFParser(file)
                document = PDFDocument(parser)
                try:
                    outlines = document.get_outlines()
                    print(outlines)
                    for level, title, dest, a, se in outlines:
                        print(f"Level: {level}, Title: {title}")
                        print(type(title))
                        titles = title
                        print(f"Title: '{title}'9879877798")
                        print(f"Title: '{titles}'55555")
                        print('##')
                        if titles == 'Methods':
                            outline_found = True
                            tofind = title
                            mLevel = level
                            print(f'check 8.3 ==========={title} found in {p}')
                        print(outline_found)

                    if outline_found==True:
                        dictin.append({'l': level, 't': title})
                        print(dictin)
                        text = extract_text(file)
                        print('CHECK 8.3.1 =====================OUTLINE=========', outline_found)
                        print('CHECK 8.3.2 =====================TOFIND VALUE=========', tofind)
                        methods_text = re.search(rf'{tofind}(.*?)', text, re.DOTALL)
                        # methods_text = re.search(rf'{tofind}(.*?)(?=(?:(?<!\d)\.{1, 2})\s+(?=\d|[A-Z]))', text,
                        # re.DOTALL)

                        print(methods_text)
                        if methods_text:
                            print('check 8.4===============================================')
                            print(methods_text.group(1))
                            textOutput = methods_text.group(1)
                            print('check 8.5===============================================')
                except PDFNoOutlines:
                    outlines = None
                    #textOutput = GetOutline.extractMethodsFromPDF(p)


        except PDFSyntaxError:
            print(f'Error parsing PDF file : Invalid or corrupted PDF file.')

    return textOutput








#entities = extract_entities(text)
getOutLineAndText()
#print('the entites are :')
#for ents in entities:
 #   print (ents)

