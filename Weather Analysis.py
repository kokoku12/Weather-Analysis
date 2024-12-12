import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# This is the application using Tkinter
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Analysis Dashboard")
        self.root.geometry("1000x700")
        self.root.config(bg="#E8F6FA")

        # This is the Header Frame
        self.header_frame = tk.Frame(self.root, bg="#93C5FD", height=60)
        self.header_frame.pack(fill=tk.X)
        self.header_label = tk.Label(
            self.header_frame, text="Weather Analysis Dashboard", 
            font=("Arial", 20, "bold"), bg="#93C5FD", fg="white"
        )
        self.header_label.pack(pady=10)

        # This is the File Upload Frame
        self.file_frame = tk.Frame(self.root, bg="#E8F6FA")
        self.file_frame.pack(pady=20)
        self.file_label = tk.Label(
            self.file_frame, text="Upload Weather Data:", font=("Arial", 12), bg="#E8F6FA"
        )
        self.file_label.grid(row=0, column=0, padx=10)
        self.upload_button = tk.Button(
            self.file_frame, text="Browse File", font=("Arial", 12), command=self.upload_file, 
            bg="#FDBEFB", fg="black"
        )
        self.upload_button.grid(row=0, column=1, padx=10)

        # This is the Placeholder for Loaded Data
        self.df = None

        # This is the Buttons for Visualizations
        self.button_frame = tk.Frame(self.root, bg="#E8F6FA")
        self.button_frame.pack(pady=20)
        self.temp_button = tk.Button(
            self.button_frame, text="Temperature Trends", font=("Arial", 12), command=self.plot_temperature, 
            bg="#93C5FD", fg="white"
        )
        self.temp_button.grid(row=0, column=0, padx=10)
        self.precip_button = tk.Button(
            self.button_frame, text="Precipitation Trends", font=("Arial", 12), command=self.plot_precipitation, 
            bg="#93C5FD", fg="white"
        )
        self.precip_button.grid(row=0, column=1, padx=10)
        self.wind_button = tk.Button(
            self.button_frame, text="Wind Trends", font=("Arial", 12), command=self.plot_wind, 
            bg="#93C5FD", fg="white"
        )
        self.wind_button.grid(row=0, column=2, padx=10)

        # Canvas for Matplotlib Plots
        self.canvas_frame = tk.Frame(self.root, bg="#E8F6FA")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    def upload_file(self):
        # Open file dialog
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if not file_path:
            return

        # Load file into a DataFrame
        try:
            if file_path.endswith(".csv"):
                self.df = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                self.df = pd.read_excel(file_path)
            messagebox.showinfo("Success", "File loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def validate_data(self):
        # Validate that required columns are present
        if self.df is None:
            messagebox.showwarning("Warning", "No file uploaded yet!")
            return False

        required_columns = {"Date", "Temperature_Max", "Temperature_Min", "Precipitation", "Wind"}
        if not required_columns.issubset(self.df.columns):
            messagebox.showerror("Error", f"File must contain the following columns: {', '.join(required_columns)}")
            return False

        # Convert Date column to datetime
        self.df["Date"] = pd.to_datetime(self.df["Date"])
        return True

    def plot_temperature(self):
        if not self.validate_data():
            return

        # Create a temperature trends plot
        fig, ax = plt.subplots(figsize=(10, 5))
        self.df.set_index("Date")[["Temperature_Max", "Temperature_Min"]].plot(ax=ax, color=["#FF5733", "#33C9FF"])
        ax.set_title("Temperature Trends", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Temperature (°C)", fontsize=12)
        ax.legend(["Max Temperature", "Min Temperature"], loc="upper right")
        self.add_plot_description(ax, "Daily temperature trends, showcasing maximum and minimum values.")
        self.show_plot(fig)

    def plot_precipitation(self):
        if not self.validate_data():
            return

        # Create a precipitation plot
        fig, ax = plt.subplots(figsize=(10, 5))
        self.df.set_index("Date")["Precipitation"].plot(kind="bar", ax=ax, color="#87CEEB")
        ax.set_title("Precipitation Trends", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Precipitation (mm)", fontsize=12)
        self.add_plot_description(ax, "Daily precipitation levels in millimeters.")
        self.show_plot(fig)

    def plot_wind(self):
        if not self.validate_data():
            return

        # Create a wind trends plot
        fig, ax = plt.subplots(figsize=(10, 5))
        self.df.set_index("Date")["Wind"].plot(ax=ax, color="#FFB6C1")
        ax.set_title("Wind Speed Trends", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Wind Speed (km/h)", fontsize=12)
        self.add_plot_description(ax, "Daily wind speed measured in kilometers per hour.")
        self.show_plot(fig)

    def add_plot_description(self, ax, description):
        ax.text(0.5, -0.2, description, fontsize=10, ha="center", transform=ax.transAxes, wrap=True)

    def show_plot(self, fig):
        # Clear previous canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Embed Matplotlib plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
