import wave
import time
import threading
import pyaudio
from tkinter import Tk, Button, Label, Menu, messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror


class Audiorecorder:

	def __init__(self):
		self.root = Tk()
		self.root.resizable(False, False)
		self.root.title("Аудіозаписувач")
		self.button = Button(text="🎙", font=("Arial", 110),
		                     command=self.handler)
		self.button.pack()
		self.label = Label(text="00:00:00")
		self.label.pack()
		self.main_menu = Menu()
		self.main_menu.add_cascade(label="Інформація", command=self.info)
		self.root.config(menu=self.main_menu)
		self.recording = False
		self.root.mainloop()

	def info(self):
		messagebox.showinfo("Інформація",
		                    'Аудіозаписувач на Python.\nНатисніть на мікрофон і записуйте звук ')

	def handler(self):
		if self.recording:
			self.recording = False
			self.button.config(fg="black")
		else:
			self.recording = True
			self.button.config(fg="red")
			threading.Thread(target=self.record).start()

	def record(self):
		audio = pyaudio.PyAudio()
		stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

		frames = []

		start = time.time()

		while self.recording:
			data = stream.read(1024)
			frames.append(data)

			passed = time.time() - start
			secs = passed % 60
			mins = passed // 60
			hours = mins // 60
			self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

		stream.stop_stream()
		stream.close()
		audio.terminate()

		try:
			file = asksaveasfilename(defaultextension=".wav", filetypes=(
				("Waveform Audio File Format", "*.wav"),
				("MP3", "*.MP3"),
				("All files", "*.*"),
			))
			with wave.open(file, "wb") as sound_file:
				sound_file.setnchannels(1)
				sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
				sound_file.setframerate(44100)
				sound_file.writeframes(b"".join(frames))
				sound_file.close()
		except Exception:
			showerror(title="Помилка", message="Помилка збереження файлу")


if __name__ == "__main__":
	Audiorecorder()
