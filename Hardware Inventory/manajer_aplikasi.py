import customtkinter as ctk
import os
import shutil
import time
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox

class ProOrganizer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Si Tukang Rapih PRO")
        self.geometry("750x650")
        ctk.set_appearance_mode("dark")

        # Konfigurasi & State
        self.history = []  # Untuk fitur Undo
        self.static_map = {
            'Gambar': ['.jpg', '.jpeg', '.png', '.gif'],
            'Dokumen': ['.pdf', '.docx', '.txt', '.xlsx'],
            'Koding': ['.py', '.js', '.html', '.cpp'],
            'Arsip': ['.zip', '.rar'],
            'Video': ['.mp4', '.mkv']
        }

        # --- UI ELEMENTS ---
        self.label_title = ctk.CTkLabel(self, text="🚀 Desktop Organizer Pro", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=15)

        # Frame Atas (Folder & Filter)
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=10, padx=20, fill="x")

        self.path_entry = ctk.CTkEntry(self.top_frame, placeholder_text="Pilih folder sumber...")
        self.path_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.btn_browse = ctk.CTkButton(self.top_frame, text="Pilih Folder", width=100, command=self.browse)
        self.btn_browse.grid(row=0, column=1, padx=10)

        self.date_filter = ctk.CTkCheckBox(self.top_frame, text="Hanya file > 30 hari")
        self.date_filter.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.top_frame.grid_columnconfigure(0, weight=1)

        # Progress Bar
        self.progress = ctk.CTkProgressBar(self, width=600)
        self.progress.set(0)
        self.progress.pack(pady=10)

        # Log Textbox
        self.log_area = ctk.CTkTextbox(self, height=250, font=("Consolas", 12))
        self.log_area.pack(pady=10, padx=20, fill="both", expand=True)

        # Button Frame
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.btn_run = ctk.CTkButton(self.btn_frame, text="JALANKAN", fg_color="green", command=self.run_organizer)
        self.btn_run.grid(row=0, column=0, padx=10)

        self.btn_undo = ctk.CTkButton(self.btn_frame, text="UNDO", fg_color="orange", command=self.undo_action)
        self.btn_undo.grid(row=0, column=1, padx=10)

        self.btn_open = ctk.CTkButton(self.btn_frame, text="BUKA FOLDER", command=self.open_folder)
        self.btn_open.grid(row=0, column=2, padx=10)

    # --- LOGIC ---

    def browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, folder)

    def open_folder(self):
        path = self.path_entry.get()
        if os.path.exists(path):
            os.startfile(path)

    def run_organizer(self):
        path = self.path_entry.get()
        if not path or not os.path.exists(path):
            return messagebox.showerror("Error", "Folder tidak valid!")

        self.log_area.delete("1.0", "end")
        self.history = [] # Reset history per sesi
        
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        total_files = len(files)
        
        if total_files == 0:
            self.log_area.insert("end", "Folder kosong.\n")
            return

        moved_count = 0
        limit_date = datetime.now() - timedelta(days=30)

        for i, file in enumerate(files):
            if file == os.path.basename(__file__): continue
            
            file_path = os.path.join(path, file)
            
            # Fitur Filter Tanggal
            if self.date_filter.get():
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime > limit_date:
                    continue

            ext = os.path.splitext(file)[1].lower()
            for folder, exts in self.static_map.items():
                if ext in exts:
                    target_dir = os.path.join(path, folder)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    new_path = os.path.join(target_dir, file)
                    shutil.move(file_path, new_path)
                    
                    # Simpan ke history untuk UNDO
                    self.history.append((new_path, file_path))
                    
                    self.log_area.insert("end", f"✅ {file} -> {folder}\n")
                    moved_count += 1
                    break
            
            # Update Progress Bar
            self.progress.set((i + 1) / total_files)
            self.update_idletasks()

        self.log_area.insert("end", f"\n--- Selesai! {moved_count} file dipindahkan ---")
        messagebox.showinfo("Sukses", f"Berhasil merapikan {moved_count} file.")

    def undo_action(self):
        if not self.history:
            return messagebox.showwarning("Undo", "Tidak ada riwayat pemindahan untuk dibatalkan.")
        
        for current_path, original_path in self.history:
            if os.path.exists(current_path):
                shutil.move(current_path, original_path)
        
        self.history = []
        self.log_area.insert("end", "\n🔄 Undo berhasil! Semua file dikembalikan.\n")
        self.progress.set(0)
        messagebox.showinfo("Undo", "Semua file telah dikembalikan ke posisi semula.")

if __name__ == "__main__":
    app = ProOrganizer()
    app.mainloop()