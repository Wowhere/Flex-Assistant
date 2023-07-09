import sys
from tkinter import Tk, Label, Button, Entry, StringVar, Radiobutton, BooleanVar, Menu, Checkbutton, IntVar, Text, ttk, NW, N, S, W, E, Canvas, Frame
from tkinter import scrolledtext as st, filedialog as fd, messagebox
#import tkinter.font
##from ttkthemes import ThemedTk
import tksheet
from sqlite_functions import *
from automate import *
import csv
import speech_recognition as sr
import os
import json

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

def show_warning(title='Warning', message='Warning during execution'):
    messagebox.showwarning(title=title, message=message)

model_flag = True
if not os.path.isdir('model'):
    show_warning('\'Model\' folder is absent',
                 '\'Model\' folder is absent. Add folder \'Model\' with vosk model in folder with application for work of voice search')
    model_flag = False
elif len(os.listdir('model')) == 0:
    show_warning('\'Model\' folder is empty',
                 '\'Model\' folder is empty. Add vosk model to folder \'Model\' for work of voice search')
    model_flag = False

if model_flag:
    recognizer = sr.Recognizer()

class DataSheet(tksheet.Sheet):
    def __init__(self, root, header, data):
        super().__init__(root, theme='light green', show_x_scrollbar=True, show_y_scrollbar=True)
        self.headers(header)
        self.hide_columns(columns=0)
        self.set_sheet_data(data)
        self.enable_bindings(('arrowkeys', 'single_select', 'drag_select',
                                    'column_select', 'row_select', 'column_width_resize', 'double_click_column_resize',
                                    'row_width_resize', 'column_height_resize',
                                    'row_height_resize', 'double_click_row_resize', 'rc_select', 'rc_popup_menu', 'copy',
                                    'undo', 'hide_columns'))
        #self.set_options(edit_cell_validation=False)
        self.configure(relief='ridge', borderwidth=1)

    def delete_sheet_entry(self):
        #pp.pprint(self.get_sheet_data())
        re1 = self.get_currently_selected()[0]
        #print(re1)
        cell_data = self.get_cell_data(re1, 0, return_copy=True)
        #print(self.get_row_data(re1, get_index=True))
        self.highlight_cells(row=re1, column=1, bg='#FE4D4D', fg='#530000', redraw=True)
        self.highlight_cells(row=re1, column=2, bg='#FE4D4D', fg='#530000', redraw=True)
        delete_row(cell_data)

    def delete_sheet_alias(self):
        #pp.pprint(self.get_sheet_data())
        re1 = self.get_currently_selected()[0]
        print(re1)
        cell_data = self.get_cell_data(re1, 3, return_copy=True)
        #print(self.get_row_data(re1, get_index=True))
        self.highlight_cells(row=re1, column=3, bg='#FE4D4D', fg='#530000', redraw=True)
        delete_alias(cell_data)

    def end_edit_cell(self, event):
        #print('end_edit_cell')
        if event[4] == 'end_edit_cell':
            cell_data = self.get_cell_data(event[0], 0, return_copy=True)
            print(event)
            update_row(cell_data, self.get_currently_selected()[1], event[3])
            self.refresh()
            return event[3]

    def show_context_menu(self):
        pass
        #Menu(self,)

class VoiceActionsMenu(Tk):
    def __init__(self):
        super().__init__()
        self.title('Variants')
        self.call('wm', 'attributes', '.', '-topmost', '1')
        self.geometry(str('800') + 'x' + str('290'))
        self.resizable(True, True)
        self.mainloop()

def voice_searching():
    search_window = Tk()
    base_width = 550
    base_height = 135
    search_window.title('Listening...')
    search_window.call('wm', 'attributes', '.', '-topmost', '1')
    #search_window.geometry('%dx%d+%d+%d' % (200, 200, 205, 290))
    search_window.geometry('%dx%d+%d+%d' % (200, 200, screen_size[0] - 205, screen_size[1] - 290))
    search_window.attributes('-toolwindow', True)
    search_window.resizable(False, False)
    canvas = Canvas(search_window)
    canvas.pack()
    indicator = canvas.create_oval(60, 60, 130, 130, fill='red')
    active_window = True
    while active_window:
        search_window.update()
        with sr.Microphone() as source:
            recognizer.pause_threshold = 0.6
            recognizer.energy_threshold = 500
            recognizer.adjust_for_ambient_noise(source, 0.8)
            audio = recognizer.listen(source)
            search_window.title('Recognizing...')
            canvas.itemconfig(indicator, fill='yellow')
            search_window.update()
            query = recognizer.recognize_vosk(audio, language='en')
            v_query = query.split(' : ')[1].strip()[1:-3]
            print(v_query)
            if v_query.strip() != '':
                search_window.destroy()
                active_window = False
                AssistantApp(query=v_query)
            else:
                show_warning('Empty message', 'Please, say louder')

class AddShortcutsWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('Add shortcut')
        self.call('wm', 'attributes', '.', '-topmost', '1')
        self.geometry(str('800') + 'x' + str('290'))
        self.resizable(False, False)

        self.insert_result = Label(self, text='')

        self.alias_field_text = StringVar(self)
        self.value_label = ttk.Label(self, text='Shortcut')
        self.value_field = st.ScrolledText(self)
        self.comment_label = ttk.Label(self, text='Comment')
        self.comment_field = st.ScrolledText(self)
        self.alias_flag = IntVar(self, 1)
        self.voice_alias_flag_checkbutton = Checkbutton(self, text='With Alias', variable=self.alias_flag, command=self.change_alias_mode)
        self.voice_alias_label = ttk.Label(self, text='Alias')
        self.voice_alias_field = Entry(self, textvariable=self.alias_field_text, borderwidth=2, relief='ridge')
        self.add_button = Button(self, text='Add',
                                    command=self.add_new_shortcut,
                                    background='#33DFF2', borderwidth=2, relief='ridge')
        self.bulk_add_button = Button(self, text='Import from file',
                                    command=self.add_csv_shortcut,
                                    background='#33DFF2', borderwidth=2, relief='ridge')
        self.insert_result.place(x=45, y=260)
        self.value_label.place(x=5, y=5)
        self.value_field.place(x=80, y=5, width=400, height=60)
        self.comment_label.place(x=5, y=75)
        self.comment_field.place(x=80, y=75, width=400, height=60)
        self.voice_alias_flag_checkbutton.place(x=80, y=135)
        self.voice_alias_label.place(x=5, y=165)
        self.voice_alias_field.place(x=80, y=165, width=400, height=30)
        self.add_button.place(x=45, y=220, width=400, height=30)

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.place(x=490, height=260)

        self.result_separator = ttk.Separator(self, orient='horizontal')
        self.result_separator.place(y=260, width=800)

        self.delimiter_field_text = StringVar(self, value=',')
        self.delimiter_label = ttk.Label(self, text='Delimiter')
        self.delimiter_field = Entry(self, textvariable=self.delimiter_field_text, borderwidth=2, relief='ridge')

        self.delimiter_label.place(x=505, y=75)
        self.delimiter_field.place(x=575, y=75)

        self.label_instruction = ttk.Label(self, text='Csv import.\n Format: \'Shortcut\', \'Comment\', \'Tag\'', anchor=W)
        self.label_instruction.place(x=505, y=5)

        self.bulk_add_button.place(x=505, y=220, width=270, height=30)

        self.mainloop()

    def add_new_shortcut(self):
        self.insert_result.config(text='')
        res = insert_entry(self.value_field.get('1.0', 'end'), self.alias_flag.get(),
                             self.alias_field_text.get(), self.comment_field.get('1.0', 'end'))
        if res[0] == False:
            self.insert_result.config(text=res[1], foreground='red')
        elif res[0] == True:
            self.insert_result.config(text=res[1], foreground='green')

    def add_csv_shortcut(self):
        self.insert_result.config(text='')
        filetypes = (
                ('Csv files', '*.csv'),
                ('Text files', '*.txt'),
                ('All files', '*.*')
        )
        filename = fd.askopenfilename(
                title='Import from file',
                initialdir='/',
                filetypes=filetypes)
        with open(filename) as importfile:
            imported_rules = list(tuple(rule) for rule in csv.reader(importfile, delimiter=self.delimiter_field_text.get()))
        #print(list(tuple(rule) for rule in imported_rules))
        res = bulk_insert_entry(imported_rules)
        if res[0] == False:
            self.insert_result.config(text=res[1], foreground='red')
        elif res[0] == True:
            self.insert_result.config(text=res[1], foreground='green')

    def change_alias_mode(self):
        if self.alias_flag.get() == 0:
            self.voice_alias_field.config(state='disabled')
        elif self.alias_flag.get() == 1:
            self.voice_alias_field.config(state='normal')

class AssistantApp(Tk):
    def __init__(self, query='', height=0, width=0):
        super().__init__()
        self.call('wm', 'attributes', '.', '-topmost', '1')
        self.title('Chill Assistant')
        self.resizable(False, False)
        self.color_backgroung = '#AEF359'
        self.color_foreground = '#3A5311'

        self.filessheet = DataSheet(self, ['Id', 'Shortcut', 'Comment', 'Tag'], data=[])

        base_width = 550
        base_height = 135
        if height == 0 and width == 0:
            #self.geometry(str(400) + 'x' + str(135) + '+' + str(screen_size[0]-405) + '+' + str(screen_size[1]-225))
            self.geometry('%dx%d+%d+%d' % (base_width, base_height, screen_size[0] - (base_width+5), screen_size[1] - (base_height+90)))
        else:
            self.geometry(str(width) + 'x' + str(height))
        self.search_type = BooleanVar(self)
        self.app_mode = 0
        self.search_type.set(1)
        self.search_text = StringVar(self)
        self.recent_searches = []
        self.launchers_handlers = dict()
        self.search_button = Button(self, text='Search',
                                    command=lambda: self.show_search_results(self.search_text.get(), self.search_type.get()),
                                    background='#33DFF2', borderwidth=2, relief='ridge')
        self.add_new_button = Button(self, text='Add new', background='#33F079', command=self.show_shortcut_window, borderwidth=2, relief='ridge')
        self.search_settings_fuzzy = Radiobutton(self, text='Fuzzy', variable=self.search_type, value=1)
        self.search_settings_strict = Radiobutton(self, text='Strict', variable=self.search_type, value=0)
        self.recent_searches_combobox = ttk.Combobox(self, textvariable=self.search_text, values=self.recent_searches, postcommand=self.update_recent_queries)
        self.editing_button = Button(self, text='Editing off', background='#B0B0B0', command=self.edit_mode_toggle, borderwidth=2, relief='ridge')
        self.values_search_flag = IntVar(self, value=1)
        self.comments_search_flag = IntVar(self, value=1)
        self.alias_search_flag = IntVar(self, value=1)
        self.uniqueness_flag = IntVar(self, value=1)
        self.shortcuts_values_search = Checkbutton(self, text='Shortcut', variable=self.values_search_flag)
        self.shortcuts_comments_search = Checkbutton(self, text='Comment', variable=self.comments_search_flag)
        self.shortcuts_alias_search = Checkbutton(self, text='Tag', variable=self.alias_search_flag)
        #self.uniqueness_results_flag = Checkbutton(self, text='Unique', variable=self.uniquenes s_flag)
        if type(query) != tuple:
            if query != "":
                #print(999)
                self.recent_searches_combobox.insert(0, query)
                self.show_search_results(query, 1)
        else:
            show_warning('Recognizing exception', query)
        self.recent_searches_combobox.place(x=5, y=10, width=280, height=30)
        self.recent_searches_combobox.bind('<Return>', lambda event: self.show_search_results(self.search_text.get(), self.search_type.get()))

        self.search_settings_fuzzy.place(x=300, y=10)
        self.search_settings_strict.place(x=300, y=35)
        self.search_button.place(x=5, y=80, width=280, height=50)

        self.add_new_button.place(x=300, y=80, width=85, height=50)
        self.editing_button.place(x=400, y=80, width=85, height=50)
        self.shortcuts_values_search.place(x=5, y=45)
        self.shortcuts_comments_search.place(x=95, y=45)
        self.shortcuts_alias_search.place(x=195, y=45)
        self.focus_force()
        self.recent_searches_combobox.focus()
        self.mainloop()

        #if query != "":
            #self.recent_searches_combobox.insert(0, query)
            #self.show_search_results(query, 1)

    def alias_selected(self):
        pass
        #if row == 4
        #cell_selected(r, c)

    def edit_mode_toggle(self):
        if self.app_mode == 0:
            self.filessheet.enable_bindings('edit_cell', 'paste')
            self.filessheet.extra_bindings([('end_edit_cell', self.filessheet.end_edit_cell)])
            self.filessheet.popup_menu_add_command(label='Delete shortcut',
                                                   func=lambda: self.filessheet.delete_sheet_entry())
            self.filessheet.popup_menu_add_command(label='Delete alias',
                                                   func=lambda: self.filessheet.delete_sheet_alias())
            tag_values = self.filessheet.get_column_data(3, get_displayed=True)
            for i in range(0, len(tag_values)):
                print(tag_values[i])
                self.filessheet.create_dropdown(r=i, c=3, values=get_aliases()[0], set_value=tag_values[i])
            self.filessheet.refresh()
            self.editing_button.config(background='#FFAC1C')
            self.editing_button.config(text='Editing on')
            self.app_mode = 1
        elif self.app_mode == 1:
            self.filessheet.disable_bindings('edit_cell', 'paste', 'begin_edit_cell')
            self.filessheet.popup_menu_del_command(label='Delete shortcut')
            self.filessheet.popup_menu_del_command(label='Delete alias')
            for i in range(0, len(self.filessheet.get_column_data(3))):
                self.filessheet.delete_dropdown(r=i, c=3)
            self.filessheet.refresh()
            self.editing_button.config(background='#B0B0B0')
            self.editing_button.config(text='Editing off')
            self.app_mode = 0

    def show_shortcut_window(self):
        add_window = AddShortcutsWindow()

    def resize_window(self, height, width, x=0, y=0):
        if x == 0 and y == 0:
            self.geometry(str(width) + 'x' + str(height) + '+' + str(screen_size[0]-(width+5)) + '+' + str(screen_size[1]-(height+90)))
        else:
            self.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))
        self.update()

    def update_recent_queries(self):
        self.recent_searches_combobox['values'] = self.recent_searches

    def setup_icon(self, icon):
        icon.visible = True

    def close_tray(self, icon):
        icon.visible = False
        icon.stop()
        self.destroy()
        sys.exit(0)

    def show_search_results(self, query, search_type):
        if query not in self.recent_searches and query.strip() != '':
            self.recent_searches.append(query)
        self.resize_window(505, 600)
        print('show_search_results(): ' + str(query))
        result = get_help_from_db(query.strip(), search_type, [self.values_search_flag.get(), self.comments_search_flag.get(), self.alias_search_flag.get()])
        print(result)
        self.filessheet.set_sheet_data([], reset_col_positions = False, reset_row_positions = False, verify = False, reset_highlights = True)
        end_result = {}
        for i in result['shortcuts_values']:
            if i not in end_result.keys():
                end_result[i] = 4
            else:
                end_result[i] += 4
        for i in result['shortcuts_comments']:
            if i not in end_result.keys():
                end_result[i] = 2
            else:
                end_result[i] += 2
        for i in result['shortcuts_tags']:
            if i not in end_result.keys():
                end_result[i] = 1
            else:
                end_result[i] += 1
        сounter = 0
        for key, value in end_result.items():
            self.filessheet.insert_row(values=key)
            color_codes = bin(value)[2:].zfill(3)
            #print(color_codes)
            for k in range(0, len(color_codes)):
                if color_codes[k] == '1':
                    self.filessheet.highlight_cells(row=сounter, column=k+1, bg=self.color_backgroung, fg=self.color_foreground)
            сounter += 1
        self.filessheet.set_sheet_data(result)
        #self.filessheet.set_column_widths([345, 120, 70])
        self.filessheet.place(x=5, y=135, width=592, height=395)
        self.filessheet.set_all_cell_sizes_to_text()
        self.filessheet.set_column_widths([345, 120, 70])
        self.recent_searches_combobox.focus()
