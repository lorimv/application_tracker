#import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

def query():
    print("Hola hola")

    print("Let's start by getting the name of the company: ")
    company_l = input()

    print("yeah aight now the shortened company name: ")
    company_s = input()

    print("Position name (full)?")
    position_l = input()

    print("Now tha shortened position name")
    position_s = input()

def method():
    creds = service_account.Credentials.from_service_account_file('creds.json', scopes=['https://www.googleapis.com/auth/documents'])

    service = build("docs", "v1", credentials=creds)

    cover_letter = service.documents()