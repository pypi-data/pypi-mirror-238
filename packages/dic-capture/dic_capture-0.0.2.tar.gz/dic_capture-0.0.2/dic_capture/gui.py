# Imports
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from dic_capture.run import run

CONFIG_DIR = "../saved_configs"

from serial.tools.list_ports import comports


def get_available_com_ports():
    available_com_ports = [port.device for port in comports()]
    if len(available_com_ports) == 0:
        return ["No COM ports available"]
    else:
        return available_com_ports


def get_available_cameras():
    pass


def load_config_from_file(config_file_path):
    with open(config_file_path, 'r') as file:
        return json.load(file)


def save_config_to_file(config_data, config_file_path):
    with open(config_file_path, 'w') as file:
        json.dump(config_data, file, indent=4)


def list_existing_configs():
    """Return a list of existing config files."""
    return [file for file in os.listdir(CONFIG_DIR) if file.endswith(".json")]


class MainWindow:
    def __init__(self, master: ThemedTk):
        self.master = master
        self.master.title("DIC-link v0.0.1")
        self.master.configure()

        # Load image
        try:
            self.logo_image = ImageTk.PhotoImage(Image.open("../logo.png"))
            self.logo_image = ImageTk.PhotoImage(Image.open("../logo.png"))
            self.logo = ttk.Label(master, image=self.logo_image)
            self.logo.grid(row=0, column=0, rowspan=6, sticky='sw', padx=10, pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Config section
        config_frame = ttk.LabelFrame(master, text="Config", padding=(10, 5))
        config_frame.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.new_config_btn = ttk.Button(config_frame, text="New Config", command=self.new_config)
        self.new_config_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

        existing_configs = list_existing_configs()
        self.configs = ttk.Combobox(config_frame, values=existing_configs, width=20)
        self.configs.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        self.select_config_btn = ttk.Button(config_frame, text="Select Config", command=self.select_config)
        self.select_config_btn.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

        self.edit_config_btn = ttk.Button(config_frame, text="Edit Config", command=self.edit_config)
        self.edit_config_btn.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

        # Run section
        run_frame = ttk.LabelFrame(master, text="Run", padding=(10, 5))
        run_frame.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        self.run_mode1_btn = ttk.Button(run_frame, text="Run Record Mode", command=self.run_record_mode)
        self.run_mode1_btn.pack(padx=10, pady=5, fill='x')

        self.run_mode2_btn = ttk.Button(run_frame, text="Run Test Mode", command=self.run_test_mode)
        self.run_mode2_btn.pack(padx=10, pady=5, fill='x')

        self.selected_config = None

    def new_config(self):
        default_config_data = load_config_from_file(CONFIG_DIR + "/default.json")
        config_window = tk.Toplevel(self.master)
        ConfigWindow(config_window, config_data=default_config_data)

    def edit_config(self):
        selected_config_name = self.configs.get()

        if selected_config_name == "":
            messagebox.showerror("Error", "No configuration selected!")
            return

        config_file_path = f"{CONFIG_DIR}/{selected_config_name}"
        if os.path.exists(config_file_path):
            config_data = load_config_from_file(config_file_path)
        else:
            messagebox.showerror("Error", "Selected configuration does not exist!")
            return

        config_window = tk.Toplevel(self.master)
        ConfigWindow(config_window, config_data=config_data)

    def select_config(self):
        """Set the path of the selected config file."""
        selected_config_path = CONFIG_DIR + "/" + self.configs.get()
        self.selected_config = json.load(open(selected_config_path, 'r'))

    def run_record_mode(self):
        """Set the config to record mode and run the program."""
        if self.selected_config is None:
            messagebox.showerror("Error", "No configuration selected!")
        else:
            self.selected_config["record_mode"] = True
            run(self.selected_config)

    def run_test_mode(self):
        """Set the config to test mode and run the program."""
        self.selected_config["record_mode"] = False
        run(self.selected_config)


# todo: make function for get available com ports
# todo: make functin for get available cameras
# todo: split configwindow into sections with headings using LabelFrame
# todo: add function for saving config settings to config file
# todo: add function for loading existing settings from config file


class ConfigWindow:
    def __init__(self, master: tk.Toplevel, config_data: Dict = None):
        self.master = master
        self.master.title("Configuration")
        self.master.configure()

        # Define settings in a dictionary
        self.settings = {
            "FPS Settings": {
                "FPS Config": {"type": "entry", "value": "30"},  # Example default value
            },
            "Port Settings": {
                "COM Port Config": {"type": "combobox", "value": get_available_com_ports()},
            },
            "IO Settings": {
                "Input Path": {"type": "filedialog", "value": "C:/example/path/input"},  # Example default value
                "Output Path": {"type": "filedialog", "value": "C:/example/path/output"},  # Example default value
            },
            "Camera Settings": {
                "CAM Select": {"type": "combobox", "value": ["CAM1", "CAM2"]},
            }
        }

        self.widgets = {}  # To store references to created widgets

        for idx, (section, controls) in enumerate(self.settings.items()):
            frame = ttk.LabelFrame(master, text=section, padding=(10, 5))
            frame.grid(row=idx, column=0, padx=10, pady=10, sticky="ew")
            self.widgets[section] = {}

            for control_idx, (label_text, control) in enumerate(controls.items()):
                ttk.Label(frame, text=label_text).grid(row=control_idx, column=0, padx=10, pady=5, sticky="w")

                if control["type"] == "entry":
                    widget = ttk.Entry(frame)
                    widget.insert(0, control["value"])
                elif control["type"] == "combobox":
                    widget = ttk.Combobox(frame, values=control["value"])
                elif control["type"] == "filedialog":
                    widget = ttk.Entry(frame)
                    widget.insert(0, control["value"])
                    ttk.Button(frame, text="Browse", command=lambda w=widget: self.browse_file(w)).grid(row=control_idx,
                                                                                                        column=2,
                                                                                                        padx=10, pady=5)

                widget.grid(row=control_idx, column=1, padx=10, pady=5, sticky="w")
                self.widgets[section][label_text] = widget

        self.save_config_btn = ttk.Button(master, text="Save Config", command=self.save_config)
        self.save_config_btn.grid(row=len(self.settings), column=0, pady=20)

        # If config_data is provided (for edit), load it.
        # Otherwise, use default values (for new).
        self.load_config(config_data if config_data else self.default_config())

    def load_config(self, config_data):
        """Load config settings into the widgets."""
        for section, controls in self.widgets.items():
            for label_text, widget in controls.items():
                widget.delete(0, tk.END)
                if config_data and section in config_data and label_text in config_data[section]:
                    widget.insert(0, config_data[section][label_text])
                else:
                    widget.insert(0, self.settings[section][label_text]['value'])

    def browse_file(self, widget):
        file_path = filedialog.askopenfilename()
        widget.delete(0, tk.END)
        widget.insert(0, file_path)

    def save_config(self):
        config = {}
        for section, controls in self.widgets.items():
            config[section] = {}
            for label_text, widget in controls.items():
                config[section][label_text] = widget.get()

        with open("config.json", "w") as file:
            json.dump(config, file)


def run_gui():
    root = ThemedTk(theme="plastik")  # Here, 'arc' is the name of the theme, but there are many others
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    root = ThemedTk(theme="plastik")  # Here, 'arc' is the name of the theme, but there are many others
    app = MainWindow(root)
    root.mainloop()
