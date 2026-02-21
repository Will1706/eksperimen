import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def search_mentions(query):
    # Menggunakan Social Searcher API (Gratis dengan limit) atau Google Search
    # Di sini kita gunakan simulasi pencarian spesifik konten (Dorking)
    search_targets = {
        "Reddit (Komentar/Post)": f"https://www.google.com/search?q=site:reddit.com+%22{query}%22",
        "Youtube (Video/Komentar)": f"https://www.google.com/search?q=site:youtube.com+%22{query}%22",
        "Twitter/X Mentions": f"https://twitter.com/search?q=%22{query}%22&f=live",
        "Facebook Public Post": f"https://www.facebook.com/search/top/?q={query}",
        "Forum Umum": f"https://www.google.com/search?q=intext:%22{query}%22+forum+OR+board"
    }
    
    results = []
    for platform, url in search_targets.items():
        # Karena kita tidak bisa 'scrape' komentar secara langsung tanpa API resmi tiap platform,
        # Kita memberikan tautan pencarian dalam (Deep Link) yang sudah terfilter.
        results.append({"platform": platform, "url": url})
    
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    profile_results = []
    mention_results = []
    query = ""
    
    if request.method == "POST":
        query = request.form.get("username")
        # Fungsi lama untuk cek profil (lihat kode sebelumnya)
        # profile_results = check_username(query) 
        
        # Fungsi baru untuk cek komentar/sebutan
        mention_results = search_mentions(query)
        
    return render_template("index.html", mention_results=mention_results, query=query)

if __name__ == "__main__":
    app.run(debug=True)