import os
from tkinter import messagebox
from pystray import Icon, Menu, MenuItem
from PIL import Image
#from keyboard import add_hotkey
from ui import AssistantApp, AddShortcutsWindow

model_flag = True
if not os.path.isdir('model'):
    #error = WarningWindow('\'Model\' folder is absent. Add folder \'Model\' with vosk model in folder with application for work of voice search')
    messagebox.showwarning(title='\'Model\' folder is absent', message='\'Model\' folder is absent. Add folder \'Model\' with vosk model in folder with application for work of voice search')
    model_flag = False
elif len(os.listdir('model')) == 0:
    #error = WarningWindow('\'Model\' folder is empty. Add vosk model to folder \'Model\' for work of voice search')
    messagebox.showwarning(title='\'Model\' folder is empty', message='\'Model\' folder is empty. Add vosk model to folder \'Model\' for work of voice search')
    model_flag = False
else:
    from voice_functions import *

def get_app_settings():
    pass

def setup_icon(icon):
    icon.visible = True

def close_tray(icon):
    icon.visible = False
    icon.stop()
    os._exit(0)

def edit_settings():
    pass

def add_note():
    note_app = AddShortcutsWindow()
    note_app.mainloop()

def voice_input():
    query = voice_command()
    app = AssistantApp(query)
    #app.mainloop()

def app_restore():
    app = AssistantApp()
    #close_tray(icon)
    #app.mainloop()

if __name__ == '__main__':
    image = Image.open('C:\\Users\\Admin\\PycharmProjects\\pythonProject1\\help.png')
    right_click_menu = Menu(
        #MenuItem('Voice Search', voice_input, enabled=True, default=True, visible=True),
        #MenuItem('Open Assistant', app_restore),
        MenuItem('Open Assistant', app_restore, enabled=True, default=True, visible=True),
        MenuItem('Voice Search', voice_input, enabled=model_flag),
        MenuItem('Add shortcut', add_note),
        MenuItem('Settings', edit_settings),
        MenuItem('Exit', lambda: close_tray(icon)))
    icon = Icon('Helper', image, 'Helper', right_click_menu)
    # add_hotkey('Ctrl+`', fast_answer)
    # greeting()
    icon.run_detached(setup_icon)