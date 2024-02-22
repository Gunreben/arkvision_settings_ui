import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import requests

class CameraConfigApp(ThemedTk):
    def __init__(self):
        super().__init__(theme="equilux")
        self.title("Camera Configuration")
        self.geometry("950x105")  # Adjusted for additional dropdown
        
        # Camera IP configuration
        self.camera_ips = [f"192.168.26.{i}" for i in range(70, 76)]
        
        # Initialize UI components
        self.init_ui()
    
    def init_ui(self):
        control_frame = ttk.Frame(self, padding="10 10 10 10")
        control_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Camera selection dropdown
        ttk.Label(control_frame, text="Select Camera:", style='TLabel').grid(column=0, row=0, sticky=tk.W)
        self.camera_selection = tk.StringVar()
        self.camera_dropdown = ttk.Combobox(control_frame, width=15, textvariable=self.camera_selection, state="readonly")
        self.camera_dropdown['values'] = ["All Cameras"] + self.camera_ips
        self.camera_dropdown.grid(column=1, row=0, padx=5, pady=5)
        
        # Codec selection dropdown
        ttk.Label(control_frame, text="Codec:", style='TLabel').grid(column=2, row=0, sticky=tk.W)
        self.codec_selection = tk.StringVar()
        self.codec_dropdown = ttk.Combobox(control_frame, width=15, textvariable=self.codec_selection, state="readonly")
        self.codec_dropdown['values'] = ["H264", "MJPEG"]
        self.codec_dropdown.grid(column=3, row=0, padx=5, pady=5)
        
        # Additional dropdowns for resolution and FPS
        self.setup_resolution_fps_dropdowns(control_frame)
        
        # Apply button
        self.apply_button = ttk.Button(control_frame, text="Apply", command=self.apply_settings)
        self.apply_button.grid(column=2, row=1, columnspan=2, pady=10)
        
        for child in control_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def setup_resolution_fps_dropdowns(self, control_frame):
        # Resolution selection
        ttk.Label(control_frame, text="Resolution:", style='TLabel').grid(column=4, row=0, sticky=tk.W)
        self.resolution_selection = tk.StringVar()
        self.resolution_dropdown = ttk.Combobox(control_frame, width=15, textvariable=self.resolution_selection, state="readonly")
        self.resolution_dropdown['values'] = ["1280x720", "960x544", "800x600", "800x480", "704x400", "640x480", "480x360", "320x240"]
        self.resolution_dropdown.grid(column=5, row=0, padx=5, pady=5)
        
        # FPS selection
        ttk.Label(control_frame, text="FPS:", style='TLabel').grid(column=6, row=0, sticky=tk.W)
        self.fps_selection = tk.StringVar()
        self.fps_dropdown = ttk.Combobox(control_frame, width=15, textvariable=self.fps_selection, state="readonly")
        self.fps_dropdown['values'] = ["25 FPS", "5 FPS", "1 FPS"]
        self.fps_dropdown.grid(column=7, row=0, padx=5, pady=5)

    def apply_settings(self):
        selected_cameras = self.camera_ips if self.camera_selection.get() == "All Cameras" else [self.camera_selection.get()]
        codec = self.codec_selection.get()
        resolution = self.resolution_selection.get()
        fps = self.fps_selection.get()
        
        resolution_params = {"1280x720": "1", "960x544": "2", "800x600": "3", "800x480": "4", "704x400": "6", "640x480": "7", "480x360": "8", "320x240": "9"}
        fps_params = {"25 FPS": "0", "5 FPS": "1", "1 FPS": "2"}
        
        for ip in selected_cameras:
            self.set_camera_config(ip, codec, resolution_params[resolution], fps_params[fps])
    
    def set_camera_config(self, ip, codec, resolution, fps):
        # Adjust the URL based on the selected codec
        if codec == "H264":
            param_prefix = "v_v_br"
        elif codec == "MJPEG":
            param_prefix = "v_v_j"
        else:
            print("Unsupported codec")
            return
        
        # Construct the URL based on codec
        if codec == "MJPEG:":
            url = f"http://{ip}/appquery.cgi?{param_prefix}r={resolution}&{param_prefix}f={fps}&{param_prefix}q=80&{param_prefix}bm=0&btOK=Apply"
        else: 
            url = f"http://{ip}/appquery.cgi?v_v_hr={resolution}&v_v_hf={fps}&v_v_hp=0&v_v_hq=40&v_v_hi=30&v_v_hbm=1&v_v_hbr=hC10m&btOK=Apply"
        
        # Example request - in real application, use requests.get or appropriate request method
        print(f"Configuring camera at {ip} with URL: {url}")
        response = requests.get(url)
        # Check response status if needed

if __name__ == "__main__":
    app = CameraConfigApp()
    app.mainloop()
