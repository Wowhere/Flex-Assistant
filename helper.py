import os
from pystray import Icon, Menu, MenuItem
from PIL import Image
from keyboard import add_hotkey
from ui import AssistantApp, AddShortcutsWindow, model_flag, voice_searching

def setup_icon(icon):
    icon.visible = True
    add_hotkey('Ctrl+Shift+z', app_restore)
    add_hotkey('Ctrl+Shift+x', voice_searching)

def close_tray(icon):
    icon.visible = False
    icon.stop()
    os._exit(0)

def add_note():
    note_app = AddShortcutsWindow()

def app_restore():
    app = AssistantApp()
    #close_tray(icon)
    #app.mainloop()

if __name__ == '__main__':
    image = Image.open(os.path.join(os.getcwd(), 'help.png'))
    right_click_menu = Menu(
        #MenuItem('Voice Search', voice_input, enabled=True, default=True, visible=True),
        #MenuItem('Open Assistant', app_restore),
        MenuItem('Open Assistant', app_restore, enabled=True, default=True, visible=True),
        MenuItem('Voice Search', voice_searching, enabled=model_flag),
        MenuItem('Add shortcut', add_note),
#        MenuItem('Settings', edit_settings),
        MenuItem('Exit', lambda: close_tray(icon)))
    icon = Icon('Helper', image, 'Helper', right_click_menu)
    #add_hotkey('Ctrl+Shift+z', app_restore)
    #add_hotkey('Ctrl+Shift+x', voice_searching)
    # greeting()
    icon.run_detached(setup_icon)