"""Copyright 2024 Franco Calegari

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import requests
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, Menu
import webbrowser

CACHE_FILE = "versions_cache.json"
URL = "https://raw.githubusercontent.com/Bedrock-OSS/BDS-Versions/refs/heads/main/versions.json"

class BDSManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BDS Downloader")
        self.create_menu()
        self.create_widgets()
        self.data = self.load_data()
        self.update_table()  # Ensure the table is populated at startup

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Sobre nosotros", command=self.show_about_info)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)

    def show_about_info(self):
        about_text = (
            "BDS Downloader\n"
            "Versión 1.0\n"
            "Creado por Franco Calegari\n\n"
            "La información de las versiones se descarga desde el repositorio de GitHub:\n"
            "https://github.com/Bedrock-OSS/BDS-Versions\n\n"
            "Gracias a ellos, este programa es posible.\n\n"
            "Este programa es de código abierto y gratuito.\n"
            "Apache-2.0.\n"
        )
        messagebox.showinfo("Sobre nosotros", about_text)

    def create_widgets(self):
        self.platform_var = tk.StringVar(value="linux")
        self.version_var = tk.StringVar()
        
        self.platform_frame = ttk.LabelFrame(self.root, text="Select Platform")
        self.platform_frame.pack(padx=10, pady=5, fill="x")
        
        self.linux_rb = ttk.Radiobutton(self.platform_frame, text="Linux", variable=self.platform_var, value="linux")
        self.linux_rb.pack(side="left", padx=5, pady=5)
        
        self.windows_rb = ttk.Radiobutton(self.platform_frame, text="Windows", variable=self.platform_var, value="windows")
        self.windows_rb.pack(side="left", padx=5, pady=5)
        
        self.platform_var.trace_add("write", self.update_table)  # Update table when platform changes
        
        self.search_frame = ttk.LabelFrame(self.root, text="Search Version")
        self.search_frame.pack(padx=10, pady=5, fill="x")
        
        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.update_table)
        
        self.update_button = ttk.Button(self.search_frame, text="Update Cache", command=self.update_cache)
        self.update_button.pack(side="left", padx=5, pady=5)
        
        self.tree_frame = ttk.LabelFrame(self.root, text="Versions")
        self.tree_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("version"), show="headings")
        self.tree.heading("version", text="Version")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        self.download_button = ttk.Button(self.root, text="Download", command=self.download_version)
        self.download_button.pack(pady=5)
        
    def load_data(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as file:
                return json.load(file)
        else:
            return self.update_cache()

    def update_cache(self):
        try:
            response = requests.get(URL)
            response.raise_for_status()
            data = response.json()
            with open(CACHE_FILE, 'w') as file:
                json.dump(data, file)
            self.data = data
            self.update_table()
            messagebox.showinfo("Success", "Cache updated successfully!")
            return data
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to update cache: {e}")
            return self.data if hasattr(self, 'data') else {}

    def update_table(self, *args):
        search_text = self.search_entry.get().lower()
        platform = self.platform_var.get()
        self.tree.delete(*self.tree.get_children())
        if platform in self.data:
            versions = self.data[platform].get("versions", []) + self.data[platform].get("preview_versions", [])
            for version in versions:
                if search_text in version.lower():
                    self.tree.insert("", "end", values=(version,))
        
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.version_var.set(self.tree.item(selected_item)["values"][0])

    def download_version(self):
        platform = self.platform_var.get()
        version = self.version_var.get()
        if not version:
            messagebox.showwarning("Warning", "Please select a version to download.")
            return
        if platform == "windows":
            platform = "win"  # Adjust platform for Windows download link
        url = f"https://minecraft.azureedge.net/bin-{platform}/bedrock-server-{version}.zip"
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = BDSManagerApp(root)
    root.mainloop()
