import customtkinter as ctk

from loading_screen import LoadingScreen
from eye_rest import EyeRestApp

# Loading Screen ---------------------------------------------------------------------------------
loading_screen = LoadingScreen(duration=2)
loading_screen.show()

# Software (Main GUI) ---------------------------------------------------------------------------------------
root = ctk.CTk()
app = EyeRestApp(root)
root.mainloop()