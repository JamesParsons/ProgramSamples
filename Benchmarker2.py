import json
import requests
from tkinter import *
from tkinter import ttk
import csv
    
##########################  make root window  ################################

# makes the root window
def make_root_window():
    root = Tk()
    root.geometry("200x200")
    root['bg'] = ['blue']
    root.title("ROOT")    
    
    root.withdraw()

##############################################################################
   
    
#############################################################################

# Defines the behavior for the API information sent to it
# and pulls the information and places it into JSON-like objects
class APIset:
    
    def __init__(self, api):
        self.api = api
        self.checkbox_results = []
        self.selections = []
        
    # runs the API's and gets the results    
    def runit(self):
        apiresult = requests.get(self.api)
        json_object = apiresult.json()
        self.json_object = json_object
        self.sub_keys = []
        for key in self.json_object[0].keys():
            self.sub_keys.append(key)
    
    # get the checkbox selections as index / position numbers
    def get_selections(self):
        sel = 0
        self.selections = []
        for selection in self.checkbox_results:
            if selection.get() == 1:
                self.selections.append(sel)
            sel = sel + 1
        return self.selections
            
        
###########################  window frame  #####################################
 
# a class to make a window dynamically.  probably unnecessary but good for expandability       
class Background_window:
    
    def __init__(self, sent_root):
        self.base = sent_root     
        self.row = 0
        self.window_name = str(sent_root)
        self.column = 0
            
        self.base = Toplevel()
        #self.base.geometry("1200x600")
        self.base['bg'] = ['Green']
        self.base.title(self.window_name)
        
    def increase_column(self):
        self.column = self.column + 1    
                      
    def increase_row(self):
        self.row = self.row + 1
        
###############################################################################
        
def set_checkbox_frame(container_window, dataset):
    
    frame = Frame(container_window.base, padx = 30)
    frame.grid(row=container_window.row, column=container_window.column)
    
    Label(frame, text=dataset.name, font=("Arial", 12)).grid(row=0,column=0)   
    
    for key in dataset.sub_keys:
        cbv = IntVar()
        Checkbutton(frame, text=key, variable=cbv).grid()
        dataset.checkbox_results.append(cbv)
        
    container_window.increase_column()
    
########################## set result frame #############################

# populates the frames
def populate(outer_frame):
            
    frame_row = 0
    frame_column = 0
    
    homeless1 = homeless1_dataset.get_selections()
    snap = snap_dataset.get_selections()
    job = job_dataset.get_selections()
    workforce = workforce_dataset.get_selections()
    employment = employment_dataset.get_selections()
    
    if homeless1:
        for row in homeless1:
            full_row = homeless1_dataset.json_object[row]
            for key, value in full_row.items():
                Label(outer_frame, text=key, bg="white").grid(row=frame_row, column=frame_column, sticky='e')
                Label(outer_frame, text=value, bg="white").grid(row=frame_row, column=frame_column + 1)         
                frame_row = frame_row + 1
                 
    if snap:
        frame_column = frame_column + 2
        for snaprow in snap:
            full_snap_row = snap_dataset.json_object[snaprow]
            for snapkey, snapvalue in full_snap_row.items():
                Label(outer_frame, text=snapkey, bg="white").grid(row=frame_row, column=frame_column, sticky='e')
                Label(outer_frame, text=snapvalue, bg="white").grid(row=frame_row, column=frame_column + 1)        
                frame_row = frame_row + 1  
                
    if job:
        frame_column = frame_column + 3
        for jobrow in job:
            full_job_row = job_dataset.json_object[jobrow]
            for jobkey, jobvalue in full_job_row.items():
                Label(outer_frame, text=jobkey, bg="white").grid(row=frame_row, column=frame_column, sticky='e')
                Label(outer_frame, text=jobvalue, bg="white").grid(row=frame_row, column=frame_column + 1)        
                frame_row = frame_row + 1   
                
    if workforce:
        frame_column = frame_column + 4
        for workforcerow in workforce:
            full_workforce_row = workforce_dataset.json_object[workforcerow]
            for workforcekey, workforcevalue in full_workforce_row.items():
                Label(outer_frame, text=workforcekey, bg="white").grid(row=frame_row, column=frame_column, sticky='e')
                Label(outer_frame, text=workforcevalue, bg="white").grid(row=frame_row, column=frame_column + 1)        
                frame_row = frame_row + 1     
                
    if employment:
        frame_column = frame_column + 4
        for employmentrow in employment:
            full_employment_row = employment_dataset.json_object[employmentrow]
            for employmentkey, employmentvalue in full_employment_row.items():
                Label(outer_frame, text=employmentkey, bg="white").grid(row=frame_row, column=frame_column, sticky='e')
                Label(outer_frame, text=employmentvalue, bg="white").grid(row=frame_row, column=frame_column + 1)        
                frame_row = frame_row + 1                 
                    
                
  
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))    
    
################################################
        
def set_checkbox_frame_list(container_window, dataset, choice_list):
    
    frame = Frame(container_window.base, padx = 30)
    frame.grid(row=container_window.row, column=container_window.column)
    
    Label(frame, text=dataset.name, font=("Arial", 12)).grid(row=0,column=0)   
    
    for item in choice_list:
        cbv = IntVar()
        Checkbutton(frame, text=item, variable=cbv).grid()
        dataset.checkbox_results.append(cbv)
        
    container_window.increase_column()
                                
############################### set nav buttons ####################################
   
def set_nav_buttons(container_window):

    Button(window1.base, text="Show Data", command=get_data, bd="8p").grid(columnspan=container_window.column, sticky='ew')
    Button(window1.base, text="Print Results to CSV", command=print_data, bd="8p").grid(columnspan=container_window.column,sticky='ew')
    Button(window1.base, text="Quit", command=quit_program, bd="8p").grid(columnspan=container_window.column,sticky='ew')
    Button(window1.base, text="Graph Results", command=show_graph, bd="8p").grid(columnspan=container_window.column,sticky='ew')
    
    container_window.increase_row()
    
#####################################################################

def show_graph():
    graph_window = Background_window('graph_window')
    
    img = PhotoImage(file='C:\\Users\\wedel\\OneDrive\\Desktop\\HomelessGraph.png')
    Label(graph_window.base,image=img).pack() 
    
    Label(graph_window.base, text="Stick With Non-Graphical Version for Free!", bd="8p").pack()
    Label(graph_window.base, text="Buy Graphical Version For $299 A Month", bd="8p").pack()
    
    graph_window.mainloop()
    
    
#######################################################################
    
def buy_graphical():
    buy_graphical_window = Background_window('buy_graphical_window')
    Label(graph_window.base, text="Thank you", bd="8p").pack()
    
#########################################################################    
    
def get_data():

    homeless1 = homeless1_dataset.get_selections()
    snap = snap_dataset.get_selections()
    job = job_dataset.get_selections()
    workforce = workforce_dataset.get_selections()
    employment = employment_dataset.get_selections()
    
    sb = Scrollbar(window2.base)
    sb.pack(side = RIGHT, fill = Y)
    
    homeless_list = Listbox(window2.base, yscrollcommand = sb.set, height=20, width=60 )
    snap_list = Listbox(window2.base, yscrollcommand=sb.set, height = 20, width = 30)
    job_list = Listbox(window2.base, yscrollcommand=sb.set, height = 20, width = 30)
    workforce_list = Listbox(window2.base, yscrollcommand=sb.set, height = 20, width = 45)
    employment_list = Listbox(window2.base, yscrollcommand=sb.set, height = 20, width = 45)
        
    for homeless_row in homeless1:
        homeless_full_row = homeless1_dataset.json_object[homeless_row]
        for homelesskey, homelessvalue in homeless_full_row.items():
            homeless_list.insert(END, "    " + homelesskey + " " + homelessvalue)
        homeless_list.insert(END, "                  ------------------")
        
    for snap_row in snap:
        snap_full_row=snap_dataset.json_object[snap_row]
        for snapkey, snapvalue in snap_full_row.items():
            snap_list.insert(END, "    " + snapkey + " " + snapvalue)
        snap_list.insert(END, "            --------------------")
        
    for job_row in job:
        job_full_row=job_dataset.json_object[job_row]
        for jobkey, jobvalue in job_full_row.items():
            job_list.insert(END, "    " + jobkey + " " + jobvalue)
        job_list.insert(END, "            --------------------")  
        
    for workforce_row in workforce:
        workforce_full_row=workforce_dataset.json_object[workforce_row]
        for workforcekey, workforcevalue in workforce_full_row.items():
            workforce_list.insert(END, "    " + workforcekey + " " + workforcevalue)
        workforce_list.insert(END, "            --------------------")   
        
    for employment_row in employment:
        employment_full_row=employment_dataset.json_object[employment_row]
        for employmentkey, employmentvalue in employment_full_row.items():
            employment_list.insert(END, "    " + employmentkey + " " + employmentvalue)
        employment_list.insert(END, "            --------------------")        
                 
    homeless_list.pack( side = LEFT, anchor=NW )
    snap_list.pack(side=LEFT, anchor=NW)
    job_list.pack(side=LEFT, anchor=NW)
    workforce_list.pack(side=LEFT, anchor=NW)
    employment_list.pack(side=LEFT, anchor=NW)
    sb.config( command = homeless_list.yview )    
        
    
         
##################################################################### 
def print_data():
    print("printing to a CSV entitled Results.txt")
    
    homeless1 = homeless1_dataset.get_selections()
    snap = snap_dataset.get_selections()
    job = job_dataset.get_selections()
    workforce = workforce_dataset.get_selections() 
    employment = employment_dataset.get_selections()
    
    # open (or create) a csv file named Results.txt
    with open('Results.txt', 'w', newline='') as file:
        writer = csv.writer(file)
   
        if homeless1:
            for row in homeless1:
                full_row = homeless1_dataset.json_object[row]
                json.dump(full_row, file, sort_keys = True, indent = 4, ensure_ascii=False)
                    
        if snap:
            for snaprow in snap:
                full_snap_row = snap_dataset.json_object[snaprow]
                json.dump(full_snap_row, file, sort_keys = True, indent = 4, ensure_ascii=False)
                               
        if job:
            for jobrow in job:
                full_job_row = job_dataset.json_object[jobrow]
                json.dump(full_job_row, file, sort_keys = True, indent = 4, ensure_ascii=False)
                                
        if workforce:
            for workforcerow in workforce:
                full_workforce_row = workforce_dataset.json_object[workforcerow]
                json.dump(full_workforce_row, file, sort_keys = True, indent = 4, ensure_ascii=False)
                 
        if employment:
            for employmentrow in employment:
                full_employment_row = employment_dataset.json_object[employmentrow]
                json.dump(full_employment_row, file, sort_keys = True, indent = 4, ensure_ascii=False)
               
    
#####################################################################
    
def quit_program():
    exit()
    
######################################
                        
homeless1_dataset = APIset('https://data.cityofnewyork.us/resource/k46n-sa2m.json')
homeless1_dataset.runit()
homeless1_dataset.name = "Homelessness 1"
homeless1_choices = ['Today', 'Yesterday', 'Two Days Ago', 'Three Days Ago', \
                    'Four Days Ago', 'Five Days Ago', 'Six Days Ago', 'One Week Ago']

snap_dataset = APIset('https://data.cityofnewyork.us/resource/5c4s-jwtq.json')
snap_dataset.runit()
snap_dataset.name = "SNAP"
snap_choices = ['This Month', 'Last Month', 'Two Months Ago', 'Three Months Ago', \
                    'Four Months Ago', 'Five Months Ago', 'Six Months Ago']

job_dataset = APIset('https://data.cityofnewyork.us/resource/dwzs-n5b9.json?program=Job Placements')
job_dataset.runit()
job_dataset.name = "Job Placements"
job_choices = ['This Month', 'Last Month', 'Two Months Ago', 'Three Months Ago', \
                    'Four Months Ago', 'Five Months Ago', 'Six Months Ago']

workforce_dataset = APIset('https://data.cityofnewyork.us/resource/ynaw-bmnm.json')
workforce_dataset.runit()
workforce_dataset.name = "Workforce - District"
workforce_choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

employment_dataset = APIset('https://data.cityofnewyork.us/resource/5hjv-bjbv.json')
employment_dataset.runit()
employment_dataset.name = "Employment - Year"
employment_choices = ['2012', '2013', '2014', '2015', '2015', '2016', '2017']

#global_checkboxes = []

make_root_window()

window1 = Background_window('window1')
window2 = Background_window('window2')

set_checkbox_frame_list(window1, homeless1_dataset, homeless1_choices)
set_checkbox_frame_list(window1, snap_dataset, snap_choices)
set_checkbox_frame_list(window1, job_dataset, job_choices)
set_checkbox_frame_list(window1, workforce_dataset, workforce_choices)
set_checkbox_frame_list(window1, employment_dataset, employment_choices)

set_nav_buttons(window1)

mainloop()
