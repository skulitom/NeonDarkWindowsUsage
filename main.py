import psutil
import GPUtil
import customtkinter as ctk
from threading import Thread
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import numpy as np
from datetime import datetime

class CircularProgressBar(ctk.CTkCanvas):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height, bg='#1a1a1a', highlightthickness=0)
        self.width = width
        self.height = height
        self.create_oval(5, 5, width-5, height-5, outline='#333333', width=10)
        self.arc = self.create_arc(5, 5, width-5, height-5, start=90, extent=0, outline='', width=10, style='arc')
        self.percentage = self.create_text(width/2, height/2, text="0%", font=("Roboto", 16, "bold"), fill='white')
        self.current_value = 0

    def update_progress(self, value, color):
        alpha = 0.3
        smoothed_value = alpha * value + (1 - alpha) * self.current_value
        self.current_value = smoothed_value
        extent = int(360 * (smoothed_value / 100))
        self.itemconfigure(self.arc, extent=extent, outline=color)
        self.itemconfigure(self.percentage, text=f"{smoothed_value:.1f}%")

class DeviceMonitor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Enhanced Advanced Device Monitor")
        self.geometry("1440x810")  # Increased window size for better visibility
        self.configure(fg_color="#121212")  # Darker background for a more sleek look

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15)
        left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        right_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15)
        right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.progress_bars = []
        self.colors = ['#00ff00', '#ff00ff', '#00ffff', '#ffff00']
        self.titles = ['CPU', 'Disk', 'Memory', 'GPU']

        for i, (title, color) in enumerate(zip(self.titles, self.colors)):
            frame = ctk.CTkFrame(left_frame, fg_color="#1e1e1e")
            frame.pack(pady=15, padx=20, fill="x")

            label = ctk.CTkLabel(frame, text=f"{title} Usage", font=("Roboto", 18, "bold"), text_color=color)
            label.pack()

            progress_bar = CircularProgressBar(frame, 140, 140)  # Slightly larger progress bars
            progress_bar.pack(pady=10)

            # Add a label for displaying the exact percentage
            percentage_label = ctk.CTkLabel(frame, text="0%", font=("Roboto", 14), text_color="white")
            percentage_label.pack()

            self.progress_bars.append((progress_bar, percentage_label))

        # Add system information
        sys_info_frame = ctk.CTkFrame(left_frame, fg_color="#1e1e1e")
        sys_info_frame.pack(pady=15, padx=20, fill="x")

        sys_info_label = ctk.CTkLabel(sys_info_frame, text="System Information", font=("Roboto", 18, "bold"), text_color="white")
        sys_info_label.pack()

        self.sys_info_text = ctk.CTkTextbox(sys_info_frame, height=100, font=("Roboto", 12))
        self.sys_info_text.pack(pady=10, fill="x")

        self.fig, self.axs = plt.subplots(2, 2, figsize=(12, 9))
        self.fig.patch.set_facecolor('#1e1e1e')

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(pady=10, padx=10, fill=ctk.BOTH, expand=True)

        self.lines = []
        self.data = [deque(maxlen=120) for _ in range(4)]

        for i, ax in enumerate(self.axs.flat):
            line, = ax.plot([], [], color=self.colors[i], linewidth=2)
            self.lines.append(line)
            ax.set_ylim(0, 100)
            ax.set_xlim(0, 120)
            ax.set_title(self.titles[i], color='white', fontweight='bold', fontsize=14)
            ax.set_facecolor('#2a2a2a')
            ax.tick_params(colors='white', labelsize=10)
            for spine in ax.spines.values():
                spine.set_edgecolor('white')
            ax.grid(True, linestyle='--', alpha=0.3)

        self.fig.tight_layout()

        # Add timestamp
        self.timestamp_label = ctk.CTkLabel(right_frame, text="", font=("Roboto", 12), text_color="white")
        self.timestamp_label.pack(pady=5)

        self.update_thread = Thread(target=self.update_stats, daemon=True)
        self.update_thread.start()

        self.after(100, self.update_charts)
        self.after(1000, self.update_system_info)
        self.after(1000, self.update_timestamp)

    def update_stats(self):
        while True:
            cpu = psutil.cpu_percent(interval=0.5)
            disk = psutil.disk_usage('/').percent
            memory = psutil.virtual_memory().percent
            
            try:
                gpus = GPUtil.getGPUs()
                gpu = gpus[0].load * 100 if gpus else 0
            except:
                gpu = 0

            new_data = [cpu, disk, memory, gpu]

            for i, value in enumerate(new_data):
                progress_bar, percentage_label = self.progress_bars[i]
                progress_bar.update_progress(value, self.colors[i])
                percentage_label.configure(text=f"{value:.1f}%")
                self.data[i].append(value)

            time.sleep(0.1)

    def update_charts(self):
        for i, line in enumerate(self.lines):
            y = list(self.data[i])
            x = np.linspace(0, len(y), len(y))
            line.set_data(x, y)
            self.axs.flat[i].relim()
            self.axs.flat[i].autoscale_view()

        self.canvas.draw_idle()
        self.after(100, self.update_charts)

    def update_system_info(self):
        cpu_info = psutil.cpu_freq()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info_text = f"CPU: {psutil.cpu_count()} cores, {cpu_info.current:.2f} MHz\n"
        info_text += f"Memory: {memory.total / (1024**3):.2f} GB total, {memory.available / (1024**3):.2f} GB available\n"
        info_text += f"Disk: {disk.total / (1024**3):.2f} GB total, {disk.free / (1024**3):.2f} GB free"
        
        self.sys_info_text.delete("1.0", ctk.END)
        self.sys_info_text.insert(ctk.END, info_text)
        
        self.after(5000, self.update_system_info)  # Update every 5 seconds

    def update_timestamp(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.configure(text=f"Last updated: {current_time}")
        self.after(1000, self.update_timestamp)  # Update every second

if __name__ == "__main__":
    app = DeviceMonitor()
    app.mainloop()