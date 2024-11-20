import tkinter
import customtkinter  # <- import the CustomTkinter module


from tkinter import Tk, Label, Button, Toplevel,Entry,Frame,Canvas, Label, Frame, PhotoImage, Checkbutton, BooleanVar
from PIL import Image, ImageTk
import threading
import time
import cv2
import face_recognition
from winotify import Notification, audio
import screen_brightness_control as sbc




from tkinter import *
from tkinter import font
from PIL import ImageTk, Image

# lording screen
# ---------------------------------------------------------------------------------------------------------------------------------------
w=Tk()

#Using piece of code from old splash screen

width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
w.overrideredirect(1) #for hiding titlebar



#new window to open
frame = Frame(w, width=427, height=250, bg='#00041A')
frame.place(x=0, y=0)

bg_image = Image.open(r'D:\project\Untitled323.png')
bg_image = bg_image.resize((width_of_window, height_of_window), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)
background_label = Label(w, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)



label2=Label(w, text='Loading...', fg='white', bg='#00041A')
label2.configure(font=("warungasem", 8))
label2.place(x=187,y=140)



#making animation

image_a = Image.open(r'D:\project\Untitled123.png')
image_a = ImageTk.PhotoImage(image_a)

image_b = Image.open(r'D:\project\Ellipse 123.png')
image_b = ImageTk.PhotoImage(image_b)


for i in range(4): #5loops
    l1=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=180, y=160)
    l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=160)
    l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=160)
    l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=160)

    w.update_idletasks()
    time.sleep(0.5)

    l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=160)
    l2=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=200, y=160)
    l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=160)
    l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=160)
    w.update_idletasks()
    time.sleep(0.5)

    l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=160)
    l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=160)
    l3=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=220, y=160)
    l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=160)
    w.update_idletasks()
    time.sleep(0.5)

    l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=160)
    l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=160)
    l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=160)
    l4=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=240, y=160)
    w.update_idletasks()
    time.sleep(0.5)

w.destroy()
w.mainloop()

# softwere
# ---------------------------------------------------------------------------------------------------------------------------------------
# --------------make tk frame---------------------

# root_tk.overrideredirect(True)


#----------------------------------------------------------------------------------------------------------------------------


conterrr=0
stop_signal=0 
frame_counter = 0
time2 = 0
setBrightness = 0
value=0
timer_time=20


def get_time():
    
    globals()['value'] = int(entry.get())
    
    globals()['timer_time'] =  globals()['value']*60
    print(globals()['timer_time'])
    globals()['frame_counter'] = 0
    hedding.configure(text=f"{timer_time // 60} minute after alarm will bell")
    
    
        
def time_only_count():
    globals()['stop_signal']=0
    time2 = 0
    while True:
        if(globals()['stop_signal']==1):
            break
        time_counting_labale.configure(text=f"Time {time2 // 60}:{time2 % 60}")
        root_tk.update()  # Ensure the window updates

        time.sleep(1)
        time2 += 1
        print(time2)

        if time2 == timer_time + 1:  # Assuming timer_time is a global variable
            print("over")
            eye_rest_reminder()
            time2 = 0
       
            # break

    # time_counting_labale.configure(text=f"Time: {time2 // 60}:{time2 % 60}")
    root_tk.update()
        
   
   
    
    
def eye_rest_reminder():
    noty = Notification(app_id='Take rest', title='Eye Rest Reminder', msg='Now is the time to rest your eyes', duration='short')
    noty.set_audio(audio.LoopingAlarm, loop=True)
    noty.show()
    sbc.fade_brightness(setBrightness)
    bright_set()

def bright_set():
    duration = threading.Timer(5, reset_bright)  # brightness set to 75% after 5 seconds
    duration.daemon = True
    duration.start()

def reset_bright():
    sbc.fade_brightness(75, start=setBrightness)

def video_time_reset(all_face_location):
    global frame_counter
    if not all_face_location:
        frame_counter += 1
        if frame_counter > 60:
            globals()['time2'] = 0
            frame_counter = 0
    else:
        frame_counter = 0

def draw_facial_landmarks(frame, landmarks):
    for facial_feature in landmarks.keys():
        # Different color for each facial feature
        color = (0, 255, 0)  # Green

        # Draw points
        for point in landmarks[facial_feature]:
            x, y = point
            x *= 4
            y *= 4
            cv2.circle(frame, (x, y), 2, color, -1)

        # Draw lines connecting the points
        if len(landmarks[facial_feature]) > 1:
            for i in range(len(landmarks[facial_feature]) - 1):
                x1, y1 = landmarks[facial_feature][i]
                x2, y2 = landmarks[facial_feature][i + 1]
                x1 *= 4
                y1 *= 4
                x2 *= 4
                y2 *= 4
                cv2.line(frame, (x1, y1), (x2, y2), color, 1)

    return frame

def video_processing(window, minute_label):

    webcam_video_stream = cv2.VideoCapture(0)
    all_face_location = []

    while True:
        ret, current_frame = webcam_video_stream.read()
        current_frame_small = cv2.resize(current_frame, (0, 0), fx=0.25, fy=0.25)
        all_face_location = face_recognition.face_locations(current_frame_small, model="hog")
        
        # Use face landmarks for better accuracy
        all_face_landmarks = face_recognition.face_landmarks(current_frame_small)

        print(len(all_face_location))
        video_time_reset(all_face_location)

        for i, landmarks in zip(all_face_location, all_face_landmarks):
            current_frame = draw_facial_landmarks(current_frame, landmarks)

        # Convert the OpenCV frame to Tkinter PhotoImage
        frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)

        window.config(image=frame)
        window.image = frame  # To prevent garbage collection

        # Update the minute window
        minute_label.config(text=f"Time: {time2 // 60}:{time2 % 60}")

        # if cv2.waitKey(1) & 0xFF == ord('q'):
            # break
        cv2.waitKey(50)
        print(globals()['conterrr'])
        globals()['conterrr'] += 1
        print(globals()['time2'])

    webcam_video_stream.release()
    cv2.destroyAllWindows()


def clock(minute_label):
    while True:
        if(globals()['stop_signal']==1):
            break
       
        time_counting_labale.configure(text=f"Time: {time2 // 60}:{time2 % 60}")
        root_tk.update()
        time.sleep(1)
        globals()['time2'] += 1
        print(time2)
        if globals()['time2'] == globals()['timer_time']:
            print("over")
            eye_rest_reminder()
            globals()['time2'] = 0
       

        
        # time_counting_labale.configure(text=f"Time: {time2 // 60}:{time2 % 60}")



def open_face_recognition():
    globals()['stop_signal']=0
    
    face_recognition_window = Toplevel(root_tk)
    face_recognition_window.title("Face Recognition App")
    
    window = Label(face_recognition_window)
    window.pack()

    minute_label = Label(face_recognition_window, font="times 23")
    minute_label.pack()

    thread_video = threading.Thread(target=video_processing, args=(window, minute_label))
    thread_video.start()

    thread_clock = threading.Thread(target=clock, args=(minute_label,))
    thread_clock.start()

# --------------------------------------------------------------------------------------------------------------
# tikbutton and face detection functions

def main_function():
    checkbox_state=check_var.get()
    if checkbox_state=="on":
        print("0")
        open_face_recognition()
    else:
        time_only_count()
        

# close botton using off!
def close_app():
    root_tk.destroy()


def reset_button():
    globals()['stop_signal']=1
    globals()['value']==0
    globals()['frame_counter'] = 0
    # globals()['timer_time']=0
    globals()['time2']=0
    print("hjbh")
    time_counting_labale.configure(text=f"00:00")
    hedding.configure(text=f"Reset Time")
    root_tk.update()  # Ensure the window updates



#---------------------------------------------------------------------------------------------------------------------------

root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("400x240")
root_tk.title("BlinkEYE")



screen_width = root_tk.winfo_screenwidth()
screen_height = root_tk.winfo_screenheight()

# Calculate the position to center the window
window_width = 800
window_height = 600
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window's position at the center of the screen
root_tk.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Load the image
side_img_data = Image.open(r'C:\Users\Hashala\Desktop\chathum\peakpx.jpg')
side_img = customtkinter.CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 500))

# Create window with image
customtkinter.CTkLabel(master=root_tk, text=" ", image=side_img).pack(expand=True, side="left")

# Create frame for content
frame = customtkinter.CTkFrame(master=root_tk, width=450, height=500, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

# Create "Get Started" window
customtkinter.CTkLabel(master=frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(30, 0))






# Use CTkButton instead of tkinter Button

button_settime = customtkinter.CTkButton(master=frame, text="Set Time", corner_radius=32, fg_color="#00051b", hover_color="#b71c46",command=get_time)
button_settime.place(relx=0.75, rely=0.28, anchor=tkinter.CENTER)

button_on = customtkinter.CTkButton(master=frame, text="Turn ON", corner_radius=32, fg_color="#00051b", hover_color="#b71c46",font=("",15),command=main_function)
button_on.place(relx=0.50, rely=0.46, anchor=tkinter.CENTER)


button_off = customtkinter.CTkButton(master=frame, text="Reset", corner_radius=32, fg_color="#00051b", hover_color="#b71c46",font=("",15),command=reset_button)
button_off.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)



hedding = customtkinter.CTkLabel(master=frame,
                               text_color="black",
                               fg_color="white",
                               text=("default 20 minute"),
                               font=("",17),
                               width=120,
                               height=25,
                               corner_radius=8)
hedding.place(relx=0.5, rely=0.36, anchor=tkinter.CENTER)



time_counting_labale = customtkinter.CTkLabel(master=frame,
                               text_color="black",
                               fg_color="white",
                               text=("00:00"),
                               font=("",35),
                               width=120,
                               height=25,
                               corner_radius=8)
time_counting_labale.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)


check_var = customtkinter.StringVar(value="off")
checkbox = customtkinter.CTkCheckBox(master=frame, text="Enable with face\n detection",variable=check_var, onvalue="on", offvalue="off",checkbox_width=17,checkbox_height=17,text_color="black",fg_color="#b71c46",hover_color="#00051b")
checkbox.place(relx=0.38, rely=0.67)




entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter Time",fg_color="white",text_color="black")
entry.place(relx=0.1, rely=0.25)



root_tk.mainloop()








