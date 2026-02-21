import customtkinter as ctk
from pygame import mixer
import os
from tkinter import filedialog, messagebox

# Pengaturan tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MusicPlayerPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Jendela Utama ---
        self.title("Python Modern Music Player 2026")
        self.geometry("900x500")

        # Inisialisasi Audio
        mixer.init()
        self.playlist = []
        self.current_index = 0
        self.is_playing = False

        # --- Layout Grid ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Playlist) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.label_sidebar = ctk.CTkLabel(self.sidebar, text="MY PLAYLIST", font=ctk.CTkFont(size=18, weight="bold"))
        self.label_sidebar.pack(pady=20)

        self.song_listbox = ctk.CTkTextbox(self.sidebar, width=220, height=300, font=("Consolas", 12))
        self.song_listbox.pack(padx=10, pady=5)
        self.song_listbox.configure(state="disabled")

        self.btn_add = ctk.CTkButton(self.sidebar, text="Tambah Lagu (Bulk)", command=self.add_songs)
        self.btn_add.pack(pady=10)

        # --- MAIN CONTENT (Controls) ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Nama Lagu
        self.song_label = ctk.CTkLabel(self.content_frame, text="Pilih lagu untuk memulai", font=ctk.CTkFont(size=22, weight="bold"), wraplength=400)
        self.song_label.pack(pady=(50, 10))

        # Visualizer Sederhana (Placeholder)
        self.vis_label = ctk.CTkLabel(self.content_frame, text="▂ ▃ ▅ ▆ █ ▆ ▅ ▃ ▂", text_color="#1DB954", font=("Arial", 24))
        self.vis_label.pack(pady=10)

        # Progress Bar (Fitur 2)
        self.progress_slider = ctk.CTkSlider(self.content_frame, from_=0, to=100, width=400)
        self.progress_slider.pack(pady=20)
        self.progress_slider.set(0)

        # Tombol Navigasi (Fitur 3 & 4)
        self.controls_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.controls_frame.pack(pady=10)

        self.btn_prev = ctk.CTkButton(self.controls_frame, text="⏮", width=60, font=("Arial", 20), command=self.prev_song)
        self.btn_prev.grid(row=0, column=0, padx=10)

        self.btn_play = ctk.CTkButton(self.controls_frame, text="▶ PLAY", width=120, font=("Arial", 16, "bold"), fg_color="#1DB954", hover_color="#18a34a", command=self.toggle_music)
        self.btn_play.grid(row=0, column=1, padx=10)

        self.btn_next = ctk.CTkButton(self.controls_frame, text="⏭", width=60, font=("Arial", 20), command=self.next_song)
        self.btn_next.grid(row=0, column=2, padx=10)

        # Volume (Fitur 4)
        self.vol_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.vol_frame.pack(pady=30)
        
        self.vol_label = ctk.CTkLabel(self.vol_frame, text="Vol 🔊")
        self.vol_label.grid(row=0, column=0, padx=10)
        
        self.vol_slider = ctk.CTkSlider(self.vol_frame, from_=0, to=1, width=150, command=self.change_volume)
        self.vol_slider.grid(row=0, column=1)
        self.vol_slider.set(0.7)

    # --- LOGIKA PROGRAM ---

    def add_songs(self):
        # Fitur: Tambah banyak lagu sekaligus
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if files:
            for f in files:
                if f not in self.playlist:
                    self.playlist.append(f)
            self.update_playlist_view()
            messagebox.showinfo("Berhasil", f"Ditambahkan {len(files)} lagu ke daftar.")

    def update_playlist_view(self):
        self.song_listbox.configure(state="normal")
        self.song_listbox.delete("0.0", "end")
        for i, path in enumerate(self.playlist):
            indicator = ">>> " if i == self.current_index and self.is_playing else "    "
            self.song_listbox.insert("end", f"{indicator}{os.path.basename(path)}\n")
        self.song_listbox.configure(state="disabled")

    def play_selected(self):
        if self.playlist:
            mixer.music.load(self.playlist[self.current_index])
            mixer.music.play()
            self.is_playing = True
            self.btn_play.configure(text="⏸ PAUSE")
            self.song_label.configure(text=os.path.basename(self.playlist[self.current_index]))
            self.update_playlist_view()
            self.update_progress()

    def toggle_music(self):
        if not self.playlist:
            self.add_songs()
            return
        
        if not self.is_playing:
            self.play_selected()
        else:
            if mixer.music.get_busy():
                mixer.music.pause()
                self.is_playing = False
                self.btn_play.configure(text="▶ RESUME")
            else:
                mixer.music.unpause()
                self.is_playing = True
                self.btn_play.configure(text="⏸ PAUSE")

    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_selected()

    def prev_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_selected()

    def change_volume(self, value):
        mixer.music.set_volume(value)

    def update_progress(self):
        if self.is_playing and mixer.music.get_busy():
            # Logika progress sederhana
            val = self.progress_slider.get()
            if val < 100:
                self.progress_slider.set(val + 0.2) # Kecepatan simulasi
            self.after(1000, self.update_progress)

if __name__ == "__main__":
    app = MusicPlayerPro()
    app.mainloop()