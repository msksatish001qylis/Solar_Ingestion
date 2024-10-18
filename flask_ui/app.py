from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Defining Solr core URL
SOLR_URL = "http://localhost:8983/solr/techproducts/select"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # Define the parameters for Solr query, including highlighting
    params = {
        'q': query,
        'hl': 'true',              # Enable highlighting
        'hl.fl': '*',              # Highlight all fields or specify a field
        'hl.simple.pre': '<b>',     # Start of highlight tag
        'hl.simple.post': '</b>'    # End of highlight tag
    }
    # Send the request to Solr
    response = requests.get(SOLR_URL, params=params)
    
    if response.status_code == 200:
        results = response.json().get('response', {}).get('docs', [])
        highlights = response.json().get('highlighting', {})  # Get the highlighted snippets
        return render_template('results.html', query=query, results=results, highlights=highlights)
    else:
        return "Error querying Solr"

if __name__ == '__main__':
    app.run(debug=True)
