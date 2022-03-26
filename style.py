import prompt_toolkit
from logger import *

program_log.debug("Defining Style and Colors")


red_color = "#E91E63"
blue_color = "#2196f3"
orange_color = "#ff8700"
cyan_color = "#00ffd7"
gray_color = "#474747"

style = prompt_toolkit.styles.Style([
    ('separator',    red_color),
    ('questionmark', red_color),
    ('focus',        blue_color),
    ('checked',      blue_color),
    ('pointer',      orange_color),
    ('instruction',  orange_color),
    ('answer',       cyan_color),
    ('question',     blue_color),
    ("disabled", gray_color)
])
