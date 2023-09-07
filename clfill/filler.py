from . import credentials

def method():
    ##TODO write logic for document editor functions

    service = build("docs", "v1", credentials=creds)

    cover_letter = service.documents()