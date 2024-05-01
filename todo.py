import tkinter as tk
from tkinter import messagebox


def addtask():
    def on_entry_click(event):
        if add_task.get(1.0,'end-1c') == "Enter a task:":
            add_task.delete(1.0, tk.END)
            add_task.configure(foreground="black")

    def on_focus_out(event):
        if add_task.get(1.0,'end-1c') == "":
            add_task.insert(1.0, "Enter a task:")
            add_task.configure(foreground="gray")

    def add():
        input_text=add_task.get(1.0, "end-1c")
        if (input_text=="Enter a task:") or (input_text==""):
            messagebox.showwarning(title="Warning!",message="Please enter a task")
        else:
            listbox_task.insert(tk.END,input_text)
            root1.destroy()

    def cancelAdd():
        root1.destroy()

    root1=tk.Tk()
    root1.title("Add task")
    root1.geometry('350x150')
    add_task=tk.Text(root1,width=40,height=4)
    add_task.insert(1.0, "Enter a task:")
    add_task.configure(foreground="gray")
    add_task.bind("<FocusIn>", on_entry_click)
    add_task.bind("<FocusOut>", on_focus_out)
    add_task.place(x=0,y=0)
    confirmButton=tk.Button(root1,text="Add task",command=add)
    cancelButton=tk.Button(root1,text="Cancel",command=cancelAdd)
    confirmButton.place(x=200,y=80)
    cancelButton.place(x=270,y=80)
    root1.mainloop()

def deletetask():
    selected=listbox_task.curselection()
    listbox_task.delete(selected[0])

def markcompleted():
    marked=listbox_task.curselection()
    temp=marked[0]
    temp_marked=listbox_task.get(marked)
    temp_marked=temp_marked+" ✔"
    listbox_task.delete(temp)
    listbox_task.insert(temp,temp_marked)

listWindow=tk.Tk()
listWindow.title("To-Do List App")

frame_task=tk.Frame(listWindow)
frame_task.pack()

listbox_task=tk.Listbox(frame_task,bg="black",fg="white",height=30,width=80,font="Helvetica")
listbox_task.pack(side=tk.LEFT)

scrollbar_task=tk.Scrollbar(frame_task)
scrollbar_task.pack(side=tk.RIGHT,fill=tk.Y)
listbox_task.config(yscrollcommand=scrollbar_task.set)
scrollbar_task.config(command=listbox_task.yview)

add_button=tk.Button(listWindow,text="Add task",width=50,command=addtask)
add_button.pack(pady=3)

delete_button=tk.Button(listWindow,text="Delete task",width=50,command=deletetask)
delete_button.pack(pady=3)

mark_button=tk.Button(listWindow,text="Mark as completed",width=50,command=markcompleted)
mark_button.pack(pady=3)

listWindow.mainloop()