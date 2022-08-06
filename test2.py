import tkinter as tk
from tkinter import ttk
#check tab change
root = tk.Tk()

nb = ttk.Notebook(root, width=800, height=600)
nb.pack()

frame1 = ttk.Frame(nb)
frame2 = ttk.Frame(nb)

nb.add(frame1, text='Tab1')
nb.add(frame2, text='Tab2')

def on_tab_change(event):
  tab = event.widget.tab('current')['text']
  if tab == 'Tab1':
    print('Tab1 is active')
  elif tab == 'Tab2':
    print('Tab2 is active')
nb.bind('<<NotebookTabChanged>>', on_tab_change)

root.mainloop()
x=10
tabs=[]
for i in range(x):
    tabs.append(ttk.Frame(nb))
    nb.add(tabs[i], text='Tab'+str(i))