import os
import platform
import shutil
import subprocess
import zipfile
import mimetypes
import psutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
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

        self.backup_button = tk.Button(self.backup_frame, text="Backup", command=self.backup_files, bg="#007bff", fg="white", bd=0)
        self.backup_button.pack(pady=10)

        self.restore_button = tk.Button(self.backup_frame, text="Restore", command=self.restore_files, bg="#28a745", fg="white", bd=0)
        self.restore_button.pack(pady=10)

    def browse_files(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.current_directory = selected_directory
            self.populate_listbox()

    def search_file(self):
        search_term = self.search_var.get().lower()
        self.file_listbox.delete(0, tk.END)
        for item in os.listdir(self.current_directory):
            if search_term in item.lower():
                self.file_listbox.insert(tk.END, item)

    def double_click_file(self, event):
        selection = self.file_listbox.curselection()
        if selection:
            selected_file = self.file_listbox.get(selection[0])
            self.current_file = os.path.join(self.current_directory, selected_file)
            if os.path.isdir(self.current_file):
                self.current_directory = self.current_file
                self.populate_listbox()
            else:
                mimetype, _ = mimetypes.guess_type(self.current_file)
                if mimetype and mimetype.startswith('image'):
                    self.preview_image()

    def populate_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for item in os.listdir(self.current_directory):
            self.file_listbox.insert(tk.END, item)

    def populate_processes(self):
        self.process_listbox.delete(0, tk.END)
        for proc in psutil.process_iter(['pid', 'name']):
            self.process_listbox.insert(tk.END, f"{proc.info['pid']}: {proc.info['name']}")

    def kill_process(self):
        selection = self.process_listbox.curselection()
        if selection:
            selected_process = self.process_listbox.get(selection[0])
            pid = int(selected_process.split(":")[0])
            proc = psutil.Process(pid)
            proc.terminate()
            self.populate_processes()

    def populate_system_info(self):
        self.system_info_text.delete(1.0, tk.END)
        info = [
            f"System: {platform.system()}",
            f"Node Name: {platform.node()}",
            f"Release: {platform.release()}",
            f"Version: {platform.version()}",
            f"Machine: {platform.machine()}",
            f"Processor: {platform.processor()}"
        ]
        self.system_info_text.insert(tk.END, "\n".join(info))

    def create_directory(self):
        new_dir = simpledialog.askstring("Create Directory", "Enter new directory name:")
        if new_dir:
            new_dir_path = os.path.join(self.current_directory, new_dir)
            os.makedirs(new_dir_path, exist_ok=True)
            self.populate_listbox()

    def rename_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            old_name = self.file_listbox.get(selection[0])
            new_name = simpledialog.askstring("Rename File", "Enter new file name:", initialvalue=old_name)
            if new_name:
                old_path = os.path.join(self.current_directory, old_name)
                new_path = os.path.join(self.current_directory, new_name)
                os.rename(old_path, new_path)
                self.populate_listbox()

    def delete_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            selected_file = self.file_listbox.get(selection[0])
            file_path = os.path.join(self.current_directory, selected_file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            self.populate_listbox()

    def copy_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            selected_file = self.file_listbox.get(selection[0])
            file_path = os.path.join(self.current_directory, selected_file)
            destination = filedialog.askdirectory(title="Select Destination")
            if destination:
                shutil.copy(file_path, destination)
                messagebox.showinfo("Copy File", "File copied successfully")

    def move_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            selected_file = self.file_listbox.get(selection[0])
            file_path = os.path.join(self.current_directory, selected_file)
            destination = filedialog.askdirectory(title="Select Destination")
            if destination:
                shutil.move(file_path, destination)
                self.populate_listbox()

    def compress_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            selected_file = self.file_listbox.get(selection[0])
            file_path = os.path.join(self.current_directory, selected_file)
            zip_path = f"{file_path}.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                if os.path.isdir(file_path):
                    for root, _, files in os.walk(file_path):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(file_path, '..')))
                else:
                    zipf.write(file_path, os.path.basename(file_path))
            messagebox.showinfo("Compress File", "File compressed successfully")

    def extract_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            selected_file = self.file_listbox.get(selection[0])
            file_path = os.path.join(self.current_directory, selected_file)
            destination = filedialog.askdirectory(title="Select Destination")
            if destination:
                with zipfile.ZipFile(file_path, 'r') as zipf:
                    zipf.extractall(destination)
                messagebox.showinfo("Extract File", "File extracted successfully")

    def sort_files(self, criteria):
        file_list = os.listdir(self.current_directory)
        if criteria == "Name":
            file_list.sort(key=lambda x: x.lower())
        elif criteria == "Size":
            file_list.sort(key=lambda x: os.path.getsize(os.path.join(self.current_directory, x)))
        elif criteria == "Modified Date":
            file_list.sort(key=lambda x: os.path.getmtime(os.path.join(self.current_directory, x)))
        self.file_listbox.delete(0, tk.END)
        for item in file_list:
            self.file_listbox.insert(tk.END, item)

    def filter_files(self, filter_by):
        self.file_listbox.delete(0, tk.END)
        for item in os.listdir(self.current_directory):
            file_path = os.path.join(self.current_directory, item)
            mimetype, _ = mimetypes.guess_type(file_path)
            if filter_by == "All Files":
                self.file_listbox.insert(tk.END, item)
            elif filter_by == "Images" and mimetype and mimetype.startswith('image'):
                self.file_listbox.insert(tk.END, item)
            elif filter_by == "Documents" and mimetype and (mimetype.endswith('pdf') or mimetype.endswith('msword') or mimetype.endswith('vnd.openxmlformats-officedocument.wordprocessingml.document')):
                self.file_listbox.insert(tk.END, item)
            elif filter_by == "Text Files" and mimetype and mimetype.startswith('text'):
                self.file_listbox.insert(tk.END, item)

    def preview_image(self):
        if self.current_file:
            mimetype, _ = mimetypes.guess_type(self.current_file)
            if mimetype and mimetype.startswith('image'):
                preview_window = tk.Toplevel(self.root)
                preview_window.title("Image Preview")

                img = Image.open(self.current_file)
                img.thumbnail((500, 500))

                img = ImageTk.PhotoImage(img)

                img_label = tk.Label(preview_window, image=img)
                img_label.image = img  # keep a reference!
                img_label.pack()

    def backup_files(self):
        source = filedialog.askdirectory(title="Select Directory to Backup")
        if source:
            backup_path = f"{source}_backup.zip"
            with zipfile.ZipFile(backup_path, 'w') as zipf:
                for root, _, files in os.walk(source):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(source, '..')))
            messagebox.showinfo("Backup Files", "Backup created successfully")

    def restore_files(self):
        backup_file = filedialog.askopenfilename(title="Select Backup File", filetypes=[("Zip files", "*.zip")])
        if backup_file:
            destination = filedialog.askdirectory(title="Select Destination")
            if destination:
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    zipf.extractall(destination)
                messagebox.showinfo("Restore Files", "Files restored successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = SysAdminToolkitApp(root)
    root.mainloop()

