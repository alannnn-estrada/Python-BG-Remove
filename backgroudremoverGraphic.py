import os
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
from rembg import remove
import threading

class BackgroundRemoverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")

        self.root.configure(bg="#101728")
        self.input_file = ""

        style = ttk.Style()
        style.configure("TButton", padding=(10, 2), background="#101728", foreground="blue")
        style.configure("TLabel", padding=(0, 10), background="#101728", foreground="white")

        label1 = ttk.Label(root, text="Input File:")
        label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.input_file_entry = ttk.Entry(root)
        self.input_file_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        browse_button1 = ttk.Button(root, text="Browse", command=self.browse_input_file)
        browse_button1.grid(row=0, column=2, padx=10, pady=10)

        process_button = ttk.Button(root, text="Process Image", command=self.process_image)
        process_button.grid(row=1, column=0, columnspan=3, padx=10, pady=20)

        self.progress_label = ttk.Label(root, text="", padding=(0, 10))
        self.progress_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def browse_input_file(self):
        self.progress_bar["value"] = 0
        self.progress_label.config(text="")
        
        self.input_file = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")]
        )
        if self.input_file:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, self.input_file)

    def process_image(self):
        if not self.input_file:
            return

        output_folder = filedialog.askdirectory()
        while not output_folder:
            output_folder = filedialog.askdirectory()
        
        self.progress_label.config(text="Procesando...")

        thread = threading.Thread(target=self._remove_background, args=(self.input_file, output_folder))
        thread.start()

    def _remove_background(self, input_path, output_folder):
        try:
            input_filename = os.path.splitext(os.path.basename(input_path))[0]
            output_filename = f"{input_filename}_background_remove.png"
            output_path = os.path.join(output_folder, output_filename)

            with open(input_path, 'rb') as inp, open(output_path, 'wb') as outp:
                background_output = remove(inp.read())
                outp.write(background_output)

            self.progress_label.config(text="Proceso completado con éxito")
        except Exception as e:
            self.progress_label.config(text=f"Error: {str(e)}")

        self.progress_bar["value"] = 100

if __name__ == '__main__':
    root = tk.Tk()
    app = BackgroundRemoverGUI(root)
    root.mainloop()
