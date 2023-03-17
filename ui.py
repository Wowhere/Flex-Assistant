import sys
from tkinter import Tk, Label, Button, Entry, StringVar, Radiobutton, BooleanVar, Menu, Checkbutton, IntVar, Text, ttk, NW, N, S, W, E, Canvas, Frame
from tkinter import scrolledtext as st
#import tkinter.font
##from ttkthemes import ThemedTk
import tksheet
import webbrowser
import pyautogui
from subprocess import check_output, run
from sqlite_functions import *
from voice_functions import *

APP_SETTINGS = {
    'energy_threshold': 450,
    'pause_threshold': 0.5,
    'adjust_for_ambient_noise': False
}

screen_size = pyautogui.size()

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DataSheet(tksheet.Sheet):
    def __init__(self, root, header, data):
        super().__init__(root, theme='light green')
        self.headers(header)
        #self.hide('row_index')
        self.display_subset_of_columns([1, 2, 3], enable = True)
        self.set_sheet_data(data)
        self.enable_bindings(('arrowkeys',  'single_select', 'drag_select',
                                    'column_select', 'row_select', 'column_width_resize', 'double_click_column_resize',
                                    'row_width_resize', 'column_height_resize',
                                    'row_height_resize', 'double_click_row_resize', 'rc_select', 'copy',
                                    'paste', 'undo', 'hide_columns'))
        self.configure(relief='ridge', borderwidth=1)
        #self.extra_bindings('edit_cell', finc=)
        #self.extra_bindings('end_edit_cell', func = self.end_edit_cell)
        #self.extra_bindings('begin_edit_cell', finc = begin_edit_cell)

    def show_context_menu(self):

        pass
        #Menu(self,)

class AddShortcutsWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('Add shortcut')
        self.call('wm', 'attributes', '.', '-topmost', '1')
        self.geometry(str('800') + 'x' + str('450'))
        self.resizable(False, False)

        self.insert_result = Label(self, text='')

        #self.value_field_text = StringVar(self)
        #self.comment_field_text = StringVar(self)
        self.alias_field_text = StringVar(self)
        self.value_label = ttk.Label(self, text='Shortcut')
        self.value_field = st.ScrolledText(self)#), borderwidth=2, relief='ridge', var)
        self.comment_label = ttk.Label(self, text='Comment')
        self.comment_field = st.ScrolledText(self)#), textvariable=self.comment_field_text, borderwidth=2, relief='ridge')
        self.alias_flag = IntVar(self, 1)
        self.alias_flag_checkbutton = Checkbutton(self, text='With Alias', variable=self.alias_flag, command=self.change_alias_mode)
        self.voice_alias_label = ttk.Label(self, text='Alias')
        self.voice_alias_field = Entry(self, textvariable=self.alias_field_text, borderwidth=2, relief='ridge')
        self.add_button = Button(self, text='Add',
                                    command=self.add_new_shortcut,
                                    background='#33DFF2', borderwidth=2, relief='ridge')
        self.bulk_add_button = Button(self, text='Bulk Add',
                                    command=self.add_csv_shortcut,
                                    background='#33DFF2', borderwidth=2, relief='ridge')
        self.insert_result.place(x=45, y=255)
        self.value_label.place(x=5, y=5)
        self.value_field.place(x=80, y=5, width=400, height=30)
        self.comment_label.place(x=5, y=65)
        self.comment_field.place(x=80, y=65, width=400, height=30)
        self.alias_flag_checkbutton.place(x=80, y=95)
        self.voice_alias_label.place(x=5, y=125)
        self.voice_alias_field.place(x=80, y=125, width=400, height=30)
        self.add_button.place(x=45, y=220, width=400, height=30)

        #self.insert_type = BooleanVar(self)
        #self.insert_type.set(0)
        #self.insert_type_flag = Checkbutton(self, text='Escaping \',\'', variable=self.insert_type, command=self.change_alias_mode)
        #self.insert_type_flag.place(x=500, y=55)
        #self.import_instruction = StringVar(self)
        #self.import_instruction.set()

        self.label_instruction = ttk.Label(self, text='Csv import.\n Format: \'Shortcut\', \'Comment\', \'Alias\'', anchor=W)
        self.label_instruction.place(x=500, y=5)

        self.csv_shortcuts = st.ScrolledText(self)#, width=20, height=30)
        self.csv_shortcuts.place(x=500, y=85, width=270, height=280)
        self.bulk_add_button.place(x=500, y=380, width=270, height=30)

        self.mainloop()

    def add_new_shortcut(self):
        self.insert_result.config(text='')
        res = insert_rule_db(self.value_field.get('1.0', 'end'), self.alias_flag.get(),
                             self.alias_field_text.get(), self.comment_field.get('1.0', 'end'))
        #res = insert_rule_db(self.value_field_text.get(), self.alias_flag.get(), self.comment_field_text.get(), self.alias_field_text.get())
        if not res:
            self.insert_result.config(text='Error of inserting', foreground='red')
        else:
            self.insert_result.config(text='Success', foreground='green')

    def add_csv_shortcut(self):
        self.insert_result.config(text='')
        res = insert_rule_db(self.value_field.get('1.0', 'end'), self.alias_flag.get(), self.alias_field_text.get(), self.comment_field.get('1.0', 'end'))
        if not res:
            self.insert_result.config(text='Error of csv inserting', foreground='red')
        else:
            self.insert_result.config(text='Success', foreground='green')

    def change_alias_mode(self, ):
        print(0)
        if self.alias_flag.get() == 0:
            self.voice_alias_field.config(state='disabled')
        elif self.alias_flag.get() == 1:
            self.voice_alias_field.config(state='normal')

    # def change_insert_type(self):
    #     if self.insert_type.get() == 0:
    #         self.import_instruction.config(text='Csv import.\n Format: \'Shortcut\', \'Comment\', \'Alias\'')
    #     elif self.insert_type.get() == 1:
    #         self.import_instruction.config(text='Csv import.\n Format: \'Shortcut\', \'Comment\', \'Alias\'')

# class ExtendedDataSheet(Tk):
#     def __init__(self, root, header, data, x, y, height, width):
#         self.headers(header)
#         self.set_sheet_data(data)
#         self.enable_bindings(('single_select', 'drag_select',
#                                     'column_select', 'row_select', 'column_width_resize','double_click_column_resize',
#                                     'row_width_resize', 'column_height_resize', 'arrowkeys',
#                                     'row_height_resize', 'double_click_row_resize', 'rc_select', 'copy',
#                                     'paste', 'undo'))
#         self.configure(relief='ridge', borderwidth=1)
#         super().__init__()
#         self.call('wm', 'attributes', '.', '-topmost', '1')
#         self.title(header)
#         self.resizable(True, True)

class AssistantApp(Tk):
    def __init__(self, query='', height=0, width=0):
        super().__init__()
        self.call('wm', 'attributes', '.', '-topmost', '1')
        self.title('Flex Assistant')
        self.resizable(False, False)
        self.color_backgroung = '#AEF359'
        self.color_foreground = '#3A5311'

        base_width = 550
        base_height = 135
        if height == 0 and width == 0:
            #self.geometry(str(400) + 'x' + str(135) + '+' + str(screen_size[0]-405) + '+' + str(screen_size[1]-225))
            self.geometry(str(base_width) + 'x' + str(base_height) + '+' + str(screen_size[0] - (base_width+5)) + '+' + str(screen_size[1] - (base_height+90)))
        else:
            self.geometry(str(width) + 'x' + str(height))
        self.search_type = BooleanVar(self)
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

        self.values_search_flag = IntVar(self, value=1)
        self.comments_search_flag = IntVar(self, value=1)
        self.alias_search_flag = IntVar(self, value=1)
        self.uniqueness_flag = IntVar(self, value=1)
        self.shortcuts_values_search = Checkbutton(self, text='Shortcut', variable=self.values_search_flag)
        self.shortcuts_comments_search = Checkbutton(self, text='Comment', variable=self.comments_search_flag)
        self.shortcuts_alias_search = Checkbutton(self, text='Alias', variable=self.alias_search_flag)
        #self.uniqueness_results_flag = Checkbutton(self, text='Unique', variable=self.uniqueness_flag)
        if query != "":
            self.recent_searches_combobox.insert(0, query)
            self.show_search_results(query, 1)
        self.recent_searches_combobox.place(x=5, y=10, width=280, height=30)
        self.recent_searches_combobox.bind('<Return>', lambda event: self.show_search_results(self.search_text.get(), self.search_type.get()))

        self.search_settings_fuzzy.place(x=300, y=10)
        self.search_settings_strict.place(x=300, y=35)
        self.search_button.place(x=5, y=80, width=280, height=50)

        self.add_new_button.place(x=300, y=80, width=85, height=50)

        self.shortcuts_values_search.place(x=5, y=45)
        self.shortcuts_comments_search.place(x=95, y=45)
        self.shortcuts_alias_search.place(x=195, y=45)
        #self.uniqueness_results_flag.place(x=320, y=50)
        self.mainloop()
        #if query != "":
            #self.recent_searches_combobox.insert(0, query)
            #self.show_search_results(query, 1)

    def show_shortcut_window(self):
        add_window = AddShortcutsWindow()

    def resize_window(self, height, width, x=0,y=0):
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

    def get_scripts(self):
        self.filessheet.popup_menu_add_command(label='test', func=lambda: print(234))

    def show_search_results(self, query, search_type):
        if query not in self.recent_searches and query.strip() != "":
            self.recent_searches.append(query)
        self.resize_window(505, 600)
        self.filessheet = DataSheet(self, ['Id', 'Shortcut', 'Comment', 'Alias'], data=[])
        self.filessheet.config()
        self.filessheet.enable_bindings('rc_popup_menu')

        #if self.winfo_children()
        #self.filessheet.destroy()

        print('show_search_results(): ' + str(query))
        result = get_help_from_db(query.strip(), search_type, [self.values_search_flag.get(), self.comments_search_flag.get(), self.alias_search_flag.get()])
        # print("Result: " + result)
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
        for i in result['shortcuts_aliases']:
            if i not in end_result.keys():
                end_result[i] = 1
            else:
                end_result[i] += 1
        #print(end_result)
        сounter = 0
        for key, value in end_result.items():
            self.filessheet.insert_row(values=key)
            color_codes = bin(value)[2:].zfill(3)
            #print(color_codes)
            for k in range(0, len(color_codes)):
                if color_codes[k] == '1':
                    #print(color_codes[k])
                    self.filessheet.highlight_cells(row=сounter, column=k+1, bg=self.color_backgroung, fg=self.color_foreground)
            сounter += 1

        #self.filessheet.set_column_widths([345, 120, 70])
        self.filessheet.place(x=5, y=135, width=592, height=395)
        self.recent_searches_combobox.focus()

    def get_voice_input(self):
        query = voice_command()
        files, shells, links = get_help_from_db(query)
        self.show_search_results([files, shells, links])
