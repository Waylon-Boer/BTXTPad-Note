from tkinter import *
from tkinter import messagebox, filedialog
import datetime
class __init__():
    def copy(self):
        self.clipboard_clear()
        try:
            self.clipboard_append(self.get("sel.first", "sel.last"))
        except:
            self.clipboard_append(self.get(1.0, "end"))  
    def note():
        root = Tk()
        root.geometry("254x254")
        root.title(str(datetime.datetime.now().date()))
        root.attributes("-toolwindow", 1)
        root.attributes("-topmost", 1)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        m = Menu(root)
        root.config(menu=m)
        mTheme = Menu(root, tearoff=0)
        m.add_cascade(label="•", menu=mTheme)
        mTheme.add_command(label="Aa", command=lambda: note.configure(bg="#fc5", fg="#000"), background="#fc5", foreground="#000")
        mTheme.add_command(label="Aa", command=lambda: note.configure(bg="#5cf", fg="#000"), background="#5cf", foreground="#000")
        mTheme.add_command(label="Aa", command=lambda: note.configure(bg="#f86", fg="#000"), background="#f86", foreground="#000")
        mTheme.add_command(label="Aa", command=lambda: note.configure(bg="#abc", fg="#000"), background="#abc", foreground="#000")
        note = Text(root, bd=8, relief=FLAT, undo=True, background="#fc5", foreground="#000", font=("", 11))
        note.grid(row=0, column=0, sticky="nsew")
        m.add_command(label="<", command=lambda: note.edit_undo())
        m.add_command(label=">", command=lambda: note.edit_redo())
        m.add_command(label="Copy", command=lambda: __init__.copy(note))
        m.add_command(label="Del", command=lambda: note.delete(1.0, "end"))
        m.add_command(label="Export", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(str(datetime.datetime.now().date())+"\n\n"+note.get(1.0, "end")))
        m.add_command(label="Info", command=lambda: messagebox.showinfo("About BTXTPad Note", "BTXTPad Note: A lightweight note app\nCopyright (C) 2022-" + str(datetime.datetime.now().year) +": Waylon Boer\n\nMIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\nBTXTPad Note is based on BTXTPad"))
        m.add_command(label="+", command=__init__.note)
        root.mainloop()
if __name__ == "__main__":
    __init__.note()
