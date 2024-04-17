import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyttsx3
import threading

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# GUI setup
root = tk.Tk()
root.title("Text-to-Speech App")

# Text input
text_label = tk.Label(root, text="Enter text:")
text_label.pack()

text_entry = tk.Text(root, width=40, height=10)
text_entry.pack()

# Language and voice selection
language_label = tk.Label(root, text="Select language:")
language_label.pack()

languages = [lang.name for lang in pyttsx3.engine.Engine().getProperty('languages')]
selected_language = tk.StringVar()
selected_language.set(languages[0])  # Set the first language as default

language_dropdown = ttk.Combobox(root, textvariable=selected_language, values=languages, state='readonly')
language_dropdown.pack()

voice_label = tk.Label(root, text="Select voice:")
voice_label.pack()

voices = engine.getProperty('voices')
voices_names = [f"{voice.name} ({voice.languages[0]})" for voice in voices]
selected_voice = tk.StringVar()
selected_voice.set(voices_names[0])  # Set the first voice as default

voice_dropdown = ttk.Combobox(root, textvariable=selected_voice, values=voices_names, state='readonly')
voice_dropdown.pack()

# Speech parameter adjustment
rate_label = tk.Label(root, text="Speech rate:")
rate_label.pack()

rate_value = tk.DoubleVar()
rate_value.set(engine.getProperty('rate'))
rate_scale = tk.Scale(root, from_=50, to=300, orient='horizontal', variable=rate_value)
rate_scale.pack()

pitch_label = tk.Label(root, text="Pitch:")
pitch_label.pack()

pitch_value = tk.DoubleVar()
pitch_value.set(engine.getProperty('pitch'))
pitch_scale = tk.Scale(root, from_=0, to=2, resolution=0.1, orient='horizontal', variable=pitch_value)
pitch_scale.pack()

volume_label = tk.Label(root, text="Volume:")
volume_label.pack()

volume_value = tk.DoubleVar()
volume_value.set(engine.getProperty('volume'))
volume_scale = tk.Scale(root, from_=0, to=1, resolution=0.1, orient='horizontal', variable=volume_value)
volume_scale.pack()

# Playback controls
def speak_text():
    text = text_entry.get("1.0", "end-1c")
    if text:
        engine.setProperty('rate', rate_value.get())
        engine.setProperty('pitch', pitch_value.get())
        engine.setProperty('volume', volume_value.get())
        engine.setProperty('voice', voices[voice_dropdown.current()].id)
        
        threading.Thread(target=engine.say, args=(text,)).start()
        threading.Thread(target=engine.runAndWait).start()

speak_button = tk.Button(root, text="Speak", command=speak_text)
speak_button.pack()

def save_audio():
    text = text_entry.get("1.0", "end-1c")
    if text:
        engine.setProperty('rate', rate_value.get())
        engine.setProperty('pitch', pitch_value.get())
        engine.setProperty('volume', volume_value.get())
        engine.setProperty('voice', voices[voice_dropdown.current()].id)
        
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            engine.save_to_file(text, file_path)
            engine.runAndWait()
            messagebox.showinfo("Success", "Audio file saved successfully.")
        else:
            messagebox.showwarning("Warning", "No file path selected.")

save_button = tk.Button(root, text="Save Audio", command=save_audio)
save_button.pack()

# Word counting
def count_words():
    text = text_entry.get("1.0", "end-1c")
    words = len(text.split())
    messagebox.showinfo("Word Count", f"The text contains {words} words.")

word_count_button = tk.Button(root, text="Count Words", command=count_words)
word_count_button.pack()

# Clear text
def clear_text():
    text_entry.delete("1.0", "end")

clear_button = tk.Button(root, text="Clear Text", command=clear_text)
clear_button.pack()

# Start the GUI event loop
root.mainloop()