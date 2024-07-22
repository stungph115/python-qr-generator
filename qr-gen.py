import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk
import requests
import os

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator by Tung PHAM")
        self.root.configure(bg='#f0f0f0')

        # Set the favorite icon for the taskbar and title bar
        self.set_favorite_icon()

        self.qr_image = None
        self.selected_button = None

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=6, relief="flat", focuscolor="none", borderwidth=0)
        style.map("TButton",
                  background=[('!active', '!pressed', '#0078d7'), ('pressed', '#0056b3'), ('active', '#0056b3')],
                  foreground=[('!active', '!pressed', 'white'), ('pressed', 'white'), ('active', 'white')])

        # Create frames in the correct order
        self.create_menu()
        self.create_description_frame()
        self.create_input_frame()
        self.create_qr_display()
        self.create_buttons()

        # Ensure input fields are updated for the initially selected option
        self.update_input_fields(self.option_var.get())

        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

    def set_favorite_icon(self):
        icon_path_ico = os.path.join('assets', 'favicon.ico')
        try:
            self.root.iconbitmap(icon_path_ico)
        except Exception as e:
            print(f"Failed to load favorite icon: {e}")

    def create_menu(self):
        self.option_var = tk.StringVar(value="URL")
        options = [("URL", "link.png"), ("Wi-Fi", "wifi.png"), ("Image", "photo.png"), ("SMS", "sms.png"), ("Email", "email.png")]
        self.menu_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.menu_frame.pack(pady=10, anchor='n')

        self.buttons = {}
        for option, image_file in options:
            image_path = os.path.join('assets', image_file)
            image = Image.open(image_path)
            image = image.resize((50, 50), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            button = tk.Label(self.menu_frame, image=photo, text=option, compound="top", font=("Helvetica", 12), bg='#f0f0f0', bd=0)
            button.image = photo
            button.bind("<Enter>", lambda event, b=button, o=option, img=image_file: self.on_hover(event, b, img))
            button.bind("<Leave>", lambda event, b=button, o=option, img=image_file: self.on_leave(event, b, img))
            button.bind("<Button-1>", lambda event, opt=option: self.update_input_fields(opt))
            button.pack(side=tk.LEFT, padx=15, pady=5)  # Adjust padx and pady for padding
            self.buttons[option] = button

        self.menu_frame.pack(pady=10, anchor='n')

    def on_hover(self, event, button, image_file):
        button.config(cursor="hand2")

    def on_leave(self, event, button, image_file):
        button.config(cursor="")

    def update_input_fields(self, option):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        if self.selected_button:
            prev_button = self.buttons[self.selected_button]
            prev_button.config(bg='#f0f0f0')
            image_file = [img for opt, img in [("URL", "link.png"), ("Wi-Fi", "wifi.png"), ("Image", "photo.png"), ("SMS", "sms.png"), ("Email", "email.png")] if opt == self.selected_button][0]
            image_path = os.path.join('assets', image_file)
            image = Image.open(image_path)  
            image = image.resize((50, 50), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            prev_button.config(image=photo)
            prev_button.image = photo
            prev_button.config(cursor="")

        self.selected_button = option
        selected_button = self.buttons[option]
        selected_button.config(bg='#d0d0d0')
        image_file = [img for opt, img in [("URL", "link.png"), ("Wi-Fi", "wifi.png"), ("Image", "photo.png"), ("SMS", "sms.png"), ("Email", "email.png")] if opt == option][0]
        image_path = os.path.join('assets', image_file)
        image = Image.open(image_path)
        image = image.resize((60, 60), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        selected_button.config(image=photo)
        selected_button.image = photo

        self.option_var.set(option)
        self.update_description(option)
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

    def create_description_frame(self):
        self.description_label = tk.Label(self.root, text="", font=("Helvetica", 14, "italic"), bg='#f0f0f0', wraplength=600, justify=tk.LEFT, anchor="w", padx=20, pady=10)
        self.description_label.pack(pady=10, padx=50, fill='x')

    def update_description(self, option):
        descriptions = {
            "URL": "* Enter a URL that you want to encode into a QR code. \n\n** When scanned, the QR code will open the specified URL in a web browser.",
            "Wi-Fi": "* Enter the Wi-Fi network details: Network Name (SSID), Password, and Encryption type (WEP/WPA). \n\n** The generated QR code will allow users to connect to the specified Wi-Fi network.",
            "Image": "* Select an image file from your computer. \n\n** The image will be uploaded to Imgur, and the generated QR code will link to the uploaded image.",
            "SMS": "* Enter a phone number and a message. \n\n** When scanned, the QR code will open the user's SMS app with the specified number and message pre-filled.",
            "Email": "* Enter an email address and a message. \n\n** When scanned, the QR code will open the user's email app with the specified email address and message pre-filled."
        }
        self.description_label.config(text=descriptions.get(option, ""))

    def create_input_frame(self):
        self.input_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.input_frame.pack(pady=20, padx=20)

    def create_url_input(self):
        self.label = tk.Label(self.input_frame, text="Enter URL:", font=("Helvetica", 14, "bold"), bg='#f0f0f0')
        self.label.pack(pady=10)
        self.entry = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry.pack(pady=5, ipadx=0, ipady=5)

    def create_wifi_input(self):
        self.label1 = tk.Label(self.input_frame, text="Network Name (SSID):", font=("Helvetica", 14, "bold"), bg='#f0f0f0')
        self.label1.pack(pady=5)
        self.entry1 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry1.pack(pady=5, ipadx=0, ipady=5)

        self.label2 = tk.Label(self.input_frame, text="Password:", font=("Helvetica", 14, "bold"), bg='#f0f0f0')
        self.label2.pack(pady=5)
        self.entry2 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry2.pack(pady=5, ipadx=0, ipady=5)

        self.label3 = tk.Label(self.input_frame, text="Encryption (WEP/WPA):", font=("Helvetica", 14, "bold"), bg='#f0f0f0')
        self.label3.pack(pady=5)
        self.entry3 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry3.pack(pady=5, ipadx=0, ipady=5)

    def create_image_input(self):
        self.label = tk.Label(self.input_frame, text="Select Image File:", font=("Helvetica", 14, "bold"), bg='#f0f0f0')
        self.label.pack(pady=10)
        self.entry = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry.pack(pady=5, ipadx=0, ipady=5)
        self.button_browse = tk.Button(self.input_frame, text="Browse", command=self.browse_image, font=("Helvetica", 10), bg='#0078d7', fg='white', bd=0, relief="flat", activebackground='#0056b3', activeforeground='white', cursor="hand2")
        self.button_browse.pack(pady=5, ipadx=10, ipady=5)

    def create_sms_input(self):
        self.label1 = tk.Label(self.input_frame, text="Phone Number:", font=("Helvetica", 14, "bold"), bg='#f0f0f0')
        self.label1.pack(pady=5)
        self.entry1 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry1.pack(pady=5, ipadx=0, ipady=5)

        self.label2 = tk.Label(self.input_frame, text="Message:", font=("Helvetica", 14, "bold"), bg='#f0f0f0')
        self.label2.pack(pady=5)
        self.entry2 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry2.pack(pady=5, ipadx=0, ipady=5)

    def create_email_input(self):
        self.label1 = tk.Label(self.input_frame, text="Email Address:", font=("Helvetica", 14, "bold"), bg='#f0f0f0')
        self.label1.pack(pady=5)
        self.entry1 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry1.pack(pady=5, ipadx=0, ipady=5)

        self.label2 = tk.Label(self.input_frame, text="Message:", font=("Helvetica", 14, "bold"), bg='#f0f0f0')
        self.label2.pack(pady=5)
        self.entry2 = tk.Entry(self.input_frame, width=40, font=("Helvetica", 12), bd=1, relief="solid", highlightthickness=1, highlightcolor="#0078d7", highlightbackground="#f0f0f0")
        self.entry2.pack(pady=5, ipadx=0, ipady=5)

    def create_qr_display(self):
        self.image_label = tk.Label(self.root, bg='#f0f0f0')
        self.image_label.pack(pady=10)

    def create_buttons(self):
        self.button_generate = tk.Button(self.root, text="Generate QR Code", command=self.generate_qr, font=("Helvetica", 14, "bold"), bg='#28a745', fg='white', bd=0, relief="flat", activebackground='#218838', activeforeground='white', cursor="hand2")
        self.button_generate.pack(pady=10, ipadx=20, ipady=10)

        self.button_save = tk.Button(self.root, text="Save QR Code", command=self.save_qr, font=("Helvetica", 14, "bold"), bg='#0078d7', fg='white', bd=0, relief="flat", activebackground='#0056b3', activeforeground='white', cursor="hand2")
        self.button_save.pack_forget()

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, file_path)

    def upload_image_to_imgur(self, file_path):
        client_id = '14b245e3ca2685b'
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
