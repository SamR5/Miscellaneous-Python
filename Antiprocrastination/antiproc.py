#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Anti-Proc

import traceback as tb
import pickle as pk
import datetime as dt
import tkinter as tk
import tkinter.messagebox as mbox


TIME_INTERVALS = ("minutes", "heures", "jours", "semaines", "mois", "ans")
TASK_PARAMETERS = ("title", "description", "time", "difficulty",
                   "state", "creation", "last_mod", "achieved")
COLUMNS_LABELS = ("Titre", "Description", "Temps", "Difficulté",
                  "Etat", "Ajout", "Modification", "Réalisation")
COLUMNS_WIDTHS = (20, 40, 12, 11, 7, 10, 12, 11)
FONT = "Courier 9 bold"

class MyApp():
    def __init__(self, master):
        self.master = master
        try:
            self.load()
        except IOError:
            self.data = []
        self.GUI()
        self.update_tasks_list()

    def save(self):
        """"""
        with open("tasks.save", 'wb') as mypk:
            pk.dump(self.data, mypk)

    def load(self):
        """"""
        with open("tasks.save", 'rb') as mypk:
            self.data = pk.load(mypk)

    def GUI(self):
        """"""
        self.myTasks = tk.Frame(self.master)
        for ind, (lab, w) in enumerate(zip(COLUMNS_LABELS, COLUMNS_WIDTHS)):
            tk.Label(self.myTasks, text=lab, relief="groove",
                     font=FONT, width=w)\
              .grid(row=0, column=ind)
        self.myTasks.grid()

        # Add task Button
        newTaskB = tk.Button(self.master, text="Ajouter une nouvelle tâche",
                             command=self.new_task)
        newTaskB.grid(pady=5)
    
    def update_tasks_list(self):
        """Update the tasks displayed"""
        try: # for the first time when labels not created
            for lab in self.tasksLabels:
                lab.destroy()
        except:
            pass
        self.tasksLabels = []
        
        for ind, t in enumerate(self.data[::-1]):
            bg = ('lightgreen' if t['state'] else 'lightgray')
            for ind2, txt in enumerate(TASK_PARAMETERS):
                if txt == "state":
                    msg = ("A faire" if t[txt] == 0 else "Fait")
                elif txt == "description":
                    msg = t[txt].replace('\n', '/')
                    msg = (msg[:37] + '...' if len(msg) > 40 else msg)
                elif txt == "title":
                    msg = (t[txt][:17] + '...' if len(t[txt]) > 20 else t[txt])
                else:
                    msg = t[txt]
                lab = tk.Label(self.myTasks, font=FONT, relief="groove",
                               bg=bg, height=2,
                               text=msg.ljust(COLUMNS_WIDTHS[ind2]))
                lab.bind("<Button-1>", lambda event, x=(ind, ind2): self.new_task(x, True))
                lab.grid(row=ind+1, column=ind2)
                self.tasksLabels.append(lab)
            # delete button
            delB = tk.Button(self.myTasks, text="Supprimer", font=FONT,
                             command=lambda x=ind: self.delete_task(x))
            delB.grid(row=ind+1, column=ind2+1)
            self.tasksLabels.append(delB)
        self.save()

    def new_task(self, event=None, modif=False):
        """New window to add tasks"""
        if event is not None:
            if event[1] == 4: # for state
                state = self.data[::-1][event[0]][TASK_PARAMETERS[event[1]]]
                self.data[::-1][event[0]][TASK_PARAMETERS[event[1]]] = (0 if state == 1 else 1)
                if state == 0:
                    td = dt.datetime.today().strftime("%d/%m/%Y")
                    self.data[::-1][event[0]]["achieved"] = td
                else:
                    self.data[::-1][event[0]]["achieved"] = "/"
                self.update_tasks_list()
                return
        
        self.window = tk.Toplevel()
        self.window.resizable(False, False)
        if modif: # when we click on a task to modify it
            self.window.title("Tâche à modifier")
        else:
            self.window.title("Nouvelle tâche")
        
        # title of the task
        titleLab = tk.Label(self.window, text='Titre')
        self.titleVar = tk.StringVar()
        titleEnt = tk.Entry(self.window, textvariable=self.titleVar)
        # description of the task
        descrLab = tk.Label(self.window, text='Description')
        self.descrTxt = tk.Text(self.window, height=8, width=20)
        # time requiered to do the task
        timeLab = tk.Label(self.window, text="Temps requis")
        self.time1Spin = tk.Spinbox(self.window, from_=0, to_=200, width=4)
        self.time2Spin = tk.Spinbox(self.window, values=TIME_INTERVALS,
                                    width=9)
        # difficulty from 1 to 10 (bar 1-10)
        diffLab = tk.Label(self.window, text="Difficulté (1-10)")
        self.diffSpin = tk.Spinbox(self.window, from_=0, to_=10, width=4)

        # add task
        validB = tk.Button(self.window, text="Valider",
                           command=lambda x=event: self.add_task(x))

        # modify task
        if event is not None:
            task = self.data[::-1][event[0]]
            self.titleVar.set(task["title"])
            #self.descrVar.set(task["description"])
            self.descrTxt.insert('end', task["description"])
            self.time1Spin.delete(0)
            self.time1Spin.insert(0, task["time"].split(" ")[0])
            self.time2Spin.delete(0, 'end')
            self.time2Spin.insert(0, task["time"].split(" ")[1])
            self.diffSpin.delete(0)
            self.diffSpin.insert(0, task["difficulty"].split(' ')[0])

        titleLab.grid(row=0, columnspan=2, pady=5)
        titleEnt.grid(row=1, columnspan=2, padx=5, pady=5)
        descrLab.grid(row=2, columnspan=2, pady=5)
        self.descrTxt.grid(row=3, columnspan=2, padx=15, pady=5)
        timeLab.grid(row=4, columnspan=2, pady=5)
        self.time1Spin.grid(row=5, pady=5, sticky='e')
        self.time2Spin.grid(row=5, column=1, pady=5)
        diffLab.grid(row=6, columnspan=2, pady=5)
        self.diffSpin.grid(row=7, columnspan=2, pady=5)
        validB.grid(row=8, columnspan=2, pady=10)

    def add_task(self, event=None):
        """Add a new task to the database"""
        # filter the wrong data
        if self.diffSpin.get() not in map(str, range(0, 11)):
            msg = "La difficulté doit être comprise entre 0 et 10"
        elif self.time2Spin.get() not in TIME_INTERVALS:
            msg = "unité de temps invalide\n" + "choix possibles :\n" +\
                  '\n'.join(TIME_INTERVALS)
        try: # to check both 'int' and < 200
            if int(self.time1Spin.get()) > 200:
                raise ValueError
        except ValueError:
            msg = "Le temps doit être un entier inférieur à 200"

        try:
            mbox.showerror("Entrée invalide", msg)
            return
        except:
            pass

        if event is not None:
            x = event[0]
            mod = False # here in case the user doesn't modify anything
            for i, j in zip(("title", "description", "difficulty"),
                            (self.titleVar.get(),
                             self.descrTxt.get("1.0", 'end').strip('\n'),
                             self.diffSpin.get()+" / 10")):
                if self.data[len(self.data)-x-1][i] != j:
                    self.data[len(self.data)-x-1][i] = j
                    mod = True
            
            formatedTime = self.time1Spin.get() + ' ' + self.time2Spin.get()
            if self.data[len(self.data)-x-1]["time"] != formatedTime:
                self.data[len(self.data)-x-1]["time"] = formatedTime
                mod = True

            if mod:
                td = dt.datetime.today().strftime("%d/%m/%Y")
                self.data[len(self.data)-x-1]["last_mod"] = td

            self.update_tasks_list()
            self.window.destroy()
            return
            
        new_task = {"title":self.titleVar.get(),
                    # from line 1, char 0 to 'end'
                    "description":self.descrTxt.get('1.0', 'end').strip('\n'),
                    "time":self.time1Spin.get() + ' ' + self.time2Spin.get(),
                    "difficulty":self.diffSpin.get() + ' / 10',
                    "state":0,
                    "creation":dt.datetime.today().strftime("%d/%m/%Y"),
                    "last_mod":"/",
                    "achieved":"/"}

        self.data.append(new_task)
        self.update_tasks_list()
        self.window.destroy()
        
    def delete_task(self, x, event=None):
        """Delete a task"""
        mb = mbox.askokcancel("Confirmation de suppression",
                              "Etes-vous sur de vouloir supprimer cette tâche")
        if mb:
            # len(data)-x-1 because the list is displayed backwards
            del self.data[len(self.data)-x-1]
            self.update_tasks_list()

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Gestionnaire")
    A = MyApp(root)
    root.mainloop()

