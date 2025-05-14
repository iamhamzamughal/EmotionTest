import cv2
import os
import time
import pandas as pd
import random
import numpy as np
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from PIL import ImageTk, Image
import ctypes

# Function to extract the image name without the digits
def extract_image_name(filename):
    return ''.join([i for i in filename if not i.isdigit()])

# Get the screen width and height
screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

x = int((screen_width - 1000) / 2)
y = int((screen_height - 780) / 2)

window = Tk()
window.title("Emotion Recognition Test")
window.geometry("1000x700")
window.wm_geometry(f"+{x}+{y}")
window.configure(bg="#2e94b9")

# Create a DataFrame to store the collected data
data = pd.DataFrame(columns=["Image", "Gender", "Time", "Option Selected", "Correct", "Correct Emotion"])

folder_path = "images/"
emotions = ["Surprise", "Disgust", "Anger", "Happy", "Fear", "Sad"]

current_image = None
selected_option = None
correct_emotion = None
total_time = 0
total_images = 0
total_correct = 0
response_timer = None
start_time = None

# Get list of image files
images = [filename for filename in os.listdir(folder_path) if filename.endswith((".jpg", ".jpeg", ".png"))]
random.shuffle(images)

# Create radio buttons for gender selection
gender = StringVar(window)
gender.set("Male")
male_radio = Radiobutton(window, text="Male", variable=gender, value="Male", bg="#2e94b9", font=("Arial", 14), selectcolor="black", fg="white", activebackground="white")
female_radio = Radiobutton(window, text="Female", variable=gender, value="Female", bg="#2e94b9", font=("Arial", 14), selectcolor="black", fg="white", activebackground="white")

instructions_label_heading = Label(window, text="\nInstructions", bg="#2e94b9", font=("Arial", 14, "bold"), fg="white")
instructions_label = Label(window, text=(
    "\nThis test analyzes a person's ability to recognize emotions. During this experimental task, you will be shown "
    "pictures of faces on the screen. Each face will display one of the following six emotions: happiness, sadness, "
    "surprise, fear, disgust, and anger. Please note that the emotional face will be presented briefly.\n\n"
    "Your task is to carefully observe each face and determine which emotion it displays. After a few seconds, you "
    "will see a field on the screen where you can select the emotion you just saw by clicking on the appropriate label.\n\n"
    "You will have ten seconds to provide your answer for each face. Pay close attention to the screen to avoid "
    "missing any pictures. The test will take approximately 10 minutes to complete."),
    font=("Arial", 12), wraplength=window.winfo_screenwidth(), bg="#2e94b9", fg="white")

image_label = Label(window, bg="#2e94b9")

emotion_buttons = []
for emotion in emotions:
    button = Button(window, text=emotion, command=lambda emotion=emotion: select_option(emotion),
                    padx=20, pady=6, width=10, font=("calibri", 14), bg="#acdcee", bd=2, relief="raised",
                    borderwidth=0, highlightthickness=2)
    emotion_buttons.append(button)

emotion_heading_label = Label(window, text="\n\n\n\n\nPlease Select Emotion\n", font=("Arial", 14, "bold"), bg="#2e94b9", fg="white")

def select_option(option):
    global selected_option, current_image, correct_emotion, total_time, total_correct, response_timer
    global start_time

    if response_timer:
        window.after_cancel(response_timer)

    selected_option = option
    image_name = extract_image_name(current_image)
    extracted_emotion = image_name.replace(".jpeg", "").replace(".jpg", "")
    correct = option.lower() == extracted_emotion.lower()
    time_taken = (datetime.now() - start_time).total_seconds() * 1000

    new_data = pd.DataFrame([[current_image, gender.get(), round(time_taken, 2), option, correct, extracted_emotion]],
                            columns=["Image", "Gender", "Time(ms)", "Option Selected", "Score", "Correct Emotion"])

    existing_data = pd.read_excel("emotion_data.xlsx") if os.path.isfile("emotion_data.xlsx") else pd.DataFrame()
    data_combined = pd.concat([existing_data, new_data], ignore_index=True)

    emotion_columns = list(set(data_combined["Correct Emotion"].astype(str).str.lower()))
    for emotion in emotion_columns:
        data_combined[emotion] = data_combined.apply(
            lambda row: 1 if row["Score"] and str(row["Correct Emotion"]).lower() == emotion else 0, axis=1)

    data_combined.to_excel("emotion_data.xlsx", index=False)
    total_time += round(time_taken, 2)
    total_correct += correct

    show_next_image()

def show_next_image():
    global current_image, correct_emotion, start_time, total_images, response_timer

    if len(images) == 0:
        show_summary()
        window.destroy()
        return

    for button in emotion_buttons:
        button.pack_forget()
    emotion_heading_label.pack_forget()

    blank_img = np.zeros((600, 600, 3), dtype=np.uint8)
    pil_blank_img = Image.fromarray(blank_img)
    blank_photo = ImageTk.PhotoImage(pil_blank_img)
    image_label.configure(image=blank_photo)
    image_label.image = blank_photo
    image_label.pack(pady=70)
    window.update()
    time.sleep(1)
    image_label.pack_forget()

    current_image = images.pop(0)
    img = cv2.imread(os.path.join(folder_path, current_image))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (600, 600))
    pil_img = Image.fromarray(img)
    photo = ImageTk.PhotoImage(pil_img)

    image_label.configure(image=photo)
    image_label.image = photo
    image_label.pack(pady=70)
    window.update()
    time.sleep(1.5)
    image_label.pack_forget()

    image_label.configure(image=blank_photo)
    image_label.image = blank_photo
    image_label.pack(pady=70)
    window.update()
    time.sleep(0.5)
    image_label.pack_forget()

    emotion_heading_label.pack()
    for button in emotion_buttons:
        button.pack(pady=10)

    response_timer = window.after(10000, lambda: select_option("No Response"))
    start_time = datetime.now()
    correct_emotion = extract_image_name(current_image)
    total_images += 1

def show_summary():
    global total_time, total_correct

    summary_data = pd.DataFrame(
        [["Total", "", total_time, "", total_correct, "", total_images]],
        columns=["Image", "Gender", "Time(ms)", "Option Selected", "Score", "Correct Emotion", "Total Images"])

    data = pd.read_excel("emotion_data.xlsx") if os.path.isfile("emotion_data.xlsx") else pd.DataFrame()
    data = pd.concat([data, summary_data], ignore_index=True)

    if "nan" in data.columns:
        data.drop("nan", axis=1, inplace=True)

    data.to_excel("emotion_data.xlsx", index=False)

def start_image_display():
    instructions_label_heading.pack_forget()
    instructions_label.pack_forget()
    gender_heading_label.pack_forget()
    female_radio.place_forget()
    male_radio.place_forget()
    male_radio.pack_forget()
    female_radio.pack_forget()
    start_button.pack_forget()
    show_next_image()

# UI Setup
instructions_label_heading.pack()
instructions_label.pack()
gender_heading_label = Label(window, text="\n\nPlease Select Gender\n", font=("Arial", 14, "bold"), bg="#2e94b9", fg="white")
gender_heading_label.pack()
male_radio.pack()
female_radio.pack()
male_radio.place(relx=0.5, rely=0.5, anchor=CENTER, x=-60, y=-10)
female_radio.place(relx=0.5, rely=0.5, anchor=CENTER, x=50, y=-10)

image_label.pack()
start_button = Button(window, text="START", width=7, command=start_image_display, padx=25, pady=6,
                      font=("calibri", 14), bg="#acdcee", bd=2, relief="raised", borderwidth=0, highlightthickness=2)
start_button.pack(pady=30)

window.mainloop()