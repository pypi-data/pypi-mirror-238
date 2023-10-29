import curses#Depends on windows-curses on win32
from curses.textpad import rectangle
from . import messagebox
import os
from time import sleep
from .transitions import _old as cursestransition
import textwrap
import threading
from .constants import *
from .utils import *

_C_INIT = False

class ArgumentError(Exception):
    def __init__(self, message, errors):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.errors = errors


def displaymsg(stdscr,message: list):
    """
    Display a message in a rectangle. Stdscr is the screen and message is a list. Each item in the list is a new line. For a single line message call displaymsg(stdscr,["message here"])
    Message will be dismissed when a key is pressed.
    """
    stdscr.clear()
    x,y = os.get_terminal_size()
    ox = 0
    for o in message:
        ox += 1
        if "\n" in o:
            message.insert(ox,o.split("\n")[1])
    message = [m[0:x-5].split("\n")[0] for m in message]#Limiting characters
    maxs = max([len(s) for s in message])
    rectangle(stdscr,y//2-(len(message)//2)-1, x//2-(maxs//2)-1, y//2+(len(message)//2)+2, x//2+(maxs//2+1)+1)
    stdscr.addstr(0,0,"Message: ")
    mi = -(len(message)/2)
    
    for msgl in message:
        mi += 1
        stdscr.addstr(int(y//2+mi),int(x//2-len(msgl)//2),msgl)
    stdscr.addstr(y-2,0,"Press any key to dismiss this message")
    stdscr.refresh()
    stdscr.getch()
    

def displaymsgnodelay(stdscr,message: list):
    """
    Display a message in a rectangle. message is a list. Each item in the list is a new line. Unlike displaymsg, the message will not need a keypress to continue. This is good for progress waiing.
    """
    stdscr.clear()
    x,y = os.get_terminal_size()
    ox = 0
    for o in message:
        ox += 1
        if "\n" in o:
            message.insert(ox,o.split("\n")[1])
    message = [m[0:x-5].split("\n")[0] for m in message]#Limiting characters
    maxs = max([len(s) for s in message])
    rectangle(stdscr,y//2-(len(message)//2)-1, x//2-(maxs//2)-1, y//2+(len(message)//2)+2, x//2+(maxs//2+1)+1)
    stdscr.addstr(0,0,"Message: ")
    mi = -(len(message)/2)
    
    for msgl in message:
        mi += 1
        stdscr.addstr(int(y//2+mi),int(x//2-len(msgl)//2),msgl)
    stdscr.refresh()


def coloured_option_menu(stdscr,options:list[str],title="Please choose an option from the list below",colouring=[["back",RED]]) -> int:
    """An alternate optionmenu that has colours"""
    selected = 0
    offset = 0
    maxl = list_get_maxlen(options)
    while True:
        stdscr.clear()
        mx,my = os.get_terminal_size()
        
        filline(stdscr,0,set_colour(BLUE,WHITE))
        filline(stdscr,1,set_colour(WHITE,BLACK))
        stdscr.addstr(0,0,title,set_colour(BLUE,WHITE))
        stdscr.addstr(1,0,"Use the up and down arrow keys to navigate and enter to select",set_colour(WHITE,BLACK))
        oi = 0
        for op in options[offset:offset+my-7]:
            col = WHITE
            for colour in colouring:
                if str_contains_word(op,colour[0]):
                    col = colour[1]
            if not oi == selected-offset:
                stdscr.addstr(oi+3,7,op,set_colour(BLACK,col))
            else:
                stdscr.addstr(oi+3,7,op,set_colour(BLACK,col) | curses.A_UNDERLINE | curses.A_BOLD)
            oi += 1
        stdscr.addstr(selected+3-offset,1,"-->")
        stdscr.addstr(selected+3-offset,maxl+9,"<--")
        stdscr.addstr(oi+3,0,"━"*(mx-1))
        if offset > 0:
            stdscr.addstr(3,maxl+15,f"{offset} options above")
        if len(options) > offset+my-8:
            stdscr.addstr(oi+2,maxl+15,f"{len(options)-offset-my+8} options below")
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == curses.KEY_DOWN and selected < len(options)-1:
            
            selected += 1
            if selected > my-8:
                offset += 1
        elif ch == curses.KEY_UP and selected > 0:
            
            selected -= 1
            if selected < offset:
                offset -= 1
        elif ch == 10 or ch == 13 or ch == curses.KEY_ENTER:
            return selected

def cursesinput(stdscr,prompt: str,lines=1,maxlen=0,passwordchar:str=None,retremptylines=False,prefiltext="",bannedcharacters="") -> str:
    """
    Get input from the user. Set maxlen to 0 for no maximum. Set passwordchar to None for no password entry. Retremptylines is if the program should return newlines even if the lines are empty. bannedcharacters is a comma-seperated list of banned words and characters
    """
    ERROR = ""
    if passwordchar is not None:
        passworduse = True
    else:
        passworduse = False

    stdscr.erase()
    mx,my = os.get_terminal_size()
    extoffscr = lines > my-3
    if extoffscr:
        lnrectmaxy = my-2
    else:
        lnrectmaxy = lines+2
    text: list[list[str]] = [[] for _ in range(lines)]
    if prefiltext != "":
        lnxi=0
        for lnx in prefiltext.splitlines():
            text[lnxi] = list(lnx)
            lnxi+= 1
    ln=0
    col=0
    xoffset = 0
    while True:
        filline(stdscr,0,set_colour(WHITE,BLACK))
        stdscr.addstr(0,0,str(prompt+[" (Press ctrl-D to submit)" if lines != 1 else " (Press enter to submit)"][0])[0:mx-2],set_colour(WHITE,BLACK))
        rectangle(stdscr,1,0,lnrectmaxy,mx-1)
        chi = 1
        for chln in text:
            chi+= 1
            if passworduse:
                stdscr.addstr(chi,1,(passwordchar*len(chln))[xoffset:xoffset+mx-3])
            else:
                stdscr.addstr(chi,1,"".join(chln)[xoffset:xoffset+mx-3])
            if xoffset > 0:
                stdscr.addstr(chi,0,"<",set_colour(BLUE,WHITE))
            if len(text[chi-2]) > xoffset + mx - 3:
                stdscr.addstr(chi,mx-1,">",set_colour(GREEN,WHITE))
        stdscr.addstr(0,mx-10,f"{ln},{col}",set_colour(WHITE,BLACK))
        stdscr.addstr(0,30,ERROR,set_colour(WHITE,RED))
        stdscr.move(ln+2,col-xoffset+1)
        
        if ERROR != "":
            ERROR = ""
        stdscr.refresh()
        ch = stdscr.getch()
        textl = "\n".join(["".join(t) for t in text])

        chn = curses.keyname(ch)
        if ch == 10 or ch == 13 or ch == curses.KEY_ENTER :
            if lines == 1:
                stdscr.erase()
                return "\n".join(["".join(t) for t in text])
            if ln == lines - 1:
                ERROR = " You have reached the bottom of the page. "
                curses.beep()
            else:
                if col < len(text[ln]) - 1:
                    #Shift down
                    text[ln+1] = text[ln][col:] + text[ln+1]
                    stdscr.clear()
                    if col > 0:
                        del text[ln][col:]
                    else:
                        text[ln] = []
                ln += 1
                col = 0
        elif ch == curses.KEY_DOWN:
            if ln == lines - 1:
                ERROR = " You have reached the bottom of the page. "
                curses.beep()
            else:
                ln += 1
                col = 0
        elif ch == curses.KEY_LEFT:
            if col > 0:
                col -= 1
                if xoffset > 0:
                    xoffset -= 1
                    stdscr.clear()
            else:
                ERROR = " You have reached the end of the text "

                curses.beep()
        elif ch == curses.KEY_RIGHT:
            if col < len(retr_nbl_lst(text[ln])):
                col += 1
                if col-xoffset > mx-2:
                    xoffset += 1
                    stdscr.clear()
            else:
                ERROR = " You have reached the end of the text "
                curses.beep()
        elif ch == curses.KEY_BACKSPACE or curses.keyname(ch) == b"^H":
            if col > 0:
                del text[ln][col-1]
                col -= 1
                if xoffset > 0:
                    xoffset -= 1
                stdscr.clear()#Fix render errors
              
            else:
                ERROR = " You may not backspace further "
                curses.beep()
        elif ch == curses.KEY_UP:
            if ln > 0:
                ln -= 1
                col = 0
            else:
                ERROR = " You have reached the top of the text "
                curses.beep()
        else:
            if len(chn) > 1:
                #Special char
                if chn == b"^D":
                    stdscr.erase()
                    if retremptylines:
                        fretr = "\n".join([lx for lx in ["".join(t) for t in text]])
                        if len(fretr.splitlines()) < len(text):
                            fretr += "\n"
                        return fretr
                    else:
                        return "\n".join([lx for lx in ["".join(t) for t in text] if lx != ""])
                elif chn == b"^K":
                    text = [[] for _ in range(lines)]#Delete
                    ln = 0
                    col = 0
                    stdscr.erase()
            else:
                #append
                if calc_nbl_list(text) == maxlen and maxlen != 0:
                    curses.beep()
                    ERROR = f" You have reached the character limit ({maxlen}) "
                else:
                    lll = False
                    if bannedcharacters != "":
                        for z in bannedcharacters.split(","):
                            if z in textl or z == chn.decode():
                                lll = True
                                ERROR = " That is a banned character"
                    if not lll:
                        col += 1
                        text[ln].insert(col-1,chn.decode())
                        
                        if col > mx-2:
                            xoffset += 1
                            stdscr.clear()
    
def checkboxlist(stdscr,options,message="Please choose options from the list below",minimumchecked=0,maximumchecked=1000) -> dict:
    """A list of checkboxes for multiselect. Options may be a list like ["Option1","Option2"]. In this case, values will be defaultd to False (unchecked.) Alternatively you can supply a dict like {"Option1":True,"Option1":False}. In that case, some options will be pre-checked. This returns a dict in the same style as the input."""
    offset = 0
    selected = 0
    if type(options) == list:
        options = {k:False for k in options}
    elif type(options) == dict:
        pass
    else:
        raise TypeError("Please provide a list or dict.")
    maxl = list_get_maxlen(list(options.keys()))
    while True:
        my,mx = stdscr.getmaxyx()
        stdscr.clear()
        filline(stdscr,0,set_colour(BLUE,WHITE))
        filline(stdscr,1,set_colour(WHITE,BLACK))
        filline(stdscr,my-1,set_colour(WHITE,BLACK))
        stdscr.addstr(0,0,message,set_colour(BLUE,WHITE))
        stdscr.addstr(1,0,"Use the up and down arrow keys to navigate, use space to select.",set_colour(WHITE,BLACK))
        stdscr.addstr(my-1,0,"Press D when you are done",set_colour(WHITE,BLACK))
        ci = 3
        for choice in list(options.items())[offset:offset+my-6]:
            #choice = list(choice)
            stdscr.addstr(ci,0,choice[0])
            stdscr.addstr(ci,maxl+2,"[ ]")
            if choice[1]:
                stdscr.addstr(ci,maxl+3,"*")
            ci += 1
        stdscr.addstr(selected-offset+3,maxl+8,"<--")
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == curses.KEY_DOWN and selected < len(options)-1:
            
            selected += 1
            if selected > my-8:
                offset += 1
        elif ch == curses.KEY_UP and selected > 0:
            
            selected -= 1
            if selected < offset:
                offset -= 1
        elif ch == 10 or ch == 13 or ch == curses.KEY_ENTER or ch == 32:
            options[list(options.keys())[selected]] = not options[list(options.keys())[selected]]
            #messagebox.showinfo(stdscr,[str(options)])
        elif ch == 100:
            if len([t for t in list(options.values()) if t]) <= maximumchecked and len([t for t in list(options.values()) if t]) >= minimumchecked:
                return options
            else:
                messagebox.showerror(stdscr,[f"You must choose between {minimumchecked} and {maximumchecked} options."])

def displayops(stdscr,options: list,title="Please choose an option") -> int:
    """Display an options menu provided by options list. ALso displays title. Returns integer value of selected item."""
    mx, my = os.get_terminal_size()
    selected = 0
    stdscr.clear()
    options = [l[0:mx-3] for l in options]
    maxlen = max([len(l) for l in options])
    stdscr.addstr(0,0,title[0:mx-1])
    offset = 0
    while True:
        stdscr.addstr(0,0,title[0:mx-1])
        mx, my = os.get_terminal_size()
        options = [l[0:mx-3] for l in options]
        maxlen = max([len(l) for l in options])
        if len(options) > my-5:
            rectangle(stdscr,1,0,my-2,mx-1)
        else:
            rectangle(stdscr,1,0,2+len(options),maxlen+2)
        oi = -1
        for o in options[offset:offset+(my-4)]:
            oi += 1
            try:
                if oi == selected-offset:
                    stdscr.addstr(oi+2,1,o,set_colour(WHITE,BLACK))
                else:
                    stdscr.addstr(oi+2,1,o)
            except curses.error:
                pass
        stdscr.addstr(my-1,0,"Please choose an option with the arrow keys then press enter."[0:mx-1])
        stdscr.refresh()
        _ch = stdscr.getch()
        if _ch == curses.KEY_ENTER or _ch == 10 or _ch == 13:
            return selected
        elif _ch == curses.KEY_UP and selected > 0:
            if offset > 0 and selected-offset == 0:
                offset -= 1
            selected -= 1
        elif _ch == curses.KEY_DOWN and selected < len(options)-1:
            if selected >= my-6:
                offset += 1
            selected += 1
        elif _ch == curses.KEY_BACKSPACE or _ch == 98:
            return -1
        stdscr.erase()
       
def optionmenu(stdscr,options:list,title="Please choose an option and press enter") -> int:
    """Alias function to displayops()"""
    return displayops(stdscr,options,title)

def askyesno_old(stdscr,title: str) -> bool:
    """Ask a yes no question provided by title."""
    result = displayops(stdscr,["Yes","No"],title)
    if result == 0:
        return True
    else:
        return False

def displayerror(stdscr,e,msg: str):
    """
    Display an error message
    """
    displaymsg(stdscr,["An error occured",msg,str(e)])

def filline(stdscr,line: int,colour: int):
    """Fill a line, colour is the result of set_colour(fg,bg)"""
    stdscr.addstr(line,0," "*(os.get_terminal_size()[0]-1),colour)

def hidecursor():
    """Hide Cursor. Can only be called in an active curses window"""
    curses.curs_set(0)

def showcursor():
    """Show cursor. Can only be called in an active curses window"""
    curses.curs_set(1)

def numericinput(stdscr,message="Please input a number",allowdecimals=False,allownegatives=False,minimum=None,maximum=None,prefillnumber=None) -> float:
    if prefillnumber is not None:
        prl = str(prefillnumber)
    else:
        prl = ""
    
    while True:
        strrepr = cursesinput(stdscr,message,maxlen=12,prefiltext=prl)
        if len(strrepr) == 0 or (allownegatives and strrepr[0] == "-" and len(strrepr) < 2):
            curses.beep()
            continue
        if not allownegatives and strrepr[0] == "-":
            curses.beep()
            continue
        if not allowdecimals:
            try:
                retr = int(strrepr)
                if maximum is not None:
                    if retr > maximum:
                        curses.beep()
                        continue
                    
                elif minimum is not None:
                    if retr < minimum:
                        curses.beep()
                        continue
                return retr
                
            except:
                curses.beep()
                continue
        else:
            try:
                retr =  float(strrepr)
                if maximum is not None:
                    if retr > maximum:
                        curses.beep()
                        continue
                elif minimum is not None:
                    if retr < minimum:
                        curses.beep()
                        continue
                return retr
            except:
                curses.beep()
                continue

def textview(stdscr,file=None,text=None,isagreement=False,requireyes=True,message="") -> bool:
    """
    ## View Text interactively

    This function is resize-friendly
    Set either file or text to not none to use mode. Set isagreement to true if you want this to be a license agreement
    Returns true if isagreement is false or if user agreed. Returns false if the user did not agree
    """
    offset = 0
    if file is None and text is None:
        raise ArgumentError("Please specify a file or text to display")
    elif file is not None and os.path.isfile(file):
        with open(file) as f:
            text = f.read()
    elif text is not None:
        text = text

    zltext = text.splitlines()
    while True:
        stdscr.clear()
        #stdscr.refresh()
        #Segment text
        mx,my = os.get_terminal_size()
        n = mx - 1
        broken_text = []
        for text in zltext:
            if text.replace(" ","") == "":
                broken_text += [""]
            else:
                broken_text += textwrap.wrap(text,n)
        filline(stdscr,0,set_colour(WHITE,BLACK))
        stdscr.addstr(0,0,message[0:mx-8],set_colour(WHITE,BLACK))
        prog = f"{offset}/{len(broken_text)}"
        stdscr.addstr(0,mx-len(prog)-1,prog,set_colour(WHITE,BLACK))
        filline(stdscr,my-1,set_colour(WHITE,BLACK))
        if isagreement:
            stdscr.addstr(my-1,0,"A: Agree | D: Disagree",set_colour(WHITE,BLACK))
        else:
            stdscr.addstr(my-1,0,"Press enter to exit",set_colour(WHITE,BLACK))
        li = 1
        for line in broken_text[offset:offset+(my-2)]:
            try:
                stdscr.addstr(li,0,line)
                li += 1
            except:
                pass

        ch = stdscr.getch()
        if ch == curses.KEY_DOWN:
            offset += 1
        elif ch == curses.KEY_UP and offset > 0:
            offset -= 1
        elif ch == curses.KEY_HOME:
            offset = 0
        elif (ch == 10 or ch == 13 or ch == curses.KEY_ENTER) and not isagreement:
            return True
        elif ch == 97 and isagreement:
            return True
        elif ch == 100 and isagreement:
            if not requireyes:
                return False
            else:
                messagebox.showwarning(stdscr,["You must agree to the license to proceed"])

class PleaseWaitScreen:
    def __init__(self,stdscr,message=["Please Wait"]):
        self.message = message + [""]
        self.screen = stdscr
        self.tick = 0
        self.stopped = False
    def _update(self):
        message = self.message
        self.screen.clear()
        #self.screen.refresh()
        self.tick += 1
        if self.tick == 4:
            self.tick = 0
        x,y = os.get_terminal_size()
        ox = 0
        for o in message:
            ox += 1
            if "\n" in o:
                message.insert(ox,o.split("\n")[1])
        message = [m[0:x-5].split("\n")[0] for m in message]#Limiting characters
        message[-2] += self.tick*"."
        maxs = max([len(s) for s in message])
        rectangle(self.screen,y//2-(len(message)//2)-1, x//2-(maxs//2)-1, y//2+(len(message)//2)+2, x//2+(maxs//2+1)+1)
        mi = -(len(message)/2)
        
        for msgl in message[0:-1]:
            mi += 1
            self.screen.addstr(int(y//2+mi),int(x//2-len(msgl)//2),msgl)
        
        self.screen.refresh()
    def _tst(self):
        while not self.stopped:
            self._update()
            sleep(0.3)
    def start(self):
        threading.Thread(target=self._tst).start()
    def stop(self):
        self.stopped = True
    def destroy(self):
        del self

class ProgressBarTypes:
    FullScreenProgressBar: int = 0
    SmallProgressBar: int = 1
class ProgressBarLocations:
    TOP = 0
    CENTER = 1
    BOTTOM = 2

class ProgressBar:
    def __init__(self,stdscr,max_value: int, bar_type=ProgressBarTypes.SmallProgressBar,bar_location=ProgressBarLocations.TOP,step_value=1,x_size=None,show_percent=True,show_log=None,message="Progress",waitforkeypress=False):
        """Display a Progress Bar with a log. Good for install progresses"""
        self.screen = stdscr
        if show_log is not None:
        
            #Kept for backwards-compatibility
            self.sl = show_log
        else:
            self.sl = bar_type == 0
        self.max = max_value
        self.stepval = step_value
        self.sp = show_percent
            
        self.msg = message
        self.ACTIVE = False
        self.value = 0
        self.loglist: list[str] = []
        self.lclist: list[int] = []
        self.submsg = ""
        self.barloc = bar_location
        if bar_type == ProgressBarTypes.FullScreenProgressBar and bar_location != ProgressBarLocations.TOP:
            raise ValueError("Full screen progress bars may not have their locations changed.")
        self.mx, self.my = os.get_terminal_size()
        self.wfkp = waitforkeypress
    def update(self):
        sz = self.screen.getmaxyx()[0]
        if self.barloc == 0:
            ydraw = 0
        elif self.barloc == 1:
            ydraw = sz //2-1
        elif self.barloc == 2:
            ydraw = sz-4
        lheight = self.my - 7
        """Redraws progress bar"""
        if self.sl:
            self.screen.erase()
        self.screen.addstr(ydraw,0," "*(self.mx-1),set_colour(BLUE,WHITE))
        self.screen.addstr(ydraw,0,self.msg[0:self.mx-1],set_colour(BLUE,WHITE))
        #filline(self.screen,1,set_colour(GREEN,WHITE))
        filline(self.screen,ydraw+2,set_colour(RED,WHITE))
        #filline(self.screen,3,set_colour(GREEN,WHITE))
        self.screen.addstr(ydraw+1,0,"-"*(self.mx-1),set_colour(RED,WHITE))
        self.screen.addstr(ydraw+3,0,"-"*(self.mx-1),set_colour(RED,WHITE))
        barfill = round((self.value/self.max)*self.mx-1)
        if not self.value > self.max:
            self.screen.addstr(ydraw+2,0," "*barfill,set_colour(GREEN,WHITE))
        else:
            self.screen.addstr(ydraw+2,0," "*self.mx-1,set_colour(GREEN,WHITE))
        self.screen.addstr(ydraw+3,0,self.submsg[0:self.mx-1],set_colour(RED,WHITE))
        if self.sp:
            self.screen.addstr(ydraw+3,self.mx-7,f"{round(self.value/self.max*100,1)} %",set_colour(RED,WHITE))
        if self.sl:
            rectangle(self.screen,4,0,self.my-2,self.mx-1)
            if len(self.loglist) > lheight:
                lx = 0
                for val in self.loglist[len(self.loglist)-lheight:]:
                    self.screen.addstr(lx+5,1,val[0:self.mx-2],self.lclist[len(self.loglist)-lheight+lx])
                    lx += 1
            else:
                lx = 0
                for val in self.loglist:
                    self.screen.addstr(lx+5,1,val[0:self.mx-2],self.lclist[lx])
                    lx += 1
        self.screen.refresh()
    def step(self,message: str = "",addmsgtolog:bool = False):
        """Perform step of self.stepval (default 1). Sets message to message. Optionally adds message to log"""
        self.value += self.stepval
        self.submsg = message
        if addmsgtolog:
            self.appendlog(message)
        self.update()
    def done(self):
        """Mark progress bar as complete. Optionally waits for keypress. Control with self.wfkp(bool)"""
        if self.wfkp:
            self.value = self.max
            self.submsg = "Press any key to continue"
            self.update()
            self.screen.getch()
        self.screen.clear()
    def appendlog(self,text: str,colour: int = 0):
        """Add text to log with colour colour"""
        self.loglist.append(text)
        self.lclist.append(colour)
        self.update() 