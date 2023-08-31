from . import credentials

def method():
    

    service = build("docs", "v1", credentials=creds)

    cover_letter = service.documents()