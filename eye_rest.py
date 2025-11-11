# This file contails all the logic and GUI for the eye rest reminder software

import threading
import time
import customtkinter as ctk

from tkinter import *
from tkinter import messagebox
from plyer import notification
from opencv_face import FaceDetector


class EyeRestApp:

    def __init__(self, root):
        # root => The Tkinter root window
        self.root = root
        self.root.title("Eye Rest Reminder")

        self.window_width = 500
        self.window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (self.window_width / 2))
        y_coordinate = int((screen_height / 2) - (self.window_height / 2))
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")

        ctk.set_appearance_mode("dark")
        # ctk.set_default_color_theme("364F6B")

        self.timer_time = 60  # default time in secs
        self.stop_signal = False
        self.time_counter = 0
        self.frame_counter = 0  # Used for face detection reset

        self.build_ui()

    def build_ui(self):
        self.title = ctk.CTkLabel(
            self.root,
            text="👁️ Eye Rest Reminder",
            font=("Segoe UI", 24, "bold"),
            text_color="#6096B4"
        )
        self.title.pack(pady=20)

        entry_frame = ctk.CTkFrame(self.root, corner_radius=15)
        entry_frame.pack(pady=10, padx=20, fill="x")

        self.heading = ctk.CTkLabel(
            entry_frame,
            text="Enter timer duration (minutes):",
            font=("Segoe UI", 13)
        )
        self.heading.pack(pady=(10, 5))

        self.entry = ctk.CTkEntry(
            entry_frame,
            width=120,
            height=35,
            justify="center",
            font=("Segoe UI", 14)
        )
        self.entry.pack(pady=10)
        self.entry.insert(0, str(self.timer_time // 60))

        self.time_count_label = ctk.CTkLabel(
            self.root,
            text="Time 00:00",
            font=("Segoe UI", 18, "bold"),
            text_color="#FFF8EA"
        )
        self.time_count_label.pack(pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(self.root, corner_radius=15)
        button_frame.pack(pady=15, padx=20)
        bold_font = ("Segoe UI", 14, "bold")

        ctk.CTkButton(
            button_frame, text="Start", font=bold_font, width=100, fg_color="#8D7B68", text_color="#F5F5F5",
            hover_color="#A4907C", command=self.start_timer
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(
            button_frame, text="Stop", font=bold_font, width=100, fg_color="#8D7B68", text_color="#F5F5F5",
            hover_color="#A4907C", command=self.stop_timer
        ).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(
            button_frame, text="Set Timer", font=bold_font, width=100, fg_color="#8D7B68", text_color="#F5F5F5",
            hover_color="#A4907C", command=self.get_time
        ).grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkButton(
            self.root, text="Open Face Detector", font=bold_font, width=220, text_color="#F5F5F5",
            fg_color="#8D7B68", hover_color="#A4907C",
            command=self.open_face_recognition
        ).pack(pady=20)

        # Timer Logic ----------------------------

    def get_time(self):
        try:
            value = int(self.entry.get())
            self.timer_time = value * 60
            self.heading.configure(text=f"Reminder set for {value} minute(s)")
            print(f"[DEBUG] Timer set for {self.timer_time} seconds")
        except ValueError:
            self.heading.configure(text="Please enter a valid number")

    def start_timer(self):
        if self.timer_time <= 0:
            messagebox.showwarning("Timer not set", "Please set the timer before starting!")
            return
        self.stop_signal = False
        # Run the timer function in a background thread
        threading.Thread(target=self.time_only_count, daemon=True).start()

    def stop_timer(self):
        self.stop_signal = True

    def time_only_count(self):
        """Count time and trigger reminders."""
        self.time_counter = 0
        break_duration = 20  # short break after timer ends

        while not self.stop_signal:
            time.sleep(1)
            self.time_counter += 1
            mins, secs = divmod(self.time_counter, 60)
            self.time_count_label.configure(text=f"Time {mins:02}:{secs:02}")
            self.root.update_idletasks()

            if self.time_counter >= self.timer_time:
                print("Time over — triggering reminder!")
                self.eye_rest_reminder()

                # Start break timer
                for remaining in range(break_duration, 0, -1):
                    if self.stop_signal:
                        break
                    self.time_count_label.configure(
                        text=f"Break {remaining:02} sec remaining",
                        fg="#ffcc00"
                    )
                    self.root.update_idletasks()
                    time.sleep(1)

                if not self.stop_signal:
                    self.break_over_reminder()

                # Reset for next cycle
                self.time_counter = 0
                self.time_count_label.configure(fg="#00FFAA")

    #  reminder notifications---------------------
    def eye_rest_reminder(self):
        notification.notify(title="Eye Rest Reminder", message="Time to take a break!")

    def break_over_reminder(self):
        # Show notification when break is over.
        notification.notify(title="Break Over 👁️", message="Time to focus again!")

    # face detection-----------------------------
    def open_face_recognition(self):
        # Open a new window for face detection.
        face_window = Toplevel(self.root)
        face_window.title("Face Recognition App")

        window_label = Label(face_window)
        window_label.pack()

        minute_label = Label(face_window, font="times 23")
        minute_label.pack()

        detector = FaceDetector(window_label, minute_label, self.video_time_reset)

        thread_video = threading.Thread(target=detector.start)
        thread_video.daemon = True
        thread_video.start()

    def video_time_reset(self, all_face_location):
        # Reset timer if face not detected for a while.
        if all_face_location is None or len(all_face_location) == 0:
            self.frame_counter += 1
            if self.frame_counter > 600:
                self.time_counter = 0
                self.frame_counter = 0
        else:
            self.frame_counter = 0

