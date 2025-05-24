import os
import zipfile


from flask import send_file, jsonify, make_response
from flask import Flask, render_template, request
from core.allinone import ALlSearch

from core.miappe_data_output import MiappeData
from core.isa_tab_data import IsaTab
from core.dbcon import dbcon
from core.extractPdf import ExtPDF
from core.charts import Charts
import json

# ------------------------------------------------------------------------------
# App Initialization & Configuration
# ------------------------------------------------------------------------------
app = Flask(__name__, static_folder='static')



# Set a secret key for session and CSRF protection (use os.urandom for security)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TEMPLATES'] = 'templates'
app.config['UPLOAD_FOLDER'] = '/var/www/html/InterText/uploads'
app.config['STATIC_FOLDER'] = '/var/www/html/InterText/static'
DOWNLOAD_FOLDER = 'downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Ensure static folder exists
if not os.path.exists(app.config['STATIC_FOLDER']):
    os.makedirs(app.config['STATIC_FOLDER'])



# ------------------------------------------------------------------------------
# App Initialization & Configuration
# ------------------------------------------------------------------------------



@app.route('/')
def my_form():
    user_id = request.cookies.get('user_id')  # Get the user ID from the cookie or generate a new one
    if user_id is None:
        user_id = os.urandom(16).hex()
        #create_user_folder(user_id)  # Create folder for new user
    response = make_response("Task complete")
    response.set_cookie('user_id', user_id)
    return render_template('home.html')
    
    
    
@app.route('/add_new_keyword/',methods = ['POST', 'GET'])
def add_new_keyword():
      global user_folder  # use the global variable
      new_key = request.form['new_keyword']
      dbval=dbcon.add_new_data(new_key)
      print("this is db insert values")
      print(dbval)
      msg = "Keyword is added"
      with open('miappe_data/miappe.json') as f:
       miappe_data = json.load(f)
      with open('miappe_data/isa_tab.json') as f:
       miappe_isa = json.load(f)
      return render_template('data.html', data=dbval,msg=msg,miappe_data=miappe_data,miappe_data_isa=miappe_isa)
      
      
      
      
      
      
      
      
      
      
@app.route('/analyze')
def analyze_page():
      dictvalues = ExtPDF.totalPubBasedOnDate('date')
      chart_data_json = Charts.createDateChart(dictvalues)
      pubname = ExtPDF.totalPubBasedOnPubname('pubname')
      chart_pubname = Charts.createPubnameChart(pubname)
      #return render_template('graph.html')
      print("file in the analyse page")
      return render_template('analyze_page.html', chart_data_json=chart_data_json,pubname_data=chart_pubname)
      
      
      
      
      
      
      
      
      
      
      
      
      

@app.route("/back/", methods=['POST'])
def home_page():
   return render_template('home.html')
   
   
   
@app.route('/build')
def build_page():
  print('going to build page')
  return render_template('build.html')
  
 
  
@app.route('/data')
def data_page():
     msg = ""
     dbval = dbcon.selects(msg)
     print("this is db select values")
     print(dbval)
     with open('miappe_data/miappe.json') as f:
      miappe_data = json.load(f)
     with open('miappe_data/isa_tab.json') as f:
      miappe_isa = json.load(f)
     return render_template('data.html',data=dbval,msg=msg,miappe_data=miappe_data,miappe_data_isa=miappe_isa)
     
     
     
     
     
     
     
     
     
@app.route('/downloads')
def downloads():
    path = "miappe_output"
    dir_list = os.listdir(path)

    csv_files = []
    excel_files = []
    json_files = []
    pdf_files = []

    # Loop through each file in the list
    for file in dir_list:
        # Get the extension of the file
        extension = file.split('.')[-1].lower()

        # Categorize the file into the corresponding list based on its extension
        if extension == 'csv':
            csv_files.append(file)
        elif extension == 'xlsx' or extension == 'xls':
            excel_files.append(file)
        elif extension == 'json':
            json_files.append(file)
        elif extension == 'pdf':
            pdf_files.append(file)
    return render_template('downloads.html',csv = csv_files, excels = excel_files,jsons = json_files, pdfs = pdf_files)


@app.route('/downloadpdf/', methods=['POST'])
def downloadpdf():
      msg = "test"
      print('going to extract data for build')
      ALlSearch.write_to_pmf(msg)
      #PMFDownnload.downloadpdf('download pmf')
      os.system("python3 pdf_downloader.py -pmf PMF")
      files = ALlSearch.listFileWithTitle(msg)
      print('files from build is :')
      print(json.dumps(files, indent=4, ensure_ascii=False))
      return render_template('build.html',lists=files,siz1=len(files))
      
      
      
      
      
      
      
      
      
      
      
@app.route('/download_miappe/<extension>', methods=['POST', 'GET'])
def download_miappe(extension):
    print("=======================================",extension)
    try:
        file_path = "miappe_output/miappe_data_output.{}".format(extension)
        abs_file_path = os.path.abspath(file_path)
        print(abs_file_path)
        return send_file(abs_file_path, as_attachment=True)
    except Exception as e:
        return str(e)
        
        
        
        
        
        
        
        
@app.route('/data_results/<file_name>', methods=['POST', 'GET'])
def data_results(file_name):
    print("=======================================",file_name)
    try:
        file_path = "data_results/{}".format(file_name)
        abs_file_path = os.path.abspath(file_path)
        print(abs_file_path)
        return send_file(abs_file_path, as_attachment=True)
    except Exception as e:
        return str(e)
        
        
        
        
        
        
        
        
        
        
@app.route("/downloadpdffile/<file_id>", methods=['POST', 'GET'])
def download(file_id):
     try:
          file_path = "fetched_pdfs/{}".format(file_id)
          abs_file_path = os.path.abspath(file_path)
          print(abs_file_path)
          return send_file(abs_file_path, as_attachment=True)
     except Exception as e:
      return str(e)
      
      
      
      
      
      
      
@app.route("/download_all/<folder_name>", methods=['POST', 'GET'])
def download_all(folder_name):
    # specify the directory containing the files
    directory = os.path.abspath(folder_name)
    if not os.path.isdir(directory):
        return "Error: {} is not a valid directory".format(directory)

    # create a zip archive and add all files in the directory
    archive_name = "{}.zip".format(folder_name)
    archive = zipfile.ZipFile(archive_name, "w")
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        archive.write(file_path, filename)
    archive.close()

    # send the archive as a response
    return send_file(archive_name, as_attachment=True)


@app.route('/extract_pdf_data/', methods=['POST'])
#this method is called from data.html page to extract data from
# downloaded pdf files
def extract_pdf_data():
   msg = 'reading data'
   print('####### i m in pdf reader ############################')
   search_list_names = request.form.getlist('search_list_names')
   print(search_list_names)
   output  =  ExtPDF.findOutput(search_list_names)
   #values = ExtPDF.readPDFTitle(search_list_names)
   #values = ExtPDF.getDocumentInfo(msg)
   '''values1 = ExtPDF.getPubDate(msg)
   values2 = ExtPDF.readPDFTitle(msg)
   values3 = ExtPDF.getKeywords(msg)
   values4 = ExtPDF.getPubName(msg)
   values5 = ExtPDF.getAuthor(msg) 
   values6 = ExtPDF.pubdate(msg)
  '''
   forward_message = "Moving Forward..."
   # RGP.csvpaste(forward_message)
   #data = ExtPDF.readCSV(forward_message)
   #results = ExtPDF.getResult(search_list_names,data)
   #dt = ExtPDF.csvtojson(forward_message)
   #print('################################',dt)
   #print(data)
   #for miappe
   #with open('miappe_data/miappe.json') as f:
    #   miappe_data = json.load(f)

   #if all(item in miappe_data for item in search_list_names):
       # Do something when the condition is met
    #   print("All items in check_list are contained in JSON values.")
   #else:
       # Do something else when the condition is not met
    #   print("Not all items in check_list are contained in JSON values.")
     #  print("the data from resutls is ",results)
   data = ExtPDF.findOutput(search_list_names)
   print(data)
   #return render_template('downloads.html',data=results,siz1=len(results),msg=msg,miappe_data=miappe_data,location="datacsv")
   return render_template('keyword_output.html',rows = data,keywords = search_list_names)

@app.route("/extract_to_table/",  methods=['POST','GET'])
def extract_to_table():
    queries = request.args.get('Q')
    print(queries)
    data = ALlSearch.extract_result_to_table(queries)
    print(data)
    message = ''
    return render_template('extr_list.html',publications=data,siz1=len(data),message=message)
    
    
    
    
@app.route('/resultspapers', methods=['POST'])
def result():
    query = request.form['PlainText']
    if not query:
        return "Empty query"
    if "[Title]" in query:
        query = query.replace("[Title]", "")
        args = "[Title]"
    elif "[Title/Abstract]" in query:
        query = query.replace("[Title/Abstract]", "")
        args = "[Title/Abstract]"
    else:
        args = "[Title]"


    page = request.args.get('page', type=int)
    if page is None:
        page = 1
    retstart = request.form.get('retstart', type=int)
    if retstart is None:
        retstart = 0
    else:
        retstart = int(retstart)
    start = (page - 1) * 10
    end = start + 100
    id_list = ALlSearch.search_publications(query, retstart, end,args)['IdList']
    print("-----------------------",id_list)
    if not id_list:
        emsg = "Please enter title based search criteria."
        return render_template('errors.html',message=emsg)
    else:
        papers = ALlSearch.fetch_details(id_list)
        totalresults =ALlSearch.search_publications(query, retstart, end,args)['Count']
        print("=======================================",totalresults)
        return render_template('result.html', papers=papers, page=page, queries=query, retstart=retstart,
                           totalresults=totalresults)

@app.route('/datapaginate')
def data():
    # Get the page number from the request
    page = request.args.get('page', 1, type=int)

    # Get the data for the requested page
    data = get_data(page)

    # Return the data as JSON
    return jsonify(data)

def get_data(page):
    # Fetch the data for the requested page from the database or another source
    # Here we will just generate some fake data
    data = []
    for i in range((page - 1) * 10, page * 10):
        data.append({'id': i, 'name': f'Item {i}'})
        
        
        
   
    return data
    
    
    
    

@app.route('/search')
def search_page():
    return render_template('index.html')
    
    
    
    
    
    
    
    
    
    
    
    
    
    

@app.route('/searchresults')
def search_result():
    print('Printing from Extract menu')
    queries = request.args.get('Q')
    print('query is ',queries)
    if queries is None:
        message = 'Please search your queries first !!!'

    return render_template('extr_list.html',message=message)
    
    
    

@app.route('/miappefunction/', methods=['POST'])
def miappefunction():
    print('into miappe function')
    with open('miappe_data/miappe.json') as f:
        miappe_data = json.load(f)
    selected_checkboxes = {}
    for category, names in miappe_data.items():
        for name in names:
            if request.form.get(name):
                if category not in selected_checkboxes:
                    selected_checkboxes[category] = []
                selected_checkboxes[category].append(name)
    print('selected checkboxes are : ', selected_checkboxes)
    miappe_output = MiappeData.findEntity(selected_checkboxes)
    print(miappe_output)
    return render_template('miappe_output.html', miappe_output=miappe_output,checkboxes=selected_checkboxes)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
@app.route('/isafunction/', methods=['POST'])
def isafunction():
    print('into isa function')
    with open('miappe_data/isa_tab.json') as f:
        isa_data = json.load(f)
    selected_checkboxes = {}
    for category, names in isa_data.items():
        for name in names:
            if request.form.get(name):
                if category not in selected_checkboxes:
                    selected_checkboxes[category] = []
                selected_checkboxes[category].append(name)
    print('selected checkboxes are : ', selected_checkboxes)
    isa_output = IsaTab.findEntity(selected_checkboxes)
    print(isa_output)
    return render_template('isatab_output.html', miappe_output=isa_output,checkboxes=selected_checkboxes)



@app.route('/manual')
def manual():
    return render_template('manual.html')


@app.route('/information')
def information():
    return render_template('information.html')














@app.route('/run')
def run():
    finaltext = "pan genome analysis of rice and constructions"
    #Se = R1.getdata(finaltext)

    #SearchPub = R1.scrape_pubmed_publications(finaltext)

    return render_template('runhtml.html')


@app.route('/json')
def load_json():
    with open('papers.json') as json_file:
        data = json.load(json_file)
    print("check 22222")

    return render_template('json.html', data=data)



if __name__ == '__main__':
    app.run(host="127.1.1.19", port=7000)
















