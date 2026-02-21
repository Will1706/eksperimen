import requests

def check_username(username):
    # Daftar platform dan struktur URL-nya
    platforms = {
        "Instagram": f"https://www.instagram.com/{username}/",
        "GitHub": f"https://api.github.com/users/{username}",
        "Twitter (X)": f"https://twitter.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
    }

    print(f"--- Mencari username: {username} ---\n")

    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            
            # Logika umum: Jika status_code 200, berarti akun ditemukan
            if response.status_code == 200:
                print(f"[✅] {platform}: Ditemukan! -> {url}")
            elif response.status_code == 404:
                print(f"[❌] {platform}: Tidak Tersedia / Tidak Ada.")
            else:
                print(f"[?] {platform}: Status tidak menentu ({response.status_code})")
        except requests.exceptions.RequestException:
            print(f"[!] {platform}: Gagal terhubung (koneksi bermasalah).")

# Jalankan fungsi
user_input = input("Masukkan username yang ingin dicari: ")
check_username(user_input)