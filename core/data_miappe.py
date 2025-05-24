import re

from core.get_outline import GetOutline


class MData:
   def find_all_data(pdfFiles):
      data_miappe = []
      print('Check 1 data ',pdfFiles)
      for p in pdfFiles:
         findData = GetOutline.data_text(p)
         print('check 2 =====================================================data ')
         #print(findData)
         print('Check 2.1 =======================================================')
         findLink = MData.findLink(findData)
         findFileDesc = MData.findFileDesc(findData)
         findVersion = MData.findVersion(findData)
         if findLink or findFileDesc or findVersion:
            data_miappe.append({'PMID_data': p, 'link': findLink, 'desc': findFileDesc, 'ver': findVersion})

      return data_miappe


   def findLink(findData):
      print('check 3 into link::::::::::::::::::::::::::::::::::::::::::')
      print(findData)
      urls = ""
      url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),\n]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

      urls = re.findall(url_pattern, findData)
      # Remove newline characters from URLs
      urls = [url.replace('\n', '') for url in urls]
      print('chekc 4 =================================================',urls)
      return urls


   def findFileDesc(findData):
      desc = ''
      return desc


   def findVersion(findData):
      ver = ''
      return ver




