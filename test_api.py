import requests
import json

url = 'http://127.0.0.1:5000/analyze'
files = {'resume': open('test_resume.docx', 'rb')}
data = {'job_description': 'Python developer, django, APIs'}

r = requests.post(url, files=files, data=data)
if 'Python' in r.text and 'Skills' in r.text:
    print("Success: API returned HTML with Python and Skills fields")
    print(r.text[:500]) # Print first 500 chars to verify
else:
    print("Failed")
