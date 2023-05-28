import sys
from tkinter import Tk, Label, Button, Entry, StringVar, Radiobutton, BooleanVar, Menu, Checkbutton, IntVar, Text, ttk, NW, N, S, W, E, Canvas, Frame
from tkinter import scrolledtext as st, filedialog as fd
#import tkinter.font
##from ttkthemes import ThemedTk
import tksheet
import pyautogui
from subprocess import check_output, run
from sqlite_functions import *
from voice_functions import *
import csv
#import pprint

#pp = pprint.PrettyPrinter(indent=4)

screen_size = pyautogui.size()

class DataSheet(tksheet.Sheet):
    def __init__(self, root, header, data):
        super().__init__(root, theme='light green')  #datasheet_theme
        self.headers(header)
        #self.hide('row_index')
        self.display_subset_of_columns([1, 2, 3], enable=True)
        self.set_sheet_data(data)
        self.enable_bindings(('arrowkeys', 'single_select', 'drag_select',
                                    'column_select', 'row_select', 'column_width_resize', 'double_click_column_resize',
                                    'row_width_resize', 'column_height_resize',
                                    'row_height_resize', 'double_click_row_resize', 'rc_select', 'rc_popup_menu', 'copy',
                                    'undo', 'hide_columns'))
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
        cell_data = self.get_cell_data(event[0], 0, return_copy=True)
        update_row(cell_data, self.get_currently_selected()[1], event[3])

    def show_context_menu(self):
        pass
        #Menu(self,)

    # def edit_mode_toggle(self):
    #     if self.app_mode == 0:
    #         self.enable_bindings('edit_cell', 'paste')
    #         self.extra_bindings([('end_edit_cell', self.end_edit_cell)])  #('begin_edit_cell', self.begin_edit_cell),
    #         self.popup_menu_add_command(label='Delete shortcut',
    #                                                func=lambda: self.delete_sheet_entry())
    #         self.popup_menu_add_command(label='Delete alias',
    #                                                func=lambda: self.delete_sheet_alias())
    #         self.refresh()
    #         self.app_mode = 1
    #     elif self.app_mode == 1:
    #         self.disable_bindings('edit_cell', 'paste', 'begin_edit_cell')
    #         self.popup_menu_del_command(label='Delete shortcut')
    #         self.popup_menu_del_command(label='Delete alias')
    #         self.app_mode = 0

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
                ('All files', '*.*')
        )
        filename = fd.askopenfilename(
                title='Import from file',
                initialdir='/',
                filetypes=filetypes)
        with open(filename) as importfile:
            imported_rules = list(csv.reader(importfile))
        print(imported_rules)
        # if not import_array:
        #     self.insert_result.config(text='Error of csv inserting', foreground='red')
        # else:
        #     self.insert_result.config(text='Success', foreground='green')

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
            self.geometry(str(base_width) + 'x' + str(base_height) + '+' + str(screen_size[0] - (base_width+5)) + '+' + str(screen_size[1] - (base_height+90)))
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
        if query != "":
            self.recent_searches_combobox.insert(0, query)
            self.show_search_results(query, 1)
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
        #self.uniqueness_results_flag.place(x=320, y=50)
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
            self.filessheet.extra_bindings([('end_edit_cell', self.filessheet.end_edit_cell)])  #('begin_edit_cell', self.begin_edit_cell),
            self.filessheet.popup_menu_add_command(label='Delete shortcut',
                                                   func=lambda: self.filessheet.delete_sheet_entry())
            self.filessheet.popup_menu_add_command(label='Delete alias',
                                                   func=lambda: self.filessheet.delete_sheet_alias())
            self.filessheet.refresh()
            self.editing_button.config(background='#FFAC1C')
            self.editing_button.config(text='Editing on')
            self.app_mode = 1
        elif self.app_mode == 1:
            self.filessheet.disable_bindings('edit_cell', 'paste', 'begin_edit_cell')
            self.filessheet.popup_menu_del_command(label='Delete shortcut')
            self.filessheet.popup_menu_del_command(label='Delete alias')
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

    def get_voice_input(self):
        query = voice_command()
        files, shells, links = get_help_from_db(query)
        self.show_search_results([files, shells, links])
