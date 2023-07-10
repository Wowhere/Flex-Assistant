import subprocess
import webbrowser
import pyautogui

screen_size = pyautogui.size()

def terminal_execute(cmd, shell=False):
    return subprocess.call(cmd, shell)

def browser_open(link, new=0):
    return webbrowser.open(link, new)

def file_open(fname):
    return subprocess.call('start', fname)

def volume_set():
    pass

def gui_recording():
    pass

def gui_replay():
    pass