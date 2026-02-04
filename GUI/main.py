import customtkinter
import os
import threading
import sys
from pathlib import Path
from tkinter import filedialog, messagebox

# Import commands - adjusting path to make sure imports work
# Assuming script is run from project root, but if run from GUI folder, need to adjust sys.path
sys.path.append(str(Path(__file__).parent.parent))

from src.setfile.commands.organize import organize_files
from src.setfile.commands.revert import revert
from src.setfile.commands.gmail_auth import gmail_auth
from GUI.utils import ClickPatcher

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("SetFile GUI")
        self.geometry("900x600")

        # Layout configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="SetFile", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # Main Area (Tabview)
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Organize")
        self.tabview.add("Revert")
        self.tabview.add("Authentication")

        # --- Organize Tab ---
        self.tabview.tab("Organize").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Organize").grid_rowconfigure(2, weight=1) # Log area expands

        self.folder_input_frame = customtkinter.CTkFrame(self.tabview.tab("Organize"))
        self.folder_input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.folder_path_entry = customtkinter.CTkEntry(self.folder_input_frame, placeholder_text="Select Folder to Organize")
        self.folder_path_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        
        self.browse_button = customtkinter.CTkButton(self.folder_input_frame, text="Browse", width=80, command=self.browse_folder)
        self.browse_button.pack(side="right", padx=(0, 10), pady=10)

        self.organize_button = customtkinter.CTkButton(self.tabview.tab("Organize"), text="Start Organization", command=self.start_organize_thread)
        self.organize_button.grid(row=1, column=0, padx=20, pady=10)

        self.organize_log = customtkinter.CTkTextbox(self.tabview.tab("Organize"), width=250)
        self.organize_log.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.organize_log.insert("0.0", "Logs will appear here...\n")
        self.organize_log.configure(state="disabled")


        # --- Revert Tab ---
        self.tabview.tab("Revert").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Revert").grid_rowconfigure(1, weight=1)

        self.revert_button = customtkinter.CTkButton(self.tabview.tab("Revert"), text="Revert Last Action", fg_color="red", hover_color="darkred", command=self.start_revert_thread)
        self.revert_button.grid(row=0, column=0, padx=20, pady=20)

        self.revert_log = customtkinter.CTkTextbox(self.tabview.tab("Revert"), width=250)
        self.revert_log.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.revert_log.insert("0.0", "Logs will appear here...\n")
        self.revert_log.configure(state="disabled")

        # --- Auth Tab ---
        self.tabview.tab("Authentication").grid_columnconfigure(0, weight=1)
        
        self.auth_info_label = customtkinter.CTkLabel(self.tabview.tab("Authentication"), text="Connect to Gmail to enable email features.", font=customtkinter.CTkFont(size=14))
        self.auth_info_label.grid(row=0, column=0, padx=20, pady=20)

        self.auth_button = customtkinter.CTkButton(self.tabview.tab("Authentication"), text="Authenticate Gmail", command=self.start_auth_thread)
        self.auth_button.grid(row=1, column=0, padx=20, pady=10)

        self.auth_log = customtkinter.CTkTextbox(self.tabview.tab("Authentication"), height=100)
        self.auth_log.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.auth_log.insert("0.0", "Auth logs...\n")
        self.auth_log.configure(state="disabled")


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def sidebar_button_event(self):
        print("sidebar_button click")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path_entry.delete(0, "end")
            self.folder_path_entry.insert(0, folder_selected)

    def confirm_dialog(self, text):
        # We need to run this on the main thread ideally, but since expected to be blocking called from thread...
        # tkinter messageboxes are thread safe enough usually, or block.
        # But since we are in a background thread (CLI command), we cannot block the main thread directly
        # with just a call if we were on main thread. 
        # Wait, messageboxes are creating a new Toplevel.
        # Let's try direct call.
        return messagebox.askyesno("Confirmation", text)

    def start_organize_thread(self):
        path = self.folder_path_entry.get()
        if not path:
            messagebox.showerror("Error", "Please select a folder first.")
            return
        
        # Clear log
        self.organize_log.configure(state="normal")
        self.organize_log.delete("0.0", "end")
        self.organize_log.configure(state="disabled")

        threading.Thread(target=self.run_organize, args=(path,), daemon=True).start()

    def run_organize(self, path):
        # Disable button
        self.organize_button.configure(state="disabled")
        try:
            with ClickPatcher(self.organize_log, self.confirm_dialog):
                try:
                    organize_files(path)
                except Exception as e:
                    print(f"\nError: {e}")
        finally:
            self.organize_button.configure(state="normal")

    def start_revert_thread(self):
        # Clear log
        self.revert_log.configure(state="normal")
        self.revert_log.delete("0.0", "end")
        self.revert_log.configure(state="disabled")

        threading.Thread(target=self.run_revert, daemon=True).start()

    def run_revert(self):
        self.revert_button.configure(state="disabled")
        try:
            with ClickPatcher(self.revert_log, self.confirm_dialog):
                try:
                    revert()
                except Exception as e:
                    print(f"\nError: {e}")
        finally:
            self.revert_button.configure(state="normal")

    def start_auth_thread(self):
        self.auth_log.configure(state="normal")
        self.auth_log.delete("0.0", "end")
        self.auth_log.configure(state="disabled")

        threading.Thread(target=self.run_auth, daemon=True).start()

    def run_auth(self):
        self.auth_button.configure(state="disabled")
        try:
             with ClickPatcher(self.auth_log, self.confirm_dialog):
                try:
                    gmail_auth()
                except Exception as e:
                    print(f"\nError: {e}")
        finally:
            self.auth_button.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
