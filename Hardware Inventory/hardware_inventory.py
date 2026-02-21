import customtkinter as ctk
import wmi

class DeviceMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PC Hardware Inventory")
        self.geometry("700x500")
        ctk.set_appearance_mode("dark")

        # Inisialisasi WMI (Windows Management Instrumentation)
        self.w = wmi.WMI()

        # UI Elements
        self.label_title = ctk.CTkLabel(self, text="Daftar Perangkat Terdeteksi", font=("Arial", 20, "bold"))
        self.label_title.pack(pady=20)

        # TextBox untuk menampilkan hasil
        self.display_area = ctk.CTkTextbox(self, width=650, height=300, font=("Courier New", 12))
        self.display_area.pack(pady=10, padx=20)

        self.btn_scan = ctk.CTkButton(self, text="Scan Perangkat", command=self.scan_devices)
        self.btn_scan.pack(pady=10)

    def scan_devices(self):
        self.display_area.delete("1.0", "end")
        self.display_area.insert("end", "Memulai pemindaian...\n" + "-"*50 + "\n")
        
        try:
            # 1. CPU
            for cpu in self.w.Win32_Processor():
                self.display_area.insert("end", f"[CPU] : {cpu.Name}\n")

            # 2. GPU (Video Controller)
            for gpu in self.w.Win32_VideoController():
                self.display_area.insert("end", f"[GPU] : {gpu.Name}\n")

            # 3. RAM
            for ram in self.w.Win32_PhysicalMemory():
                gb_size = int(ram.Capacity) / (1024**3)
                self.display_area.insert("end", f"[RAM] : {ram.Manufacturer} {gb_size:.1f} GB\n")

            # 4. Disk Drive
            for disk in self.w.Win32_DiskDrive():
                size_gb = int(disk.Size) / (1024**3)
                self.display_area.insert("end", f"[DISK]: {disk.Caption} ({size_gb:.1f} GB)\n")
            
            # 5. Network Adapter
            for nic in self.w.Win32_NetworkAdapter(PhysicalAdapter=True):
                self.display_area.insert("end", f"[NET] : {nic.Name}\n")

        except Exception as e:
            self.display_area.insert("end", f"Error: {str(e)}")

        self.display_area.insert("end", "\n" + "-"*50 + "\nScan Selesai!")

if __name__ == "__main__":
    app = DeviceMonitorApp()
    app.mainloop()