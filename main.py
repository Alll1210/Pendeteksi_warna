import cv2
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Fungsi untuk membaca data warna dari file CSV
def read_colors_from_csv(csv_file):
    colors_df = pd.read_csv(csv_file)
    return colors_df

# Fungsi untuk mencari warna yang sesuai dengan warna yang terdeteksi
def detect_color(frame, colors_df):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    average_color = np.mean(frame_rgb, axis=(0, 1))
    
    min_diff = float('inf')
    detected_color = None

    for index, row in colors_df.iterrows():
        csv_color = np.array([row['RGB_R'], row['RGB_G'], row['RGB_B']])
        color_diff = np.linalg.norm(average_color - csv_color)
        
        if color_diff < min_diff:
            min_diff = color_diff
            detected_color = row['Name']
    
    return detected_color

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Fungsi untuk memperbarui tampilan
def update_interface():
    ret, frame = cap.read()

    if ret:
        detected_color = detect_color(frame, colors_df)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)
        video_frame.config(image=img)
        video_frame.image = img
        color_label.config(text=f"Detected Color: {detected_color}")
    
    root.after(10, update_interface)

# Baca data warna dari file CSV
colors_df = read_colors_from_csv('colors.csv')

# Buat jendela Tkinter
root = tk.Tk()
root.title("Color Detection")

# Buat label untuk frame video dengan border
video_frame = tk.Label(root, borderwidth=2, relief="solid")
video_frame.pack(padx=10, pady=10)

# Buat label untuk warna yang terdeteksi
color_label = tk.Label(root, text="Detected Color: ", font=("Helvetica", 16))
color_label.pack(pady=10)

# Fungsi untuk menutup kamera dan jendela Tkinter saat tombol "Esc" ditekan
def close_app(event):
    if event.keysym == 'Escape':
        cap.release()
        root.destroy()

root.bind('<Key>', close_app)

update_interface()
root.mainloop()
