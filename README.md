
# Python QR Code Generator

A simple QR code generator made with Python. This application allows you to generate QR codes for various types of data including URLs, Wi-Fi credentials, images, SMS, and emails. It provides an intuitive graphical user interface with icons for easy navigation.

## Features

- **Generate QR Codes for Different Types of Data**:
  - **URL**: Create a QR code for a URL.
  - **Wi-Fi**: Generate a QR code for Wi-Fi credentials, including network name, password, and encryption type.
  - **Image**: Upload an image to Imgur and generate a QR code for the image URL.
  - **SMS**: Create a QR code for sending an SMS to a specific number with a predefined message.
  - **Email**: Generate a QR code to send an email with a predefined message.

- **User-Friendly Interface**:
  - Custom menu with icons for different QR code types.
  - Dynamic input fields that change based on the selected QR code type.
  - Real-time display of the generated QR code.
  - Options to save the generated QR code as an image file.

## Installation

### Prerequisites

- Python 3.x
- Required Python packages: `qrcode`, `Pillow`, `requests`, `tkinter`

### Installing Dependencies

Install the necessary packages using pip:

```
pip install qrcode[pil] Pillow requests
```

### Running the Application

```
python qr-gen.py
```
## Rendering Executable

To create an executable file, use PyInstaller:

```
pyinstaller --name app-name --onefile --noconsole qr-gen.py
```

This command will generate a standalone executable in the `dist` directory.

## Obtaining Imgur Client ID

To upload images to Imgur, you need to register an application with Imgur to get a Client ID.

1. Go to the [Imgur API Registration Page](https://api.imgur.com/oauth2/addclient).
2. Register your application with "OAuth 2 authorization without a callback URL".
3. Obtain your Client ID.

## Instructions for Using the App

1. **Launch the Application**:
   - Open the application (either by running the Python script or the generated executable).

2. **Select QR Code Type**:
   - Use the menu at the top to select the type of QR code you want to generate (URL, Wi-Fi, Image, SMS, Email).

3. **Enter Data**:
   - Based on the selected QR code type, input the required data in the provided fields.

4. **Generate QR Code**:
   - Click the "Generate QR Code" button to generate and display the QR code.

5. **Save QR Code**:
   - Click the "Save QR Code" button to save the generated QR code as an image file.

## Screenshots

![QR Code Generator](screenshot.png)

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
