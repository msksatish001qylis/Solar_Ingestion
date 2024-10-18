import os
import requests

# Define your Solr core URL
SOLR_URL = "http://localhost:8983/solr/techproducts/update/extract?commit=true"

# Specify the directory containing your PDF files
PDF_DIRECTORY = r"C:\Users\Admin\Downloads\qylis_ld\slr_ingest\solr-8.11.4\example\exampledocs"

# Function to upload PDF files to Solr
def upload_pdf_to_solr(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            files = {'myfile': (os.path.basename(pdf_path), pdf_file)}
            # Add a unique ID for the document 
            data = {'literal.id': os.path.basename(pdf_path)}  # Use the file name as ID
            response = requests.post(SOLR_URL, files=files, data=data)
            
            if response.status_code == 200:
                print(f"Successfully indexed: {pdf_path}")
            else:
                print(f"Failed to index {pdf_path}: {response.content}")
    except Exception as e:
        print(f"Error uploading {pdf_path}: {e}")

# Iterate over all files in the directory
for filename in os.listdir(PDF_DIRECTORY):
    if filename.endswith('.pdf'):
        pdf_file_path = os.path.join(PDF_DIRECTORY, filename)
        upload_pdf_to_solr(pdf_file_path)

print("All PDF files have been processed.")
