import asyncio
import threading
import tkinter as tk
from tkinter import messagebox, colorchooser
from tkinter import ttk
from bleak import BleakScanner
from device import GoveeDevice  # Your GoveeDevice class file

class GoveeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Govee BLE Controller")
        self.root.geometry("450x450")
        self.root.resizable(False, False)

        self.device_list = []

        # Style configuration for ttk
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TLabel', font=('Segoe UI', 10))

        # Frame for devices
        device_frame = ttk.LabelFrame(root, text="Govee Devices")
        device_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

        self.listbox = tk.Listbox(device_frame, height=8, font=('Segoe UI', 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=5)

        scrollbar = ttk.Scrollbar(device_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(0,5), pady=5)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Buttons Frame
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill=tk.X, padx=10)

        self.scan_button = ttk.Button(btn_frame, text="Scan Devices", command=self.start_scan_thread)
        self.scan_button.grid(row=0, column=0, padx=5, pady=5)

        self.power_on_button = ttk.Button(btn_frame, text="Turn ON", command=self.turn_on)
        self.power_on_button.grid(row=0, column=1, padx=5, pady=5)

        self.power_off_button = ttk.Button(btn_frame, text="Turn OFF", command=self.turn_off)
        self.power_off_button.grid(row=0, column=2, padx=5, pady=5)

        self.color_button = ttk.Button(btn_frame, text="Pick Color", command=self.pick_color)
        self.color_button.grid(row=0, column=3, padx=5, pady=5)

        self.status_label = ttk.Label(root, text="Status: Idle")
        self.status_label.pack(pady=10)

        self.current_device = None

    def start_scan_thread(self):
        self.status_label.config(text="Status: Scanning...")
        self.listbox.delete(0, tk.END)
        self.device_list = []
        thread = threading.Thread(target=self.scan_devices)
        thread.daemon = True
        thread.start()

    def scan_devices(self):
        devices = asyncio.run(self.do_scan())
        govee_devices = [d for d in devices if d.name and d.name.startswith("GBK")]
        self.device_list = govee_devices
        self.root.after(0, self.update_listbox)

    async def do_scan(self):
        devices = await BleakScanner.discover(timeout=5.0)
        return devices

    def update_listbox(self):
        if not self.device_list:
            messagebox.showinfo("Scan Result", "No Govee devices found.")
        else:
            for d in self.device_list:
                self.listbox.insert(tk.END, f"{d.name} [{d.address}]")
        self.status_label.config(text="Status: Scan Complete")

    def get_selected_device_mac(self):
        try:
            idx = self.listbox.curselection()[0]
            device = self.device_list[idx]
            return device.address
        except IndexError:
            messagebox.showwarning("Select device", "Please select a device first.")
            return None

    def turn_on(self):
        mac = self.get_selected_device_mac()
        if mac:
            self.status_label.config(text="Turning ON...")
            threading.Thread(target=self._turn_on, args=(mac,), daemon=True).start()

    def _turn_on(self, mac):
        dev = GoveeDevice(mac)
        success, status, out = dev.setPower(True)
        self.root.after(0, lambda: self.status_label.config(text=f"Turn On: {out}"))

    def turn_off(self):
        mac = self.get_selected_device_mac()
        if mac:
            self.status_label.config(text="Turning OFF...")
            threading.Thread(target=self._turn_off, args=(mac,), daemon=True).start()

    def _turn_off(self, mac):
        dev = GoveeDevice(mac)
        success, status, out = dev.setPower(False)
        self.root.after(0, lambda: self.status_label.config(text=f"Turn Off: {out}"))

    def pick_color(self):
        mac = self.get_selected_device_mac()
        if not mac:
            return
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code[0] is None:
            return  # User cancelled

        rgb = [int(c) for c in color_code[0]]
        self.status_label.config(text=f"Setting color to RGB: {rgb}...")
        threading.Thread(target=self._set_color, args=(mac, rgb), daemon=True).start()

    def _set_color(self, mac, rgb):
        dev = GoveeDevice(mac)
        try:
            success, color, out = dev.setColor(rgb)
            if success:
                self.root.after(0, lambda: self.status_label.config(text=f"Color set to {color}"))
            else:
                self.root.after(0, lambda: self.status_label.config(text=f"Failed to set color"))
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"Error: {str(e)}"))


def main():
    root = tk.Tk()
    app = GoveeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
