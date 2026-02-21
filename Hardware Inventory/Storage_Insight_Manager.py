import customtkinter as ctk
import os
import psutil
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkinter import filedialog, messagebox

class StorageManagerPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi Jendela Utama
        self.title("Storage Insight Manager Pro - Williyanto Adi")
        self.geometry("1100x850")
        ctk.set_appearance_mode("dark")

        # Data Mapping untuk Filter & Ikon
        self.filters = {
            "Semua": [],
            "Gambar": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
            "Video": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm"],
            "Dokumen": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
            "Arsip": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Koding": [".py", ".js", ".html", ".css", ".cpp", ".java", ".php"]
        }

        # Layout Utama
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR UI ---
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="📊 STORAGE ANALYZER", font=("Arial", 20, "bold")).pack(pady=30)

        filter_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        filter_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(filter_frame, text="Filter Jenis File:", font=("Arial", 12)).pack(anchor="w", padx=5)
        self.filter_var = ctk.StringVar(value="Semua")
        self.filter_menu = ctk.CTkOptionMenu(filter_frame, values=list(self.filters.keys()), variable=self.filter_var)
        self.filter_menu.pack(pady=10, fill="x")

        self.btn_scan = ctk.CTkButton(self.sidebar, text="Mulai Scan Folder", height=40,
                                     fg_color="#1f538d", hover_color="#14375e", 
                                     font=("Arial", 14, "bold"), command=self.start_scan_thread)
        self.btn_scan.pack(pady=20, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Ready", text_color="gray")
        self.status_label.pack(pady=5)

        # --- MAIN CONTENT AREA ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.tabview = ctk.CTkTabview(self.main_frame, segmented_button_selected_color="#1f538d")
        self.tabview.pack(fill="both", expand=True)
        self.tabview.add("Top Files (Terbesar)")
        self.tabview.add("Analisis Grafik")

        # --- FOOTER ---
        self.footer = ctk.CTkLabel(self, text="Williyanto Adi 2026", font=("Arial", 11), text_color="#555555")
        self.footer.grid(row=1, column=0, columnspan=2, pady=5)

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024: return f"{size:.2f} {unit}"
            size /= 1024

    def start_scan_thread(self):
        folder = filedialog.askdirectory()
        if not folder: return
        
        self.btn_scan.configure(state="disabled")
        self.status_label.configure(text="Scanning... ⏳", text_color="yellow")
        
        thread = threading.Thread(target=self.scan_logic, args=(folder,), daemon=True)
        thread.start()

    def scan_logic(self, folder):
        all_files_for_list = []
        stats = {cat: {"size": 0, "count": 0} for cat in self.filters.keys() if cat != "Semua"}
        stats["Lainnya"] = {"size": 0, "count": 0}

        try:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(path)
                        found_cat = False
                        for cat, exts in self.filters.items():
                            if cat == "Semua": continue
                            if ext in exts:
                                stats[cat]["size"] += file_size
                                stats[cat]["count"] += 1
                                found_cat = True
                                break
                        if not found_cat:
                            stats["Lainnya"]["size"] += file_size
                            stats["Lainnya"]["count"] += 1

                        user_filter = self.filter_var.get()
                        if user_filter == "Semua" or ext in self.filters[user_filter]:
                            all_files_for_list.append({'name': file, 'size': file_size, 'path': path})
                    except: continue

            top_large = sorted(all_files_for_list, key=lambda x: x['size'], reverse=True)[:25]
            self.after(0, lambda: self.update_ui(top_large, stats))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.after(0, lambda: self.btn_scan.configure(state="normal"))

    def update_ui(self, top_files, stats):
        tab_list = self.tabview.tab("Top Files (Terbesar)")
        for widget in tab_list.winfo_children(): widget.destroy()

        scroll_frame = ctk.CTkScrollableFrame(tab_list, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        if not top_files:
            ctk.CTkLabel(scroll_frame, text="Tidak ada file ditemukan.", font=("Arial", 14)).pack(pady=50)
        else:
            for item in top_files:
                self.create_file_card(scroll_frame, item)

        self.show_category_chart(stats)
        self.btn_scan.configure(state="normal")
        self.status_label.configure(text="Scan Selesai ✅", text_color="green")

    def create_file_card(self, master, item):
        ext = os.path.splitext(item['name'])[1].lower()
        icon, color = "📄", "#ABB2B9"
        if ext in self.filters["Gambar"]: icon, color = "📷", "#3498db"
        elif ext in self.filters["Video"]: icon, color = "🎥", "#e74c3c"
        elif ext in self.filters["Dokumen"]: icon, color = "📁", "#2ecc71"
        elif ext in self.filters["Arsip"]: icon, color = "📦", "#f1c40f"
        elif ext in self.filters["Koding"]: icon, color = "💻", "#9b59b6"

        card = ctk.CTkFrame(master, height=85, fg_color="#212121", border_width=1, border_color="#333333")
        card.pack(pady=6, padx=10, fill="x")
        card.grid_columnconfigure(1, weight=1)

        lbl_icon = ctk.CTkLabel(card, text=icon, font=("Arial", 28))
        lbl_icon.grid(row=0, column=0, rowspan=2, padx=20, pady=10)

        name_label = ctk.CTkLabel(card, text=item['name'], font=("Arial", 14, "bold"), anchor="w")
        name_label.grid(row=0, column=1, sticky="ew", pady=(10, 0))

        path_label = ctk.CTkLabel(card, text=item['path'], font=("Arial", 11), text_color="#777777", anchor="w")
        path_label.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.grid(row=0, column=2, rowspan=2, padx=20)

        size_label = ctk.CTkLabel(action_frame, text=self.format_size(item['size']), font=("Consolas", 13, "bold"), text_color=color)
        size_label.pack()

        btn_open = ctk.CTkButton(action_frame, text="Lihat Lokasi", width=90, height=24, font=("Arial", 11), fg_color="#333333", hover_color="#444444", command=lambda p=item['path']: self.open_folder(p))
        btn_open.pack(pady=5)

    def open_folder(self, path):
        folder = os.path.dirname(path)
        if os.path.exists(folder):
            os.startfile(folder)

    def show_category_chart(self, stats):
        tab_graph = self.tabview.tab("Analisis Grafik")
        for widget in tab_graph.winfo_children(): widget.destroy()

        labels, sizes = [], []
        for cat, data in stats.items():
            if data["count"] > 0:
                labels.append(f"{cat}\n({data['count']} file)")
                sizes.append(data["size"])

        if not sizes: return

        fig, ax = plt.subplots(figsize=(7, 6), dpi=100)
        fig.patch.set_facecolor('#1a1a1a')
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6', '#1abc9c', '#95a5a6']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'color': "w", 'fontsize': 10}, pctdistance=0.85, wedgeprops={'edgecolor': '#1a1a1a'})

        centre_circle = plt.Circle((0,0), 0.70, fc='#1a1a1a')
        fig.gca().add_artist(centre_circle)
        ax.set_title("Distribusi Penggunaan Ruang", color="w", pad=20, fontdict={'fontsize': 15, 'weight': 'bold'})
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=tab_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

if __name__ == "__main__":
    app = StorageManagerPro()
    app.mainloop()