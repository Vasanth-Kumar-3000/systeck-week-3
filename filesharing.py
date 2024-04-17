import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import os
from cryptography.fernet import Fernet

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8000

# Encryption key
KEY = b'YOUR_ENCRYPTION_KEY_HERE'  # Replace with a secure key
CIPHER = Fernet(KEY)

# User credentials (for demo purposes)
USERS = {
    'username': 'password'
}

# GUI setup
root = tk.Tk()
root.title("File Sharing App")

# User authentication
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in USERS and USERS[username] == password:
        messagebox.showinfo("Login", "Login successful!")
        login_window.destroy()
        main_window()
    else:
        messagebox.showerror("Login", "Invalid username or password")

login_window = tk.Toplevel(root)
login_window.title("Login")

username_label = tk.Label(login_window, text="Username:")
username_label.pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

password_label = tk.Label(login_window, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack()

# Main window
def main_window():
    main_win = tk.Toplevel(root)
    main_win.title("File Sharing App")

    # File upload
    def upload_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            encrypted_data = CIPHER.encrypt(file_data)

            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((SERVER_IP, SERVER_PORT))
                client_socket.send(b'upload')
                client_socket.send(os.path.basename(file_path).encode())
                client_socket.send(encrypted_data)
                messagebox.showinfo("Upload", "File uploaded successfully")
            except Exception as e:
                messagebox.showerror("Upload", f"Error uploading file: {str(e)}")
            finally:
                client_socket.close()

    upload_button = tk.Button(main_win, text="Upload File", command=upload_file)
    upload_button.pack()

    # File download
    def download_file():
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))
            client_socket.send(b'list')
            file_list = client_socket.recv(1024).decode().split('\n')

            selected_file = tk.simpledialog.askstring("Download", "Enter the file name to download", parent=main_win)
            if selected_file in file_list:
                client_socket.send(b'download')
                client_socket.send(selected_file.encode())
                encrypted_data = client_socket.recv(1024)
                decrypted_data = CIPHER.decrypt(encrypted_data)

                save_path = filedialog.asksaveasfilename(defaultextension=".txt")
                if save_path:
                    with open(save_path, 'wb') as file:
                        file.write(decrypted_data)
                    messagebox.showinfo("Download", "File downloaded successfully")
            else:
                messagebox.showerror("Download", "Invalid file name")
        except Exception as e:
            messagebox.showerror("Download", f"Error downloading file: {str(e)}")
        finally:
            client_socket.close()

    download_button = tk.Button(main_win, text="Download File", command=download_file)
    download_button.pack()

    # List files
    def list_files():
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))
            client_socket.send(b'list')
            file_list = client_socket.recv(1024).decode().split('\n')
            messagebox.showinfo("File List", "\n".join(file_list))
        except Exception as e:
            messagebox.showerror("File List", f"Error retrieving file list: {str(e)}")
        finally:
            client_socket.close()

    list_files_button = tk.Button(main_win, text="List Files", command=list_files)
    list_files_button.pack()

# Start the GUI event loop
root.mainloop()