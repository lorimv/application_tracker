from . import credentials
from googleapiclient.discovery import build
import json

##TODO 'documentId' environmental var?
# TODO when should it be set up? 

def method():
    ##TODO write logic for document editor functions

    service = build("docs", "v1", credentials=credentials)
                                                         
    # cl_template contains the Document we will make a copy of / TODO Template Id
    cl_template = service.documents().get(documentId=INSERT_TEMPLATE_ID_HERE).execute()

    # cl_filled is the new Document, to be filled with contents of cl_template (excluding template's Id)
    cl_filled = service.documents().create()