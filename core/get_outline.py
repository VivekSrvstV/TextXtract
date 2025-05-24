import re

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from io import StringIO
import spacy
from spacy.matcher import Matcher

# Ensure you have run: python -m spacy download en_core_sci_lg
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfparser import PDFParser

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLine, LTChar



class GetOutline:
    '''def getOutLine(p):
        print('Check 8 ==============================================')

        #outs =  GetOutline.test(p)
        level_title = []
        level_title_text = []
        try:
            with open('fetched_pdfs/'+p, 'rb') as file:
                    parser = PDFParser(file)
                    document = PDFDocument(parser)
                    outlines = document.get_outlines()
                    for level, title, dest, a, se in outlines:
                        print(f"Level: {level}, Title: {title}")
                        level_title.append({
                            'Level': level, 'Title': title
                        })
                        #if(title=='Methodology'):
                            #print(f'check 8.1 ==========={title} found in {p}')

        except PDFSyntaxError:
            print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        #print(level_title_text)
        return level_title'''

    def getOutLineAndText(p):
        print('Check 8.2 ==============================================')
        outline_found = False
        print(outline_found)
        textOutput = ''
        tofind = None
        mLevel = None
        next_title = None
        try:
            with open('fetched_pdfs/' + p, 'rb') as file:
                parser = PDFParser(file)
                document = PDFDocument(parser)
                try:
                    print('inside try')
                    outlines = document.get_outlines()
                    for level, title, dest, a, se in outlines:
                        #print(f"Level: {level}, Title: {title}")
                        if title == 'Materials and Methods':
                            outline_found = True
                            tofind = title
                            mLevel = level
                            print(f'check 8.3 ==========={title} found in {p}')
                        elif title == 'Methodologies':
                            outline_found = True
                            tofind = title
                            mLevel = level
                            print(f'check 8.3 ==========={title} found in {p}')
                        elif title == 'Methods':
                            outline_found = True
                            tofind = title
                            mLevel = level
                            print(f'check 8.3 ==========={title} found in {p}')
                        elif title == 'Methods and Materials':
                            outline_found = True
                            tofind = title
                            mLevel = level
                            print(f'check 8.3 ==========={title} found in {p}')
                        elif outline_found and level == mLevel:
                            # found next title at the same level as Methods
                            next_title = title
                            break
                    if outline_found:
                        text = extract_text(file)
                        print('CHECK 8.3.1 =====================OUTLINE=========', outline_found)
                        print('CHECK 8.3.2 =====================TOFIND VALUE=========', tofind)
                        print(f'Next title at level {mLevel}: {next_title}')
                        methods_text = re.search(rf'{tofind}(.*?){next_title}', text, re.DOTALL)
                        print(methods_text)
                        if methods_text:
                            print('check 8.4===============================================')
                            #print(methods_text.group(1))
                            textOutput = methods_text.group(1)
                            print('check 8.5===============================================')
                    else:
                        print('outline not found last check')
                        textOutput = GetOutline.extractMethodsFromPDF(p)
                except PDFNoOutlines:
                    print('inside except')
                    outlines = None
                    textOutput = GetOutline.extractMethodsFromPDF(p)
        except PDFSyntaxError:
            print(f'Error parsing PDF file : Invalid or corrupted PDF file.')

        return textOutput


    def extractMethodsFromPDF(pdfFiles):
        print('into pdf no outlines')
        # define the patterns
        method_pattern = [{"LOWER": {"IN": ["method", "methods"]}}]
        material_pattern = [{"LOWER": "materials"}, {"OP": "?"}]
        mm_pattern = [{"LOWER": "materials"}, {"LOWER": "and"}, {"LOWER": "methods"}]
        methodology_pattern = [{"LOWER": "methodology"}]
        am_pattern = [{"LOWER": "materials"}, {"LOWER": "and"}, {"LOWER": "methods"}]
        m_pattern = [{"LOWER": "material"}, {"LOWER": "and"}, {"LOWER": "method"}]
        ms_pattern = [{"LOWER": "materials"}, {"LOWER": "and"}, {"LOWER": "methods"}]

        # initialize the matcher and add the patterns to it
        try:
            nlp = spacy.load("en_core_sci_lg")
        except OSError:
            raise OSError("Please install the English language model by running: python -m spacy download en_core_sci_lg")
        matcher = Matcher(nlp.vocab)
        pattern_list = [method_pattern, material_pattern, mm_pattern, methodology_pattern, am_pattern, m_pattern,
                        ms_pattern]
        for pattern in pattern_list:
            matcher.add("MaterialMethods", [pattern])

        paragraph = ''
        #a = ['Materials and methods','Method', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        b = ['Results', 'Discussion', 'Conclusion', 'Limitations', 'Future Work','Supporting information']  # add more topics as needed
        try:
                pdf_text = extract_text("fetched_pdfs/"+pdfFiles)
                doc = nlp(pdf_text)
                matches = matcher(doc)
                for match_id, start, end in matches:
                    matched_token = doc[start:end]
                    if ("\n" in pdf_text[matched_token.start_char + len(matched_token.text)]) and (pdf_text[matched_token.start_char - 1] == "\n"):
                        print('matched topic found',matched_token)
                        paragraph = pdf_text[matched_token.start_char:]
                        for topicE in b:
                            topic_index = paragraph.find(topicE)
                            if topic_index != -1 and paragraph[topic_index + len(topicE)].startswith('\n'):
                                #print("Topic found after method " + topicM + ": " + topicE)
                                end_index = matched_token.start_char + topic_index
                                paragraph = pdf_text[matched_token.start_char:end_index]


                '''for topicM in a:
                    index = pdf_text.find(topicM)
                    print(index)
                    if index != -1 and pdf_text[index+len(topicM)].startswith('\n'):
                        print("Method found: " + topicM)
                        method_index = index + len(topicM)
                        paragraph = pdf_text[method_index:]
                        for topicE in b:
                            topic_index = paragraph.find(topicE)
                            if topic_index != -1 and paragraph[topic_index + len(topicE)].startswith('\n'):
                                print("Topic found after method " + topicM + ": " + topicE)
                                end_index = method_index + topic_index
                                paragraph = pdf_text[method_index:end_index]

                        print(f"The word '{topicM}' was found in the PDF file.")
                    else:
                        print(f"The word '{topicM}' was not found in the PDF file.")'''

        except PDFSyntaxError:
            print(f'Error parsing PDF file : Invalid or corrupted PDF file.')

        return paragraph
    '''def test(p):
        #print('check 8.2=================================================')
        pdf_path = 'fetched_pdfs/30568721.pdf'
        text = extract_text(pdf_path)
        methods_text = re.search(r'Methodology(.*?)Results', text, re.DOTALL)
        print(methods_text.group(1))
        #print('check 8.3===============================================')
    def method_text(p):
        print('check 7====================================================================')
        print('the value of p is ', p)
        output_string = StringIO()
        # Load the spacy model and create the matcher with the patterns
        nlp = spacy.load('en_core_sci_lg')
        matcher = Matcher(nlp.vocab)
        method_pattern = [{"LOWER": "methods"}, {"OP": "?"}]
        material_pattern = [{"LOWER": "materials"}, {"OP": "?"}]
        mm_pattern = [{"LOWER": "methods"}, {"LOWER": "and"}, {"LOWER": "materials"}]
        methodology_pattern = [{"LOWER": "methodology"}]
        am_pattern = [{"LOWER": "materials"}, {"LOWER": "and"}, {"LOWER": "methods"}]
        m_pattern = [{"LOWER": "material"}, {"LOWER": "and"}, {"LOWER": "method"}]
        ms_pattern = [{"LOWER": "materials"}, {"LOWER": "and"}, {"LOWER": "methods"}]
        pattern_list = [method_pattern, material_pattern, mm_pattern, methodology_pattern, am_pattern, m_pattern,
                        ms_pattern]
        for pattern in pattern_list:
            matcher.add("MaterialMethods", [pattern])
        try:
            with open('fetched_pdfs/' + p, 'rb') as file:
                # Create a PDF parser object
                parser = PDFParser(file)
                # Create a PDF document object
                document = PDFDocument(parser)
                # Get the outlines
                outlines = document.get_outlines()
                # Find the level 1 outline item with the material/methods pattern
                material_methods_outline = None
                for level, title, dest, a, se in outlines:
                    if level == 1:
                        doc = nlp(title.lower())
                        matches = matcher(doc)
                        if matches:
                            material_methods_outline = (level, title, dest, a, se)
                            break
                # Extract the text until the next level 1 outline item
                if material_methods_outline is not None:
                    _, material_methods_title, material_methods_dest, _, _ = material_methods_outline
                    manager = PDFResourceManager()
                    converter = TextConverter(manager, output_string, laparams=None)
                    interpreter = PDFPageInterpreter(manager, converter)

                    for page in PDFPage.get_pages(file):
                        interpreter.process_page(page)
                        text = output_string.getvalue()
                        if material_methods_title in text:
                            text = text.split(material_methods_title)[-1]
                            output_string = StringIO(text)
                        elif '\n1 ' in text:
                            # Found another level 1 outline item, stop extracting
                            break
                        elif not text:
                            # No more pages, stop extracting
                            break
                    # Print the extracted text
                    #print(output_string.getvalue())

        except PDFSyntaxError:
            print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return (output_string.getvalue())'''

    def data_text(p):
        a = ['Data Availability', 'DATA ACCESSIBILITY','Supplementary Information','DATA ARCHIVING', 'Additional files','Supporting Information','Additional material','Supplementary Data', 'Associated Data', 'Supplementary Materials', 'Data Availability Statement']  # add more topics as needed
        b = ['Acknowledgments','Author Contributions','Abbreviations','Publisher’s Note','References']
        paragraph = ''
        try:
            pdf_text = extract_text("fetched_pdfs/" + p)
            for topicM in a:
                index = pdf_text.lower().find(topicM.lower())  # convert to lowercase and ignore case
                #index = pdf_text.find(topicM)
                print(index)
                if index != -1 and pdf_text[index + len(topicM)].startswith('\n') and pdf_text[index - 1].startswith('\n'):
                    print("check 00 ==============================================================================data found: " + topicM)
                    method_index = index + len(topicM)
                    paragraph = pdf_text[method_index:]
                    for topicE in b:
                        topic_index = paragraph.lower().find(topicE.lower())
                        if topic_index != -1 and paragraph[topic_index + len(topicE)].startswith('\n'):
                            print("Topic found after data " + topicM + ": " + topicE)
                            end_index = method_index + topic_index
                            paragraph = pdf_text[method_index:end_index]

                        print(f"The word '{topicM}' was found in the PDF file.")
                else:
                    print(f"The word '{topicM}' was not found in the PDF file.")
        except PDFSyntaxError:
            print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return (paragraph)

