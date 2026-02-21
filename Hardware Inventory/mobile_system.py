import customtkinter as ctk
from datetime import datetime
import cv2
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")

class PyPhoneOSV2(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PyPhone Pro 2026")
        self.geometry("360x680")
        self.resizable(False, False)

        # State management
        self.is_locked = True
        self.camera_running = False
        
        # --- UI Tetap (Status Bar) ---
        self.status_bar = ctk.CTkFrame(self, height=30, fg_color="#1a1a1a", corner_radius=0)
        self.status_bar.pack(side="top", fill="x")
        
        self.clock_status = ctk.CTkLabel(self.status_bar, text="", font=("Arial", 12))
        self.clock_status.pack(side="right", padx=10)
        
        self.signal_label = ctk.CTkLabel(self.status_bar, text="📶 5G  🔋 95%", font=("Arial", 10))
        self.signal_label.pack(side="left", padx=10)

        # Container Utama (Layar)
        self.screen = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.screen.pack(expand=True, fill="both")

        self.show_lock_screen()
        self.update_system_clock()

    def clear_screen(self):
        self.camera_running = False # Stop kamera jika pindah layar
        for widget in self.screen.winfo_children():
            widget.destroy()

    # --- 1. LOCK SCREEN & NOTIFIKASI ---
    def show_lock_screen(self):
        self.clear_screen()
        
        # Jam Besar
        self.lock_time = ctk.CTkLabel(self.screen, text="", font=("Arial", 50, "bold"))
        self.lock_time.pack(pady=(80, 5))
        
        # Fitur: Notifikasi
        notif_card = ctk.CTkFrame(self.screen, fg_color="#333333", width=300, height=80)
        notif_card.pack(pady=20)
        notif_card.pack_propagate(False)
        
        ctk.CTkLabel(notif_card, text="💬 WhatsApp", font=("Arial", 11, "bold"), text_color="#2ecc71").pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkLabel(notif_card, text="Budi: P, besok mabar gak?", font=("Arial", 12)).pack(anchor="w", padx=10)

        unlock_btn = ctk.CTkButton(self.screen, text="🔓 UNLOCK", command=self.show_home_screen, 
                                   fg_color="#1DB954", corner_radius=20)
        unlock_btn.pack(side="bottom", pady=60)

    # --- 2. HOME SCREEN ---
    def show_home_screen(self):
        self.clear_screen()
        
        grid = ctk.CTkFrame(self.screen, fg_color="transparent")
        grid.pack(expand=True, fill="both", padx=20, pady=40)

        apps = [
            ("📸 Camera", "#e74c3c", self.show_camera_app),
            ("💬 SMS", "#3498db", self.show_sms_app),
            ("🔢 Calc", "#f1c40f", self.show_calc_app),
            ("🔒 Lock", "#95a5a6", self.show_lock_screen)
        ]

        r, c = 0, 0
        for name, color, cmd in apps:
            btn = ctk.CTkButton(grid, text=name, fg_color=color, width=120, height=120, 
                                corner_radius=20, font=("Arial", 14, "bold"), command=cmd)
            btn.grid(row=r, column=c, padx=15, pady=15)
            c += 1
            if c > 1: c = 0; r += 1

    # --- 3. APLIKASI KAMERA (Fitur Baru) ---
    def show_camera_app(self):
        self.clear_screen()
        self.camera_running = True
        
        self.cam_label = ctk.CTkLabel(self.screen, text="")
        self.cam_label.pack(fill="both", expand=True)

        self.cap = cv2.VideoCapture(0)
        
        btn_capture = ctk.CTkButton(self.screen, text="◯", width=60, height=60, corner_radius=30,
                                    fg_color="white", text_color="black", command=self.show_home_screen)
        btn_capture.place(relx=0.5, rely=0.9, anchor="center")
        
        self.update_camera_frame()

    def update_camera_frame(self):
        if self.camera_running:
            ret, frame = self.cap.read()
            if ret:
                # Resize agar pas dengan layar HP
                frame = cv2.flip(frame, 1)
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(img)
                img = img.resize((360, 500))
                imgtk = ImageTk.PhotoImage(image=img)
                self.cam_label.imgtk = imgtk
                self.cam_label.configure(image=imgtk)
            self.after(10, self.update_camera_frame)
        else:
            self.cap.release()

    # --- FITUR LAIN (SMS & CALC) ---
    def show_sms_app(self):
        self.clear_screen()
        ctk.CTkLabel(self.screen, text="Messages", font=("Arial", 20, "bold")).pack(pady=20)
        # (Logika SMS sama seperti sebelumnya...)
        ctk.CTkButton(self.screen, text="⬅ Back", command=self.show_home_screen).pack(side="bottom", pady=20)

    def show_calc_app(self):
        self.clear_screen()
        # (Logika Kalkulator sama seperti sebelumnya...)
        ctk.CTkButton(self.screen, text="⬅ Back", command=self.show_home_screen).pack(side="bottom", pady=20)

    # --- SYSTEM ---
    def update_system_clock(self):
        now = datetime.now().strftime("%H:%M")
        self.clock_status.configure(text=now)
        if hasattr(self, 'lock_time'):
            try: self.lock_time.configure(text=now)
            except: pass
        self.after(1000, self.update_system_clock)

if __name__ == "__main__":
    app = PyPhoneOSV2()
    app.mainloop()