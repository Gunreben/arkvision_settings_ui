import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import requests

# Define the main application class with a modern theme and appearance
class CameraConfigApp(ThemedTk):
    def __init__(self):
        super().__init__(theme="equilux")  # Choose a theme that suits your taste
        
        self.title("Camera Configuration")
        self.geometry("700x110")  # Adjusted for theme spacing
        
        # Customizing the look further
        self.configure(bg='gray25')  # Set a background color
        
        # Since we're using ThemedTk, the style configuration is slightly different
        self.style = ttk.Style(self)
        
        # Custom style for labels and buttons
        self.style.configure('TLabel', background='gray25', foreground='white', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TCombobox', font=('Arial', 10))
        
        # Camera IP configuration
        self.camera_ips = [f"192.168.26.{i}" for i in range(70, 76)]
        self.init_ui()
    
    def init_ui(self):
        # Frame for controls
        control_frame = ttk.Frame(self, padding="10 10 10 10")
        control_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        control_frame.configure(style='TFrame')
        
        # Camera selection
        ttk.Label(control_frame, text="Select Camera:", style='TLabel').grid(column=0, row=0, sticky=tk.W)
        self.camera_selection = tk.StringVar()
        self.camera_dropdown = ttk.Combobox(control_frame, width=15, textvariable=self.camera_selection, state="readonly")
        self.camera_dropdown['values'] = ["All Cameras"] + self.camera_ips
        self.camera_dropdown.grid(column=1, row=0, padx=5, pady=5)
        
        # Resolution selection
        ttk.Label(control_frame, text="Resolution:", style='TLabel').grid(column=2, row=0, sticky=tk.W)
        self.resolution_selection = tk.StringVar()
        self.resolution_dropdown = ttk.Combobox(control_frame, width=15, textvariable=self.resolution_selection, state="readonly")
        self.resolution_dropdown['values'] = [
            "1280x720", "960x544", "800x600", "800x480",
            "704x400", "640x480", "480x360", "320x240"
        ]
        self.resolution_dropdown.grid(column=3, row=0, padx=5, pady=5)
        
        # FPS selection
        ttk.Label(control_frame, text="FPS:", style='TLabel').grid(column=4, row=0, sticky=tk.W)
        self.fps_selection = tk.StringVar()
        self.fps_dropdown = ttk.Combobox(control_frame, width=15, textvariable=self.fps_selection, state="readonly")
        self.fps_dropdown['values'] = ["25 FPS", "5 FPS", "1 FPS"]
        self.fps_dropdown.grid(column=5, row=0, padx=5, pady=5)
        
        # Apply button
        self.apply_button = ttk.Button(control_frame, text="Apply", command=self.apply_settings)
        self.apply_button.grid(column=3, row=1, columnspan=2, pady=10)
        
        for child in control_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
    
    def apply_settings(self):
        selected_cameras = self.camera_ips if self.camera_selection.get() == "All Cameras" else [self.camera_selection.get()]
        resolution = self.resolution_selection.get()
        fps = self.fps_selection.get()
        
        resolution_params = {
            "1280x720": "1", "960x544": "2", "800x600": "3", "800x480": "4",
            "704x400": "6", "640x480": "7", "480x360": "8", "320x240": "9"
        }
        fps_params = {"25 FPS": "0", "5 FPS": "1", "1 FPS": "2"}
        
        for ip in selected_cameras:
            self.set_camera_config(ip, resolution_params[resolution], fps_params[fps])
    
    def set_camera_config(self, ip, resolution, fps):
        url = f"http://{ip}/appquery.cgi?v_v_hr={resolution}&v_v_hf={fps}&v_v_hp=0&v_v_hq=40&v_v_hi=30&v_v_hbm=1&v_v_hbr=hC10m&btOK=Apply"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Configuration applied successfully to {ip}")
            else:
                print(f"Failed to apply configuration to {ip}")
        except Exception as e:
            print(f"Error configuring {ip}: {e}")

if __name__ == "__main__":
    app = CameraConfigApp()
    app.mainloop()
