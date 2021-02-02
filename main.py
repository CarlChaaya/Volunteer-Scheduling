from Optimizer import *
from Rescuer import *
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk,Image


window = Tk()
window.title("Rescuer Scheduling Done Right")
window.geometry('800x700')

heading = Label(text = 'Welcome to the simple Beta Version of the rescuer scheduling program.',
                bg = "red", fg = "white", font = '10', width = 700, height = 4)

heading.pack()

menubar = Menu(window)



ttk.Label(window, text = "Import Excel File: ").pack(padx = 20, pady = 4)
open_file = ttk.Button(window, text="Open File")
open_file.pack(padx = 20, pady = 0, anchor = 'c')

box_red_path = ttk.Label(window, text="")
box_red_path.pack()

ttk.Label(window, text = "Choose Output Location: ").pack(padx = 20, pady = 4)
choose_location = ttk.Button(window, text="Choose Location")
choose_location.pack(padx = 20, pady = 0)

box2_red_path = ttk.Label(window, text="")
box2_red_path.pack()

ttk.Label(window, text = "Choose Tolerance Level: ").pack(padx = 20, pady = (4,2))
ttk.Label(window, text = "Increasing tolerance will result in a more equal distribution among teams ", font = 'Helvetica 8 italic').pack(padx = 20, pady = (0,4))

slider_frame = Frame(window, borderwidth=5, relief=SUNKEN)
slider_frame.pack(pady=5)


def get_tolerance(value):
    global tolerance
    tolerance = float(value)/10.0

def get_days(value):
    global days
    days = int(value)


slider = Scale(slider_frame, from_=0.0, to=10.0,orient=HORIZONTAL, length=400, width = 20,tickinterval=1, resolution=0.1, command=get_tolerance)
slider.set(10.0)
slider.pack()

ttk.Label(window, text = "Choose Number of days per week: ").pack(padx = 20, pady = 4)

slider_frame2 = Frame(window, borderwidth=5, relief=SUNKEN)
slider_frame2.pack(pady=5)



slider2 = Scale(slider_frame2, from_=1, to=7,orient=HORIZONTAL, length=300, width = 20,tickinterval=1, resolution=1, command=get_days)
slider2.set(7)
slider2.pack()

var1 = IntVar(value = 0)
checkbox = ttk.Checkbutton(window, text='Optimal?', variable=var1, onvalue=1, offvalue=0, command=None)
checkbox.pack()

start = ttk.Button(window, text="Start")
start.pack(pady = (20,4))

box3_red_path = ttk.Label(window, text="")
box3_red_path.pack()



def upload_file():
    global input_path
    filename = filedialog.askopenfilename(title="Select a File", filetype=(("Excel", "*.xlsx"), ("Excel", "*.xls")))
    input_path= filename
    box_red_path.configure(text=input_path)

def choose_loc():
    global output_path
    folder_selected = filedialog.askdirectory()
    output_path= folder_selected
    box2_red_path.configure(text=output_path)


def start_optimizer():
    global start_counter
    optimal = var1.get()
    text = Optimizer(data_path = input_path,
          output_path = output_path + '\Solution_' + str(start_counter) + '.xlsx',
          num_days = days, tolerance_level = tolerance, optimal = bool(optimal))
    box3_red_path.configure(text = text + str(start_counter))
    start_counter += 1

def popup():
    popup = Toplevel()
    popup.title('Check the sample excel file and follow it accordingly.')
    canvas = Canvas(popup, width=825, height=288)
    canvas.pack()
    img = ImageTk.PhotoImage(Image.open("sample.png").resize((825, 288), Image.ANTIALIAS))
    canvas.create_image(5,5,anchor = NW, image = img)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

open_file.config(command=upload_file)
choose_location.config(command = choose_loc)
menubar.add_command(label = 'Check Sample Excel', command = popup)
start_counter = 0
start.config(command = start_optimizer)
window.config(menu = menubar)
window.mainloop()

