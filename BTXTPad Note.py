from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
import datetime, random

def cut(note):
    try:
        note.clipboard_clear()
        note.delete(SEL_FIRST, SEL_LAST)
        note.clipboard_append(note.get(SEL_FIRST, SEL_LAST))
    except:
        note.get(1.0, END)

def copy(note):
    note.clipboard_clear()
    try:
        note.clipboard_append(note.get(SEL_FIRST, SEL_LAST))
    except:
        note.clipboard_append(note.get(1.0, END))

def delete_text(note):
    try:
        note.delete(SEL_FIRST, SEL_LAST)
    except:
        if messagebox.askyesno("BTXTPad Note", "Do you want to delete all text in this note?"):
            note.delete(1.0, END)

def move_to_front(note):
    try:
        text = note.get(SEL_FIRST, SEL_LAST)
        note.delete(SEL_FIRST, SEL_LAST)
        note.insert(1.0, text)
    except:
        note.get(1.0, END)

def toggle_menubar(window, empty_menubar, menubar):
    if window.cget("menu") == str(menubar):
        window.configure(menu=empty_menubar)
    else:
        window.configure(menu=menubar)

def set_icon(window, icon_path):
    try:
        window.iconbitmap(icon_path)
    except:
        window.iconbitmap()
    
def set_theme(note, bg, bg2):
    note.configure(background=bg)
    note.tag_configure(SEL, background=bg2)

def pin(window, menubar):
    if menubar.entrycget(2, "label") == "Pin":
        menubar.entryconfig(2, label="Unpin")
    else:
        menubar.entryconfig(2, label="Pin")
    window.attributes("-topmost", not window.attributes("-topmost"))

def new_note(title):
    global notes
    if title == "":
        title = str(datetime.datetime.now())
        window_title = str(datetime.datetime.now().time())
    else:
        window_title = title
    if title == "Clipboard":
        messagebox.showerror("BTXTPad Note", "The provided name is invalid.")
        bar.focus_set()
    elif title not in note_list.get(0, END):
        view_toolbar()
        window = Tk()
        window.title(window_title)
        window.geometry("254x254")
        window.minsize(254, 254)
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        window.protocol("WM_DELETE_WINDOW", lambda: window.withdraw())
        set_icon(window, "icon-default.ico")

        empty_menubar = Menu(window, tearoff=False)
        menubar = Menu(window, tearoff=False)

        menuColor = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
        menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[0], list(colors.values())[0]), background="#fc5", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[1], list(colors.values())[1]), background="#5cf", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[2], list(colors.values())[2]), background="#d8d", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[3], list(colors.values())[3]), background="#8d8", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[4], list(colors.values())[4]), background="#f84", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[5], list(colors.values())[5]), background="#bbb", foreground="#000")

        menuIcon = Menu(window, tearoff=False, activeborderwidth=2.5)
        menuIcon.add_command(label="Default", command=lambda: set_icon(window, "icon-default.ico"), activebackground="#06b", activeforeground="#fff")
        menuIcon.add_command(label="Classic", command=lambda: set_icon(window, "icon-classic.ico"), activebackground="#f80", activeforeground="#000")
        menuIcon.add_separator()
        menuIconRGB = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
        menuIcon.add_cascade(label="RGB", menu=menuIconRGB, activebackground="#444", activeforeground="#fff")
        menuIconRGB.add_command(label="Red", background="#f00", foreground="#fff", command=lambda: set_icon(window, "icon0.ico"))
        menuIconRGB.add_command(label="Green", background="#0f0", foreground="#000", command=lambda: set_icon(window, "icon1.ico"))
        menuIconRGB.add_command(label="Blue", background="#00f", foreground="#fff", command=lambda: set_icon(window, "icon2.ico"))
        menuIconCYMK = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
        menuIcon.add_cascade(label="CYMK", menu=menuIconCYMK, activebackground="#444", activeforeground="#fff")
        menuIconCYMK.add_command(label="Cyan", background="#0ff", foreground="#000", command=lambda: set_icon(window, "icon3.ico"))
        menuIconCYMK.add_command(label="Yellow", background="#ff0", foreground="#000", command=lambda: set_icon(window, "icon4.ico"))
        menuIconCYMK.add_command(label="Magenta", background="#f0f", foreground="#fff", command=lambda: set_icon(window, "icon5.ico"))
        menuIconCYMK.add_command(label="Black", background="#000", foreground="#fff", command=lambda: set_icon(window, "icon6.ico"))
        menuIconMore = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
        menuIcon.add_cascade(label="More", menu=menuIconMore, activebackground="#444", activeforeground="#fff")
        menuIconMore.add_command(label="Orange", background="#f80", foreground="#000", command=lambda: set_icon(window, "icon7.ico"))
        menuIconMore.add_command(label="Brown", background="#840", foreground="#fff", command=lambda: set_icon(window, "icon8.ico"))
        menuIconMore.add_command(label="Grey", background="#888", foreground="#fff", command=lambda: set_icon(window, "icon9.ico"))

        menubar.add_cascade(label="Icon", menu=menuIcon)
        menubar.add_cascade(label="Background", menu=menuColor)
        menubar.add_command(label="Pin", command=lambda: pin(window, menubar))
        menubar.add_command(label="Save", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(note.get(1.0, END)))

        menuB3_note = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
        menuB3_note.add_command(label="Undo", command=lambda: note.edit_undo())
        menuB3_note.add_command(label="Redo", command=lambda: note.edit_redo())
        menuB3_note.add_separator()
        menuB3_note.add_command(label="Cut", command=lambda: cut(note))
        menuB3_note.add_command(label="Copy", command=lambda: copy(note))
        menuB3_note.add_command(label="Paste", command=lambda: note.insert(INSERT, note.selection_get(selection="CLIPBOARD")))
        menuB3_note.add_command(label="Delete", command=lambda: delete_text(note))
        menuB3_note.add_separator()
        menuB3_note.add_command(label="Select All", command=lambda: note.tag_add(SEL, 1.0, END))
        menuB3_note.add_command(label="Move to front", command=lambda: move_to_front(note))

        note = Text(window, bd=8, relief=FLAT, undo=True, wrap=WORD, background=random.choice(["#fc5", "#5cf", "#d8d", "#8d8", "#f84", "#bbb"]), foreground="#000", font=("", 11))
        note.grid(row=0, column=0, sticky="nsew")
        note.tag_configure(SEL, background=colors[note["bg"]], foreground="#000")

        notes[title] = note
        refresh()

        window.bind("<Double-Button-1>", lambda i: toggle_menubar(window, empty_menubar, menubar))
        window.bind("<Button-3>", lambda event: b3_menu_note(event, menuB3_note))
        window.mainloop()
    else:
        messagebox.showerror("BTXTPad Note", "The provided name has already been used.")
        bar.focus_set()

def new():
    toolbar.grid_forget()
    bar.delete(0, END)
    toolbar_new.grid(row=0, column=0, sticky="nsew")
    bar.focus_set()

def save_all():
    all_notes = []
    for note in notes:
        all_notes.append(f"{note}:\n{notes[note].get(1.0, END)}\n")
    all_notes = "".join(all_notes)
    open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(all_notes)

def delete_all():
    global notes
    ch = messagebox.askyesno("BTXTPad Note", "Are you sure that you want to delete all notes?")
    if ch:
        for note in notes:
            notes[note].winfo_toplevel().destroy()
        notes = {}
        refresh()

def open_note():
    if note_list.curselection() != ():
        title = note_list.get(note_list.curselection())
        note = notes[title]
        notes.pop(note_list.get(note_list.curselection()))
        notes[title] = note
        notes[note_list.get(note_list.curselection())].winfo_toplevel().deiconify()
        refresh()

def close_note():
    if note_list.curselection() != ():
        notes[note_list.get(note_list.curselection())].winfo_toplevel().withdraw()

def rename():
    if note_list.curselection() != ():
        toolbar.grid_forget()
        bar_1.delete(0, END)
        bar_1.insert(INSERT, notes[note_list.get(note_list.curselection())].winfo_toplevel().wm_title())
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

def save():
    if note_list.curselection() != ():
        open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(notes[note_list.get(note_list.curselection())].get(1.0, END))
    
def delete():
    global notes
    if note_list.curselection() != ():
        ch = messagebox.askyesno("BTXTPad Note", f"Are you sure that you want to delete \"{note_list.get(note_list.curselection())}\"?")
        if ch:
            notes[note_list.get(note_list.curselection())].winfo_toplevel().destroy()
            notes.pop(note_list.get(note_list.curselection()))
        refresh()

def view_toolbar():
    toolbar_new.grid_forget()
    toolbar_rename.grid_forget()
    toolbar.grid(row=0, column=0, sticky="nsew")
    toolbar.focus_set()

def clipboard():
    if "Clipboard" not in notes:
        create_clipboard()
        
def create_clipboard():
    window = Tk()
    window.title("Clipboard")
    window.geometry("254x254")
    window.minsize(254, 254)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    window.protocol("WM_DELETE_WINDOW", lambda: window.withdraw())
    set_icon(window, "icon-default.ico")

    empty_menubar = Menu(window, tearoff=False)
    menubar = Menu(window, tearoff=False)

    menuColor = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
    menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[0], list(colors.values())[0]), background="#fc5", foreground="#000")
    menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[1], list(colors.values())[1]), background="#5cf", foreground="#000")
    menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[2], list(colors.values())[2]), background="#d8d", foreground="#000")
    menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[3], list(colors.values())[3]), background="#8d8", foreground="#000")
    menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[4], list(colors.values())[4]), background="#f84", foreground="#000")
    menuColor.add_command(label="Aa", command=lambda: set_theme(note, list(colors.keys())[5], list(colors.values())[5]), background="#bbb", foreground="#000")

    menuIcon = Menu(window, tearoff=False, activeborderwidth=2.5)
    menuIcon.add_command(label="Default", command=lambda: set_icon(window, "icon-default.ico"), activebackground="#06b", activeforeground="#fff")
    menuIcon.add_command(label="Classic", command=lambda: set_icon(window, "icon-classic.ico"), activebackground="#f80", activeforeground="#000")
    menuIcon.add_separator()
    menuIconRGB = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
    menuIcon.add_cascade(label="RGB", menu=menuIconRGB, activebackground="#444", activeforeground="#fff")
    menuIconRGB.add_command(label="Red", background="#f00", foreground="#fff", command=lambda: set_icon(window, "icon0.ico"))
    menuIconRGB.add_command(label="Green", background="#0f0", foreground="#000", command=lambda: set_icon(window, "icon1.ico"))
    menuIconRGB.add_command(label="Blue", background="#00f", foreground="#fff", command=lambda: set_icon(window, "icon2.ico"))
    menuIconCYMK = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
    menuIcon.add_cascade(label="CYMK", menu=menuIconCYMK, activebackground="#444", activeforeground="#fff")
    menuIconCYMK.add_command(label="Cyan", background="#0ff", foreground="#000", command=lambda: set_icon(window, "icon3.ico"))
    menuIconCYMK.add_command(label="Yellow", background="#ff0", foreground="#000", command=lambda: set_icon(window, "icon4.ico"))
    menuIconCYMK.add_command(label="Magenta", background="#f0f", foreground="#fff", command=lambda: set_icon(window, "icon5.ico"))
    menuIconCYMK.add_command(label="Black", background="#000", foreground="#fff", command=lambda: set_icon(window, "icon6.ico"))
    menuIconMore = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
    menuIcon.add_cascade(label="More", menu=menuIconMore, activebackground="#444", activeforeground="#fff")
    menuIconMore.add_command(label="Orange", background="#f80", foreground="#000", command=lambda: set_icon(window, "icon7.ico"))
    menuIconMore.add_command(label="Brown", background="#840", foreground="#fff", command=lambda: set_icon(window, "icon8.ico"))
    menuIconMore.add_command(label="Grey", background="#888", foreground="#fff", command=lambda: set_icon(window, "icon9.ico"))

    menubar.add_cascade(label="Icon", menu=menuIcon)
    menubar.add_cascade(label="Background", menu=menuColor)
    menubar.add_command(label="Pin", command=lambda: pin(window, menubar))
    menubar.add_command(label="Save", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(note.get(1.0, END)))

    note = Text(window, bd=8, relief=FLAT, undo=True, wrap=WORD, background=random.choice(["#fc5", "#5cf", "#d8d", "#8d8", "#f84", "#bbb"]), foreground="#000", font=("", 11))
    note.grid(row=0, column=0, sticky="nsew")
    note.tag_configure(SEL, background=colors[note["bg"]], foreground="#000")

    notes["Clipboard"] = note
    refresh()

    window.bind("<Double-Button-1>", lambda i: toggle_menubar(window, empty_menubar, menubar))
    window.mainloop()

def refresh_clipboard():
    global after_function
    if "Clipboard" in notes:
        notes["Clipboard"].configure(state=NORMAL)
        notes["Clipboard"].delete(1.0, END)
        notes["Clipboard"].insert(INSERT, Text().selection_get(selection="CLIPBOARD"))
        notes["Clipboard"].configure(state=DISABLED)
    after_function = root.after(100, refresh_clipboard)

def help():
    window = Tk()
    try:
        window.iconbitmap("icon-default.ico")
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
     
def b3_menu(event):
    if note_list.curselection() == ():
        menuB3_no_sel.tk_popup(event.x_root, event.y_root)
    else:
        if notes[note_list.get(note_list.curselection())].winfo_toplevel().winfo_viewable() == 0:
            menuB3_sel.tk_popup(event.x_root, event.y_root)  
        else:
            menuB3_sel_active.tk_popup(event.x_root, event.y_root)

def b3_menu_note(event, menu):
    menu.tk_popup(event.x_root, event.y_root)
    
root = Tk()
root.title("BTXTPad Note")
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

after_function = ""

notes = {}
colors = {"#fc5": "#d19e27", "#5cf": "#279ed1", "#d8d": "#af5aaf", "#8d8": "#5aaf5a", "#f84": "#d15a16", "#bbb": "#8d8d8d"}

try:
    root.iconbitmap("icon-default.ico")
finally:
    root.geometry("325x500")

toolbar = Frame(root, border=8)
toolbar.grid(row=0, column=0, sticky="nsew")
for i in range(0, 3):
    toolbar.columnconfigure(i, weight=1)
button_new = Button(toolbar, text="New", command=new)
button_new.grid(row=0, column=0, sticky="nsew")
button_rename = Button(toolbar, text="Save All", command=save_all)
button_rename.grid(row=0, column=1, sticky="nsew")
button_delete = Button(toolbar, text="Delete All", command=delete_all)
button_delete.grid(row=0, column=2, sticky="nsew")

toolbar_new = Frame(root, border=8)
toolbar_new.columnconfigure(0, weight=1)
bar = Entry(toolbar_new)
bar.grid(row=0, column=0, sticky="nsew")
bar.bind("<Return>", lambda i: new_note(bar.get()))
button_ok = Button(toolbar_new, text="OK", command=lambda: new_note(bar.get()))
button_ok.grid(row=0, column=1, sticky="nsew")
button_cancel = Button(toolbar_new, text="Cancel", command=view_toolbar)
button_cancel.grid(row=0, column=2, sticky="nsew")

toolbar_rename = Frame(root, border=8)
toolbar_rename.columnconfigure(0, weight=1)
bar_1 = Entry(toolbar_rename)
bar_1.grid(row=0, column=0, sticky="nsew")
bar_1.bind("<Return>", lambda i: rename_note())
button_ok_1 = Button(toolbar_rename, text="Rename", command=rename_note)
button_ok_1.grid(row=0, column=1, sticky="nsew")
button_cancel_1 = Button(toolbar_rename, text="Cancel", command=view_toolbar)
button_cancel_1.grid(row=0, column=2, sticky="nsew")

main = Frame(root)
main.grid(row=1, column=0, sticky="nsew")
main.rowconfigure(0, weight=1)
main.columnconfigure(0, weight=1)
note_list = Listbox(main, border=8, relief=FLAT, font=("Segoe UI", 11))
note_list.grid(row=0, column=0, sticky="nsew")
scrollbar = Scrollbar(main, command=note_list.yview)
scrollbar.grid(row=0, column=1, sticky="nsew")
note_list.configure(yscrollcommand=scrollbar.set)

menuB3_no_sel = Menu(root, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
menuB3_no_sel.add_command(label="Clipboard", command=clipboard)
menuB3_no_sel.add_command(label="Help", command=help)

menuB3_sel = Menu(root, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
menuB3_sel.add_command(label="Open", command=open_note)
menuB3_sel.add_command(label="Rename", command=rename)
menuB3_sel.add_command(label="Save", command=save)
menuB3_sel.add_command(label="Delete", command=delete)
menuB3_sel.add_separator()
menuB3_sel.add_command(label="Clipboard", command=clipboard)
menuB3_sel.add_command(label="Help", command=help)

menuB3_sel_active = Menu(root, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
menuB3_sel_active.add_command(label="Close", command=close_note)
menuB3_sel_active.add_command(label="Rename", command=rename)
menuB3_sel_active.add_command(label="Save", command=save)
menuB3_sel_active.add_command(label="Delete", command=delete)
menuB3_sel_active.add_separator()
menuB3_sel_active.add_command(label="Clipboard", command=clipboard)
menuB3_sel_active.add_command(label="Help", command=help)

note_list.bind("<Button-3>", b3_menu)

root.bind("<Control-n>", lambda i: new())
root.bind("<Control-N>", lambda i: new())
root.bind("<F1>", lambda i: help())
root.bind("<F2>", lambda i: rename())
note_list.bind("<Double-Button-1>", lambda i: open_note())
note_list.bind("<F5>", lambda i: open_note())
note_list.bind("<Return>", lambda i: open_note())
note_list.bind("<Delete>", lambda i: delete())


root.after(100, refresh_clipboard)

root.mainloop()