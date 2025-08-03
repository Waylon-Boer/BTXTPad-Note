from tkinter import *
from tkinter.ttk import *
from tkinter import Label as tkLabel
from tkinter import messagebox, simpledialog, font, filedialog, scrolledtext
from urllib.request import urlopen
import os, shutil, datetime, calendar, math, html, re, random, string, webbrowser

class main():
    def new():
        global filepath, saved_text
        if editor.grid_info() == {}:
            for i in content.winfo_children():
                i.grid_forget()
            editor.grid(row=0, column=0, sticky="nsew")
        if "*" in root.wm_title():
            choice = messagebox.askyesnocancel("BTXTPad","Do you want to save the changes made to this file?")
            if choice == True:
                main.save()
                editor.delete(1.0, END)
                filepath = "Untitled"
                saved_text = "\n"
            elif choice == False:
                editor.delete(1.0, END)
                filepath = "Untitled"
                saved_text = "\n"
        editor.delete(1.0, END)
        filepath = "Untitled"
        saved_text = "\n"

    def open():
        if "*" in root.wm_title():
            choice = messagebox.askyesnocancel("BTXTPad","Do you want to save the changes made to this file?")
            if choice == True:
                main.save()
                main.open2()
            elif choice == False:
                main.open2()
        main.open2()

    def open2():
        global filepath, saved_text
        path = filepath
        if editor.grid_info() == {}:
            for i in content.winfo_children():
                i.grid_forget()
            editor.grid(row=0, column=0, sticky="nsew")
        filepath = filedialog.askopenfilename(filetypes=[("BTXTPad Documents", "*.btxt*"), ('Plain Text Files', "*.txt*"), ("HyperText Markup Language", "*.html*"), ("All Files", "*.*")])
        if filepath == "":
            filepath = path
        else:
            editor.delete(1.0, END)
            saved_text = open(filepath, "r", encoding="utf8").read()
            editor.insert(INSERT, '\n'.join(saved_text.splitlines()[:-1]))

    def save():
        global filepath, saved_text
        if filepath == "Untitled":
            main.save_as()
        else:
            open(filepath, "w", encoding='utf8').write(editor.get(1.0, END))
            saved_text = editor.get(1.0, END)

    def save_as():
        global filepath, saved_text
        path = filepath
        try:
            if filepath != "":
                filepath = filedialog.asksaveasfilename(defaultextension=".btxt", filetypes=[("All Files", "*.*")])
                open(filepath, "w", encoding='utf8').write(editor.get(1.0, END))
                saved_text = editor.get(1.0, END)
        except FileNotFoundError:
            filepath = path

    def duplicate():
        filepath = filedialog.askopenfilename(title="Copy", filetypes=[("BTXTPad Documents", "*.btxt*"), ('Plain Text Files', "*.txt*"), ("HyperText Markup Language", "*.html*"), ("Comma Separated Values", "*.csv*"), ("SubRip File Format", "*.srt*"), ("All Files", "*.*")])
        shutil.copy(filepath, filedialog.askdirectory(title="Copy to")+"/"+filepath.split("/")[len(filepath.split("/")) - 1])

    def read_edit():
        if editor["state"] == "disabled":
            editor.configure(state="normal")
        else:
            editor.configure(state="disabled")

    def cut():
        try:
            editor.clipboard_clear()
            editor.delete(SEL_FIRST, SEL_LAST)
            editor.clipboard_append(editor.get(SEL_FIRST, SEL_LAST))
        except:
            editor.get(1.0, END)

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.get(SEL_FIRST, SEL_LAST))

    def delete(self):
        try:
            self.delete(SEL_FIRST, SEL_LAST)
        except:
            self.get(1.0, END)

    def keep():
        try:
            editor.delete(1.0, SEL_FIRST)
            editor.delete(SEL_LAST, END)
        except:
            editor.get(1.0, END)

    def replace_a():
        if frameReplace.winfo_viewable() == 0:
            main.sidebar("r")
            main.replace()
        replace.focus_set()

    def go_to_a():
        if frameReplace.winfo_viewable() == 0:
            main.sidebar("r")
            main.replace()
        ln.focus_set()

    def find_next(find):
        lc = editor.search(find, editor.index(INSERT))
        editor.tag_remove(SEL, 1.0, END)
        editor.tag_add(SEL, lc, "{}.{}".format(*lc.split(".")[:-1], int(lc.split(".")[-1])+len(find)))
        editor.mark_set(INSERT, "{}.{}".format(*lc.split(".")[:-1], int(lc.split(".")[-1])+len(find)))
        editor.focus_set()

    def replace_next(find, replace):
        main.find_next(find)
        text = editor.get(SEL_FIRST, SEL_LAST)
        editor.delete(SEL_FIRST, SEL_LAST)
        editor.insert(INSERT, replace)

    def replace_all(find, replace):
        text = editor.get(1.0, END).replace(find, replace)
        editor.delete(1.0, END)
        editor.insert(INSERT, text)
        editor.delete("end-1c linestart", END)

    def go_to():
        editor.mark_set(INSERT, float(str(int(ln.get()))+"."+str(int(col.get()))))
        editor.focus_set() 

    def capitalize():
        chars = {"a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ғ", "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ", "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ", "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ", "z": "ᴢ"}
        text = editor.get(SEL_FIRST, SEL_LAST)    
        check = 0
        for i in list(chars.keys()):
            if i in text:
                check = 1
        if check == 1:
            for i in chars:
                text = text.replace(i, chars[i])
        else:
            for i in chars:
                text = text.replace(chars[i], i)
        editor.delete(SEL_FIRST, SEL_LAST)
        editor.insert(INSERT, text)

    def line(chars):
        try:
            text = editor.get(SEL_FIRST, SEL_LAST)
            editor.delete(SEL_FIRST, SEL_LAST)
            if chars in text:
                editor.insert(INSERT, text.replace(chars, ""))
            else:    
                for i in text:
                    if chars == "̶":
                        editor.insert(INSERT, chars + i)
                    else:
                        if i == " " or i == "\n" or i == "\t" or i == "\r":
                            editor.insert(INSERT, i)
                        else:
                            editor.insert(INSERT, i + chars)
        except:
            editor.insert(INSERT, chars)

    def list():
        try:
            text = editor.get(SEL_FIRST, SEL_LAST)
            editor.delete(SEL_FIRST, SEL_LAST)
            if "• " in text:
                editor.insert(INSERT, text.replace("• ", ""))
            else:
                text = re.sub(r"\d+\.\t", "", text)    
                editor.insert(INSERT, "• " + text.replace("\n", "\n• "))
        except:
            editor.insert(INSERT, "\n• ")

    def numbered_list():
        try:
            text = editor.get(SEL_FIRST, SEL_LAST)
            editor.delete(SEL_FIRST, SEL_LAST)
            if not re.search(r"\d+\.\t", text):
                text = text.split("\n")
                new_text = []
                for i in range(0, len(text)):
                    new_text.append(f"{i + 1}.\t{text[i]}")
                text = "\n".join(new_text).replace("• ", "")
            else:
                text = re.sub(r"\d+\.\t", "", text)
            editor.insert(INSERT, text)
        except:
            text = editor.get(str(int(str(editor.index(INSERT)).split(".")[0]))+".0", str(int(str(editor.index(INSERT)).split(".")[0]) + 1)+".0")
            try:
                if "." in text.split()[0]:
                    number = int(text.split()[0].replace(".", ""))
                    editor.insert(str(int(str(editor.index(INSERT)).split(".")[0]) + 1)+".0", f"\n{number + 1}.\t")
                else:
                    editor.insert(str(int(str(editor.index(INSERT)).split(".")[0]) + 1)+".0", f"\n1.\t")
            except:
                editor.insert(str(int(str(editor.index(INSERT)).split(".")[0]) + 1)+".0", f"\n1.\t")

    def increase_indent():
        try:
            text = editor.get(str(int(str(editor.index(SEL_FIRST)).split(".")[0]) - 1)+".0", SEL_LAST)
            if "\n" in text:
                editor.delete(str(int(str(editor.index(SEL_FIRST)).split(".")[0]) - 1)+".0", SEL_LAST)  
                editor.insert(INSERT, text.replace("\n", "\n\t"))
        except:
            position = editor.index(INSERT)
            text = editor.get(str(int(str(editor.index(INSERT)).split(".")[0]))+".0", str(int(str(editor.index(INSERT)).split(".")[0]) + 1)+".0")
            editor.delete(str(int(str(editor.index(INSERT)).split(".")[0]))+".0", str(int(str(editor.index(INSERT)).split(".")[0]) + 1)+".0")  
            editor.insert(INSERT, f"\t{text}")
            editor.mark_set(INSERT, position)

    def decrease_indent():
        try:
            text = editor.get(str(int(str(editor.index(SEL_FIRST)).split(".")[0]) - 1)+".0", SEL_LAST)
            if "\n" in text:
                editor.delete(str(int(str(editor.index(SEL_FIRST)).split(".")[0]) - 1)+".0", SEL_LAST)  
                editor.insert(INSERT, text.replace("\n\t", "\n"))
        except:
            position = editor.index(INSERT)
            text = editor.get(str(int(str(editor.index(INSERT)).split(".")[0]))+".0", str(int(str(editor.index(INSERT)).split(".")[0]) + 1)+".0")
            if list(text)[0] == "\t":  
                editor.delete(str(int(str(editor.index(INSERT)).split(".")[0]))+".0", str(int(str(editor.index(INSERT)).split(".")[0]) + 1)+".0")
                line = list(text)
                line.pop(0)
                editor.insert(INSERT, "".join(line))
                editor.mark_set(INSERT, position)

    def solve():
        try:
            text = editor.get("sel.first", "sel.last")
            if re.match(r'^[\d\s.+\-*/%]+$', text):
                editor.delete("sel.first", "sel.last")
                editor.insert(INSERT, eval(text))
        except:
            text = editor.get(1.0, END)

    def move_to_front(self):
        try:
            text = self.get(SEL_FIRST, SEL_LAST)
            self.delete(SEL_FIRST, SEL_LAST)
            self.insert(1.0, text)
        except:
            self.get(1.0, END)

    def pin(window, menubar):
        if menubar.entrycget(2, "label") == "Pin":
            menubar.entryconfig(2, label="Unpin")
        else:
            menubar.entryconfig(2, label="Pin")
        window.attributes("-topmost", not window.attributes("-topmost"))

    def toggle_menubar(window, menubar):
        if window.cget("menu") == str(menubar):
            window.configure(menu="")
        else:
            window.configure(menu=menubar)

    def b3_menu_note(event, menu):
        menu.tk_popup(event.x_root, event.y_root)
            
    def set_note_theme(note, bg, bg2):
        note.configure(background=bg, foreground="#000", insertbackground="#000")
        note.tag_configure(SEL, background=bg2)
        
    def note():
        window = Tk()
        window.title("Note - BTXTPad")
        window.geometry("254x254")
        window.minsize(254, 254)
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        window.protocol("WM_DELETE_WINDOW", lambda: window.withdraw())
        window.iconbitmap("")
        menubar = Menu(window, tearoff=False)
        menuColor = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
        menuColor.add_command(command=lambda: main.set_note_theme(note, list(colors.keys())[0], list(colors.values())[0]), background="#fc5", foreground="#000", label="Yellow")
        menuColor.add_command(command=lambda: main.set_note_theme(note, list(colors.keys())[1], list(colors.values())[1]), background="#5cf", foreground="#000", label="Blue")
        menuColor.add_command(command=lambda: main.set_note_theme(note, list(colors.keys())[2], list(colors.values())[2]), background="#d8d", foreground="#000", label="Pink")
        menuColor.add_command(command=lambda: main.set_note_theme(note, list(colors.keys())[3], list(colors.values())[3]), background="#8d8", foreground="#000", label="Green")
        menuColor.add_command(command=lambda: main.set_note_theme(note, list(colors.keys())[4], list(colors.values())[4]), background="#f84", foreground="#000", label="Orange")
        menuColor.add_command(command=lambda: main.set_note_theme(note, list(colors.keys())[5], list(colors.values())[5]), background="#bbb", foreground="#000", label="Grey")
        menubar.add_cascade(label="Color", menu=menuColor)
        menubar.add_command(label="Save", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(note.get(1.0, END)))
        menuB3_note = Menu(window, tearoff=False, activeborderwidth=2.5, activebackground="#e0e0e0", activeforeground="#000000")
        menuB3_note.add_command(label="Undo", command=lambda: note.edit_undo())
        menuB3_note.add_command(label="Redo", command=lambda: note.edit_redo())
        menuB3_note.add_separator()
        menuB3_note.add_command(label="Cut", command=lambda: main.cut(note))
        menuB3_note.add_command(label="Copy", command=lambda: main.copy(note))
        menuB3_note.add_command(label="Paste", command=lambda: note.insert(INSERT, note.selection_get(selection="CLIPBOARD")))
        menuB3_note.add_command(label="Delete", command=lambda: main.delete(note))
        menuB3_note.add_separator()
        menuB3_note.add_command(label="Select All", command=lambda: note.tag_add(SEL, 1.0, END))
        menuB3_note.add_command(label="Move to front", command=lambda: main.move_to_front(note))
        note = Text(window, bd=8, relief=FLAT, undo=True, wrap=WORD, background=random.choice(["#fc5", "#5cf", "#d8d", "#8d8", "#f84", "#bbb"]), foreground="#000", font=("", 11))
        note.grid(row=0, column=0, sticky="nsew")
        note.tag_configure(SEL, background=colors[note["bg"]], foreground="#000")
        window.bind("<Double-Button-1>", lambda i: main.toggle_menubar(window, menubar))
        window.bind("<Button-3>", lambda event: main.b3_menu_note(event, menuB3_note))
        window.mainloop()

    def help():
        window = Tk()
        try:
            window.iconbitmap("")
        finally:
            window.title("Help - BTXTPad")
        window.geometry("600x450")
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        help_tabs = Notebook(window, width=320)
        help_tabs.grid(row=0, column=0, sticky="nsew")
        about = Text(help_tabs, relief=FLAT, border=16, font=("Consolas", 11), wrap=WORD, background="#dcb")
        about.insert(INSERT, f"BTXTPad - A text editor\nCopyright (c) 2022-{str(datetime.datetime.now().year)}: Waylon Boer\n\nBTXTPad is a simple text editor. BTXTPad has some additional features, such as a sidebar. The default file format is .btxt, but BTXTPad also supports other file formats. There is also a standalone notetaking app available: BTXTPad Note.")
        about.configure(state=DISABLED)
        help_tabs.add(about, text="About")
        mit_license = Text(help_tabs, relief=FLAT, border=16, font=("Consolas", 11), wrap=WORD, background="#dcb")
        mit_license.insert(INSERT, """Copyright (c) 2022 Waylon Boer\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR a PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.""")
        mit_license.configure(state=DISABLED)
        help_tabs.add(mit_license, text="License")
        window.mainloop()

    def sidebar(i):
        if i == "l":
            menu_bar_sidebar.grid(row=0, column=0, sticky="nsew")
            sidebar.grid(row=1, column=0, sticky="nsew")
            menu_bar_editor.grid(row=0, column=1, sticky="nsew")
            content.grid(row=1, column=1, sticky="nsew")
            root.columnconfigure(0, weight=0, minsize=320)
            root.columnconfigure(1, weight=1)
            root.unbind("<Double-Button-1>")
        elif i == "r":
            menu_bar_editor.grid(row=0, column=0, sticky="nsew")
            content.grid(row=1, column=0, sticky="nsew")
            menu_bar_sidebar.grid(row=0, column=1, sticky="nsew")
            sidebar.grid(row=1, column=1, sticky="nsew")
            root.columnconfigure(0, weight=1)
            root.columnconfigure(1, weight=0, minsize=320)
            root.unbind("<Double-Button-1>")
        else:
            menu_bar_editor.grid(row=0, column=0, sticky="nsew")
            content.grid(row=1, column=0, sticky="nsew")
            root.columnconfigure(0, weight=1)
            root.columnconfigure(1, weight=0, minsize=0)
            menu_bar_sidebar.grid_forget()
            sidebar.grid_forget()
            editor.focus_set()
            root.unbind("<Double-Button-1>")

    def notebook():
        buttonWidgets.configure(text="Notebook")
        for i in [calc, frameReplace, frameSettings]:
            i.grid_forget()
        notebook.grid(row=0, column=0, sticky="nsew")
        notebook.focus_set()

    def calculate(option):
        text = bar.get()
        bar.delete(0, END)
        try:
            if re.match(r'^[\d\s.+\-*/%]+$', text):
                if option == "b":
                    answer = str(bin(int(eval(text))))
                elif option == "o":
                    answer = str(oct(int(eval(text))))
                elif option == "h":
                    answer = str(hex(int(eval(text))))
                elif option == "s":
                    answer = str(eval(text) ** 2)
                elif option == "r":
                    answer = str(math.sqrt(eval(text)))
                elif option == "i":
                    answer = str(1/float(eval(text)))                
                else:
                    answer = eval(text)
                bar.insert(INSERT, answer)
            else:
                bar.insert(INSERT, "Error!")
        except:
           bar.insert(INSERT, "Error!")

    def calculator():
        buttonWidgets.configure(text="Calculator")
        for i in [notebook, frameReplace, frameSettings]:
            i.grid_forget()
        calc.grid(row=0, column=0, sticky="nsew")
        bar.focus_set()

    def replace():
        buttonWidgets.configure(text="Replace")
        for i in [notebook, calc, frameSettings]:
            i.grid_forget()
        frameReplace.grid(row=0, column=0, sticky="nsew")
        find.focus_set()
        
    def theme(bg0, bg1, bg2, fg, abg):
        editor.configure(bg=bg0, fg=fg, insertbackground=fg)
        editor.tag_configure(SEL, background=bg2, foreground=fg)
        for i in ["TButton", "TCheckbutton", "TCombobox", "TEntry", "TFrame", "TLabel", "TNotebook", "TRadiobutton", "TScrollbar", "TSpinbox"]:
            a.configure(i, background=bg1)
        a.configure("TMenubutton", background=bg1, foreground=fg)
        for i in [menuFile, menuEdit, menuDelete, menuFormat, menuInsert, menuView, menuSidebar, menuWidgets, menuB3]:
            i.configure(background=bg1, foreground=fg, activebackground=abg, activeforeground=fg)
        for i in ["TCheckbutton", "TLabel", "TRadiobutton"]:
            a.configure(i, foreground=fg)
        for i in [(menuFile, 8), (menuSidebar, 0), (menuSidebar, 1), (menuSidebar, 2), (menuView, 6), (menuWidgets, 0), (menuWidgets, 1), (menuWidgets, 2), (menuWidgets, 3)]:
            i[0].entryconfig(i[1], selectcolor=fg)
        a.configure("Treeview", background=bg0, foreground=fg)
        a.configure("Custom.TFrame", background=abg)
        a.configure("Custom.TLabel", background=abg, foreground=fg)

    def settings():
        buttonWidgets.configure(text="Settings")
        for i in [notebook, calc, frameReplace]:
            i.grid_forget()
        frameSettings.grid(row=0, column=0, sticky="nsew")

    def reset_settings():
        font_family.delete(0, END)
        font_family.insert(INSERT, "Consolas")
        size.delete(0, END)
        size.insert(INSERT, 11)
        bar_wrap.delete(0, END)
        bar_wrap.insert(INSERT, "Word")
        bar_border.delete(0, END)
        bar_border.insert(INSERT, 16)
        for i in [styleBold, styleItalic, styleUnderline, styleOverstrike, always_on_top]:
            i.set(0)
        theme.set(1)

    def save_settings():
        style = []
        if styleBold.get() == 1:
            style.append("bold")
        if styleItalic.get() == 1:
            style.append("italic")
        if styleUnderline.get() == 1:
            style.append("underline")
        if styleOverstrike.get() == 1:
            style.append("overstrike")
        style = " ".join(style)
        editor.configure(font=(font_family.get(), size.get(), style), border=int(bar_border.get()))
        root.attributes("-topmost", always_on_top.get())
        if theme.get() == 1:
            main.theme("#fff", "#f0f0f0", "#e0e0e0", "#000", "#e0e0e0")
        elif theme.get() == 2:
            main.theme("#dcb", "#f0f0f0", "#bead9c", "#000", "#e0e0e0")
        elif theme.get() == 3:
            main.theme("#222", "#000", "#505050", "#fff", "#444")
        elif theme.get() == 4:
            main.theme("#000", "#000", "#2e2e2e", "#fff", "#444")  
        if bar_wrap.get() == "Disabled":
            editor.configure(wrap=NONE)
        elif bar_wrap.get() == "Character":
            editor.configure(wrap=CHAR)
        else:
            editor.configure(wrap=WORD)

    def b3_menu(event):
        menuB3.tk_popup(event.x_root, event.y_root)

    def b3_options(event):
        menuOptions.tk_popup(event.x_root, event.y_root)

    def exit():
        if "*" in root.wm_title():
            choice = messagebox.askyesnocancel("BTXTPad","Do you want to save the changes made to this file?")
            if choice == True:
                main.save()
                root.destroy()
            elif choice == False:
                root.destroy()
        else: 
             root.destroy()

    def refresh():
        ln.delete(0, END)
        ln.insert(INSERT, str(editor.index(INSERT)).split(".")[0])
        col.delete(0, END)
        col.insert(INSERT, str(editor.index(INSERT)).split(".")[1])
        try:
            text = editor.get("sel.first", "sel.last")
            char_count = len(text.replace("\n", "").replace("\t", "").replace("\r", ""))
            if char_count == 1:
                char_counter.configure(text=f"{char_count} character selected")
            else:
                char_counter.configure(text=f"{char_count} characters selected")
            word_count = len(text.split())
            if word_count == 1:
                word_counter.configure(text=f"{word_count} word selected")
            else:
                word_counter.configure(text=f"{word_count} words selected")
            line_count = len(text.split("\n")) - 1
            if line_count == 1:
                line_counter.configure(text=f"{line_count} line selected")
            else:
                line_counter.configure(text=f"{line_count} lines selected")
        except:
            text = editor.get(1.0, END)
            char_count = len(text.replace("\n", "").replace("\t", "").replace("\r", ""))
            if char_count == 1:
                char_counter.configure(text=f"{char_count} character")
            else:
                char_counter.configure(text=f"{char_count} characters")
            word_count = len(text.split())
            if word_count == 1:
                word_counter.configure(text=f"{word_count} word")
            else:
                word_counter.configure(text=f"{word_count} words")
            line_count = len(text.split("\n")) - 1
            if line_count == 1:
                line_counter.configure(text=f"{line_count} line")
            else:
                line_counter.configure(text=f"{line_count} lines")
        if editor.grid_info() == {}:
            root.title(f"{filepath.split('/')[len(filepath.split('/')) - 1]} - BTXTPad")
        else:
            if editor.get(1.0, END) == saved_text or f"{editor.get(1.0, END)}\n" == saved_text:
                root.title(f"{filepath.split('/')[len(filepath.split('/')) - 1]} - BTXTPad")
            else:
                root.title(f"*{filepath.split('/')[len(filepath.split('/')) - 1]} - BTXTPad")
        if editor.cget("state") == DISABLED:
            read_only.set(1)
        else:
            read_only.set(0)
        if sidebar.grid_info() == {}:
            sidebar_status.set(1)
        else:
            if sidebar.grid_info()["column"] == 0:
                sidebar_status.set(2)
            else:
                sidebar_status.set(3)
        full_screen.set(root.attributes("-fullscreen"))
        if notebook.grid_info() != {}:
            widget.set(1)
        if calc.grid_info() != {}:
            widget.set(2)
        if frameSettings.grid_info() != {}:
            widget.set(3)
        if frameReplace.grid_info() != {}:
            widget.set(4)

if __name__ == "__main__":
    root = Tk()
    filepath = "Untitled"
    saved_text = "\n"
    root.title("BTXTPad")
    root.geometry("800x600")
    a = Style(root)
    colors = {"#fc5": "#d19e27", "#5cf": "#279ed1", "#d8d": "#af5aaf", "#8d8": "#5aaf5a", "#f84": "#d15a16", "#bbb": "#8d8d8d"}
    try:
        root.iconbitmap("")
    except:
        root.iconbitmap("")
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.protocol('WM_DELETE_WINDOW', lambda: main.exit())
    menu_bar_editor = Frame(root, border=4)
    menu_bar_editor.grid(row=0, column=0, sticky="nsew")
    menu_bar_editor.columnconfigure(4, weight=1)
    buttonFile = Menubutton(menu_bar_editor, text="File")
    buttonFile.grid(row=0, column=0, sticky="nsew")
    buttonEdit = Menubutton(menu_bar_editor, text="Edit")
    buttonEdit.grid(row=0, column=1, sticky="nsew")
    buttonInsert = Menubutton(menu_bar_editor, text="Insert")
    buttonInsert.grid(row=0, column=2, sticky="nsew")
    buttonView = Menubutton(menu_bar_editor, text="View")
    search_bar = Entry(menu_bar_editor, width=36)
    search_bar.grid(row=0, column=4, sticky="nse", ipady=1)
    buttonView.grid(row=0, column=3, sticky="nsew")
    buttonFind = Button(menu_bar_editor, text="Find", command=lambda: main.find_next(search_bar.get()))
    buttonFind.grid(row=0, column=5, sticky="nsew")

    read_only = IntVar(value=0)
    sidebar_status = IntVar(value=1)
    full_screen = IntVar(value=0)
    widget = IntVar(value=1)

    menuFile = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuFile.add_command(label="New", command=main.new, accelerator="Ctrl+N")
    menuFile.add_command(label="Open", command=main.open, accelerator="Ctrl+O")
    menuFile.add_command(label="Save", command=main.save, accelerator="Ctrl+S")
    menuFile.add_command(label="Save As", command=main.save_as, accelerator="Ctrl+Shift+S")
    menuFile.add_separator()
    menuFile.add_command(label="Print", command=lambda: os.startfile(filepath, "print"), accelerator="Ctrl+P")
    menuFile.add_command(label="Duplicate", command=main.duplicate, accelerator="Ctrl+D")
    menuFile.add_separator()
    menuFile.add_checkbutton(label="Read-only", command=main.read_edit, accelerator="Ctrl+E", variable=read_only)
    menuFile.add_separator()
    menuFile.add_command(label="Exit", command=main.exit, accelerator="Alt+F4")
    menuEdit = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuEdit.add_command(label="Undo", command=lambda: editor.edit_undo(), accelerator="Ctrl+Z")
    menuEdit.add_command(label="Redo", command=lambda: editor.edit_redo(), accelerator="Ctrl+Y")
    menuEdit.add_separator()
    menuEdit.add_command(label="Cut", command=lambda: main.cut(), accelerator="Ctrl+X")
    menuEdit.add_command(label="Copy", command=lambda: main.copy(editor), accelerator="Ctrl+C")
    menuEdit.add_command(label="Paste", command=lambda: editor.insert(INSERT, editor.selection_get(selection="CLIPBOARD")), accelerator="Ctrl+V")
    menuEdit.add_command(label="Select All", command=lambda: editor.tag_add(SEL, 1.0, END), accelerator="Ctrl+A")
    menuEdit.add_separator()
    menuDelete = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuEdit.add_cascade(label="Delete", menu=menuDelete, accelerator="Del")
    menuDelete.add_command(label="Delete", command=lambda: main.delete(editor), accelerator="Del")
    menuDelete.add_command(label="Delete All", command=lambda: editor.delete(1.0, END), accelerator="Shift+Del")
    menuDelete.add_command(label="Keep", command=main.keep, accelerator="Ctrl+K")
    menuDelete.add_separator()
    menuDelete.add_command(label="Before", command=lambda: editor.delete(1.0, editor.index(INSERT)), accelerator="Ctrl+BS")
    menuDelete.add_command(label="After", command=lambda: editor.delete(editor.index(INSERT), END), accelerator="Ctrl+Del")
    menuEdit.add_separator()
    menuEdit.add_command(label="Find", command=search_bar.focus_set, accelerator="Ctrl+F")
    menuEdit.add_command(label="Replace", command=main.replace_a, accelerator="Ctrl+R")
    menuEdit.add_command(label="Go To", command=main.go_to_a, accelerator="Ctrl+G")
    menuEdit.add_separator()
    menuFormat = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuEdit.add_cascade(label="Format", menu=menuFormat, accelerator="F10")
    menuFormat.add_command(label="Capitalize", command=main.capitalize, accelerator="Ctrl+B")
    menuFormat.add_separator()
    menuFormat.add_command(label="Underline", command=lambda: main.line("̲"), accelerator="Ctrl+U")
    menuFormat.add_command(label="Double Underline", command=lambda: main.line("̳"), accelerator="Ctrl+Shift+U")
    menuFormat.add_command(label="Strikethrough", command=lambda: main.line("̶"), accelerator="Ctrl+Shift+X")
    menuFormat.add_separator()
    menuFormat.add_command(label="List", command=main.list, accelerator="F8")
    menuFormat.add_command(label="Numbered List", command=main.numbered_list, accelerator="F9")
    menuFormat.add_separator()
    menuFormat.add_command(label="Increase Indent", command=main.increase_indent, accelerator="Ctrl+M")
    menuFormat.add_command(label="Decrease Indent", command=main.decrease_indent, accelerator="Ctrl+Shift+M")
    menuInsert = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuInsert.add_command(label="Calendar (year)", command=lambda: editor.insert(INSERT, str(calendar.calendar(int(datetime.datetime.now().year)))))
    menuInsert.add_command(label="Calendar (month)", command=lambda: editor.insert(INSERT, str(calendar.month(int(datetime.datetime.now().year), int(datetime.datetime.now().month)))))
    menuInsert.add_separator()
    menuInsert.add_command(label="Date & Time", command=lambda: editor.insert(INSERT, datetime.datetime.now()))
    menuInsert.add_command(label="Week Number", command=lambda: editor.insert(INSERT, "Week " + str(int(datetime.datetime.now().isocalendar().week))))
    menuInsert.add_separator()
    menuInsert.add_command(label="Finance", command=lambda: editor.insert(INSERT, "\t\tIncome\t\tCost\t\tSavings\nJanuary\t\t\t\t\t\t\nFebruary\t\t\t\t\t\t\nMarch\t\t\t\t\t\t\nApril\t\t\t\t\t\t\nMay\t\t\t\t\t\t\nJune\t\t\t\t\t\t\nJuly\t\t\t\t\t\t\nAugust\t\t\t\t\t\t\nSeptember\t\t\t\t\t\t\nOctober\t\t\t\t\t\t\nNovember\t\t\t\t\t\t\nDecember\t\t\t\t\t\t\n------------------------------------------------------------\nTotal\t\t\t\t\t\t"))
    menuInsert.add_command(label="RSS Headlines", command=lambda: editor.insert(INSERT, html.unescape("\n".join(re.findall(r'<title>(.*?)</title>', urlopen(simpledialog.askstring("BTXTPad", "Feed URL")).read().decode("utf8")))).replace("<![CDATA[", "").replace("]]>", "")))
    menuView = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuSidebar = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuView.add_cascade(label="Sidebar", menu=menuSidebar)
    menuSidebar.add_radiobutton(label="Hide", command=lambda: main.sidebar("h"), accelerator="Ctrl+,", variable=sidebar_status, value=1)
    menuSidebar.add_radiobutton(label="Left", command=lambda: main.sidebar("l"), accelerator="Ctrl+.", variable=sidebar_status, value=2)
    menuSidebar.add_radiobutton(label="Right", command=lambda: main.sidebar("r"), accelerator="Ctrl+/", variable=sidebar_status, value=3)
    menuView.add_separator()
    menuView.add_command(label="Help", command=main.help, accelerator="F1")
    menuView.add_command(label="Clipboard", command=lambda: messagebox.showinfo("Clipboard", editor.selection_get(selection="CLIPBOARD")), accelerator="F2")
    menuView.add_command(label="Note", command=main.note, accelerator="Ctrl+T")
    menuView.add_separator()
    menuView.add_checkbutton(label="Full Screen", command=lambda: root.attributes("-fullscreen", not root.attributes("-fullscreen")), accelerator="F11", variable=full_screen)

    buttonFile.configure(menu=menuFile)
    buttonEdit.configure(menu=menuEdit)
    buttonInsert.configure(menu=menuInsert)
    buttonView.configure(menu=menuView)

    content = Frame(root)
    content.grid(row=1, column=0, sticky="nsew")
    content.rowconfigure(0, weight=1)
    content.columnconfigure(0, weight=1)

    editor = scrolledtext.ScrolledText(content, bd=16, relief=FLAT, undo=True, wrap=WORD, font=("Consolas", 11, "normal"))
    editor.grid(row=0, column=0, sticky="nsew")

    menu_bar_sidebar = Frame(root, border=4)
    menu_bar_sidebar.columnconfigure(0, weight=1)
    menuWidgets = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuWidgets.add_radiobutton(label="Notebook", command=main.notebook, variable=widget, value=1)
    menuWidgets.add_radiobutton(label="Calculator", command=main.calculator, variable=widget, value=2)
    menuWidgets.add_radiobutton(label="Settings", command=main.settings, variable=widget, value=3)
    menuWidgets.add_radiobutton(label="Replace", command=main.replace, variable=widget, value=4)
    buttonWidgets = Menubutton(menu_bar_sidebar, text="Widgets", menu=menuWidgets)
    buttonWidgets.grid(row=0, column=0, sticky="nsw")

    sidebar = Frame(root)
    sidebar.rowconfigure(0, weight=1)
    sidebar.columnconfigure(0, weight=1)

    notebook = Text(sidebar, bd=16, relief=FLAT, undo=True, wrap=WORD, background="#fc5", foreground="#000", font=("Consolas", 11), width=36)
    menuOptions = Menu(root, tearoff=False, activeborderwidth=2.5, activebackground="#444", activeforeground="#fff")
    menuOptions.add_command(label="Aa", command=lambda: notebook.configure(bg="#fc5"), background="#fc5", foreground="#000")
    menuOptions.add_command(label="Aa", command=lambda: notebook.configure(bg="#5cf"), background="#5cf", foreground="#000")
    menuOptions.add_command(label="Aa", command=lambda: notebook.configure(bg="#d8d"), background="#d8d", foreground="#000")
    menuOptions.add_command(label="Aa", command=lambda: notebook.configure(bg="#8d8"), background="#8d8", foreground="#000")
    menuOptions.add_command(label="Aa", command=lambda: notebook.configure(bg="#f84"), background="#f84", foreground="#000")
    menuOptions.add_command(label="Aa", command=lambda: notebook.configure(bg="#bbb"), background="#bbb", foreground="#000")

    calc = Frame(sidebar, width=36)
    calc.rowconfigure(1, weight=1)
    calc.columnconfigure(0, weight=1, minsize=320)
    bar = Entry(calc, font=("", 12))
    bar.grid(row=0, column=0, sticky="nsew", ipady=8)
    frameCalculator = Frame(calc)
    frameCalculator.grid(row=1, column=0, sticky="nsew")
    for i in range(0, 6):
        frameCalculator.rowconfigure(i, weight=1)
    for j in range(0, 4):
        frameCalculator.columnconfigure(j, weight=1)
    Button(frameCalculator, text="bin", command=lambda: main.calculate("b")).grid(row=0, column=0, sticky="nsew")
    Button(frameCalculator, text="oct", command=lambda: main.calculate("o")).grid(row=0, column=1, sticky="nsew")
    Button(frameCalculator, text="hex", command=lambda: main.calculate("h")).grid(row=0, column=2, sticky="nsew")
    Button(frameCalculator, text="^", command=lambda: bar.insert(INSERT, " ** ")).grid(row=0, column=3, sticky="nsew")
    Button(frameCalculator, text="x²", command=lambda: main.calculate("s")).grid(row=1, column=0, sticky="nsew")
    Button(frameCalculator, text="√", command=lambda: main.calculate("r")).grid(row=1, column=1, sticky="nsew")
    Button(frameCalculator, text="1/x", command=lambda: main.calculate("i")).grid(row=1, column=2, sticky="nsew")
    Button(frameCalculator, text="+", command=lambda: bar.insert(INSERT, " + ")).grid(row=1, column=3, sticky="nsew")
    Button(frameCalculator, text="7", command=lambda: bar.insert(INSERT, "7")).grid(row=2, column=0, sticky="nsew")
    Button(frameCalculator, text="8", command=lambda: bar.insert(INSERT, "8")).grid(row=2, column=1, sticky="nsew")
    Button(frameCalculator, text="9", command=lambda: bar.insert(INSERT, "9")).grid(row=2, column=2, sticky="nsew")
    Button(frameCalculator, text="-", command=lambda: bar.insert(INSERT, " - ")).grid(row=2, column=3, sticky="nsew")
    Button(frameCalculator, text="4", command=lambda: bar.insert(INSERT, "4")).grid(row=3, column=0, sticky="nsew")
    Button(frameCalculator, text="5", command=lambda: bar.insert(INSERT, "5")).grid(row=3, column=1, sticky="nsew")
    Button(frameCalculator, text="6", command=lambda: bar.insert(INSERT, "6")).grid(row=3, column=2, sticky="nsew")
    Button(frameCalculator, text="x", command=lambda: bar.insert(INSERT, " * ")).grid(row=3, column=3, sticky="nsew")
    Button(frameCalculator, text="1", command=lambda: bar.insert(INSERT, "1")).grid(row=4, column=0, sticky="nsew")
    Button(frameCalculator, text="2", command=lambda: bar.insert(INSERT, "2")).grid(row=4, column=1, sticky="nsew")
    Button(frameCalculator, text="3", command=lambda: bar.insert(INSERT, "3")).grid(row=4, column=2, sticky="nsew")
    Button(frameCalculator, text="÷", command=lambda: bar.insert(INSERT, " / ")).grid(row=4, column=3, sticky="nsew")
    Button(frameCalculator, text="C", command=lambda: bar.delete(0, END)).grid(row=5, column=0, sticky="nsew")
    Button(frameCalculator, text="0", command=lambda: bar.insert(INSERT, "0")).grid(row=5, column=1, sticky="nsew")
    Button(frameCalculator, text=".", command=lambda: bar.insert(INSERT, ".")).grid(row=5, column=2, sticky="nsew")
    Button(frameCalculator, text="=", command=lambda: main.calculate("e")).grid(row=5, column=3, sticky="nsew")

    frameSettings = Frame(sidebar, width=36, border=16)
    frameSettings.rowconfigure(8, weight=1)
    frameSettings.columnconfigure(0, weight=1)
    Label(frameSettings, font=("Segoe UI", 18), text="Settings").grid(row=0, column=0, sticky="nsew", pady=(0, 10))
    Label(frameSettings, font=("Segoe UI", 13), text="Font").grid(row=1, column=0, sticky="nsew", pady=(0, 3))
    frameFont1 = Frame(frameSettings)
    frameFont1.grid(row=2, column=0, sticky="nsew")
    font_family = Combobox(frameFont1, width=32, values=font.families())
    font_family.grid(row=0, column=0, sticky="ew")
    size = Combobox(frameFont1, width=8, values=("8", "9", "10", "11", "12", "13", "14", "15", "16", "18", "20", "22", "24", "26", "28", "36", "48", "72"))
    size.grid(row=0, column=1, sticky="ew")
    frameFont2 = Frame(frameSettings)
    frameFont2.grid(row=3, column=0, sticky="nsew", pady=5)
    frameFont2.columnconfigure(0, weight=1)
    frameFont2.columnconfigure(1, weight=1)
    styleBold = IntVar(value=0)
    buttonB = Checkbutton(frameFont2, text="Bold", variable=styleBold)
    buttonB.grid(row=0, column=0, sticky="nsew")
    styleItalic = IntVar(value=0)
    buttonI = Checkbutton(frameFont2, text="Italic", variable=styleItalic)
    buttonI.grid(row=0, column=1, sticky="nsew")
    styleUnderline = IntVar(value=0)
    buttonU = Checkbutton(frameFont2, text="Underline", variable=styleUnderline)
    buttonU.grid(row=1, column=0, sticky="nsew")
    styleOverstrike = IntVar(value=0)
    buttonS = Checkbutton(frameFont2, text="Overstrike", variable=styleOverstrike)
    buttonS.grid(row=1, column=1, sticky="nsew")
    Label(frameSettings, font=("Segoe UI", 13), text="Theme").grid(row=4, column=0, sticky="nsew", pady=(0, 3))
    frameThemes = Frame(frameSettings)
    frameThemes.grid(row=5, column=0, sticky="nsew")
    frameThemes.columnconfigure(0, weight=1)
    frameThemes.columnconfigure(1, weight=1)
    theme = IntVar(value=1)
    theme_preview_1 = tkLabel(frameThemes, text="Aa", font=(16), height=3, bg="#fff", fg="#000")
    theme_preview_1.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
    theme_preview_2 = tkLabel(frameThemes, text="Aa", font=(16), height=3, bg="#dcb", fg="#000")
    theme_preview_2.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
    theme_button_1 = Radiobutton(frameThemes, variable=theme, value=1, text="Light")
    theme_button_1.grid(row=1, column=0, sticky="ns", pady=2)
    theme_button_2 = Radiobutton(frameThemes, variable=theme, value=2, text="Paper")
    theme_button_2.grid(row=1, column=1, sticky="ns", pady=2)
    theme_preview_3 = tkLabel(frameThemes, text="Aa", font=(16), height=3, bg="#222", fg="#fff")
    theme_preview_3.grid(row=2, column=0, sticky="nsew", padx=(0, 5))   
    theme_preview_4 = tkLabel(frameThemes, text="Aa", font=(16), height=3, bg="#000", fg="#fff")
    theme_preview_4.grid(row=2, column=1, sticky="nsew", padx=(5, 0))
    theme_button_3 = Radiobutton(frameThemes, variable=theme, value=3, text="Dark")
    theme_button_3.grid(row=3, column=0, sticky="ns", pady=(2, 0))
    theme_button_4 = Radiobutton(frameThemes, variable=theme, value=4, text="Black")
    theme_button_4.grid(row=3, column=1, sticky="ns", pady=(2, 0))
    Label(frameSettings, font=("Segoe UI", 13), text="More").grid(row=6, column=0, sticky="nsew", pady=(5, 3))
    frameMoreSettings = Frame(frameSettings)
    frameMoreSettings.grid(row=7, column=0, sticky="nsew")
    frameMoreSettings.columnconfigure(1, weight=1)
    Label(frameMoreSettings, width=16, text="Border").grid(row=0, column=0, sticky="nsew", pady=(0, 1))
    bar_border = Spinbox(frameMoreSettings, values=list(range(0, 65)))
    bar_border.grid(row=0, column=1, sticky="nsew", pady=(0, 1))
    bar_border.insert(INSERT, 16)
    Label(frameMoreSettings, width=16, text="Wrap").grid(row=1, column=0, sticky="nsew", pady=(1, 0))
    bar_wrap = Combobox(frameMoreSettings, values=["Disabled", "Word", "Character"])
    bar_wrap.grid(row=1, column=1, sticky="nsew", pady=(1, 0))
    Label(frameMoreSettings, width=16, text="Always on top").grid(row=2, column=0, sticky="nsew", pady=1)
    always_on_top = IntVar(value=0)
    button_pin = Checkbutton(frameMoreSettings, text="Pin", variable=always_on_top)
    button_pin.grid(row=2, column=1, sticky="nsew", pady=1)
    frameActions = Frame(frameSettings)
    frameActions.grid(row=8, column=0, sticky="sew")
    frameActions.columnconfigure(1, weight=1)
    button_reset = Button(frameActions, text="Reset", command=main.reset_settings)
    button_reset.grid(row=0, column=0, sticky="sw", ipady=5)
    button_save = Button(frameActions, text="Save", command=main.save_settings)
    button_save.grid(row=0, column=1, sticky="se", ipady=5)
    main.reset_settings()

    frameReplace = Frame(sidebar, width=36)
    frameReplace.rowconfigure(1, weight=1)
    frameReplace.columnconfigure(0, weight=1)
    frameReplace1 = Frame(frameReplace)
    frameReplace1.grid(row=0, column=0, sticky="nsew", padx=16, pady=(16, 8))
    frameReplace1.columnconfigure(1, weight=1)
    Label(frameReplace1, text="Find", width=12).grid(row=0, column=0, sticky=EW, ipady=5)
    find = Entry(frameReplace1)
    find.grid(row=0, column=1, sticky="nsew")
    Label(frameReplace1, text="Replace", width=12).grid(row=1, column=0, sticky=EW, ipady=5)
    replace = Entry(frameReplace1)
    replace.grid(row=1, column=1, sticky="nsew")
    Label(frameReplace1, text="Line", width=12).grid(row=2, column=0, sticky=EW, ipady=5)
    ln = Entry(frameReplace1)
    ln.grid(row=2, column=1, sticky="nsew")
    ln.insert(INSERT, str(editor.index(INSERT)).split(".")[0])
    Label(frameReplace1, text="Colunn", width=12).grid(row=3, column=0, sticky=EW, ipady=5)
    col = Entry(frameReplace1)
    col.grid(row=3, column=1, sticky="nsew")
    col.insert(INSERT, str(editor.index(INSERT)).split(".")[1])
    frameReplace2 = Frame(frameReplace)
    frameReplace2.grid(row=1, column=0, sticky="nsew", padx=16, pady=(8, 16))
    for i in range(0, 3):
        frameReplace2.rowconfigure(i, weight=1)
    frameReplace2.columnconfigure(0, weight=1)
    frameReplace2.columnconfigure(1, weight=1)
    Button(frameReplace2, text="Find", command=lambda: main.find_next(find.get())).grid(row=0, column=0, sticky="nsew")
    Button(frameReplace2, text="Go To", command=main.go_to).grid(row=0, column=1, sticky="nsew")
    Button(frameReplace2, text="Replace", command=lambda: main.replace_next(find.get(), replace.get())).grid(row=1, column=0, sticky="nsew")
    Button(frameReplace2, text="Replace All", command=lambda: main.replace_all(find.get(), replace.get())).grid(row=1, column=1, sticky="nsew")
    Button(frameReplace2, text="Delete", command=lambda: main.replace_next(find.get(), "")).grid(row=2, column=0, sticky="nsew")
    Button(frameReplace2, text="Delete All", command=lambda: main.replace_all(find.get(), "")).grid(row=2, column=1, sticky="nsew")
    frameReplace3 = Frame(frameReplace, style="Custom.TFrame")
    frameReplace3.grid(row=2, column=0, sticky="nsew")
    char_counter = Label(frameReplace3, style="Custom.TLabel")
    char_counter.grid(row=0, column=0, sticky="nsew", padx=16, pady=(16, 0))
    word_counter = Label(frameReplace3, style="Custom.TLabel")
    word_counter.grid(row=1, column=0, sticky="nsew", padx=16)
    line_counter = Label(frameReplace3, style="Custom.TLabel")
    line_counter.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))

    menuB3 = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuB3.add_command(label="Undo", command=lambda: editor.edit_undo())
    menuB3.add_command(label="Redo", command=lambda: editor.edit_redo())
    menuB3.add_separator()
    menuB3.add_command(label="Cut", command=lambda: main.cut())
    menuB3.add_command(label="Copy", command=lambda: main.copy(editor))
    menuB3.add_command(label="Paste", command=lambda: editor.insert(INSERT, editor.selection_get(selection="CLIPBOARD")))
    menuB3.add_command(label="Select All", command=lambda: editor.tag_add(SEL, 1.0, END))
    menuB3.add_separator()
    menuB3.add_cascade(label="Delete", command=lambda: main.delete(editor))
    menuB3.add_separator()
    menuB3.add_command(label="Solve", command=main.solve)
    menuB3.add_command(label="Move to front", command=lambda: move_to_front(editor))

    main.theme("#fff", "#f0f0f0", "#e0e0e0", "#000", "#e0e0e0")
    main.notebook()
    main.refresh()
    editor.focus_set()

    editor.bind("<Control-b>", lambda i: main.capitalize())
    editor.bind("<Control-B>", lambda i: main.capitalize())
    editor.bind("<Control-d>", lambda i: main.duplicate())
    editor.bind("<Control-D>", lambda i: main.duplicate())
    editor.bind("<Control-e>", lambda i: main.read_edit())
    editor.bind("<Control-E>", lambda i: main.read_edit())
    root.bind("<Control-f>", lambda i: search_bar.focus_set())
    root.bind("<Control-F>", lambda i: search_bar.focus_set())
    root.bind("<Control-g>", lambda i: main.go_to_a())
    root.bind("<Control-G>", lambda i: main.go_to_a())
    editor.bind("<Control-k>", lambda i: main.keep())
    editor.bind("<Control-K>", lambda i: main.keep())
    editor.bind("<Control-m>", lambda i: main.increase_indent())
    editor.bind("<Control-M>", lambda i: main.increase_indent())
    editor.bind("<Control-Shift-m>", lambda i: main.decrease_indent())
    editor.bind("<Control-Shift-M>", lambda i: main.decrease_indent())
    editor.bind("<Control-n>", lambda i: main.new())
    editor.bind("<Control-N>", lambda i: main.new())
    editor.bind("<Control-o>", lambda i: main.open())
    editor.bind("<Control-O>", lambda i: main.open())
    editor.bind("<Control-s>", lambda i: main.save())
    editor.bind("<Control-S>", lambda i: main.save())
    editor.bind("<Control-Shift-s>", lambda i: main.save_as())
    editor.bind("<Control-Shift-S>", lambda i: main.save_as())
    root.bind("<Control-t>", lambda i: main.note())
    root.bind("<Control-T>", lambda i: main.note())
    editor.bind("<Control-p>", lambda i: os.startfile(filepath, "print"))
    editor.bind("<Control-P>", lambda i: os.startfile(filepath, "print"))
    root.bind("<Control-r>", lambda i: main.replace_a())
    root.bind("<Control-R>", lambda i: main.replace_a())
    editor.bind("<Control-u>", lambda i: main.line("̲"))
    editor.bind("<Control-U>", lambda i: main.line("̲"))
    editor.bind("<Control-Shift-u>", lambda i: main.line("̳"))
    editor.bind("<Control-Shift-U>", lambda i: main.line("̳"))
    root.bind("<Control-w>", lambda i: main.exit())
    root.bind("<Control-W>", lambda i: main.exit())
    editor.bind("<Control-Shift-x>", lambda i: main.line("̶"))
    editor.bind("<Control-Shift-X>", lambda i: main.line("̶"))
    root.bind("<Control-,>", lambda i: main.sidebar("h"))
    root.bind("<Control-.>", lambda i: main.sidebar("l"))
    root.bind("<Control-/>", lambda i: main.sidebar("r"))
    editor.bind("<Shift-Delete>", lambda i: editor.delete(1.0, END))
    editor.bind("<Control-BackSpace>", lambda i: editor.delete(1.0, editor.index(INSERT)))
    editor.bind("<Control-Delete>", lambda i: editor.delete(editor.index(INSERT), END))
    root.bind("<Insert>", lambda i: editor.insert(INSERT, editor.selection_get(selection="CLIPBOARD")))
    root.bind("<Alt-f>", lambda i: menuFile.tk_popup(buttonFile.winfo_rootx(), buttonFile.winfo_rooty()+25))
    root.bind("<Alt-F>", lambda i: menuFile.tk_popup(buttonFile.winfo_rootx(), buttonFile.winfo_rooty()+25))
    root.bind("<Alt-e>", lambda i: menuEdit.tk_popup(buttonEdit.winfo_rootx(), buttonEdit.winfo_rooty()+25))
    root.bind("<Alt-E>", lambda i: menuEdit.tk_popup(buttonEdit.winfo_rootx(), buttonEdit.winfo_rooty()+25))
    root.bind("<Alt-i>", lambda i: menuInsert.tk_popup(buttonInsert.winfo_rootx(), buttonInsert.winfo_rooty()+25))
    root.bind("<Alt-I>", lambda i: menuInsert.tk_popup(buttonInsert.winfo_rootx(), buttonInsert.winfo_rooty()+25))
    root.bind("<Alt-v>", lambda i: menuView.tk_popup(buttonView.winfo_rootx(), buttonView.winfo_rooty()+25))
    root.bind("<Alt-V>", lambda i: menuView.tk_popup(buttonView.winfo_rootx(), buttonView.winfo_rooty()+25))
    root.bind("<Alt-q>", lambda i: search_bar.focus_set())
    root.bind("<Alt-Q>", lambda i: search_bar.focus_set())
    root.bind("<Alt-s>", lambda i: main.find_next(search_bar.get()))
    root.bind("<Alt-S>", lambda i: main.find_next(search_bar.get()))
    root.bind("<Escape>", lambda i: root.attributes("-fullscreen", 0))
    root.bind("<F1>", lambda i: main.help())
    root.bind("<F2>", lambda i: messagebox.showinfo("Clipboard", editor.selection_get(selection="CLIPBOARD")))
    root.bind("<F3>", lambda i: search_bar.focus_set())
    root.bind("<F5>", lambda i: main.open())
    root.bind("<F6>", lambda i: main.settings())
    editor.bind("<F7>", lambda i: main.read_edit())
    root.bind("<F8>", lambda i: main.list())
    root.bind("<F9>", lambda i: main.numbered_list())
    editor.bind("<F10>", lambda i: menuFormat.tk_popup(buttonEdit.winfo_rootx(), buttonEdit.winfo_rooty()+25))
    notebook.bind("<F10>", lambda i: menuOptions.tk_popup(notebook.winfo_rootx()+16, notebook.winfo_rooty()+16))
    root.bind("<F11>", lambda i: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
    root.bind("<F12>", lambda i: main.save_as())
    editor.bind("<Button-3>", main.b3_menu)
    notebook.bind("<Button-3>", main.b3_options)
    bar.bind("<Return>", lambda i: main.calculate(eval(bar.get())))
    frameSettings.bind("<Return>", lambda i: main.save_settings())
    root.bind("<Button>", lambda i: main.refresh())
    root.bind("<Motion>", lambda i: main.refresh())
    root.bind("<Key>", lambda i: main.refresh())
    root.mainloop()
