from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
import datetime, random

def copy(self):
    self.clipboard_clear()
    try:
        self.clipboard_append(self.get("sel.first", "sel.last"))
    except:
        self.clipboard_append(self.get(1.0, "end"))

def new():
    toolbar.grid_forget()
    bar.delete(0, END)
    toolbar_new.grid(row=0, column=0, sticky="nsew")
    bar.focus_set()

def new_note():
    global notes
    view_toolbar()
    title = bar.get()
    if title == "":
        title = str(datetime.datetime.now())
        window_title = str(datetime.datetime.now().time())
    else:
        window_title = title
    if title not in note_list.get(0, END):
        window = Tk()
        window.title(window_title)
        try:
            window.iconbitmap("BTXTPad-Note.ico")
        finally:
            window.geometry("254x254")
            window.minsize(254, 254)
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        window.protocol("WM_DELETE_WINDOW", lambda: window.withdraw())
        menubar = Menu(window)
        window.config(menu=menubar)
        menuColor = Menu(window, tearoff=0)
        menubar.add_cascade(label="•", menu=menuColor)
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#fc5"), background="#fc5", foreground="#000", activebackground="#000", activeforeground="#fff")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#5cf"), background="#5cf", foreground="#000", activebackground="#000", activeforeground="#fff")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#d8d"), background="#d8d", foreground="#000", activebackground="#000", activeforeground="#fff")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#8d8"), background="#8d8", foreground="#000", activebackground="#000", activeforeground="#fff")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#f84"), background="#f84", foreground="#000", activebackground="#000", activeforeground="#fff")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#bbb"), background="#bbb", foreground="#000", activebackground="#000", activeforeground="#fff")
        menubar.add_command(label="<", command=lambda: note.edit_undo())
        menubar.add_command(label=">", command=lambda: note.edit_redo())
        menubar.add_command(label="Copy", command=lambda: copy(note))
        menubar.add_command(label="Del", command=lambda: note.delete(1.0, END))
        menubar.add_command(label="Export", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(str(datetime.datetime.now().date())+"\n\n"+note.get(1.0, "end")))
        menubar.add_command(label="Pin", command=lambda: window.attributes("-topmost", not window.attributes("-topmost")))
        menubar.add_command(label="+", command=lambda: window.attributes("-fullscreen", not window.attributes("-fullscreen")))
        note = Text(window, bd=8, relief=FLAT, undo=True, wrap=WORD, background=random.choice(["#fc5", "#5cf", "#d8d", "#8d8", "#f84", "#bbb"]), foreground="#000", font=("", 11))
        note.grid(row=0, column=0, sticky="nsew")
        notes[title] = note
        refresh()
        window.bind("<F11>", lambda i: window.attributes("-fullscreen", not window.attributes("-fullscreen")))
        window.mainloop()
    else:
        messagebox.showerror("BTXTPad Note", "The provided name has already been used.")

def rename():
    if note_list.curselection() != ():
        toolbar.grid_forget()
        bar_1.delete(0, END)
        toolbar_rename.grid(row=0, column=0, sticky="nsew")
        bar_1.focus_set()

def rename_note():
    global notes
    view_toolbar()
    note = notes[note_list.get(note_list.curselection())]
    notes.pop(note_list.get(note_list.curselection()))
    notes[bar_1.get()] = note
    note.winfo_toplevel().title(bar_1.get())
    note.winfo_toplevel().withdraw()
    note.winfo_toplevel().deiconify()
    refresh()

def delete():
    global notes
    if note_list.curselection() != ():
        ch = messagebox.askyesno("BTXTPad Note", f"Are you sure that you want to delete \"{note_list.get(note_list.curselection())}\"?")
        if ch:
            notes[note_list.get(note_list.curselection())].winfo_toplevel().destroy()
            notes.pop(note_list.get(note_list.curselection()))
        refresh()

def delete_all():
    global notes
    ch = messagebox.askyesno("BTXTPad Note", "Are you sure that you want to delete all notes?")
    if ch:
        for note in notes:
            note.winfo_toplevel().destroy()
        notes = {}
        refresh()

def view_toolbar():
    toolbar_new.grid_forget()
    toolbar_rename.grid_forget()
    toolbar.grid(row=0, column=0, sticky="nsew")
    toolbar.focus_set()

def open_note():
    if note_list.curselection() != ():
        title = note_list.get(note_list.curselection())
        note = notes[title]
        notes.pop(note_list.get(note_list.curselection()))
        notes[title] = note
        notes[note_list.get(note_list.curselection())].winfo_toplevel().deiconify()
        refresh()

def clipboard():
    if "Clipboard" not in notes:
        bar.delete(0, END)
        bar.insert(INSERT, "Clipboard")
        new_note()
        refresh()

def help():
    window = Tk()
    try:
        window.iconbitmap("BTXTPad-Note.ico")
    finally:
        window.title("Help - BTXTPad Note")
    window.geometry("600x450")
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    help_tabs = Notebook(window, width=320)
    help_tabs.grid(row=0, column=0, sticky="nsew")
    about = Text(help_tabs, relief=FLAT, border=16, font=("Consolas", 11), wrap=WORD, background="#dcb")
    about.insert(INSERT, f"BTXTPad Note: A lightweight note app\nCopyright (C) 2022-{str(datetime.datetime.now().year)}: Waylon Boer")
    about.configure(state=DISABLED)
    help_tabs.add(about, text="About")
    mit_license = Text(help_tabs, relief=FLAT, border=16, font=("Consolas", 11), wrap=WORD, background="#dcb")
    mit_license.insert(INSERT, """Copyright (c) 2022 Waylon Boer\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR a PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.""")
    mit_license.configure(state=DISABLED)
    help_tabs.add(mit_license, text="License")
    window.mainloop()
 
def refresh():
    note_list.delete(0, END)
    for i in dict(reversed(list(notes.items()))):
        note_list.insert(END, i)
    if "Clipboard" in notes:
        notes["Clipboard"].configure(state=NORMAL)
        notes["Clipboard"].delete(1.0, END)
        notes["Clipboard"].insert(INSERT, notes["Clipboard"].selection_get(selection="CLIPBOARD"))
        notes["Clipboard"].configure(state=DISABLED)
     
def b3_menu(event):
    menuB3.tk_popup(event.x_root, event.y_root)  
    
root = Tk()
root.title("BTXTPad Note")
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

notes = {}

try:
    root.iconbitmap("BTXTPad-Note.ico")
finally:
    root.geometry("450x300")

toolbar = Frame(root, border=8)
toolbar.grid(row=0, column=0, sticky="nsew")
for i in range(0, 3):
    toolbar.columnconfigure(i, weight=1)
button_new = Button(toolbar, text="New", command=new)
button_new.grid(row=0, column=0, sticky="nsew")
button_rename = Button(toolbar, text="Rename", command=rename)
button_rename.grid(row=0, column=1, sticky="nsew")
button_delete = Button(toolbar, text="Delete", command=delete)
button_delete.grid(row=0, column=2, sticky="nsew")

toolbar_new = Frame(root, border=8)
toolbar_new.columnconfigure(0, weight=1)
bar = Entry(toolbar_new)
bar.grid(row=0, column=0, sticky="nsew")
bar.bind("<Return>", lambda i: new_note())
button_ok = Button(toolbar_new, text="OK", command=new_note)
button_ok.grid(row=0, column=1, sticky="nsew")
button_cancel = Button(toolbar_new, text="Cancel", command=view_toolbar)
button_cancel.grid(row=0, column=2, sticky="nsew")

toolbar_rename = Frame(root, border=8)
toolbar_rename.columnconfigure(0, weight=1)
bar_1 = Entry(toolbar_rename)
bar_1.grid(row=0, column=0, sticky="nsew")
bar_1.bind("<Return>", lambda i: new_note())
button_ok_1 = Button(toolbar_rename, text="Rename", command=rename_note)
button_ok_1.grid(row=0, column=1, sticky="nsew")
button_cancel_1 = Button(toolbar_rename, text="Cancel", command=view_toolbar)
button_cancel_1.grid(row=0, column=2, sticky="nsew")

main = Frame(root)
main.grid(row=1, column=0, sticky="nsew")
main.rowconfigure(0, weight=1)
main.columnconfigure(0, weight=1)
note_list = Listbox(main, border=0, font=("Segoe UI", 11))
note_list.grid(row=0, column=0, sticky="nsew")
scrollbar = Scrollbar(main, command=note_list.yview)
scrollbar.grid(row=0, column=1, sticky="nsew")
note_list.configure(yscrollcommand=scrollbar.set)

menuB3 = Menu(root, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
menuB3.add_command(label="Open", command=open_note)
menuB3.add_command(label="Rename", command=rename)
menuB3.add_command(label="Delete", command=delete)
menuB3.add_separator()
menuB3.add_command(label="Delete All", command=delete_all)
menuB3.add_command(label="Clipboard", command=clipboard)
note_list.bind("<Button-3>", b3_menu)

root.bind("<Control-n>", lambda i: new())
root.bind("<Control-N>", lambda i: new())
root.bind("<F1>", lambda i: help())
root.bind("<F2>", lambda i: rename())
note_list.bind("<Double-Button-1>", lambda i: open_note())
note_list.bind("<F5>", lambda i: open_note())
note_list.bind("<Return>", lambda i: open_note())
note_list.bind("<Delete>", lambda i: delete())
root.mainloop()
