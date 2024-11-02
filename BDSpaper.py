import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import webbrowser
import platform
import os
import re
import threading

class MinecraftServerInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Server Installer")
        self.root.geometry("800x600")
        self.create_tabs()
        self.check_java_installation()
        self.check_python_installation()
        self.check_platform()

        self.version_table = {
            '1.8': 'Java 8',
            '1.9': 'Java 8',
            '1.10': 'Java 8',
            '1.11': 'Java 8',
            '1.12': 'Java 11',
            '1.13': 'Java 11',
            '1.14': 'Java 11',
            '1.15': 'Java 11',
            '1.16': 'Java 11',
            '1.16.1': 'Java 11',
            '1.16.2': 'Java 11',
            '1.16.3': 'Java 11',
            '1.16.4': 'Java 11',
            '1.16.5': 'Java 16',
            '1.17': 'Java 21',
            '1.17.1': 'Java 21',
            '1.18': 'Java 21',
            '1.18.1': 'Java 21',
            '1.18.2': 'Java 21',
            '1.19': 'Java 21',
            '1.19.1': 'Java 21',
            '1.19.2': 'Java 21',
            '1.20': 'Java 21',
        }

        self.paper_jar_file = None
        self.server_process = None

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.root)

        self.requirements_tab = ttk.Frame(self.tab_control)
        self.download_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.requirements_tab, text="Requerimientos")
        self.tab_control.add(self.download_tab, text="Download")

        self.tab_control.pack(expand=1, fill="both")

        self.create_requirements_tab()
        self.create_download_tab()

    def create_requirements_tab(self):
        self.java_status_label = ttk.Label(self.requirements_tab, text="Java: Desconocido")
        self.java_status_label.pack(padx=10, pady=5)

        self.python_status_label = ttk.Label(self.requirements_tab, text="Python: Desconocido")
        self.python_status_label.pack(padx=10, pady=5)

        self.platform_label = ttk.Label(self.requirements_tab, text="Plataforma: Desconocido")
        self.platform_label.pack(padx=10, pady=5)

    def create_download_tab(self):
        self.warning_label = ttk.Label(self.download_tab, text="", foreground="red")
        self.warning_label.pack(padx=10, pady=5)

        self.download_java_button = ttk.Button(self.download_tab, text="Descargar Java", command=self.download_java)
        self.download_java_button.pack(padx=10, pady=5)
        self.download_java_button.pack_forget()  # Hide the button initially

        self.intro_frame = ttk.Frame(self.download_tab)
        self.intro_frame.pack(padx=10, pady=10)

        self.intro_label = ttk.Label(self.intro_frame, text="Descargar Host Paper")
        self.intro_label.pack(padx=5, pady=5)

        self.download_button = ttk.Button(self.intro_frame, text="Descargar", command=self.open_paper_download)
        self.download_button.pack(padx=5, pady=5)

        self.instructions_label = ttk.Label(self.download_tab, text="Coloca el archivo paper.jar en la carpeta del programa llamada 'server'.")
        self.instructions_label.pack(padx=10, pady=10)

        self.check_paper_button = ttk.Button(self.download_tab, text="Comprobar", command=self.check_paper_jar)
        self.check_paper_button.pack(padx=10, pady=5)

        self.ram_frame = ttk.Frame(self.download_tab)
        self.ram_frame.pack(padx=10, pady=10)
        self.ram_frame.pack_forget()  # Hide the frame initially

        self.ram_label = ttk.Label(self.ram_frame, text="RAM a asignar (en GB):")
        self.ram_label.pack(side="left", padx=5, pady=5)

        self.ram_entry = ttk.Entry(self.ram_frame)
        self.ram_entry.pack(side="left", padx=5, pady=5)

        self.start_button = ttk.Button(self.download_tab, text="Iniciar Servidor", command=self.start_server)
        self.start_button.pack(padx=10, pady=5)
        self.start_button.pack_forget()  # Hide the button initially

        self.stop_button = ttk.Button(self.download_tab, text="Detener Servidor", command=self.stop_server)
        self.stop_button.pack(padx=10, pady=5)
        self.stop_button.pack_forget()  # Hide the stop button initially

        self.output_text = scrolledtext.ScrolledText(self.download_tab, height=10, state='disabled')
        self.output_text.pack(padx=10, pady=10, fill='both', expand=True)

        self.progress_bar = ttk.Progressbar(self.download_tab, mode='indeterminate')
        self.progress_bar.pack(padx=10, pady=10, fill='x')
        self.progress_bar.pack_forget()  # Hide the progress bar initially

    def check_java_installation(self):
        java_installed = False
        java_version = None
        required_versions = ["17", "21"]

        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
            output = result.stderr.lower()  # Java version info is usually in stderr
            for version in required_versions:
                if f'"{version}.' in output:
                    java_installed = True
                    java_version = version
                    break
        except (subprocess.CalledProcessError, FileNotFoundError):
            java_installed = False

        if java_installed:
            self.java_status_label.config(text=f"Java: Instalado (Versión {java_version})")
        else:
            self.java_status_label.config(text="Java: No instalado")
            self.warning_label.config(text="Advertencia: Java 21 o Java 17 no está instalado. PaperMC requiere Java.")
            self.download_java_button.pack(padx=10, pady=5)  # Show the button

    def check_python_installation(self):
        python_installed = False
        try:
            version = subprocess.run(["python", "--version"], capture_output=True, text=True)
            if version.returncode == 0:
                python_installed = True
                self.python_status_label.config(text=f"Python: Instalado (Versión {version.stdout.strip()})")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.python_status_label.config(text="Python: No instalado")

    def check_platform(self):
        os_type = platform.system()
        self.platform_label.config(text=f"Plataforma: {os_type}")

    def download_java(self):
        os_type = platform.system()
        if os_type == "Windows":
            java_download_url = "https://www.oracle.com/java/technologies/downloads/#java21"
        elif os_type == "Linux":
            java_download_url = "https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html"
        else:
            messagebox.showerror("Error", "Sistema operativo no soportado.")
            return

        webbrowser.open(java_download_url)

    def open_paper_download(self):
        webbrowser.open("https://papermc.io/downloads/all")

    def check_paper_jar(self):
        server_folder = './server'
        if not os.path.exists(server_folder):
            messagebox.showerror("Error", f"La carpeta '{server_folder}' no existe.")
            return

        jar_files = [f for f in os.listdir(server_folder) if f.endswith('.jar') and 'paper' in f]

        if not jar_files:
            messagebox.showerror("Error", "No se encontró ningún archivo paper.jar en la carpeta 'server'.")
            return

        self.paper_jar_file = max(jar_files, key=lambda f: os.path.getctime(os.path.join(server_folder, f)))
        paper_version_match = re.search(r'paper-(\d+\.\d+\.\d+)-\d+\.jar', self.paper_jar_file)

        if not paper_version_match:
            messagebox.showerror("Error", "El archivo encontrado no sigue el formato esperado.")
            return

        paper_version = paper_version_match.group(1)
        recommended_java_version = self.get_recommended_java_version(paper_version)
        self.java_status_label.config(text=f"Java: Recomendado {recommended_java_version}")

        self.ram_frame.pack(padx=10, pady=10)  # Show the RAM frame
        self.start_button.pack(padx=10, pady=5)  # Show the start button
        self.stop_button.pack(padx=10, pady=5)  # Show the stop button

    def get_recommended_java_version(self, paper_version):
        for version in self.version_table.keys():
            if paper_version.startswith(version):
                return self.version_table[version]
        return "No disponible"

    def start_server(self):
        ram_amount = self.ram_entry.get()
        if not ram_amount.isdigit() or int(ram_amount) <= 0:
            messagebox.showerror("Error", "Por favor, ingrese un valor válido para la RAM.")
            return

        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)

        self.progress_bar.start()
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')

        threading.Thread(target=self.run_server, args=(int(ram_amount),)).start()

    def run_server(self, ram_amount):
        server_folder = './server'
        
        java_command = ["java", "-Xmx" + str(ram_amount) + "G", "-Xms" + str(ram_amount) + "G", "-jar", self.paper_jar_file, "nogui"]

        try:
            self.server_process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=server_folder)

            while True:
                output = self.server_process.stdout.readline()
                if output == "" and self.server_process.poll() is not None:
                    break
                if output:
                    self.output_text.insert(tk.END, output)
                    self.output_text.see(tk.END)

                    # Detectar el mensaje EULA
                    if "You need to agree to the EULA" in output:
                        self.handle_eula_agreement()  # Llamar a la función para manejar la aceptación del EULA

            self.output_text.insert(tk.END, "Servidor detenido.\n")

        except Exception as e:
            self.output_text.insert(tk.END, f"Error al iniciar el servidor: {e}\n")

        self.progress_bar.stop()
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.server_process = None

    def handle_eula_agreement(self):
        # Mostrar un messagebox para confirmar la aceptación del EULA
        result = messagebox.askyesno("Confirmar EULA", "Se debe confirmar el EULA de Minecraft. ¿Desea aceptar?")
        if result:  # Si el usuario acepta
            eula_file_path = os.path.join('./server', 'eula.txt')  # Ruta del archivo eula.txt
            # Cambiar el contenido de eula.txt
            with open(eula_file_path, 'w') as eula_file:
                eula_file.write("eula=true\n")  # Cambiar a eula=true
            self.output_text.insert(tk.END, "EULA aceptada. Cambiando eula.txt a eula=true.\n")
        else:  # Si el usuario no acepta
            self.output_text.insert(tk.END, "Proceso cancelado. EULA no aceptada.\n")
            self.stop_server()  # Detener el servidor si el EULA no es aceptado

    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()  # Terminar el proceso del servidor
            self.server_process = None
            self.output_text.insert(tk.END, "Servidor detenido por el usuario.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftServerInstaller(root)
    root.mainloop()
