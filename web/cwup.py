from googleapiclient.http import MediaFileUpload 
from googleapiclient.discovery import build 
from google.oauth2 import service_account 
import os 
import argparse 
import pickle 
import magic 
 
parser = argparse.ArgumentParser() 
parser.add_argument('-f', "--file") 
args = parser.parse_args() 
 
file = args.file 
 
def get_gdrive_service(): 
 creds = None 
 SCOPES = ['https://www.googleapis.com/auth/drive'] 
 try: 
  creds = service_account.Credentials.from_service_account_file('web/1.json') 
 except Exception: 
  if os.path.exists('token.pickle'): 
   with open('token.pickle', 'rb') as token: 
    creds = pickle.load(token) 
  
 
 return build('drive', 'v3', credentials=creds) 
 
service = get_gdrive_service() 
 
folder_id = '0dCt1eG1o8yXecVI6Wkg0nDdJm-rb3nf' 
file_name = f"{file}" 
file_path = f'/usr/src/app/{file_name}' 
 
def get_mime_type(file_path): 
 mime = magic.Magic(mime=True) 
 mime_type = mime.from_file(file_path) 
 mime_type = mime_type or "text/plain" 
 return mime_type 
 
mime_type = get_mime_type(file_path) 
 
file_metadata = { 
 'name': file_name, 
 'description': 'π-TEK', 
 'mimeType': mime_type, 
 'parents': [folder_id] 
} 
 
media = MediaFileUpload(file_name, resumable=True, mimetype=mime_type, chunksize=70 * 1024 * 1024) 
file = service.files().create(supportsTeamDrives=True, 
         body=file_metadata, 
         media_body=media, 
         fields='id').execute() 
print ('https://drive.google.com/open?id=%s' % file.get('id'))
