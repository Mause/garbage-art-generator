#!/usr/bin/env python

import math
import time
import random
import colorsys
from Tkinter import *
from threading import Thread

try:
    import queue
except ImportError:
    import Queue as queue

# intro, credits...
print 'Canvas Based Garbage Art'
print 'Written by Dominic May, with valuable input from Steven Smith'
print '									'


fh = open('log.log', 'wb')


q = queue.Queue()
cna = {'width': '800', 'height': '800'}

print '\nStarting canvas cage...\n'

root = Tk()
art_canvas = Canvas(root,
                width = cna['width'],
                height = cna['height'],
                border = 5)


def run():
    user_input = get_user_input()
#    user_input = format_user_input(divrat, debug, height, width, tf_outline, enhanced, colour_offset)
    setup_watcher = Thread(target=setup,
                          args=(art_canvas, cna, q, fh, user_input))
    setup_watcher.start()


# Three different choices of colour generators :D


def one(offset, debug):
    if offset == '':
        offset = int(50)
    else:
        offset = int(offset)
    colours = (colorsys.hsv_to_rgb(random.random(), 0.5, 0.95))
    final_colours = []
    for colour_num in range(len(colours)):
        final_colours.append(offset + int(colours[colour_num] * 100))
    if debug:
        print str(colours)
    temp_fill = '#'
    temp_fill += str(final_colours[0])
    temp_fill += str(final_colours[1])
    temp_fill += str(final_colours[2])
    return temp_fill[:7]


def two():
    blue = hex(random.randint(0, 65536))
    green = hex(random.randint(0, 65536))
    red = hex(random.randint(0, 65536))
    colours = red[2:] + green[2:] + blue[2:]
    out = '#' + colours
    return out


def three():
    #colours += str(random.randint(100, 360))
    #colours += str(random.randint(100, 360))
    #colours += str(random.randint(100, 360))
#    out='#' + colours
    out = '#' + str(random.randint(100000000, 999999999))
    return out

def package_user_input(divrat, debug, height, width, tf_outline, enhanced, colour_offset):
    pass


def get_user_input():
    user_input = {}
    user_input['divrat'] = divrat_widget.get()
    user_input['debug'] = debug.get()
    user_input['height'] = height_widget.get()
    user_input['width'] = width_widget.get()
    user_input['tf_outline'] = tf_outline.get()
    user_input['enhanced'] = enhanced.get()
    user_input['colour_offset'] = colour_offset_widget.get()
    return user_input


def do_colour(col, colour_offset, debug):
    col = int(col.get())
    if col == 1:
        fill = one(colour_offset, debug)
    if col == 2:
        fill = two()
    if col == 3:
        fill = three()
    return fill


def setup(art_canvas, cna, q, fh, user_input):
    divrat, debug = user_input['divrat'], user_input['debug']
    width, height = user_input['width'], user_input['height']
    tf_outline, enhanced = user_input['tf_outline'], user_input['enhanced']
    colour_offset = user_input['colour_offset']
    if debug:
        print 'DIVRAT: ', divrat
    output_array = dict()
    row_num = 0
    output_array[str(row_num)] = list()
    art_canvas.delete(ALL)
    if divrat == '':
        print 'DIVRAT is outside recommended specifications, setting to ten'
        divrat = int(10)
    if width == '':
        width = int(800)
    if height == '':
        height = int(800)
    divrat, height, width = int(divrat), int(height), int(width)

    art_canvas.config(width = width, height = height)
    cna['height'], cna['width'] = int(height), int(width)
    cur_y = 0
    cur_x = 0
    cube_num = 0
    cube_on_row = 0
    positions = range((cna['height'] / divrat) * (cna['width'] / divrat))
    user_input=format_user_input(divrat, debug, height, width, tf_outline, enhanced, colour_offset)
    
    art_creator_watcher = Thread(target=create_art,
                          args=(art_canvas, cna, fh, user_input, q, fh))
    art_creator_watcher.start()
    if not stable:
        art_creator_watcher.join()
        #print 'Starting printer...'
        #printer(q.get())
        #Thread(target=printer, args=(q.get()))


def create_art(positions, art_canvas, cna, q, fh, user_input):
    for temp in positions:
        cube_num += 1
        cube_on_row += 1
        while True:
            if enhanced == True:
                if debug:
                    print 'Enhanced equals True :D'
                if random.choice(range(2)) == 1:
                    fill = do_colour(col, colour_offset, debug)
                    if col == 1:
                        while len(fill) <= 9:
                            fill = do_colour(col, colour_offset, debug)
            else:
                fill = do_colour(col, colour_offset, debug)
            #print 'fill: ', fill
            try:
                if cube_on_row != 1 and cur_y != 0:
                    if debug:
                        print str(row_num), ':', str(cur_x / divrat)
                    output_array[str(row_num)].append(str(fill))
                    if tf_outline:
                        art_canvas.create_rectangle(cur_x, cur_y, cur_x + divrat,
                                                cur_y + divrat, fill)
                    else:
                        art_canvas.create_rectangle(cur_x, cur_y, cur_x + divrat,
                                                cur_y + divrat, fill, fill)
                break
            except:
                pass
        cur_x = cur_x + divrat
        if cube_on_row == (cna['width']) / divrat:
            row_num += 1
            output_array[str(row_num)] = list()
            if debug:
                print "Beginning a new row"
            cube_on_row = 0
            cur_y += divrat
            cur_x = 0

        if debug:
            print 'X&Y:', cur_x, ':', cur_y
            print 'CN&COR:', cube_num, ':', cube_on_row
    q.put(output_array)
    print '\nCreating done.\n'


def printer(output_array):
    print 'Printer is starting...'
    fh.write(str(output_array))
    for x in output_array['1']:
        pass


def run_exporter():
    Thread(target=exporter, args=(art_canvas,)).start()


def exporter(art_canvas):
    filename = "Colour_grid_" + str(random.randint(1000, 2000)) + ".ps"
    print '''Exporting the canvas;
contents will be in the PostScript format; heres the filename:''', filename
    art_canvas.postscript(file='output\\' + filename)
#    command += '''C:\\Program Files (x86)\\gs\\gs9.04\\bin\\gswin32.exe'''
#    command += '''-sOutputFile='''
#    command += filename[:-3] + ' '+str(os.getcwd()) + '\\'+filename
 #   print command
  #  os.system(command)


def execute_p():
    exec execute_p_widget.get()


# The rest of the code defines the gui elements

menubar = Menu(root)
menubar.add_command(label = "Generate A.R.T.", command = run)
#menubar.add_command(label = "Settings", command = create_settings_window)
menubar.add_command(label = "Export A.R.T.", command = run_exporter)

# The following chunk of code defines the tearaway settings window.
# More intuitive for users not familiar with the command line :)
#settings_window = Frame(root)
#settings_window.width = 30
settings_window = Toplevel()
settings_window.config(menu = menubar)
settings_window.title('Settings Window')

execute_p_widget = Entry(settings_window)
#execute_p_widget.pack(side = TOP, fill = BOTH, expand = 1)

executer=Button(settings_window, text = "Execute", command = execute_p)
#executer.pack(fill = BOTH, expand = 1)


divrat_label = Label(settings_window,
                     text = 'Square size in pixels? (1-400)',
                     relief = RIDGE)
divrat_label.pack(side = TOP)
divrat_widget = Entry(settings_window)
divrat_widget.pack(side = TOP)

width_label = Label(settings_window,
                    text = 'Image width? leave blank for default',
                    relief = RIDGE)
width_label.pack(side = TOP)
width_widget = Entry(settings_window)
width_widget.pack(side = TOP)

height_label = Label(settings_window,
                     text = 'Image height? leave blank for default',
                     relief = RIDGE)
height_label.pack(side = TOP)
height_widget = Entry(settings_window)
height_widget.pack(side = TOP)


#checkbox_frame=Frame(settings_window)
checkbox_frame = settings_window

enhanced = IntVar()
tf_outline = IntVar()
debug = IntVar()
stable = IntVar()


enhanced_check = Checkbutton(checkbox_frame,
                             text="Enable enhanced operation",
                             variable=enhanced).pack(side = TOP)
debug_check = Checkbutton(checkbox_frame,
                          text="Enable debugging",
                          variable=debug).pack(side = TOP)
stable_check = Checkbutton(checkbox_frame,
                           text="Stable (may cause latency)",
                           variable=stable).pack(side = TOP)
tf_outline_check = Checkbutton(checkbox_frame,
                               text="Square outline generation",
                               variable=tf_outline).pack(side = TOP)

#checkbox_frame.pack(side = LEFT)


col_frame = Frame(settings_window)
col_label = Label(col_frame,
                  text = 'Which colour generator would you like to use? ',
                  relief = RIDGE)
col_label.pack(side = TOP)
col = StringVar()
Radiobutton(col_frame, text="One", variable=col, value=1).pack()
Radiobutton(col_frame, text="Two", variable=col, value=2).pack()
Radiobutton(col_frame, text="Three", variable=col, value=3).pack()
col.set('2')
col_frame.pack(side = TOP)


colour_offset_label = Label(settings_window,
                            text = 'An offset for colour generator 1;',
                            relief = RIDGE)
colour_offset_label.pack(side = TOP)
colour_offset_widget = Entry(settings_window)
colour_offset_widget.pack(side = TOP)

start = Button(settings_window, text="Start", command=run)
start.pack(fill=BOTH, expand=1)

#settings_window.pack(side = TOP)

art_canvas.pack()
root.config(menu=menubar)
root.title(string="Canvas Based A.R.T. Generator - Written by Dominic May")

#settings_window.focus()

root.mainloop()
