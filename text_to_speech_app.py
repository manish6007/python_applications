import tkinter as tk
from tkinter import filedialog
from gtts import gTTS
import time

conversion_in_progress = False
start_time = 0

def read_file_into_variable(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def text_to_speech_hindi(input_text, output_file):
    try:
        # Specify the language for Hindi
        language = 'hi'

        # Create a gTTS object
        tts = gTTS(text=input_text, lang=language, slow=False)

        # Start counting the time
        global start_time
        start_time = time.time()

        # Save the audio to an mp3 file
        tts.save(output_file)

        # Stop counting the time and calculate the elapsed seconds
        elapsed_seconds = int(time.time() - start_time)
        return True, elapsed_seconds
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, 0

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        input_text = read_file_into_variable(file_path)
        if input_text:
            input_text_entry.delete('1.0', tk.END)
            input_text_entry.insert(tk.END, input_text)
            output_file = file_path.replace(".txt", ".mp3")
            convert_button.config(state=tk.NORMAL)
            status_label.config(text=f"Selected file: {file_path}")

def convert_to_mp3_button_clicked():
    global conversion_in_progress
    if not conversion_in_progress:
        input_text = input_text_entry.get("1.0", tk.END)
        if input_text:
            output_file = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
            if output_file:
                conversion_in_progress = True
                success, elapsed_seconds = text_to_speech_hindi(input_text, output_file)
                if success:
                    status_label.config(text=f"Speech generated and saved as: {output_file}")
                    update_counter(elapsed_seconds)
                else:
                    status_label.config(text="An error occurred during conversion.")
                conversion_in_progress = False
                convert_button.config(state=tk.NORMAL)

def update_counter(seconds):
    if conversion_in_progress:
        elapsed_seconds = int(time.time() - start_time)
        counter_label.config(text=f"Time taken: {elapsed_seconds} seconds")
        counter_label.after(1000, update_counter, elapsed_seconds)

# Create the main Tkinter window
app = tk.Tk()
app.title("Text-to-Speech Hindi Converter")

# Create a button to select the text file
select_file_button = tk.Button(app, text="Select Text File", command=select_file)
select_file_button.pack(pady=10)

# Create a text entry for input text
input_text_entry = tk.Text(app, height=10, wrap=tk.WORD)
input_text_entry.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a "Convert to MP3" button
convert_button = tk.Button(app, text="Convert to MP3", command=convert_to_mp3_button_clicked, state=tk.DISABLED)
convert_button.pack(pady=10)

# Create a label to display status
status_label = tk.Label(app, text="", fg="green")
status_label.pack()

# Create a label to display the conversion time
counter_label = tk.Label(app, text="Time taken: 0 seconds", fg="blue")
counter_label.pack()

# Start the Tkinter main loop
app.mainloop()
