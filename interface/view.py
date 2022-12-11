from prompt_toolkit import Application

from prompt_toolkit.layout.containers import VSplit, Window, HSplit, Container, WindowAlign
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.application import get_app


from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl, UIControl, UIContent
from prompt_toolkit.buffer import Buffer


import InquirerPy.prompts as ipp
import InquirerPy.validator as ipv
import InquirerPy.separator as ips
import InquirerPy.utils as ipu
import InquirerPy.base.control as ipbc
from InquirerPy import inquirer
from InquirerPy import get_style

# generated using pyfiglet
title_str = ' _       _______   ______  ___   __  ______  ______\n| |     / /  _/ | / / __ \\/   | / / / / __ )/ ____/\n| | /| / // //  |/ / / / / /| |/ / / / __  / __/   \n| |/ |/ // // /|  / /_/ / ___ / /_/ / /_/ / /___   \n|__/|__/___/_/ |_/_____/_/  |_\\____/_____/_____/   \n                                                   \n   _____ ____  __  ___   ______     __________  ____  __ \n  / ___// __ \\/ / / / | / / __ \\   /_  __/ __ \\/ __ \\/ / \n  \\__ \\/ / / / / / /  |/ / / / /    / / / / / / / / / /  \n ___/ / /_/ / /_/ / /|  / /_/ /    / / / /_/ / /_/ / /___\n/____/\\____/\\____/_/ |_/_____/    /_/  \\____/\\____/_____/\n                                                         \n'
subtitle_str = "un outil pour compenser les faiblesses d'un OS éclatax !\n\n "
credit_str = "Github/allemand-instable"

title_prompt_toolkit_text = FormattedText(
    [
        ('class:title', title_str),
        ('class:subtitle', subtitle_str),
        ('class:credit', credit_str)
    ]
)

import InquirerPy.prompts as ipp
import InquirerPy.validator as ipv
import InquirerPy.separator as ips
import InquirerPy.utils as ipu
from InquirerPy import inquirer
from InquirerPy import get_style

class_style = Style.from_dict(
    {
        "title" : "#fd79a8",
        "subtitle": "#81ecec",
        "credit": "#ffeaa7"
    })


kb = KeyBindings()

@kb.add('c-q')
@kb.add('c-c')
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit()
    
    




question1_choice = [
    ips.Separator(),
    ipbc.Choice("ap-southeast-2", name="Sydney", enabled=True),
    ipbc.Choice("ap-southeast-1", name="Singapore", enabled=False),
    ips.Separator(),
    "us-east-1",
    "us-west-1",
    ips.Separator(),
]

def question2_choice(_):
    return [
        "Apple",
        "Cherry",
        "Orange",
        "Peach",
        "Melon",
        "Strawberry",
        "Grapes",
    ]

@kb.add('t')
def kbfcn(event):
    
    
    event.regions = inquirer.checkbox(
            message="Select regions:",
            choices=question1_choice,
            cycle=False,
            transformer=lambda result: "%s region%s selected"
            % (len(result), "s" if len(result) > 1 else ""),
        ).execute()
    event.regions = inquirer.checkbox(
            message="Select regions:",
            choices=question1_choice,
            cycle=False,
            transformer=lambda result: "%s region%s selected"
            % (len(result), "s" if len(result) > 1 else ""),
        ).execute() 






left_buffer = Buffer()
right_buffer = Buffer()

left_control = BufferControl(buffer=left_buffer, focus_on_click=True, focusable=True)
right_control = BufferControl(buffer=right_buffer, focus_on_click=True, focusable=True)

left = Window(left_control,wrap_lines = True)
right = Window(right_control,wrap_lines = True)

title_window = Window(content = FormattedTextControl(title_prompt_toolkit_text, focusable=False), height=15, align=WindowAlign.CENTER,)

too_small_warning_container = Window()

content_container = VSplit(
    children = [
        left,
        Window(width=1, char="|", style="class:line"),
        right
    ],
    window_too_small = too_small_warning_container,
    
)

master_container = HSplit(
    [
        title_window,
        Window(height=1, char="—", style="class:line"),
        content_container
    ]
)



layout = Layout(master_container, focused_element=content_container.children[1])


app = Application(layout=layout, full_screen=True, key_bindings=kb,mouse_support=True,  style=class_style)


    
app.run()