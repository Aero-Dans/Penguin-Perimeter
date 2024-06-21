import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
import subprocess

def run_file(root):
    try:
        subprocess.run(["python", "main.py"], check=True)
        messagebox.showinfo("Success", "The script ran successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while running the script: {e}")
    finally:
        root.destroy()

def create_menu():
    root = tk.Tk()
    root.geometry("1080x720")

    # Load the background image
    background_image = Image.open("assets/images/startmenu.png")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a label to display the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # Create a frame to hold the buttons and center it
    frame = tk.Frame(root, bg='white')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Add Start button
    start_button = tk.Button(frame, text="Start", font=("Comic Sans.. MS", 16), command=lambda: run_file(root))
    start_button.pack(pady=10)

    # Add Quit button
    quit_button = tk.Button(frame, text="Quit", font=("Comic Sans MS", 16), command=root.quit)
    quit_button.pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    create_menu()

