import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import os
import shutil
import mimetypes
import zipfile
import psutil
import platform
import subprocess
import time
import json
from PIL import Image, ImageTk

class SysAdminToolkitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SysAdmin Toolkit")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.current_directory = os.getcwd()
        self.current_file = None

        self.create_widgets()

    def create_widgets(self):
        # Top Frame
        self.top_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.top_frame.pack(pady=10)

        self.label = tk.Label(self.top_frame, text="SysAdmin Toolkit", font=("Helvetica", 24), bg="#f0f0f0")
        self.label.pack(side="left", padx=10)

        self.browse_button = tk.Button(self.top_frame, text="Browse", command=self.browse_files, bg="#007bff", fg="white", bd=0)
        self.browse_button.pack(side="left", padx=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, width=30, font=("Helvetica", 12))
        self.search_entry.pack(side="left", padx=10)

        self.search_button = tk.Button(self.top_frame, text="Search", command=self.search_file, bg="#28a745", fg="white", bd=0)
        self.search_button.pack(side="left", padx=10)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # File Management Tab
        self.file_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.file_frame, text="File Management")

        self.create_file_management_widgets()

        # Process Management Tab
        self.process_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.process_frame, text="Process Management")

        self.create_process_management_widgets()

        # System Information Tab
        self.system_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.system_frame, text="System Information")

        self.create_system_information_widgets()

        # Backup & Restore Tab
        self.backup_frame = tk.Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.backup_frame, text="Backup & Restore")

        self.create_backup_widgets()

    def create_file_management_widgets(self):
        # File Management Widgets
        self.file_top_frame = tk.Frame(self.file_frame, bg="#f0f0f0")
        self.file_top_frame.pack(pady=10)

        self.file_label = tk.Label(self.file_top_frame, text="File Management", font=("Helvetica", 18), bg="#f0f0f0")
        self.file_label.pack(side="left", padx=10)

        self.file_listbox_frame = tk.Frame(self.file_frame)
        self.file_listbox_frame.pack(expand=True, fill="both")

        self.file_scrollbar = tk.Scrollbar(self.file_listbox_frame, orient="vertical")
        self.file_scrollbar.pack(side="right", fill="y")

        self.file_listbox = tk.Listbox(self.file_listbox_frame, yscrollcommand=self.file_scrollbar.set, font=("Helvetica", 14))
        self.file_listbox.pack(expand=True, fill="both")

        self.file_scrollbar.config(command=self.file_listbox.yview)

        self.file_listbox.bind("<Double-Button-1>", self.double_click_file)

        # Bottom Frame
        self.file_bottom_frame = tk.Frame(self.file_frame, bg="#f0f0f0")
        self.file_bottom_frame.pack(pady=10)

        self.create_dir_button = tk.Button(self.file_bottom_frame, text="Create Directory", command=self.create_directory, bg="#17a2b8", fg="white", bd=0)
        self.create_dir_button.pack(side="left", padx=10)

        self.rename_button = tk.Button(self.file_bottom_frame, text="Rename", command=self.rename_file, bg="#ffc107", fg="white", bd=0)
        self.rename_button.pack(side="left", padx=10)

        self.delete_button = tk.Button(self.file_bottom_frame, text="Delete", command=self.delete_file, bg="#dc3545", fg="white", bd=0)
        self.delete_button.pack(side="left", padx=10)

        self.copy_button = tk.Button(self.file_bottom_frame, text="Copy", command=self.copy_file, bg="#28a745", fg="white", bd=0)
        self.copy_button.pack(side="left", padx=10)

        self.move_button = tk.Button(self.file_bottom_frame, text="Move", command=self.move_file, bg="#6610f2", fg="white", bd=0)
        self.move_button.pack(side="left", padx=10)

        self.compress_button = tk.Button(self.file_bottom_frame, text="Compress", command=self.compress_file, bg="#007bff", fg="white", bd=0)
        self.compress_button.pack(side="left", padx=10)

        self.extract_button = tk.Button(self.file_bottom_frame, text="Extract", command=self.extract_file, bg="#17a2b8", fg="white", bd=0)
        self.extract_button.pack(side="left", padx=10)

        self.sort_by_var = tk.StringVar(value="Name")
        self.sort_by_menu = tk.OptionMenu(self.file_bottom_frame, self.sort_by_var, "Name", "Size", "Modified Date", command=self.sort_files)
        self.sort_by_menu.pack(side="left", padx=10)

        self.filter_var = tk.StringVar(value="All Files")
        self.filter_menu = tk.OptionMenu(self.file_bottom_frame, self.filter_var, "All Files", "Images", "Documents", "Text Files", command=self.filter_files)
        self.filter_menu.pack(side="left", padx=10)

        # Preview Button for Images
        self.preview_button = tk.Button(self.file_bottom_frame, text="Preview", command=self.preview_image, bg="#6610f2", fg="white", bd=0)
        self.preview_button.pack(side="left", padx=10)

        # Populate file listbox with initial contents
        self.populate_listbox()

    def create_process_management_widgets(self):
        # Process Management Widgets
        self.process_top_frame = tk.Frame(self.process_frame, bg="#f0f0f0")
        self.process_top_frame.pack(pady=10)

        self.process_label = tk.Label(self.process_top_frame, text="Process Management", font=("Helvetica", 18), bg="#f0f0f0")
        self.process_label.pack(side="left", padx=10)

        self.process_listbox_frame = tk.Frame(self.process_frame)
        self.process_listbox_frame.pack(expand=True, fill="both")

        self.process_scrollbar = tk.Scrollbar(self.process_listbox_frame, orient="vertical")
        self.process_scrollbar.pack(side="right", fill="y")

        self.process_listbox = tk.Listbox(self.process_listbox_frame, yscrollcommand=self.process_scrollbar.set, font=("Helvetica", 14))
        self.process_listbox.pack(expand=True, fill="both")

        self.process_scrollbar.config(command=self.process_listbox.yview)

        self.process_refresh_button = tk.Button(self.process_frame, text="Refresh", command=self.populate_processes, bg="#28a745", fg="white", bd=0)
        self.process_refresh_button.pack(pady=10)

        self.process_kill_button = tk.Button(self.process_frame, text="Kill", command=self.kill_process, bg="#dc3545", fg="white", bd=0)
        self.process_kill_button.pack(pady=10)

        # Populate process listbox with initial contents
        self.populate_processes()

    def create_system_information_widgets(self):
        # System Information Widgets
        self.system_top_frame = tk.Frame(self.system_frame, bg="#f0f0f0")
        self.system_top_frame.pack(pady=10)

        self.system_label = tk.Label(self.system_top_frame, text="System Information", font=("Helvetica", 18), bg="#f0f0f0")
        self.system_label.pack(side="left", padx=10)

        self.system_info_text = tk.Text(self.system_frame, width=100, height=20, font=("Helvetica", 12))
        self.system_info_text.pack(expand=True, fill="both", padx=10, pady=10)

        self.populate_system_info()

    def create_backup_widgets(self):
        # Backup & Restore Widgets
        self.backup_top_frame = tk.Frame(self.backup_frame, bg="#f0f0f0")
        self.backup_top_frame.pack(pady=10)

        self.backup_label = tk.Label(self.backup_top_frame, text="Backup & Restore", font=("Helvetica", 18), bg="#f0f0f0")
        self.backup_label.pack(side="left", padx=10)

        self.backup_source_button = tk.Button(self.backup_frame, text="Select Source", command=self.select_backup_source, bg="#007bff", fg="white", bd=0)
        self.backup_source_button.pack(pady=10)

        self.backup_dest_button = tk.Button(self.backup_frame, text="Select Destination", command=self.select_backup_dest, bg="#28a745", fg="white", bd=0)
        self.backup_dest_button.pack(pady=10)

        self.backup_start_button = tk.Button(self.backup_frame, text="Start Backup", command=self.start_backup, bg="#ffc107", fg="white", bd=0)
        self.backup_start_button.pack(pady=10)

        self.backup_progress = ttk.Progressbar(self.backup_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.backup_progress.pack(pady=10)

    def populate_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for item in os.listdir(self.current_directory):
            self.file_listbox.insert(tk.END, item)

    def browse_files(self):
        self.current_directory = filedialog.askdirectory()
        self.populate_listbox()

    def create_directory(self):
        new_dir_name = simpledialog.askstring("Create Directory", "Enter new directory name:")
        if new_dir_name:
            new_dir_path = os.path.join(self.current_directory, new_dir_name)
            try:
                os.mkdir(new_dir_path)
                messagebox.showinfo("Directory Created", f"Directory '{new_dir_name}' created successfully.")
                self.populate_listbox()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def rename_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            new_name = simpledialog.askstring("Rename", f"Enter new name for '{selected_file}':")
            if new_name:
                try:
                    old_path = os.path.join(self.current_directory, selected_file)
                    new_path = os.path.join(self.current_directory, new_name)
                    os.rename(old_path, new_path)
                    messagebox.showinfo("Rename", "File/Directory renamed successfully.")
                    self.populate_listbox()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete '{selected_file}'?")
            if confirm:
                try:
                    file_path = os.path.join(self.current_directory, selected_file)
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)
                    messagebox.showinfo("Delete", "File/Directory deleted successfully.")
                    self.populate_listbox()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def copy_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            source = os.path.join(self.current_directory, selected_file)
            destination = filedialog.askdirectory(initialdir=self.current_directory)
            if destination:
                try:
                    if os.path.isdir(source):
                        shutil.copytree(source, os.path.join(destination, selected_file))
                    else:
                        shutil.copy2(source, destination)
                    messagebox.showinfo("Copy", "File/Directory copied successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def move_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            source = os.path.join(self.current_directory, selected_file)
            destination = filedialog.askdirectory(initialdir=self.current_directory)
            if destination:
                try:
                    shutil.move(source, os.path.join(destination, selected_file))
                    messagebox.showinfo("Move", "File/Directory moved successfully.")
                    self.populate_listbox()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def compress_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            source = os.path.join(self.current_directory, selected_file)
            destination = filedialog.asksaveasfilename(initialdir=self.current_directory, defaultextension=".zip")
            if destination:
                try:
                    with zipfile.ZipFile(destination, 'w') as zipf:
                        zipf.write(source, os.path.basename(source))
                    messagebox.showinfo("Compress", "File/Directory compressed successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def extract_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            source = os.path.join(self.current_directory, selected_file)
            destination = filedialog.askdirectory(initialdir=self.current_directory)
            if destination:
                try:
                    with zipfile.ZipFile(source, 'r') as zipf:
                        zipf.extractall(destination)
                    messagebox.showinfo("Extract", "File/Directory extracted successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def double_click_file(self, event):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        file_path = os.path.join(self.current_directory, selected_file)
        if os.path.isfile(file_path):
            subprocess.Popen(['xdg-open', file_path])

    def search_file(self):
        query = self.search_var.get()
        if query:
            results = [f for f in os.listdir(self.current_directory) if query.lower() in f.lower()]
            self.file_listbox.delete(0, tk.END)
            for item in results:
                self.file_listbox.insert(tk.END, item)

    def sort_files(self, event):
        option = self.sort_by_var.get()
        if option == "Name":
            self.populate_listbox()
        elif option == "Size":
            files = [(f, os.path.getsize(os.path.join(self.current_directory, f))) for f in os.listdir(self.current_directory)]
            files.sort(key=lambda x: x[1], reverse=True)
            self.file_listbox.delete(0, tk.END)
            for item in files:
                self.file_listbox.insert(tk.END, item[0])
        elif option == "Modified Date":
            files = [(f, os.path.getmtime(os.path.join(self.current_directory, f))) for f in os.listdir(self.current_directory)]
            files.sort(key=lambda x: x[1], reverse=True)
            self.file_listbox.delete(0, tk.END)
            for item in files:
                self.file_listbox.insert(tk.END, item[0])

    def filter_files(self, event):
        option = self.filter_var.get()
        if option == "All Files":
            self.populate_listbox()
        else:
            self.file_listbox.delete(0, tk.END)
            for item in os.listdir(self.current_directory):
                if self.check_file_type(item, option):
                    self.file_listbox.insert(tk.END, item)

    def check_file_type(self, filename, category):
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type:
            if category == "Images" and mime_type.startswith("image"):
                return True
            elif category == "Documents" and mime_type.startswith("application/pdf"):
                return True
            elif category == "Text Files" and mime_type.startswith("text"):
                return True
        return False

    def preview_image(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            file_path = os.path.join(self.current_directory, selected_file)
            if os.path.isfile(file_path):
                try:
                    img = Image.open(file_path)
                    img.show()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def populate_processes(self):
        self.process_listbox.delete(0, tk.END)
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            self.process_listbox.insert(tk.END, f"{proc.info['pid']}: {proc.info['name']}")

    def kill_process(self):
        selected_process = self.process_listbox.get(tk.ACTIVE)
        if selected_process:
            pid = int(selected_process.split(":")[0])
            try:
                process = psutil.Process(pid)
                process.terminate()
                messagebox.showinfo("Process Killed", f"Process with PID {pid} killed successfully.")
                self.populate_processes()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def populate_system_info(self):
        system_info = f"System: {platform.system()} {platform.release()}\n"
        system_info += f"Machine: {platform.machine()}\n"
        system_info += f"Processor: {platform.processor()}\n"
        system_info += f"CPU Count: {psutil.cpu_count()}\n"
        system_info += f"Memory: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB\n"
        system_info += f"Boot Time: {time.ctime(psutil.boot_time())}\n"
        self.system_info_text.insert(tk.END, system_info)

    def select_backup_source(self):
        self.backup_source = filedialog.askdirectory()

    def select_backup_dest(self):
        self.backup_dest = filedialog.askdirectory()

    def start_backup(self):
        if not hasattr(self, 'backup_source') or not hasattr(self, 'backup_dest'):
            messagebox.showerror("Error", "Please select source and destination directories.")
            return

        if self.backup_source == self.backup_dest:
            messagebox.showerror("Error", "Source and destination directories cannot be the same.")
            return

        self.backup_progress['value'] = 0
        self.root.update_idletasks()

        total_files = sum(len(files) for _, _, files in os.walk(self.backup_source))

        with zipfile.ZipFile(os.path.join(self.backup_dest, 'backup.zip'), 'w') as backup_zip:
            for root, _, files in os.walk(self.backup_source):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.backup_source)
                    backup_zip.write(file_path, relative_path)
                    self.backup_progress['value'] += 100 / total_files
                    self.root.update_idletasks()

        messagebox.showinfo("Backup Complete", "Backup completed successfully.")

root = tk.Tk()
app = SysAdminToolkitApp(root)
root.mainloop()

