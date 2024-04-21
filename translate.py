from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import requests
import os



load_dotenv()


SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = os.getenv.SERVICE_ACCOUNT_FILE 
DOCUMENT_ID = os.getenv.DOCUMENT_ID


def write():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('docs', 'v1', credentials=creds)

    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    # print('Title: {}'.format(document.get('title')))
    # print('Content:')
    for element in document.get('body').get('content'):
        if 'paragraph' in element:
            
            # This is where the transltion will be done
      
            url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

            payload = {
                "q": element.get('paragraph').get('elements')[0].get('textRun').get('content'),
                "target": "am",
                "source": "en"
            }
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "application/gzip",
                "X-RapidAPI-Key": "87b2b3cb55mshc57682867e63f95p1fc225jsn0f780eb36d90",
                "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
            }

            response = requests.post(url, data=payload, headers=headers)

            document = service.documents().get(documentId=DOCUMENT_ID).execute()


            # Find the index of the last paragraph in the document
            last_paragraph_index = find_last_paragraph_index(document)

            # Write the translated to the end of document
            new_content = [
                {
                    'insertText': {
                        'location': {
                            'index': last_paragraph_index-1
                        },
                        'text':response.json().get('data').get('translations')[0].get('translatedText')
                    }
                }
            ]
            result = service.documents().batchUpdate(
                documentId=DOCUMENT_ID, body={'requests': new_content}).execute()
            print('Document updated: {}'.format(result))

def find_last_paragraph_index(document):
    content = document.get('body').get('content')
    return content[-1].get('endIndex')



if __name__ == '__main__':
    write()
