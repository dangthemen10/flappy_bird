import qrcode
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image

# Creating the window
win = Tk()
win.title('QR Code Generator')
win.geometry('650x800')
win.config(bg='DarkTurquoise')

# Function to generate the QR code and save it
def generateCode():
    # Creating a QRCode object of the size specified by the user
    qr = qrcode.QRCode(version=int(size.get()), box_size=10, border=5)
    qr.add_data(text.get())  # Adding the data to be encoded to the QRCode object
    qr.make(fit=True)  # Making the entire QR Code space utilized

    # Customize the QR Code color
    img = qr.make_image(fill_color='blue', back_color='lightgreen')  # Generating the QR Code with colors

    # Automatically save the QR code in the current directory for display
    filePath = name.get() + '.png'  # Full path to the file
    img.save(filePath)  # Saving the QR Code

    # Displaying success message
    messagebox.showinfo("QR Code Generator", "QR Code is generated successfully!")

    # Display the QR code on the heading frame
    qr_image = Image.open(filePath)  # Open the saved image
    qr_image = qr_image.resize((200, 200), Image.LANCZOS)  # Resize the image to fit in the frame (using LANCZOS)
    qr_photo = ImageTk.PhotoImage(qr_image)
    headingLabel.config(image=qr_photo)  # Displaying image on label (heading frame)
    headingLabel.image = qr_photo  # Keep reference to the image

    # Enable the download button
    download_button.config(state=NORMAL)

# Function to download the QR code
def downloadCode():
    # Get the name for the file from the input field
    file_name = name.get()
    if not file_name:  # Check if the name is empty
        messagebox.showwarning("Warning", "Please enter a name for the QR Code.")
        return

    # Ask the user where to save the QR code image
    filePath = filedialog.asksaveasfilename(defaultextension=".png", 
                                              initialfile=f"{file_name}.png",
                                              filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if filePath:  # Proceed if a valid file path is provided
        img = qrcode.QRCode(version=int(size.get()), box_size=10, border=5)
        img.add_data(text.get())  # Adding the data to be encoded to the QRCode object
        img.make(fit=True)  # Making the entire QR Code space utilized
        qr_image = img.make_image(fill_color='blue', back_color='lightgreen')  # Customize colors
        qr_image.save(filePath)  # Save the QR code at the specified path
        messagebox.showinfo("Download", f'QR Code downloaded successfully to {filePath}')

# Label for the window and QR display area
headingFrame = Frame(win, bg="azure", bd=5)
headingFrame.place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.35)  # Made it larger to fit the QR code
headingLabel = Label(headingFrame, text="Generate QR Code", bg='azure', font=('Times', 20, 'bold'))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

# Taking the input of the text or URL to get QR code
Frame1 = Frame(win, bg="DarkTurquoise")
Frame1.place(relx=0.1, rely=0.4, relwidth=0.7, relheight=0.15)

label1 = Label(Frame1, text="Enter the text/URL: ", bg="DarkTurquoise", fg='azure', font=('FiraMono', 13, 'bold'))
label1.place(relx=0.05, rely=0.2, relheight=0.2)

text = Entry(Frame1, font=('Century 12'))
text.place(relx=0.05, rely=0.5, relwidth=1, relheight=0.4)

# Getting input of the QR Code image name 
Frame3 = Frame(win, bg="DarkTurquoise")
Frame3.place(relx=0.1, rely=0.55, relwidth=0.7, relheight=0.15)

label3 = Label(Frame3, text="Enter the name of the QR Code: ", bg="DarkTurquoise", fg='azure', font=('FiraMono', 13, 'bold'))
label3.place(relx=0.05, rely=0.2, relheight=0.2)

name = Entry(Frame3, font=('Century 12'))
name.place(relx=0.05, rely=0.5, relwidth=1, relheight=0.4)

# Getting the input of the size of the QR Code
Frame4 = Frame(win, bg="DarkTurquoise")
Frame4.place(relx=0.1, rely=0.7, relwidth=0.7, relheight=0.15)

label4 = Label(Frame4, text="Enter the size from 1 to 40 (1 is 21x21): ", bg="DarkTurquoise", fg='azure', font=('FiraMono', 13, 'bold'))
label4.place(relx=0.05, rely=0.2, relheight=0.2)

size = Entry(Frame4, font=('Century 12'))
size.place(relx=0.05, rely=0.5, relwidth=0.5, relheight=0.4)

# Button to generate and save the QR Code
button = Button(win, text='Generate Code', font=('FiraMono', 15, 'normal'), command=generateCode)
button.place(relx=0.35, rely=0.85, relwidth=0.25, relheight=0.05)

# Button to download the QR Code
download_button = Button(win, text='Download Code', font=('FiraMono', 15, 'normal'), command=downloadCode, state=DISABLED)
download_button.place(relx=0.65, rely=0.85, relwidth=0.25, relheight=0.05)

# Runs the window till it is closed manually
win.mainloop()
