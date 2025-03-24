import tkinter, keyboard, pyperclip, pystray, os, json
import pydirectinput as dirinput
from math import sqrt
from PIL import Image, ImageDraw
from tkinter.messagebox import showerror, showinfo
#from plyer import notification
from win10toast import ToastNotifier


def resource_path(relative_path):
    base_path = os.path.dirname(os.path.abspath(__file__)) # path to the working directory

    location = os.path.join(base_path, relative_path) # path from where the file is running to the one you want
    print(location)
    return location

hotkeyseries = ["ctrl","shift","e"]
prompt_on_error = True
startup_message = True
show_changed = True


def load_settings():
    # Get settings from config file
    with open(resource_path("settings/config.json"),"r") as f:
        data = json.load(f)
        if ("hotkey" in data and type(data["hotkey"]) is list):
            global hotkeyseries
            hotkeyseries = data["hotkey"]
            print(hotkeyseries)

        if ("showAlertOnFail" in data and type(data["showAlertOnFail"]) is bool):
            global prompt_on_error
            prompt_on_error = data["showAlertOnFail"]

        if ("promptOnStart" in data and type(data["promptOnStart"]) is bool):
            global startup_message
            startup_message = data["promptOnStart"]

        if ("promptOnReload" in data and type(data["promptOnReload"]) is bool):
            global show_changed
            show_changed = data["promptOnReload"]

        f.close()


    try:
        keyboard.add_hotkey("+".join(hotkeyseries), runit)
    except ValueError as e:
        showerror("Math Hotkey",str(e).split("ValueError(")[1].split(")")[0])
        quit()
    

def reload_settings():
    keyboard.unhook_all_hotkeys()
    load_settings()

    if (show_changed):
        ToastNotifier().show_toast(
            "Math Hotkey",
            "Settings changed. Use `%s` to evaluate selected text"%("+".join(hotkeyseries)),
            icon_path = resource_path("./MathKey.ico"),
            duration = 5)



def create_icon():
    image = Image.open(resource_path("./MathKey.ico"))
    return image

def quit_window():
    keyboard.unhook_all()
    os._exit(1)
    

def hide_window():
    menu = (pystray.MenuItem('Reload Settings', reload_settings), pystray.MenuItem('Quit', quit_window))
    icon = pystray.Icon("Math Hotkey", create_icon(), "'Text Select to Math' Hotkey", menu)

    if (startup_message):
        ToastNotifier().show_toast(
            "Math Hotkey",
            "Minimized to system tray, use `%s` to evaluate selected text"%("+".join(hotkeyseries)),
            icon_path = resource_path("./MathKey.ico"),
            duration = 5)

    icon.run_detached()


# Main function
def runit():
    app = tkinter.Tk() # tkinter makes clipboard stuff easy!
    app.withdraw()  # hide any window
    predata = ""
    postdata = "err"

    try:
        predata = app.clipboard_get() # save what's already on the clipboard as to not overwrite it
    except(tkinter.TclError):
        predata = "" # do nothin
    finally:
        try:
            for keydown in hotkeyseries:
                dirinput.keyUp(keydown) # release keys that are down so they don't interfere with the cut command

            dirinput.keyDown("ctrl") # cut the selected text
            dirinput.press("x") 
            dirinput.keyUp("ctrl")
            postdata = app.clipboard_get() # save what was cut
        except(tkinter.TclError):
            postdata = ""
        finally:
            pyperclip.copy(predata) # put back the original data so what you had copied stays copied!


    outit = postdata
    try:
        outit = evaluate(postdata) # convert text into math, evaluate said math
    except:
        outit = postdata # I probably don't need this here but am stoopid so here it is anyway
    finally:
        keyboard.write(str(outit))
        if outit == postdata and prompt_on_error:
            showerror("Math Hotkey", "The following input could not be evaluated:\n'%s'"%postdata) # Some confirmation that it did run and it's the user that made a whoopsie
    
    app.destroy() # delete the window, it's useless now



def evaluate(inp):
    inp = inp.replace("\n","") #inserted because line breaks should be able to be selected, but can not be used in math

    #outp = "("+outp+")+0" # why did I have this??
    outp = inp

    outp = outp.replace(",","") # I was debating on making commas a divider, like if i selected '5+2,4*6' it would return '7,24' but this is kinda for casual use, and commas in numbers are much more casual
    outp = outp.replace("{","(").replace("[","(").replace("}",")").replace("]",")") # it just matters how many parantheses you have, computers don't use the other ones for "style"

    #multiplication
    outp = outp.replace("x","*")

    #division
    outp = outp.replace("÷","/")

    #fancy shmancy
    outp = outp.replace("π","pi")
    outp = outp.replace("pi","3.14159265358979323") # should be enough, right?
    outp = outp.replace("^","**") # exponential
    outp = outp.replace("√","v") # square roots

    while outp.find("v") > -1:
        start = outp.index("v")
        after = outp[start+1:]
        endat = re.search('\+|-|/|\*|\)|$',after)
        outp = outp[:start]+"sqrt("+after[:endat.start()]+")"+outp[start+endat.end():] # changes 'v64+2' to 'sqrt(64)+2' which can be evaluated

    outp = outp.replace("v","")

    if outp[-1] == "=":
        calc = outp[:-1]
        calc = eval(calc)
        outp = inp+str(calc) # use inp, so when you use '5^2=' it doesn't show '5**2=25'
    else:
        outp = eval(outp)

    return outp


load_settings()
hide_window()
keyboard.wait()