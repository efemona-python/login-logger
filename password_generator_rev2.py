# Password Generator
import random
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
HEADINGS = ['Domain', 'Username', 'Password']
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


def get_values():
    global VALUES
    VALUES = [[data, DB[data]['Username'], DB[data]['Password']] for data in DB]
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
    return sg.Window('editor', layout=popup_layout)


def update_db(domain_name, user_name, pass_word):
    global DB
    DB.update({
        domain_name: {'Username': user_name,
                      'Password': pass_word}
            })
    get_values()


def delete_values(domain_name):
    global DB
    DB.pop(domain_name)
    get_values()


def save():
    # -- Save JSON FIle
    with open(DB_PATH, 'w') as file:
        json.dump(DB, file, indent=4)



col1 = [
    [sg.Text('Domain/Website', text_color=TEXT_COLOR, font=FONT, pad=((0, 0), (0, 5)))],
    [sg.Text('Email/username', text_color=TEXT_COLOR, font=FONT, pad=((0, 0), (0, 5)))],
    [sg.Text('Password', text_color=TEXT_COLOR, font=FONT, pad=((0, 0), (0, 5)))],
    [sg.Text('', text_color=TEXT_COLOR, font=FONT)]
]

col2 = [
    [sg.Input(key='-DOMAIN-', justification=INPUT_ALIGN,
              background_color=INPUT_BGC, size=INPUT_SIZE, font=FONT),
     sg.Button('Search', key='-Search-', size=(20, 1))],
    [sg.Input(key='-USERNAME-', justification=INPUT_ALIGN,
              background_color=INPUT_BGC, size=INPUT_SIZE, font=FONT)],
    [sg.Input(key='-PASSWORD-', justification=INPUT_ALIGN,
              background_color=INPUT_BGC, size=INPUT_SIZE, password_char='', font=FONT),
     sg.Button('Generate password', key='-GENERATE-'), sg.Button('Edit', key='-Edit-', enable_events=True)],
    [sg.Button('Add', key='-Add-', size=(12, 1)), sg.Button('Select', key='-Select-', size=(12, 1)),
     sg.Button('Update', key='-Update-', size=(12, 1), disabled=True),
     sg.Button('Delete', key='-Delete-', size=(12, 1), disabled=True)]
]
frame_layout = [[sg.Column(col1), sg.VerticalSeparator(), sg.Column(col2)]]
tab1_layout = [
    [sg.Image(filename=IMAGE, size=(200, 200), background_color=WINDOWS_BG), sg.VerticalSeparator(),
     sg.Table(headings=HEADINGS, justification='left', values=get_values(),
              expand_y=True, expand_x=True, enable_events=False, key='-TABLE-')],
    [sg.Frame('password generator', layout=frame_layout, expand_x=True)]
]
tab2_layout = [[sg.T('sample', s=(15, 2))]]
layout = [[sg.TabGroup([[sg.Tab('Safe Key Pass', tab1_layout), sg.Tab('Tab2', tab2_layout)]])]]
window = sg.Window('Encryption Generator', layout, background_color=WINDOWS_BG)
table = window['-TABLE-']

while True:
    event, values = window.read()
    #   print(event,values)
    if event == sg.WIN_CLOSED or event == 'exit':

        break
    if event == '-GENERATE-':
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
        try:
            row_indices = values['-TABLE-']
            if len(row_indices) > 1:
                #   multiple rows selected
                string = 'MULTIPLE ROWS SELECTED'
                window['-DOMAIN-'].update(value=string)
                window['-USERNAME-'].update(value=string)
                window['-PASSWORD-'].update(value=string)
                window['-Add-'].update(disabled=True)
                window['-GENERATE-'].update(disabled=True)
                window['-Edit-'].update(disabled=True)
                window['-Update-'].update(disabled=True)
            else:
                selected_values = VALUES[row_indices[0]]
                sel_domain = selected_values[0]
                sel_username = selected_values[1]
                sel_password = selected_values[2]
                window['-DOMAIN-'].update(value=sel_domain)
                window['-USERNAME-'].update(value=sel_username)
                window['-PASSWORD-'].update(value=sel_password)
                window['-Add-'].update(disabled=False)
                window['-Update-'].update(disabled=False)
                window['-Delete-'].update(disabled=False)
                window['-GENERATE-'].update(disabled=False)
                window['-Edit-'].update(disabled=False)

        except IndexError:
            sg.popup_quick_message('No record selected.')
    if event == '-Add-' or event == '-Update-':
        add_domain = values['-DOMAIN-'].lower()
        add_username = values['-USERNAME-'].lower()
        add_password = values['-PASSWORD-']
        if add_domain in DB:
            window['-Update-'].update(disabled=True)
            window['-Delete-'].update(disabled=True)
            sg.popup_quick_message('Record Updated successfully.')
        else:
            sg.popup_quick_message('Record added successfully.')
        update_db(add_domain, add_username, add_password)
        save()
        # Check if record exist

    if event == '-Delete-':
        e = sg.popup_yes_no('Would you like to delete this items?')
        if e == 'Yes':
            delete_values(sel_domain)
            string = ''
            window['-DOMAIN-'].update(value=string)
            window['-USERNAME-'].update(value=string)
            window['-PASSWORD-'].update(value=string)
            window['-Update-'].update(disabled=True)
            window['-Delete-'].update(disabled=True)
            sg.popup_quick_message('record successfully deleted!!')
            save()

    if event == '-Search-':
        sch_domain = values['-DOMAIN-'].lower()
        try:
            values = DB[sch_domain]
        except KeyError as e:
            sg.popup_quick_message(f'{e} Data not found')
        else:
            sg.popup( f'Username: {values["Username"]} \n Password: {values["Password"]} ', title='Search')


    table.update(values=VALUES)

    #  ---- Password Generator code -----
