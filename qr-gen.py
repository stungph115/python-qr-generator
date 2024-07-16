import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator by Tung PHAM")
        self.root.geometry("800x500")
        self.root.configure(bg='#f0f0f0')  # Set background color
        
        style = ttk.Style()
        style.configure("TButton",
                        font=("Helvetica", 12),
                        padding=6,
                        relief="flat",
                        focuscolor="none",
                        borderwidth=0)
        style.map("TButton",
                  background=[('!active', '!pressed', '#0078d7'), ('pressed', '#0056b3'), ('active', '#0056b3')],
                  foreground=[('!active', '!pressed', 'white'), ('pressed', 'white'), ('active', 'white')])

        self.label = tk.Label(root, text="Enter URL:", font=("Helvetica", 14), bg='#f0f0f0')
        self.label.pack(pady=10)
        
        entry_frame = tk.Frame(root, bg='#f0f0f0')
        entry_frame.pack(pady=10)
        
        self.entry = tk.Entry(entry_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry.pack(side=tk.LEFT, padx=5, pady=5, ipadx=0, ipady=5)
        
        self.button_clear = tk.Button(entry_frame, text="Clear", command=self.clear_text, font=("Helvetica", 10), bg='#dc3545', fg='white', bd=0, relief="flat", activebackground='#c82333', activeforeground='white', cursor="hand2")
        self.button_clear.pack(side=tk.RIGHT, padx=5, pady=5, ipadx=10, ipady=5)
        
        self.button_generate = tk.Button(root, text="Generate QR Code", command=self.generate_qr, font=("Helvetica", 12), bg='#28a745', fg='white', bd=0, relief="flat", activebackground='#218838', activeforeground='white', cursor="hand2")
        self.button_generate.pack(pady=10, ipadx=20, ipady=10)
        
        self.button_save = tk.Button(root, text="Save QR Code", command=self.save_qr, font=("Helvetica", 12), bg='#0078d7', fg='white', bd=0, relief="flat", activebackground='#0056b3', activeforeground='white', cursor="hand2")
        self.button_save.pack_forget()  # Initially hide the save button
        
        self.image_label = tk.Label(root, bg='#f0f0f0')
        self.image_label.pack(pady=10)
        
        self.qr_image = None
    
    def generate_qr(self):
        url = self.entry.get()
        if url:
            qr = qrcode.make(url)
            qr = qr.resize((200, 200), Image.LANCZOS)
            self.qr_image = qr
            qr_image_tk = ImageTk.PhotoImage(qr)
            self.image_label.config(image=qr_image_tk)
            self.image_label.image = qr_image_tk
            self.button_save.pack(pady=10, ipadx=20, ipady=10)  # Show the save button with packing options
        else:
            messagebox.showwarning("Input Error", "Please enter a URL")
    
    def save_qr(self):
        if self.qr_image:
            default_filename = "qr_code.png"
            file_path = filedialog.asksaveasfilename(initialfile=default_filename, defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.qr_image.save(file_path)
                messagebox.showinfo("Save QR Code", "QR code saved successfully!")
        else:
            messagebox.showwarning("Save Error", "No QR code to save. Please generate a QR code first.")
    
    def clear_text(self):
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
