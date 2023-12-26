from subprocess import call
call(['C4.env\\Scripts\\activate'], shell=True)

from tkinter import Tk,PhotoImage,Frame,Canvas,NW,SE,Button
from numpy import zeros,rot90,diag
from pickle import dump,load
from math import pi,sin,cos
from pygame import mixer

C4 = Tk(className=" CONNECT 4")
WIDTH = 550
HEIGHT = 600
C4.geometry(f"{WIDTH}x{HEIGHT}+{(C4.winfo_screenwidth()-550)//2}+0")

Sframe = Frame(C4,width=WIDTH,height=HEIGHT,bg='black') #! Starting screen
Gframe = Frame(C4,width=WIDTH,height=HEIGHT)            #! Game screen
Wframe = Frame(C4,width=WIDTH,height=HEIGHT,bg='green')#! Win screen
Sframe.pack()


Mainbg = PhotoImage(file='background/Main_BG.png')
RuBd   = PhotoImage(file='background/Rup-Bdn.png')
BuRd   = PhotoImage(file='background/Bup-Rdn.png')
REDbg  = PhotoImage(file='background/REDbg.png'  )
BLUEbg = PhotoImage(file='background/BLUEbg.png' )
Btn    = PhotoImage(file='background/Button.png' )

Scan = Canvas(Sframe,width=WIDTH,height=HEIGHT,borderwidth=0,highlightthickness=0)
Mbg = Scan.create_image(0,0,anchor=NW,image=Mainbg)
Rt = Scan.create_text(25,25,text="RED",font=("Comic Sans MS",26,'bold underline'),fill='#3A0603',anchor=NW)
Rscr = Scan.create_text(48,65,text="0",font=("Comic Sans MS",26,'bold'),fill='#3A0603',anchor=NW,tags='Rscr')
Bt = Scan.create_text(525,535,text="BLUE",font=("Comic Sans MS",26,'bold underline'),fill='#000480',anchor=SE)
Bscr = Scan.create_text(491,575,text="0",font=("Comic Sans MS",26,'bold'),fill='#000480',anchor=SE,tags='Bscr')
Scan.pack()
Gcan = Canvas(Gframe,width=WIDTH,height=HEIGHT,borderwidth=0,highlightthickness=0)
B = Gcan.create_image(0,0,anchor=NW,image=BLUEbg,tags='Btag')
R = Gcan.create_image(0,0,anchor=NW,image=REDbg,tags='tag')
Gcan.pack()
Wcan = Canvas(Wframe,width=WIDTH,height=HEIGHT,borderwidth=0,highlightthickness=0)
uRB = Wcan.create_image(0,-150,anchor=NW,image=RuBd) 
uBR = Wcan.create_image(0,600,anchor=NW,image=BuRd)
wtxt = Wcan.create_text(WIDTH//2,HEIGHT//2,text="",font=("Comic Sans MS",70,'bold'),fill='Black',anchor='center')
Wcan.pack()

play = Button(Sframe,image=Btn,relief="flat",border=0,command=lambda:exec("Sframe.forget(),Gframe.pack()"))
play.place(x=WIDTH//2,y=HEIGHT//2,anchor='center')

"""*****DECORATION*****"""
p = [(WIDTH//2 + 120 * cos((2 * pi / 360) * i)-25,HEIGHT//2 + 120 * sin((2 * pi / 360) * i)-25)for i in range(360)]
for e,i in enumerate(p[:360:45]):
    Scan.create_oval(i[0],i[1],i[0]+50,i[1]+50,fill='#F77A7A' if e%2==0 else '#83F7F7',outline='')
z = 1
def spin():
    global z
    Scan.moveto('6',*p[z%360])
    Scan.moveto('7',*p[(z+45)%360])
    Scan.moveto('8',*p[(z+90)%360])
    Scan.moveto('9',*p[(z+135)%360])
    Scan.moveto('10',*p[(z+180)%360])
    Scan.moveto('11',*p[(z+225)%360])
    Scan.moveto('12',*p[(z+270)%360])
    Scan.moveto('13',*p[(z+315)%360])
    z += 1
    Scan.after(10,spin)
Scan.after(25,spin)

"""*****BACKGROUND MUSIC*****"""
mixer.init()
mixer.music.load("background/Dear Little Brother....mp3")
mixer.music.play(loops = -1)

"""*****ALl FUNCTIONS*****"""
def ball_preview(event):
    try:
        xyxy,_ = CAN[event.widget][-1]
        user_color = "#3A0603" if user==1 else "#000480"  #?  Red else Blue
        event.widget.create_oval(xyxy,fill=user_color,outline='')
    except IndexError: pass

def ball_gone(event):
    try:
        xyxy,_ = CAN[event.widget][-1]
        event.widget.create_oval(xyxy,fill="#1E1E3F",outline='')
    except IndexError: pass

def ball_confirm(event):
    global user,active_color
    xyxy,(x,y) = CAN[event.widget][-1]
    event.widget.create_oval(xyxy,fill=active_color,outline='')
    board[x,y]=user
    if check(x,y) == 'WIN':
        win_game()
    active_color = "#00FFFF" if active_color=="#FF0000" else "#FF0000" #? Blue else Red
    try:
        if user==1:
            user=2
            Gcan.tag_raise('Btag')
            mini['1'].create_rectangle(0,0,20,20,fill="#0F8D9E",outline='') #topleftbox
            mini['1'].create_arc(0,0,40,40,fill="#2D2B55",outline='',start=90,extent=90) #topleftarc
            mini['1'].create_rectangle(0,400,20,420,fill="#1D2343",outline='') #bottomleftbox
            mini['1'].create_arc(0,380,40,420,fill="#2D2B55",outline='',start=180,extent=90) #bottomleftarc
            mini['7'].create_rectangle(50,0,70,20,fill="#0F8D9E",outline='') #toprighttbox
            mini['7'].create_arc(30,0,70,40,fill="#2D2B55",outline='',start=0,extent=90) #toprighttarc
            mini['7'].create_rectangle(50,400,70,420,fill="#1D2343",outline='') #bottomrighttbox
            mini['7'].create_arc(30,380,70,420,fill="#2D2B55",outline='',start=270,extent=90) #bottomrighttarc
        elif user==2:
            user=1
            global red
            def red():
                Gcan.tag_raise('tag')
                mini['1'].create_rectangle(0,0,20,20,fill="#8C0F20",outline='') #topleftbox
                mini['1'].create_arc(0,0,40,40,start=90,extent=90,fill="#2D2B55",outline='') #topleftarc
                mini['1'].create_rectangle(0,400,20,420,fill="#231D3E",outline='') #bottomleftbox
                mini['1'].create_arc(0,380,40,420,start=180,extent=90,fill="#2D2B55",outline='') #bottomleftarc
                mini['7'].create_rectangle(50,0,70,20,fill="#8C0F20",outline='') #toprighttbox
                mini['7'].create_arc(30,0,70,40,start=0,extent=90,fill="#2D2B55",outline='') #toprighttarc
                mini['7'].create_rectangle(50,400,70,420,fill="#231D3E",outline='') #bottomrighttbox
                mini['7'].create_arc(30,380,70,420,start=270,extent=90,fill="#2D2B55",outline='') #bottomrighttarc
            red = red
            red()
        CAN[event.widget].pop()
        if not CAN[event.widget]:  #? If the list is empty unbind everything
            event.widget.unbind('<Button-1>')
            event.widget.unbind('<Enter>')
            event.widget.unbind('<Leave>')
        else:
            xyxy,_ = CAN[event.widget][-1]
            user_color = "#3A0603" if user==1 else "#000480"  #?  Red else Blue
            event.widget.create_oval(xyxy,fill=user_color,outline='')
    except IndexError:pass

def restart_game(event=None):
    Wframe.forget()
    Sframe.pack()
    global CAN,user,board,CANsave,active_color,active_bg
    for column in CANsave:
        column.bind('<Leave>',ball_gone) #!
        column.bind('<Enter>',ball_preview) #!
        column.bind('<Button-1>',ball_confirm) #!
        CAN[column].clear()
        CAN[column].extend(CANsave[column])
        for xyxy,_ in CAN[column]:
            column.create_oval(xyxy,fill="#1E1E3F",outline='')
    user = 1
    red()
    active_color = '#FF0000' #! restarting with red
    active_bg = REDbg #! red
    board = zeros((6,7))

def win_game():
    win_color = '#A05F5F-RED' if user==1 else '#5FA0A0-BLUE'
    Wcan.config(bg=win_color[0:7])
    score_update()
    if user==1:
        Wcan.moveto(uRB,0,150)
        Wcan.moveto(uBR,0,300)
    else:
        Wcan.moveto(uBR,0,150)
        Wcan.moveto(uRB,0,300)
    Wcan.itemconfig(wtxt,text=win_color[8:]+" WON")
    Gframe.forget()
    Wframe.pack()
    C4.after(2690,restart_game)

def score_update():
    scr = load(open('score.dat','rb'))
    scr[user] += 1
    dump(scr,open('score.dat','wb'))
    Scan.itemconfig('Rscr' if user==1 else 'Bscr',text=scr[user])



dump({1:0,2:0},open('score.dat','wb')) #! Scores are saved here
CAN,mini = {}, {} #! CAN - contains the main canvas, don't mind the mini it's for the corner shaping
active_color = '#FF0000'      #! start with red
active_bg = REDbg #! red
user = 1                      #! red

"""*****CONSTRUCTION OF THE GAME SCREEN*****"""
cany,canx = HEIGHT*0.25, HEIGHT*0.05
for clm in (r:=range(7)):
    if clm==r[0] or clm==r[-1]:
        mini[f'{clm+1}'] = column = Canvas(Gcan,bg="#2D2B55",width=70,height=420,borderwidth=0,highlightthickness=0)
    else:
        column = Canvas(Gcan,bg="#2D2B55",width=70,height=420,borderwidth=0,highlightthickness=0)
    column.bind('<Button-1>',ball_confirm) #!
    column.bind('<Enter>',ball_preview) #!
    column.bind('<Leave>',ball_gone) #!
    column.place(y=cany,x=canx+70*(clm))

    if clm==r[0]: #? making the top-left & bottom-left corners curved
        column.create_rectangle(0,0,20,20,fill="#8C0F20",outline='') #topleftbox
        column.create_arc(0,0,40,40,start=90,extent=90,fill="#2D2B55",outline='') #topleftarc
        column.create_rectangle(0,400,20,420,fill="#231D3E",outline='') #bottomleftbox
        column.create_arc(0,380,40,420,start=180,extent=90,fill="#2D2B55",outline='') #bottomleftarc
    
    if clm==r[-1]: #? making the top-right & bottom-right corners curved
        column.create_rectangle(50,0,70,20,fill="#8C0F20",outline='') #toprighttbox
        column.create_arc(30,0,70,40,start=0,extent=90,fill="#2D2B55",outline='') #toprighttarc
        column.create_rectangle(50,400,70,420,fill="#231D3E",outline='') #bottomrighttbox
        column.create_arc(30,380,70,420,start=270,extent=90,fill="#2D2B55",outline='') #bottomrighttarc
    
    CAN[column] = []
    for row in range(6): #? creating a cirle of diameter 50 inside the box of lenght 70
        x_y = [20,(row*70)+20,50,(row+1)*70-20]
        column.create_oval(x_y,fill="#1E1E3F",outline='')
        CAN[column].append((x_y,(row,clm)))

board = zeros((6,7))
CANsave = {}     #! Creating a copy for later use
for k,v in CAN.items():
    CANsave[k]=[]
    CANsave[k].extend(v)

"""*****CONSTRUCTION OF THE GAME ALGORITHM*****"""
def check(i,j):
    cx,cy = i,j
    # horizondal
    hy = 0 if (cy-3) < 0 else (cy-3)
    row = ''.join([str(int(ball)) for ball in board[cx,hy:cy+4]])
    if str(user)*4 in row:
        return 'WIN'    #! WINWINWINWINWINWINWINWINWINWINWINWINWINWINWINWIN
    
    #vertical
    vx = 0 if (cx-3) < 0 else (cx-3)
    row = ''.join([str(int(ball)) for ball in board[vx:cx+4,cy]])
    if str(user)*4 in row:
        return 'WIN'   #! WINWINWINWINWINWINWINWINWINWINWINWINWINWINWINWIN
    #diagonal
    dx = cx - min(cx,cy)
    dy = cy - min(cx,cy)
    dboard = board[dx:cx+4,dy:cy+4]
    row = ''.join([str(int(ball)) for ball in diag(dboard)])
    if str(user)*4 in row:
        return 'WIN'   #! WINWINWINWINWINWINWINWINWINWINWINWINWINWINWINWIN
    #anti-diagonal
    """Lazy solution here too"""
    adx = cx
    ady = cy
    while 1:
        try:
            _=board[adx,ady]
            if adx==0: break   #? Reached top boarder
            adx,ady=adx-1,ady+1
        except IndexError:
            adx,ady=adx+1,ady-1
            break              #? Reached right boarder
    cut_board = rot90(board[adx:cx+4,hy:ady+1])
    row = ''.join([str(int(ball)) for ball in diag(cut_board)])
    if str(user)*4 in row:
        return 'WIN'   #! WINWINWINWINWINWINWINWINWINWINWINWINWINWINWINWIN


C4.mainloop()
