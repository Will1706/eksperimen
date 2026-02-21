import requests

def search_person(name):
    api_key = "YOUR_GOOGLE_API_KEY"
    search_engine_id = "YOUR_CX_ID"
    url = f"https://www.googleapis.com/customsearch/v1?q={name}&key={api_key}&cx={search_engine_id}"
    
    response = requests.get(url)
    results = response.json()
    
    for item in results.get("items", []):
        print(f"Judul: {item['title']}")
        print(f"Link: {item['link']}\n")

# Contoh penggunaan
search_person("Budi Santoso")