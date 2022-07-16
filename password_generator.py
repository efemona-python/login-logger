# Password Generator
"""

Last update: April 23rd, 2022.
revision: changed data storage format from CSV to JSON, with code implementation.
todo: implement SQLite for storage


"""
import PySimpleGUI as sg
from keyGen import Generator
import json
import os

#  ----constants ---
PATH = os.path.dirname(os.path.abspath(__file__))
FONT = 'courier 10 normal'
TEXT_BACKGROUND = 'white'
TEXT_COLOR = 'black'
INPUT_ALIGN = 'left'
INPUT_BGC = 'white'
INPUT_SIZE = (50, 10)
INPUT_TEST_COLOR = 'black'
WINDOWS_BG = 'white'
FRAME_BG = 'gray'
HEADINGS = ['Domain', 'Username', 'Password', 'API_key']
IMAGE = os.path.join(PATH, 'encryption_logo_small.png')
DB_PATH = os.path.join(PATH, 'password_file.json')
VALUES = []
sg.theme('LightGrey2')
pass_gen = Generator()
if os.path.isfile(DB_PATH):
    with open(DB_PATH) as file:
        DB = json.load(file)
else:
    DB = {}


def get_table_values():
    global VALUES
    VALUES = [[data, DB[data]['Username'], DB[data]['Password'], DB[data]['API_key']] for data in DB]
    return VALUES


def create_pop():
    popup_layout = [[sg.Text('Password Length'),
                     sg.Input(default_text=pass_gen.get_lenth(),
                              key='-PASSWORD LENGTH-', pad=(15, 0), size=(10, 10))],
                    [sg.Text('Special Characters'),
                     sg.Input(default_text=pass_gen.get_special_char(), key='-SPECIAL CHAR-', pad=(5, 0),
                              size=(10, 10))],
                    [sg.Text('Numeric Characters'),
                     sg.Input(default_text=pass_gen.get_numeric(), key='-NUMERIC CHAR-', pad=(0, 0), size=(10, 10))],
                    [sg.OK(size=(5, 1))]
                    ]
    return sg.Window('editor', layout=popup_layout, no_titlebar=True, keep_on_top=True, modal=True)


def update_db(domain_name, user_name, pass_word, api_key_):
    global DB
    DB.update({
        domain_name: {'Username': user_name,
                      'Password': pass_word,
                      'API_key': api_key_}
    })
    clear_fields(window)
    get_table_values()


def delete_values(domain_name):
    global DB
    DB.pop(domain_name)
    get_table_values()


def save():
    # -- Save JSON FIle
    with open(DB_PATH, 'w') as f:
        json.dump(DB, f, indent=4)


def build_graphics():
    col1 = [
        [sg.Text('Domain/Website', text_color=TEXT_COLOR, font=FONT, pad=((0, 0), (0, 5)))],
        [sg.Text('Email/username', text_color=TEXT_COLOR, font=FONT, pad=((0, 0), (0, 5)))],
        [sg.Text('Password', text_color=TEXT_COLOR, font=FONT, pad=((0, 0), (0, 5)))],
        [sg.Text('API_Key', text_color=TEXT_COLOR, font=FONT, pad=((0, 0), (0, 5)))],
        [sg.Text('', text_color=TEXT_COLOR, font=FONT)]
    ]
    col2 = [
        [sg.Input(key='-DOMAIN-', default_text='enter website or domain', justification=INPUT_ALIGN,
                  background_color=INPUT_BGC, size=INPUT_SIZE, font=FONT),
         sg.Button('Search', key='-Search-', size=(20, 1))],
        [sg.Input(key='-USERNAME-', default_text='enter username', justification=INPUT_ALIGN,
                  background_color=INPUT_BGC, size=INPUT_SIZE, font=FONT)],
        [sg.Input(key='-PASSWORD-', default_text='enter password', justification=INPUT_ALIGN,
                  background_color=INPUT_BGC, size=INPUT_SIZE, password_char='', font=FONT),
         sg.Button('Generate password', key='-Generate-'), sg.Button('Edit', key='-Edit-', enable_events=True)],
        [sg.Input(key='-API_KEY-', default_text='enter api key', justification=INPUT_ALIGN,
                  background_color=INPUT_BGC, size=INPUT_SIZE, font=FONT)],
        [sg.Button('Add', key='-Add-', size=(12, 1)), sg.Button('Select', key='-Select-', size=(12, 1)),
         sg.Button('Update', key='-Update-', size=(12, 1), disabled=True),
         sg.Button('Delete', key='-Delete-', size=(12, 1), disabled=True)]
    ]
    password_gen_frame_layout = [[sg.Column(col1), sg.VerticalSeparator(), sg.Column(col2)]]
    tab1_layout = [
        [sg.Image(filename=IMAGE, size=(200, 200), background_color=WINDOWS_BG, visible=False), sg.VerticalSeparator(),
         sg.Table(headings=HEADINGS, justification='left', values=get_table_values(),
                  expand_y=True, expand_x=True, enable_events=False, key='-TABLE-')],
        [sg.Frame('Add/Edit', layout=password_gen_frame_layout, expand_x=True)]
    ]
    tab2_layout = [[sg.T('sample', s=(15, 2))]]
    layout = [[sg.TabGroup([[sg.Tab('Password Safe', tab1_layout), sg.Tab('Tab2', tab2_layout)]], enable_events=True,
                           key='-Tabs-')]]
    return sg.Window('Encryption Generator', layout, background_color=WINDOWS_BG)


def clear_fields(active_window):
    _ = ''
    active_window['-DOMAIN-'].update(value=_)
    active_window['-USERNAME-'].update(value=_)
    active_window['-PASSWORD-'].update(value=_)
    active_window['-API_KEY-'].update(value=_)


window = build_graphics()
table = window['-TABLE-']
while True:

    event, values = window.read()

    #   print(event, values)
    if event == sg.WIN_CLOSED or event == 'exit':
        save()
        break
    if event == '-Generate-':
        window['-PASSWORD-'].update(pass_gen.generate())
    if event == '-Edit-':

        popup_window = create_pop()
        event2, values2 = popup_window.read()
        try:
            password_len = int(values2['-PASSWORD LENGTH-'])
            special_char = int(values2['-SPECIAL CHAR-'])
            password_num = int(values2['-NUMERIC CHAR-'])
        except ValueError:
            pass
        else:
            pass_gen.update_generator(password_len, special_char, password_num)

        if event2 == 'OK':
            popup_window.close()
    if event == '-Select-':
        row_indices = values['-TABLE-']
        try:

            if len(row_indices) > 1:
                #   multiple rows selected
                string = 'MULTIPLE ROWS SELECTED'
                window['-DOMAIN-'].update(value=string)
                window['-USERNAME-'].update(value=string)
                window['-PASSWORD-'].update(value=string)
                window['-API_KEY-'].update(value=string)
                # -- button visibility and access control
                window['-Add-'].update(disabled=True)
                window['-Generate-'].update(disabled=True)
                window['-Edit-'].update(disabled=True)
                window['-Update-'].update(disabled=True)
            else:
                selected_values = VALUES[row_indices[0]]
                sel_domain = selected_values[0]
                sel_username = selected_values[1]
                sel_password = selected_values[2]
                api_key = selected_values[3]
                window['-DOMAIN-'].update(value=sel_domain)
                window['-USERNAME-'].update(value=sel_username)
                window['-PASSWORD-'].update(value=sel_password)
                window['-API_KEY-'].update(value=api_key)
                # -- button visibility and access control
                window['-Add-'].update(disabled=False)
                window['-Update-'].update(disabled=False)
                window['-Delete-'].update(disabled=False)
                window['-Generate-'].update(disabled=False)
                window['-Edit-'].update(disabled=False)

        except IndexError:
            sg.popup_quick_message('No record selected.')
    if event == '-Add-' or event == '-Update-':
        add_domain = values['-DOMAIN-'].lower()
        add_username = values['-USERNAME-'].lower()
        add_password = values['-PASSWORD-']
        api_key = values['-API_KEY-']
        if add_domain in DB:
            window['-Update-'].update(disabled=True)
            window['-Delete-'].update(disabled=True)
            sg.popup_quick_message('Record Updated successfully.')
        else:
            sg.popup_quick_message('Record added successfully.')
        update_db(add_domain, add_username, add_password, api_key)
        save()

        # Check if record exist
    if event == '-Delete-':
        e = sg.popup_yes_no('Would you like to delete this items?')
        if e == 'Yes':
            delete_values(row_indices)
            string = ''
            window['-DOMAIN-'].update(value=string)
            window['-USERNAME-'].update(value=string)
            window['-PASSWORD-'].update(value=string)
            window['-API_KEY-'].update(value=string)
            window['-Update-'].update(disabled=True)
            window['-Delete-'].update(disabled=True)
            sg.popup_quick_message('record successfully deleted!!')
            save()

            # delete record
    if event == '-Search-':
        search_string = values['-DOMAIN-'].lower()
        domain_list = DB.keys()
        result = ''
        for domain in domain_list:
            if search_string in domain:
                values = DB[domain]
                result += ''.join(f'Domain: {domain} '
                                  f'\nUsername: {values["Username"]} '
                                  f'\nPassword: {values["Password"]} '
                                  f'\nAPI_Key: {values["API_key"]}\n\n')
        if result != '':
            sg.popup(result, title='Search')
        else:
            sg.popup_quick_message(f'Data not found!')

    table.update(values=VALUES)

    #  ---- Password Generator code -----
