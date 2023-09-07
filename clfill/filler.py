from . import credentials
from googleapiclient.discovery import build
import json

##TODO 'documentId' environmental var?
# when should it be set up? 

def method():
    ##TODO write logic for document editor functions

    service = build("docs", "v1", credentials=credentials)
                                                         
    # cl_template contains the Document we will make a copy of / TODO Template Id
    cl_template = service.documents().get(documentId=INSERT_TEMPLATE_ID_HERE).execute()
    print(cl_template.body)