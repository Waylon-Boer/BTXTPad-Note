import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog, font
import datetime, os, json

class BTXTPadNoteApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BTXTPad Note")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=0, minsize=325)
        self.root.columnconfigure(1, weight=1)
        self.root.resizable(width=False, height=True)
        self.root["bg"] = "#FFD980"

        self.pages = {}
        self.current_page = ""
        self.page_colors = {"#FFE099": "#D1B26B", "#99E0FF": "#6BB2D1", "#FF99FF": "#D16BD1", "#99FF99": "#6BD16B", "#FFBE99": "#D1906B", "#CCCCCC": "#9E9E9E"}
        self.note_colors = {"#FFCC55": "#D19E27", "#55CCFF": "#279ED1", "#DD88DD": "#AF5AAF", "#88DD88": "#5AAF5A", "#FF8844": "#D16526", "#BBBBBB": "#8D8D8D"}

        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        self.root.geometry("325x500")
        
        self.toolbar = tk.Frame(self.root, border=10)
        self.toolbar.grid(row=0, column=0, sticky="nsew")
        for i in range(0, 3):
            self.toolbar.columnconfigure(i, weight=1)

        self.button_new_page = ttk.Button(self.toolbar, text="New Page", command=lambda: self.new_page("New Page", 0, ""))
        self.button_new_page.grid(row=0, column=0, sticky="nsew")
        self.button_new_note = ttk.Button(self.toolbar, text="New Note", command=self.new_note)
        self.button_new_note.grid(row=0, column=1, sticky="nsew")
        self.button_open = ttk.Button(self.toolbar, text="Open", command=self.open_file)
        self.button_open.grid(row=0, column=2, sticky="nsew")

        self.main = tk.Frame(self.root)
        self.main.grid(row=1, column=0, sticky="nsew")
        self.main.rowconfigure(0, weight=1)
        self.main.columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(self.main, border=10, relief="flat", highlightthickness=0, font=("Segoe UI", 11))
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.scrollbar = tk.Scrollbar(self.main, command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="nsew")
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.listbox.bind("<Double-Button-1>", lambda event: self.open_page())
        self.listbox.bind("<Return>", lambda event: self.open_page())

        self.menuListbox = tk.Menu(self.root, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
        self.menuListbox.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.menuListbox.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.menuListbox.add_command(label="Save All", command=self.save_all, accelerator="Ctrl+Shift+S")
        self.menuListbox.add_separator()
        self.menuListbox.add_command(label="Import", command=self.import_file, accelerator="Ctrl+R")
        self.menuListbox.add_command(label="Export", command=self.export_file, accelerator="Ctrl+E")
        self.menuListbox.add_separator()
        self.menuListbox.add_command(label="Help", command=self.help_window, accelerator="F1")
        self.listbox.bind("<Button-3>", lambda event: self.menuListbox.tk_popup(event.x_root, event.y_root))

        self.framePageToolbar = tk.Frame(self.root)
        self.framePageToolbar.grid(row=0, column=1, sticky="nsew", padx=10, pady=(10, 3))
        self.framePageToolbar.columnconfigure(0, weight=1)

        self.page_title_bar = tk.Entry(self.framePageToolbar, relief="flat", font=(font.nametofont("TkDefaultFont").actual()["family"], 11, "bold"))
        self.page_title_bar.grid(row=0, column=0, sticky="nsew")

        self.menuPageTitleBar = tk.Menu(self.root, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
        self.menuPageTitleBar.add_command(label="Cut", command=lambda: (self.page_title_bar.event_generate("<<Cut>>"), self.rename_page()), accelerator="Ctrl+X")
        self.menuPageTitleBar.add_command(label="Copy", command=lambda: self.page_title_bar.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        self.menuPageTitleBar.add_command(label="Paste", command=lambda: (self.page_title_bar.event_generate("<<Paste>>"), self.rename_page()), accelerator="Ctrl+V")
        self.menuPageTitleBar.add_separator()
        self.menuPageTitleBar.add_command(label="Select All", command=lambda: self.page_title_bar.event_generate("<<SelectAll>>"), accelerator="Ctrl+A")
        self.page_title_bar.bind("<Button-3>", lambda event: self.menuPageTitleBar.tk_popup(event.x_root, event.y_root))

        self.buttonPageColor = tk.Menubutton(self.framePageToolbar, text="<<", bd=0, relief="flat", activebackground="#444444", activeforeground="#FFFFFF", font=(font.nametofont("TkDefaultFont").actual()["family"], 10), direction="left")
        self.buttonPageColor.grid(row=0, column=1, sticky="nsew")
        self.menuPageColor = tk.Menu(self.buttonPageColor, tearoff=False, activeborderwidth=2.5, activebackground="#444444", activeforeground="#FFFFFF")

        self.menuPageColor.add_command(command=lambda: self.set_page_color(list(self.page_colors.keys())[0], list(self.page_colors.values())[0]), background=list(self.page_colors.keys())[0], foreground="#000000", label="Yellow")
        self.menuPageColor.add_command(command=lambda: self.set_page_color(list(self.page_colors.keys())[1], list(self.page_colors.values())[1]), background=list(self.page_colors.keys())[1], foreground="#000000", label="Blue")
        self.menuPageColor.add_command(command=lambda: self.set_page_color(list(self.page_colors.keys())[2], list(self.page_colors.values())[2]), background=list(self.page_colors.keys())[2], foreground="#000000", label="Pink")
        self.menuPageColor.add_command(command=lambda: self.set_page_color(list(self.page_colors.keys())[3], list(self.page_colors.values())[3]), background=list(self.page_colors.keys())[3], foreground="#000000", label="Green")
        self.menuPageColor.add_command(command=lambda: self.set_page_color(list(self.page_colors.keys())[4], list(self.page_colors.values())[4]), background=list(self.page_colors.keys())[4], foreground="#000000", label="Orange")
        self.menuPageColor.add_command(command=lambda: self.set_page_color(list(self.page_colors.keys())[5], list(self.page_colors.values())[5]), background=list(self.page_colors.keys())[5], foreground="#000000", label="Grey")
        self.buttonPageColor.configure(menu=self.menuPageColor)

        self.menuPage = tk.Menu(self.root, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
        self.menuPage.add_command(label="Undo", command=lambda: self.pages[self.current_page].event_generate("<<Undo>>"))
        self.menuPage.add_command(label="Redo", command=lambda: self.pages[self.current_page].event_generate("<<Redo>>"))
        self.menuPage.add_separator()
        self.menuPage.add_command(label="Cut", command=lambda: self.pages[self.current_page].event_generate("<<Cut>>"))
        self.menuPage.add_command(label="Copy", command=lambda: self.pages[self.current_page].event_generate("<<Copy>>"))
        self.menuPage.add_command(label="Paste", command=lambda: self.pages[self.current_page].event_generate("<<Paste>>"))
        self.menuPage.add_command(label="Select All", command=lambda: self.pages[self.current_page].event_generate("<<SelectAll>>"))
        self.menuPage.add_separator()
        self.menuPage.add_command(label="Delete", command=lambda: self.pages[self.current_page].event_generate("<<Clear>>"))

        self.menuInsert = tk.Menu(self.root, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
        self.menuInsert.add_command(label="Date & Time", command=lambda: self.pages[self.current_page].insert(tk.INSERT, datetime.datetime.now()))
        self.menuInsert.add_separator()
        self.menuInsert.add_command(label="Bulleted List", command=lambda: self.pages[self.current_page].insert(tk.INSERT, "\n• "))
        self.menuInsert.add_command(label="Numbered List", command=lambda: self.pages[self.current_page].insert(tk.INSERT, "\n1.\t"))
        self.menuPage.add_cascade(label="Insert", menu=self.menuInsert)
        self.menuPage.add_separator()
        self.menuPage.add_cascade(label="Remove", command=self.remove_page)

        self.root.bind("<Control-e>", lambda event: self.export_file())
        self.root.bind("<Control-E>", lambda event: self.export_file())
        self.root.bind("<Control-n>", lambda event: self.new_page("New Page", 0, ""))
        self.root.bind("<Control-N>", lambda event: self.new_page("New Page", 0, ""))
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-O>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-S>", lambda event: self.save_file())
        self.root.bind("<Control-Shift-s>", lambda event: self.save_all())
        self.root.bind("<Control-Shift-S>", lambda event: self.save_all())
        self.root.bind("<Control-r>", lambda event: self.import_file())
        self.root.bind("<Control-R>", lambda event: self.import_file())
        self.root.bind("<Control-t>", lambda event: self.new_note())
        self.root.bind("<Control-T>", lambda event: self.new_note())
        self.root.bind("<F1>", lambda event: self.help_window())
        self.root.bind("<F2>", lambda event: self.go_to_title_bar())
        self.root.bind("<F5>", lambda event: self.open_file())
        self.root.bind("<F12>", lambda event: self.save_file())

    def new_page(self, title, pageColor, text):
        if title in list(self.pages.keys()):
            num = 2
            temp_title = f"{title} ({num})"
            while temp_title in list(self.pages.keys()):
                num += 1
                temp_title = f"{title} ({num})"
            title = temp_title

        self.current_page = title
        self.page_title_bar.delete(0, "end")
        self.page_title_bar.insert(0, title)
        self.page_title_bar.unbind("<KeyRelease>")
        self.page_title_bar.bind("<KeyRelease>", lambda event: self.rename_page())

        self.root["bg"] = list(self.page_colors.keys())[0]
        self.page_title_bar.configure(background=list(self.page_colors.keys())[0], foreground="#000000", insertbackground="#000000")

        page = tk.Text(self.root, relief="flat", undo=True, wrap="word", font=(font.nametofont("TkDefaultFont").actual()["family"], 11))
        page.insert(1.0, text)
        page.grid(row=1, column=1, sticky="nsew", padx=10, pady=(3, 10))
        page.bind("<Control-w>", lambda event: self.remove_page())
        page.bind("<Control-W>", lambda event: self.remove_page())
        page.bind("<Button-3>", lambda event: self.menuPage.tk_popup(event.x_root, event.y_root))
        page.bind("<Return>", lambda event: self.continue_list(page))
        page.focus_set()

        self.pages[title] = page
        self.set_page_color(list(self.page_colors.keys())[pageColor], list(self.page_colors.values())[pageColor])
        self.refresh()

    def open_page(self):
        selection = self.listbox.curselection()
        if selection:
            for page in self.pages.values():
                page.grid_forget()
            self.current_page = self.listbox.get(selection[0])
            self.page_title_bar.delete(0, "end")
            self.page_title_bar.insert(0, self.current_page)
            page = self.pages[self.current_page]
            self.set_page_color(page.cget("bg"), self.page_colors[page.cget("bg")])
            page.grid(row=1, column=1, sticky="nsew", padx=10, pady=(3, 10))
            self.pages.pop(self.current_page)
            self.pages[self.current_page] = page
            self.refresh()

    def rename_page(self):
        if self.current_page:
            note = self.pages[self.current_page]
            title = self.page_title_bar.get()
            if title == "":
                title = "New Page"
            if not title.strip():
                return
            if title == self.current_page:
                return

            self.pages.pop(self.current_page)
            if title in self.pages:
                num = 2
                temp_title = f"{title} ({num})"
                while temp_title in self.pages:
                    num += 1
                    temp_title = f"{title} ({num})"
                title = temp_title

            self.pages[title] = note
            self.current_page = title
            self.page_title_bar.delete(0, "end")
            self.page_title_bar.insert(0, self.current_page)
            self.refresh()

    def remove_page(self):
        if not self.current_page:
            return
        if self.pages[self.current_page].get(1.0, "end-1c") == "":
            ch = 1
        else:
            ch = messagebox.askyesno("BTXTPad Note", "Do you want to delete this page?")
        if ch:
            page_title = self.current_page
            self.pages[page_title].grid_forget()
            self.page_title_bar.delete(0, "end")
            self.current_page = ""
            self.pages.pop(page_title)
            self.refresh()
            if self.pages:
                self.listbox.selection_set(0)
                self.listbox.activate(0)
                self.listbox.see(0)
                self.open_page()
            else:
                self.current_page = ""

    def refresh(self):
        self.listbox.delete(0, "end")
        for i in dict(reversed(list(self.pages.items()))):
            self.listbox.insert("end", i)
        if self.pages == {}:
            if self.root.resizable()[0] == True:
                self.root.geometry(f"325x{self.root.geometry().split('+')[0].split('x')[1]}")
                self.root.resizable(width=False, height=True)
                self.root.minsize(width=325, height=500)
        else:
            if self.root.resizable()[0] == False:
                self.root.resizable(width=True, height=True)
                self.root.minsize(width=650, height=500)

    def set_note_color(self, window, note_title_bar, buttonNoteColor, note, bg, bg2):
        window["bg"] = bg
        note_title_bar.configure(background=bg, foreground="#000000", insertbackground="#000000", selectbackground=bg2, selectforeground="#000000")
        buttonNoteColor.configure(background=bg, foreground="#000000", activebackground=bg2, activeforeground="#000000")
        note.configure(background=bg, foreground="#000000", insertbackground="#000000")
        note.tag_configure(tk.SEL, background=bg2, foreground="#000000")

    def set_page_color(self, bg, bg2):
        self.root["bg"] = bg
        self.framePageToolbar["bg"] = bg
        self.page_title_bar.configure(background=bg, foreground="#000000", insertbackground="#000000", selectbackground=bg2, selectforeground="#000000")
        self.buttonPageColor.configure(background=bg, foreground="#000000", activebackground=bg2, activeforeground="#000000")
        self.pages[self.current_page].configure(background=bg, foreground="#000000", insertbackground="#000000")
        self.pages[self.current_page].tag_configure(tk.SEL, background=bg2, foreground="#000000")

    def continue_list(self, text_widget):  
        if text_widget.index("insert") == text_widget.index(f"{text_widget.index('insert').split('.')[0]}.end"):
            start = str(int(str(text_widget.index("insert")).split(".")[0])) + ".0"
            end = str(int(str(text_widget.index("insert")).split(".")[0])) + ".2"
            next_line = str(int(str(text_widget.index("insert")).split(".")[0]) + 1) + ".0"
            next_line_2 = str(int(str(text_widget.index("insert")).split(".")[0]) + 1) + ".2"
            text = text_widget.get(start, next_line)

            try:
                text_split = text.split()[0]
            except:
                text_split = ""

            if text_widget.get(start, end) == "• " and text_widget.get(next_line, next_line_2) != "• ":
                text_widget.insert(next_line, "\n• ")
                return "break"

            elif "." in text_split:
                number = text_split.replace(".", "")
                if number.isdigit():
                    number = int(number)
                    text_widget.insert(next_line, f"\n{number + 1}.\t")
                    return "break"

    def go_to_title_bar(self):
        if self.pages:
            self.page_title_bar.focus_set()

    def open_file(self):
        try:
            filepath = filedialog.askopenfilename(title="Open", filetypes=[("BTXTPad Documents", "*.btxt*"), ('Plain Text Files', "*.txt*"), ("All Files", "*.*")])
            if filepath:
                with open(filepath, "r", encoding="utf8") as file:
                    data = file.read()
                self.new_page(os.path.split(filepath)[1], 0, data)
        except:
            pass

    def save_file(self):
        if self.current_page:
            try:
                filepath = filedialog.asksaveasfilename(title="Save As", defaultextension=".btxt", filetypes=[("All Files", "*.*")])
                if filepath:
                    data = self.pages[self.current_page].get(1.0, "end-1c")
                    with open(filepath, "w", encoding="utf8") as file:
                        file.write(f"{self.current_page}:\n{data}")
            except:
                pass

    def save_all(self):
        filepath = filedialog.asksaveasfilename(title="Save All", defaultextension=".btxt", filetypes=[("All Files", "*.*")])
        if filepath:
            try:
                with open(filepath, "w", encoding="utf8") as f:
                    for title, note in reversed(list(self.pages.items())):
                        data = note.get("1.0", "end-1c")
                        f.write(f"{title}:\n{data}\n\n")
            except:
                pass

    def import_file(self):
        filepath = filedialog.askopenfilename(title="Import", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf8") as file:
                data = json.load(file)
            for i in data:
                self.new_page(i.get("title"), i.get("pageColor"), i.get("text"))
        except:
            pass

    def export_file(self):
        if not self.pages:
            return

        filepath = filedialog.asksaveasfilename(title="Export", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not filepath:
            return

        try:
            data = []
            for title, note in self.pages.items():
                text = note.get("1.0", "end-1c")
                page_color = list(self.page_colors.keys()).index(note.cget("bg"))
                data.append({"title": title, "pageColor": page_color, "text": text})
            with open(filepath, "w", encoding="utf8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except:
            pass

    def new_note(self):
        def remove_note():
            if note.get(1.0, "end-1c") == "":
                ch = 1
            else:
                ch = messagebox.askyesno("BTXTPad Note", "Do you want to delete this note?")
            if ch:
                window.destroy()
                
        window = tk.Toplevel()
        window.title("BTXTPad Note")
        window.geometry("254x254")
        window.minsize(254, 254)
        window.rowconfigure(1, weight=1)
        window.columnconfigure(0, weight=1)
        window.protocol("WM_DELETE_WINDOW", lambda: remove_note())

        try:
            window.iconbitmap("icon.ico")
        except:
            pass

        frameNoteToolbar = tk.Frame(window)
        frameNoteToolbar.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 3))
        frameNoteToolbar.columnconfigure(0, weight=1)

        note_title_bar = tk.Entry(frameNoteToolbar, relief="flat", background=list(self.note_colors.keys())[0], font=(font.nametofont("TkDefaultFont").actual()["family"], 11, "bold"))
        note_title_bar.grid(row=0, column=0, sticky="nsew")
        note_title_bar.insert(0, "New Sticky Note")

        menuNoteTitleBar = tk.Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
        menuNoteTitleBar.add_command(label="Cut", command=lambda: note_title_bar.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        menuNoteTitleBar.add_command(label="Copy", command=lambda: note_title_bar.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        menuNoteTitleBar.add_command(label="Paste", command=lambda: note_title_bar.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        menuNoteTitleBar.add_separator()
        menuNoteTitleBar.add_command(label="Select All", command=lambda: note_title_bar.event_generate("<<SelectAll>>"), accelerator="Ctrl+A")
        note_title_bar.bind("<Button-3>", lambda event: menuNoteTitleBar.tk_popup(event.x_root, event.y_root))

        buttonNoteColor = tk.Menubutton(frameNoteToolbar, text="<<", bd=0, relief="flat", activebackground="#444444", activeforeground="#FFFFFF", font=(font.nametofont("TkDefaultFont").actual()["family"], 10), direction="left")
        buttonNoteColor.grid(row=0, column=1, sticky="nsew")

        menuNote = tk.Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
        menuNote.add_command(label="Undo", command=lambda: note.event_generate("<<Undo>>"))
        menuNote.add_command(label="Redo", command=lambda: note.event_generate("<<Redo>>"))
        menuNote.add_separator()
        menuNote.add_command(label="Cut", command=lambda: note.event_generate("<<Cut>>"))
        menuNote.add_command(label="Copy", command=lambda: note.event_generate("<<Copy>>"))
        menuNote.add_command(label="Paste", command=lambda: note.event_generate("<<Paste>>"))
        menuNote.add_command(label="Select All", command=lambda: note.event_generate("<<SelectAll>>"))
        menuNote.add_separator()
        menuNote.add_command(label="Delete", command=lambda: note.event_generate("<<Clear>>"))

        menuInsert = tk.Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
        menuInsert.add_command(label="Date & Time", command=lambda: note.insert(tk.INSERT, datetime.datetime.now()))
        menuInsert.add_separator()
        menuInsert.add_command(label="Bulleted List", command=lambda: note.insert(tk.INSERT, "\n• "))
        menuInsert.add_command(label="Numbered List", command=lambda: note.insert(tk.INSERT, "\n1.\t"))
        menuNote.add_cascade(label="Insert", menu=menuInsert)
        menuNote.add_separator()
        menuNote.add_command(label="Add As Page", command=lambda: self.new_page(note_title_bar.get(), list(self.note_colors.keys()).index(note.cget("bg")), note.get(1.0, "end-1c")))

        menuNoteColor = tk.Menu(buttonNoteColor, tearoff=False, activeborderwidth=2.5, activebackground="#444444", activeforeground="#FFFFFF")
        menuNoteColor.add_command(command=lambda: self.set_note_color(window, note_title_bar, buttonNoteColor, note, list(self.note_colors.keys())[0], list(self.note_colors.values())[0]), background="#fc5", foreground="#000000", label="Yellow")
        menuNoteColor.add_command(command=lambda: self.set_note_color(window, note_title_bar, buttonNoteColor, note, list(self.note_colors.keys())[1], list(self.note_colors.values())[1]), background="#5cf", foreground="#000000", label="Blue")
        menuNoteColor.add_command(command=lambda: self.set_note_color(window, note_title_bar, buttonNoteColor, note, list(self.note_colors.keys())[2], list(self.note_colors.values())[2]), background="#d8d", foreground="#000000", label="Pink")
        menuNoteColor.add_command(command=lambda: self.set_note_color(window, note_title_bar, buttonNoteColor, note, list(self.note_colors.keys())[3], list(self.note_colors.values())[3]), background="#8d8", foreground="#000000", label="Green")
        menuNoteColor.add_command(command=lambda: self.set_note_color(window, note_title_bar, buttonNoteColor, note, list(self.note_colors.keys())[4], list(self.note_colors.values())[4]), background="#f84", foreground="#000000", label="Orange")
        menuNoteColor.add_command(command=lambda: self.set_note_color(window, note_title_bar, buttonNoteColor, note, list(self.note_colors.keys())[5], list(self.note_colors.values())[5]), background="#bbb", foreground="#000000", label="Grey")
        buttonNoteColor.configure(menu=menuNoteColor)

        note = tk.Text(window, relief="flat", undo=True, wrap="word", font=(font.nametofont("TkDefaultFont").actual()["family"], 11))
        note.grid(row=1, column=0, sticky="nsew", padx=10, pady=(3, 10))
        note.focus_set()
        note.bind("<Button-3>", lambda event: menuNote.tk_popup(event.x_root, event.y_root))
        note.bind("<Return>", lambda event: self.continue_list(note))
        self.set_note_color(window, note_title_bar, buttonNoteColor, note, list(self.note_colors.keys())[0], list(self.note_colors.values())[0])

        window.bind("<Double-Button-1>", lambda event: (window.overrideredirect(not window.overrideredirect()), window.attributes("-topmost", not window.attributes("-topmost"))))

    def help_window(self):
        window = tk.Toplevel()

        try:
            window.iconbitmap("icon.ico")
        except:
            pass

        window.title("Help - BTXTPad Note")
        window.geometry("700x510")
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        help_tabs = ttk.Notebook(window)
        help_tabs.grid(row=0, column=0, sticky="nsew")

        about = tk.Text(help_tabs, relief="flat", border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap="word", background="#e1e1e1")
        about.insert(tk.INSERT, f"BTXTPad Note: A lightweight note app\nCopyright (C) 2022-{str(datetime.datetime.now().year)}: Waylon Boer")
        about.configure(state="disabled")
        help_tabs.add(about, text="About")

        mit_license = tk.Text(help_tabs, relief="flat", border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap="word", background="#e1e1e1")
        mit_license.insert(tk.INSERT, """MIT License

Copyright (c) 2022 Waylon Boer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""")
        mit_license.configure(state="disabled")
        help_tabs.add(mit_license, text="License")

    def run(self):
        self.root.mainloop()

def run_program():
    app = BTXTPadNoteApp()
    app.run()

if __name__ == "__main__":
    run_program()
