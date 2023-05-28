import os
from tkinter import messagebox
from pystray import Icon, Menu, MenuItem
from PIL import Image
#from keyboard import add_hotkey
from ui import AssistantApp, AddShortcutsWindow
import json

model_flag = True
if not os.path.isdir('model'):
    messagebox.showwarning(title='\'Model\' folder is absent', message='\'Model\' folder is absent. Add folder \'Model\' with vosk model in folder with application for work of voice search')
    model_flag = False
elif len(os.listdir('model')) == 0:
    messagebox.showwarning(title='\'Model\' folder is empty', message='\'Model\' folder is empty. Add vosk model to folder \'Model\' for work of voice search')
    model_flag = False
else:
    from voice_functions import *

DEFAULT_APP_SETTINGS = {
    'app_shortcut': '',
    'energy_threshold': 450,
    'pause_threshold': 0.5,
    'adjust_for_ambient_noise': False,
    'datasheet_theme': 'light green',
    'datasheet_text_color': '',
    'datasheet_highlight_color': '',
    'datasheet_background_color': '',
    'add_window_width': 800,
    'add_window_height': 270,
    'add_window_topmost': True,
    'add_window_single': True,
    'assistant_window_width': 530,
    'assistant_window_height': 135,
    'assistant_window_topmost': True,
    'assistant_window_single': True
}

def get_app_settings():
    pass

def setup_icon(icon):
    icon.visible = True

def close_tray(icon):
    icon.visible = False
    icon.stop()
    os._exit(0)

#def edit_settings():
#    pass

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
    image = Image.open(os.path.join(os.getcwd(),'help.png'))
    right_click_menu = Menu(
        #MenuItem('Voice Search', voice_input, enabled=True, default=True, visible=True),
        #MenuItem('Open Assistant', app_restore),
        MenuItem('Open Assistant', app_restore, enabled=True, default=True, visible=True),
        MenuItem('Voice Search', voice_input, enabled=model_flag),
        MenuItem('Add shortcut', add_note),
#        MenuItem('Settings', edit_settings),
        MenuItem('Exit', lambda: close_tray(icon)))
    icon = Icon('Helper', image, 'Helper', right_click_menu)
    # add_hotkey('Ctrl+`', fast_answer)
    # greeting()
    icon.run_detached(setup_icon)