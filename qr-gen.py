import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk
import requests

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator by Tung PHAM")
        self.root.configure(bg='#f0f0f0')
        
        self.qr_image = None
        
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=6, relief="flat", focuscolor="none", borderwidth=0)
        style.map("TButton",
                  background=[('!active', '!pressed', '#0078d7'), ('pressed', '#0056b3'), ('active', '#0056b3')],
                  foreground=[('!active', '!pressed', 'white'), ('pressed', 'white'), ('active', 'white')])
        
        self.create_menu()
        self.create_input_frame()
        self.create_qr_display()
        self.create_buttons()
        
        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
    
    def create_menu(self):
        self.option_var = tk.StringVar(value="URL")
        options = ["URL", "Wi-Fi", "Image", "SMS", "Email"]
        self.menu_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.menu_frame.pack(pady=10, fill=tk.X)
        
        for option in options:
            button = tk.Radiobutton(self.menu_frame, text=option, variable=self.option_var, value=option, font=("Helvetica", 12), bg='#f0f0f0', command=self.update_input_fields)
            button.pack(side=tk.LEFT, padx=10)
    
    def create_input_frame(self):
        self.input_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.input_frame.pack(pady=10, fill=tk.X)
        self.update_input_fields()
    
    def update_input_fields(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        
        option = self.option_var.get()
        if option == "URL":
            self.create_url_input()
        elif option == "Wi-Fi":
            self.create_wifi_input()
        elif option == "Image":
            self.create_image_input()
        elif option == "SMS":
            self.create_sms_input()
        elif option == "Email":
            self.create_email_input()
        
        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
    
    def create_url_input(self):
        self.label = tk.Label(self.input_frame, text="Enter URL:", font=("Helvetica", 14), bg='#f0f0f0')
        self.label.pack(pady=10)
        self.entry = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry.pack(pady=5, ipadx=0, ipady=5)
    
    def create_wifi_input(self):
        self.label1 = tk.Label(self.input_frame, text="Network Name (SSID):", font=("Helvetica", 14), bg='#f0f0f0')
        self.label1.pack(pady=5)
        self.entry1 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry1.pack(pady=5, ipadx=0, ipady=5)
        
        self.label2 = tk.Label(self.input_frame, text="Password:", font=("Helvetica", 14), bg='#f0f0f0')
        self.label2.pack(pady=5)
        self.entry2 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry2.pack(pady=5, ipadx=0, ipady=5)
        
        self.label3 = tk.Label(self.input_frame, text="Encryption (WEP/WPA):", font=("Helvetica", 14), bg='#f0f0f0')
        self.label3.pack(pady=5)
        self.entry3 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry3.pack(pady=5, ipadx=0, ipady=5)
    
    def create_image_input(self):
        self.label = tk.Label(self.input_frame, text="Select Image File:", font=("Helvetica", 14), bg='#f0f0f0')
        self.label.pack(pady=10)
        self.entry = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry.pack(pady=5, ipadx=0, ipady=5)
        self.button_browse = tk.Button(self.input_frame, text="Browse", command=self.browse_image, font=("Helvetica", 10), bg='#0078d7', fg='white', bd=0, relief="flat", activebackground='#0056b3', activeforeground='white', cursor="hand2")
        self.button_browse.pack(pady=5, ipadx=10, ipady=5)
    
    def create_sms_input(self):
        self.label1 = tk.Label(self.input_frame, text="Phone Number:", font=("Helvetica", 14), bg='#f0f0f0')
        self.label1.pack(pady=5)
        self.entry1 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry1.pack(pady=5, ipadx=0, ipady=5)
        
        self.label2 = tk.Label(self.input_frame, text="Message:", font=("Helvetica", 14), bg='#f0f0f0')
        self.label2.pack(pady=5)
        self.entry2 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry2.pack(pady=5, ipadx=0, ipady=5)
    
    def create_email_input(self):
        self.label1 = tk.Label(self.input_frame, text="Email Address:", font=("Helvetica", 14), bg='#f0f0f0')
        self.label1.pack(pady=5)
        self.entry1 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry1.pack(pady=5, ipadx=0, ipady=5)
        
        self.label2 = tk.Label(self.input_frame, text="Message:", font=("Helvetica", 14), bg='#f0f0f0')
        self.label2.pack(pady=5)
        self.entry2 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry2.pack(pady=5, ipadx=0, ipady=5)
    
    def create_qr_display(self):
        self.image_label = tk.Label(self.root, bg='#f0f0f0')
        self.image_label.pack(pady=10)
    
    def create_buttons(self):
        self.button_generate = tk.Button(self.root, text="Generate QR Code", command=self.generate_qr, font=("Helvetica", 12), bg='#28a745', fg='white', bd=0, relief="flat", activebackground='#218838', activeforeground='white', cursor="hand2")
        self.button_generate.pack(pady=10, ipadx=20, ipady=10)
        
        self.button_save = tk.Button(self.root, text="Save QR Code", command=self.save_qr, font=("Helvetica", 12), bg='#0078d7', fg='white', bd=0, relief="flat", activebackground='#0056b3', activeforeground='white', cursor="hand2")
        self.button_save.pack_forget()
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, file_path)
    
    def upload_image_to_imgur(self, file_path):
        client_id = 'imgur_client_id
        headers = {'Authorization': f'Client-ID {client_id}'}
        url = "https://api.imgur.com/3/upload"
        with open(file_path, 'rb') as image_file:
            response = requests.post(url, headers=headers, files={'image': image_file})
        if response.status_code == 200:
            return response.json()['data']['link']
        else:
            return None
    
    def generate_qr(self):
        option = self.option_var.get()
        data = ""
        
        if option == "URL":
            data = self.entry.get()
        elif option == "Wi-Fi":
            ssid = self.entry1.get()
            password = self.entry2.get()
            encryption = self.entry3.get()
            data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
        elif option == "Image":
            file_path = self.entry.get()
            if file_path:
                imgur_url = self.upload_image_to_imgur(file_path)
                if imgur_url:
                    data = imgur_url
                else:
                    messagebox.showerror("Upload Error", "Failed to upload image to Imgur.")
                    return
        elif option == "SMS":
            number = self.entry1.get()
            message = self.entry2.get()
            data = f"SMSTO:{number}:{message}"
        elif option == "Email":
            email = self.entry1.get()
            message = self.entry2.get()
            data = f"mailto:{email}?body={message}"
        
        if data:
            qr = qrcode.make(data)
            qr = qr.resize((200, 200), Image.LANCZOS)
            self.qr_image = qr
            qr_image_tk = ImageTk.PhotoImage(qr)
            self.image_label.config(image=qr_image_tk)
            self.image_label.image = qr_image_tk
            self.button_save.pack(pady=10, ipadx=20, ipady=10)
        else:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
        
        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
    
    def save_qr(self):
        if self.qr_image:
            default_filename = "qr_code.png"
            file_path = filedialog.asksaveasfilename(initialfile=default_filename, defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.qr_image.save(file_path)
                messagebox.showinfo("Save QR Code", "QR code saved successfully!")
        else:
            messagebox.showwarning("Save Error", "No QR code to save. Please generate a QR code first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
