import datetime
from tkinter import *
from tkinter import ttk
import time
import winsound
import pandas as pd
import modules
import win32api, win32con, keyboard as K
from tkinter import messagebox

#assets:
##DataBase
can_vote_boy = 'assets\Can_Vote_boy.csv'
can_vote_girl = 'assets\Can_Vote_girl.csv'
can_boy = 'assets\Can_boy.csv'
can_girl = 'assets\Can_girl.csv'
voters_det = 'assets\Voters_det.csv'
vote_skip  = 'assets\Vote_skip.csv'
icon = "assets\icon-voting.ico"
##fonts
fnt_1 = 'Consolas'  #title
fnt_2 = 'Consolas'  #text1
fnt_3 = 'Consolas'  #text2
fnt_4 = 'Consolas'  #buttons
#Pre-defines:
Delay = 5
title = 'Aspl Election'
#Pre-Defined Funtions
def back():
    clr_scrn()
    mainwindow()
def clr_scrn():
    for x in rtm.winfo_children():
        x.destroy()
def BackButton(fr):
    return Button(fr, text="\u274C", font=(fnt_4, 20),bg='#d62929', command=back).place(relx=0.98, rely=0.98, anchor=SE)  
def Screen():
    rtf = LabelFrame(rtm)
    rtf.place(relx=0.5, rely=0.5, relheight=0.983, relwidth=0.983, anchor=CENTER)
    return rtf

#root
rtm = Tk()
rtm.title(title)
rtm.iconbitmap(icon)
width = rtm.winfo_screenwidth() - 50
height = rtm.winfo_screenheight() - 50
rtm.geometry('%dx%d'%(width, height))

def mainwindow():
    rtf = LabelFrame(rtm)
    rtf.place(relx=0.5, rely=0.5, relheight=0.983, relwidth=0.983, anchor=CENTER)
    #Labels
    Label(rtf, text=title, font=(fnt_1, 30)).pack()
    #buttons
    Button(rtf, text="Button1", font=(fnt_4, 15), command=PrePolling).pack()
    Button(rtf, text="Button2", font=(fnt_4, 15), command=Result).pack()

def CanAdd():
    clr_scrn()
    #frame
    rtf = Screen()  #rtv - frame for view widgets
    rtv_b = Frame(rtf)
    rtv_b.place(relx=0.45, rely=0.26)
    rtv_g = Frame(rtf)
    rtv_g.place(relx=0.65, rely=0.26)
    rtv_tr_b = Frame(rtf)
    rtv_tr_b.place(relx=0.02, rely=0.26)
    rtv_tr_g = Frame(rtf)
    rtv_tr_g.place(relx=0.2, rely=0.26)
    #View
    Tr_boy = modules.ListCre(rtv_tr_b)
    Tr_girl= modules.ListCre(rtv_tr_g)
    Boy_List = modules.ListCre(rtv_b)
    Girl_List = modules.ListCre(rtv_g)
    df_girl = modules.read(can_girl)
    df_boy = modules.read(can_boy)          #df to dis in treeView
    modules.ListIns(Tr_boy, list(df_boy.iloc[:, 0])) 
    modules.ListIns(Tr_girl, list(df_girl.iloc[:, 0]))   
    #PreDefines
    def boy_add(to_add):
        if str(to_add.get()) == '':
            return 
        modules.ListIns(Boy_List, [str(to_add.get()).upper()])
        to_add.delete(0, END)
    def girl_add(to_add):
        if str(to_add.get()) == '':
            return 
        modules.ListIns(Girl_List, [str(to_add.get()).upper()])
        to_add.delete(0, END)
    def remove():
        for x in Girl_List.curselection():
            Girl_List.delete(x)
        for x in Boy_List.curselection():
            Boy_List.delete(x)
    def Confrm_add(buf = True):
        Data_boy = list(Boy_List.get(0, END))
        Data_boy.sort()
        Data_girl = list(Girl_List.get(0, END))
        Data_girl.sort()
        if len(Data_boy) == 0 or len(Data_girl) == 0:
            buf = messagebox.askokcancel('warning', 'One of the ListBoxes are empty, Proceed?')
        if not buf:
            return
        df_boy = pd.DataFrame(list(Data_boy), columns=['Boy'])
        df_girl= pd.DataFrame(list(Data_girl), columns=['Girl'])
        modules.write(df_boy, can_boy, mod='w', hdr=True)
        modules.write(df_girl, can_girl, mod='w', hdr=True)
        lst = []
        for x in range(df_boy.shape[0]):
            lst.append(0)
        df_boy = pd.concat([df_boy, pd.DataFrame(list(list(lst)), columns=['VOTE'])], axis=1)
        modules.write(df_boy, can_vote_boy, mod='w', hdr=True)
        lst = []
        for x in range(df_girl.shape[0]):
            lst.append(0)
        df_girl = pd.concat([df_girl, pd.DataFrame(list(list(lst)), columns=['VOTE'])], axis=1)
        modules.write(df_girl, can_vote_girl, mod='w', hdr=True)
        CanAdd()
    #Labels
    Label(rtf, text="Edit Candidate List", font=(fnt_1, 30)).place(relx=0.01, rely=0.01, anchor=NW)
    Label(rtf, text='Boy Candidate', font=(fnt_2, 15)).place(relx=0.01, rely=0.12)
    Label(rtf, text='Girl Candidate', font=(fnt_2, 15)).place(relx=0.5, rely=0.12)
    Label(rtf, text='Current List', font=(fnt_1, 18)).place(relx=0.02, rely=0.2)
    Label(rtf, text='New List Boy', font=(fnt_1, 18)).place(relx=0.45, rely=0.2)
    Label(rtf, text='New List Girl', font=(fnt_1, 18)).place(relx=0.65, rely=0.2)
    #Entry
    boy = Entry(rtf, width=20, font=(fnt_3, 15))
    boy.place(relx=0.125, rely=0.12)
    girl= Entry(rtf, width=20, font=(fnt_3, 15))
    girl.place(relx=0.625, rely=0.12)
    #Buttons
    BackButton(rtf)
    Button(rtf, text="\u2795", font=(fnt_4, 15), command=lambda: boy_add(boy)).place(relx=0.3, rely=0.11) 
    Button(rtf, text="\u2795", font=(fnt_4, 15), command=lambda: girl_add(girl)).place(relx=0.8, rely=0.11)
    Button(rtf, text='Remove', font=(fnt_4, 20), command=remove).place(relx=0.55, rely=0.6, relwidth=0.15)
    Button(rtf, text="Confrim Add", font=(fnt_4, 20), command= Confrm_add).place(relx=0.55, rely=0.7, relwidth=0.15)
    #PostDefines
    def Binds(e = None):
        focs = str(rtm.focus_get())[13:]
        if focs == '.!entry':
            boy_add(boy)
        if focs == '.!entry2':
            girl_add(girl)
    #bindings
    rtm.bind('<Return>', Binds)
def EditVoter():
    clr_scrn()
    #Frames
    rtf = Screen()
    rtr1 = Frame(rtf)
    rtr1.place(relx=0.02, rely=0.26)
    rtr2 = Frame(rtf)
    rtr2.place(relx=0.45, rely=0.26)
    #DataCorrections
    def DataCorrection():
        lst = []
        df = modules.read(voters_det)
        df_dup = df[df.duplicated() == False]
        for x in range(df_dup.shape[0]):
            lst.append(df[df['VOTERS ID'] == df_dup.iloc[x, 0]].shape[0])
        df_toDis = pd.concat([df_dup['VOTERS ID'], pd.DataFrame(list(lst), columns=['Students'])], axis=1).drop_duplicates()
        return df_toDis
    df_tr_Current = DataCorrection()
    #View
    modules.TableDis(df_tr_Current, ('Section', 'Students Count'), 15, rtr1, True, 200)
    Tr_New     = modules.TableDis([], ('Section', 'Students Count'), 15, rtr2, False, 200)
    #PreDefines
    def Remove():
        for x in Tr_New.selection():
            Tr_New.delete(x)
    def Save():
        sec_lst = []
        no_lst  = []
        df = modules.TableFetch(Tr_New, ['VOTERS ID', 'NO'])
        for x in range(df.shape[0]):
            Sec_Str = df.iloc[x, 0]
            for y in range(int(df.iloc[x, 1])):
                sec_lst.append(Sec_Str)
                no_lst.append(y+1)
        df_Data = pd.concat([pd.DataFrame(sec_lst, columns=['VOTERS ID']), pd.DataFrame(no_lst, columns=['NO'])], axis=1)
        modules.write(df_Data, voters_det, mod='w', hdr=True)
        EditVoter()
    def Add(section, count):
        if str(section.get()) == '':
            return
        try:
            int(student.get())
        except:
            messagebox.showerror('Invalid Format', 'Student count expects \'int\' format only')
            return
        lst = [[section.get(), count.get()]]
        df = pd.DataFrame(lst, columns=['SECTION', 'STUDENT'])
        modules.TableApp(df, Tr_New, False)
        section.delete(len(str(section.get()))-1, END)
        student.delete(0, END)
        student.insert(0, '0')
        section.focus_set()
    #Labels
    Label(rtf ,text = "Edit Voters Detials", font=(fnt_1, 30)).place(relx=0.01, rely=0.01, anchor=NW)
    Label(rtf, text='Section', font=(fnt_2, 15)).place(relx=0.017, rely=0.12)
    Label(rtf, text='Students Count', font=(fnt_2, 15)).place(relx=0.3, rely=0.12)
    Label(rtf, text='Current List', font=(fnt_1, 18)).place(relx=0.02, rely=0.2)
    Label(rtf, text='New List', font=(fnt_1, 18)).place(relx=0.45, rely=0.2)
    #Entry
    section = Entry(rtf, width=10, font=(fnt_3, 15))
    section.place(relx=0.09, rely=0.12)
    student = Entry(rtf, width=10, font=(fnt_3, 15))
    student.place(relx=0.425, rely=0.12)
    student.insert(0, '0')
    #Buttons
    BackButton(rtf)
    Button(rtf, text='Remove', font=(fnt_4, 20), command=Remove).place(relx=0.8, rely=0.26, relwidth=0.1)
    Button(rtf, text="Save", font=(fnt_4, 20), command= Save).place(relx=0.8, rely=0.36, relwidth=0.1)
    Button(rtf, text="\u2795", font=(fnt_4, 15), command=lambda: Add(section, student)).place(relx=0.55, rely=0.11) 
    #Binds
    def AutoFocus():
        focs = str(rtm.focus_get())[13:]
        if focs == '.!entry':
            student.delete(0, END)
            student.focus_set()
        if focs == '.!entry2':
            Add(section, student)
    #Bindings
    rtm.bind('<Return>', lambda e: AutoFocus())
def Polling():
    clr_scrn()
    rtf = Screen()
    rtm.attributes('-fullscreen', True)
    delay_fr = Frame(rtf)
    Id = Frame(rtf)
    boy = Frame(rtf)
    girl= Frame(rtf)
    Id.place(relx=0.01, rely=0.1)
    boy.place(relx=0.15, rely=0.2)
    girl.place(relx=0.5, rely=0.2)
    delay_fr.place(relx=0.5, rely=0.5, anchor=CENTER)
    voter = modules.read(voters_det)
    ind = [0]
    reset = pd.DataFrame(list([]), columns = ['Voters_id']) 
    modules.write(reset, vote_skip, mod = 'w', hdr=True)
    #Label
    Label(rtf, text=title, font=(fnt_1, 30)).place(relx=0.5, rely=0.01, anchor=N)
    rtf.update()
    def Poll():
        BoyFlag = [False]
        GirlFlag= [False]
        VoteBoy = IntVar()
        VoteGirl= IntVar()
        rtf.update()
        def Over(): 
            for x in range(5, -1, -1):
                for y in rtf.winfo_children():
                    y.destroy()
                rtm.update()
                Label(rtf, text = 'Back In', font = (fnt_3, 15)).pack()
                Label(rtf, text=str(x)+' seconds', font = (fnt_3, 15)).pack()
                rtm.update()
                time.sleep(1)
                rtm.update()
            rtm.attributes('-fullscreen', False)
            PostPolling()
        def Save():
            VoteCountBoy = modules.read(can_vote_boy)
            VoteCountGirl = modules.read(can_vote_girl)
            boy_ind = VoteBoy.get()
            girl_ind= VoteGirl.get()
            VoteCountBoy.iloc[boy_ind, -1] += 1
            VoteCountGirl.iloc[girl_ind, -1] += 1
            modules.write(VoteCountBoy , can_vote_boy , mod = 'w', hdr=True)
            modules.write(VoteCountGirl, can_vote_girl, mod = 'w', hdr=True)
        def boyFlag():
            BoyFlag.clear()
            BoyFlag.append(True)
            if GirlFlag[0]:
                rtm.update()
                winsound.Beep(2500, 1500)
                Next(ind)
        def girlFlag():
            GirlFlag.clear()
            GirlFlag.append(True)
            if BoyFlag[0]:
                rtm.update()
                winsound.Beep(2500, 1500)
                Next(ind)
        def clr_all():
            for a in boy.winfo_children():
                a.destroy()
            for a in girl.winfo_children():
                a.destroy()
            for a in Id.winfo_children():
                a.destroy()
        def Next(ind):
            if ind[0]>=voter.shape[0]-1:
                Over()
            ind[0]+=1
            Save()
            clr_all()
            Create()
        def Skip(e = None):
            df_Skip = pd.DataFrame([str(voter.iloc[ind[0], 0])+" - "+str(voter.iloc[ind[0], 1])], columns=['Voters_id'])
            if ind[0]>=voter.shape[0]-1:
                Over()
            ind[0]+=1
            modules.write(df_Skip, vote_skip)
            clr_all()
            Create()
        def Create():
            BoyFlag.clear()
            BoyFlag.append(False)
            GirlFlag.clear()
            GirlFlag.append(False)
            Label(Id, text=str(voter.iloc[ind[0], 0])+" - "+str(voter.iloc[ind[0], 1]), font=(fnt_2, 25)).pack()
            VoteBoy.set(None)
            VoteGirl.set(None)
            df_boy = list(modules.read(can_boy).iloc[:, 0])
            df_girl= list(modules.read(can_girl).iloc[:, 0])
            rtm.update()
            rtm.unbind('<Return>')
            K.press_and_release("capslock")
            delay_fr.tkraise()
            for x in range(Delay, 0, -1):
                Label(delay_fr, text="Please Wait for \n"+str(x)+' Seconds', font=(fnt_3, 15)).pack()
                rtm.update()
                time.sleep(1)
                for x in delay_fr.winfo_children():
                    x.destroy()
            rtm.update()
            for frame in [Id, boy, girl]:
                frame.tkraise()
            for val,x in enumerate(df_boy):
                r = Radiobutton(boy, text=x, value=val, variable=VoteBoy, font=(fnt_4, 25), width=20,indicatoron=0, selectcolor='green', command=boyFlag)
                r.pack(fill = X, pady=3)
            for val,x in enumerate(df_girl):
                r = Radiobutton(girl, text=x, value=val, variable=VoteGirl, font=(fnt_4, 25), width=20,indicatoron=0, selectcolor='green',command=girlFlag)
                r.pack(fill = X, pady=3)
            rtm.bind('<Return>', lambda e: Skip())
            K.press_and_release("capslock")
        if not win32api.GetKeyState(win32con.VK_CAPITAL):
            K.press_and_release("capslock")
        Create()
        rtf.update()
    Poll()
def PreView(back = True):
    clr_scrn()
    rtf = Screen()
    rtm.attributes('-fullscreen', True)
    delay_fr = Frame(rtf)
    Id = Frame(rtf)
    boy = Frame(rtf)
    girl= Frame(rtf)
    Id.place(relx=0.01, rely=0.1)
    boy.place(relx=0.15, rely=0.2)
    girl.place(relx=0.5, rely=0.2)
    delay_fr.place(relx=0.5, rely=0.5, anchor=CENTER)
    voter = modules.read(voters_det)
    ind = [0]
    #Label
    Label(rtf, text=title, font=(fnt_1, 30)).place(relx=0.5, rely=0.01, anchor=N)
    rtf.update()
    def Poll():
        BoyFlag = [False]
        GirlFlag= [False]
        VoteBoy = IntVar()
        VoteGirl= IntVar()
        rtf.update()
        def Over(): 
            for x in range(5, -1, -1):
                for y in rtf.winfo_children():
                    y.destroy()
                rtm.update()
                Label(rtf, text = 'Back In', font = (fnt_3, 15)).pack()
                Label(rtf, text=str(x)+' seconds', font = (fnt_3, 15)).pack()
                rtm.update()
                time.sleep(1)
                rtm.update()
            rtm.attributes('-fullscreen', False)
            back()
        def Save():
            VoteCountBoy = modules.read(can_vote_boy)
            VoteCountGirl = modules.read(can_vote_girl)
            boy_ind = VoteBoy.get()
            girl_ind= VoteGirl.get()
            VoteCountBoy.iloc[boy_ind, -1] += 1
            VoteCountGirl.iloc[girl_ind, -1] += 1
            modules.write(VoteCountBoy , can_vote_boy , mod = 'w', hdr=True)
            modules.write(VoteCountGirl, can_vote_girl, mod = 'w', hdr=True)
        def boyFlag():
            BoyFlag.clear()
            BoyFlag.append(True)
            if GirlFlag[0]:
                rtm.update()
                winsound.Beep(2500, 1500)
                Next(ind)
        def girlFlag():
            GirlFlag.clear()
            GirlFlag.append(True)
            if BoyFlag[0]:
                rtm.update()
                winsound.Beep(2500, 1500)
                Next(ind)
        def clr_all():
            for a in boy.winfo_children():
                a.destroy()
            for a in girl.winfo_children():
                a.destroy()
            for a in Id.winfo_children():
                a.destroy()
        def Next(ind):
            if ind[0]>=voter.shape[0]-1:
                Over()
            ind[0]+=1
            #Save()
            clr_all()
            Create()
        def Skip(e = None):
            df_Skip = pd.DataFrame([str(voter.iloc[ind[0], 0])+" - "+str(voter.iloc[ind[0], 1])], columns=['Voters_id'])
            if ind[0]>=voter.shape[0]-1:
                Over()
            ind[0]+=1
            clr_all()
            Create()
        def Create():
            BoyFlag.clear()
            BoyFlag.append(False)
            GirlFlag.clear()
            GirlFlag.append(False)
            Label(Id, text=str(voter.iloc[ind[0], 0])+" - "+str(voter.iloc[ind[0], 1]), font=(fnt_2, 25)).pack()
            VoteBoy.set(None)
            VoteGirl.set(None)
            df_boy = list(modules.read(can_boy).iloc[:, 0])
            df_girl= list(modules.read(can_girl).iloc[:, 0])
            rtm.update()
            rtm.unbind('<Return>')
            K.press_and_release("capslock")
            delay_fr.tkraise()
            for x in range(Delay, 0, -1):
                Label(delay_fr, text="Please Wait for \n"+str(x)+' Seconds', font=(fnt_3, 15)).pack()
                rtm.update()
                time.sleep(1)
                for x in delay_fr.winfo_children():
                    x.destroy()
            rtm.update()
            for frame in [Id, boy, girl]:
                frame.tkraise()
            for val,x in enumerate(df_boy):
                r = Radiobutton(boy, text=x, value=val, variable=VoteBoy, font=(fnt_4, 25), width=20,indicatoron=0, selectcolor='green', command=boyFlag)
                r.pack(fill = X, pady=3)
            for val,x in enumerate(df_girl):
                r = Radiobutton(girl, text=x, value=val, variable=VoteGirl, font=(fnt_4, 25), width=20,indicatoron=0, selectcolor='green',command=girlFlag)
                r.pack(fill = X, pady=3)
            rtm.bind('<Return>', lambda e: Skip())
            K.press_and_release("capslock")
        if not win32api.GetKeyState(win32con.VK_CAPITAL):
            K.press_and_release("capslock")
        def fun_but():
            if back:
                back()
            else:
                clr_scrn()
                PrePolling()
            rtm.attributes('-fullscreen', False)
        but = Button(rtf, text="\u274C", font=(fnt_4, 20),bg='#d62929', command=fun_but).place(relx=0.98, rely=0.98, anchor=SE)
        Create()
        rtf.update()
    Poll()
def PrePolling():
    #SuperPreDefines
    totalVoters =modules.read(voters_det).shape[0]
    def StartPolling():
        st = messagebox.askokcancel("Agree", "Don\'t close the window or\nDon\'t turn off the Computer before polling gets over")
        if st:
            Polling()
    def DataCorrected():
        lst = []
        df = modules.read(voters_det)
        df_dup = df[df.duplicated() == False]
        for x in range(df_dup.shape[0]):
            lst.append(df[df['VOTERS ID'] == df_dup.iloc[x, 0]].shape[0])
        df_toDis = pd.concat([df_dup['VOTERS ID'], pd.DataFrame(list(lst), columns=['Students'])], axis=1).drop_duplicates()
        return df_toDis
    clr_scrn()
    #Frames
    rtf = Screen()
    CanBoy = Frame(rtf)
    CanBoy.place(relx = 0.05, rely = 0.1)
    CanGirl = Frame(rtf)
    CanGirl.place(relx = 0.3, rely = 0.1)
    Tree = Frame(rtf)
    Tree.place(relx=0.6, rely=.1)
    #Views
    modules.ListIns(modules.ListCre(CanBoy), list(modules.read(can_boy).iloc[:, 0]))
    modules.ListIns(modules.ListCre(CanGirl), list(modules.read(can_girl).iloc[:, 0]))
    modules.TableDis(DataCorrected(), ('Section', 'Students'), 11, Tree, True, 200)
    #Labels
    Label(rtf, text='BoyCandiate', font=(fnt_1, 20)).place(relx=0.05, rely=0.05)
    Label(rtf, text='GirlCandiate', font=(fnt_1, 20)).place(relx=0.3, rely=0.05)
    Label(rtf, text='VotersDetials', font=(fnt_1, 20)).place(relx=0.6, rely=0.05)
    Label(rtf, text="Title : "+title, font=(fnt_1, 25)).place(relx=0.05, rely=0.5)
    Label(rtf, text="Delay : "+str(Delay)+" Seconds", font=(fnt_1, 25)).place(relx=0.05, rely=0.6)
    Label(rtf, text="Estimated Total Time : "+str(datetime.timedelta(seconds=(Delay+10)*totalVoters)), font=(fnt_1, 25)).place(relx=0.05, rely=0.7)
    Label(rtf, text="Total Voters : "+str(totalVoters), font=(fnt_1, 27)).place(relx=0.6, rely=0.5)
    State = Label(rtf, font=(fnt_1, 25))
    State1= Label(rtf, font=(fnt_1, 25))
    clr = False
    if modules.read(can_boy).shape[0] <= 11:
        State['text'] = 'No. of BoyCandidates : Good'
        State['fg'] = "green"
    else:
        State['text'] = 'No. of BoyCandidates : not \nunder recomended range'
        State['fg'] = 'red'
        clr = True
    if modules.read(can_girl).shape[0] <= 11:
        State1['text'] = 'No. of GirlCandidates : Good'
        State1['fg'] = "green"
    else:
        State1['text'] = 'No. of GirlCandidates : not \nunder recomended range'
        State1['fg'] = 'red'
        clr = True
    State.place(relx=0.6, rely=0.6)
    State1.place(relx=0.6, rely=0.7)
    #Button
    poll =Button(rtf, text="Start Polling", font=(fnt_4, 25),background='green', command=StartPolling)
    poll.place(relx=0.4, rely=0.95, anchor=S)
    BackButton(rtf)
    if clr:
        poll['background'] = 'Red'
    Button(rtf, text="PreView", font=(fnt_4, 25), background='yellow', command=lambda :PreView(False)).place(relx=0.6, rely=0.95, anchor=S)
def PostPolling():
    clr_scrn()
    #SuperPreDefines
    skips = modules.read(vote_skip).shape[0]
    voter = modules.read(voters_det).shape[0]
    voted = voter-skips
    per = round((voted/voter)*100, 2)
    #Frames
    rtf = Screen()
    rt = Frame(rtf)
    rt.place(relx=0.5, rely=0.5, anchor=CENTER)
    #Labels
    Label(rtf, text=title, font=(fnt_1, 30)).place(relx=0.5, rely=0.02, anchor=N)
    Label(rt, text='Polling completed', font=(fnt_1, 35)).pack()
    Label(rt, text='Total Voters : '+str(voter), font=(fnt_1, 25)).pack()
    Label(rt, text='Total Votes : '+str(voter-skips), font=(fnt_1, 25)).pack()
    Label(rt, text='Total Non Voters : '+str(skips), font=(fnt_1, 25)).pack()
    Label(rt, text="Poll Percentage : "+str(per)+'%', font=(fnt_1, 25)).pack()
    #Buttons
    BackButton(rtf)
def Result():
    #Data
    Boy = modules.read(can_vote_boy).sort_values(by='VOTE', ascending=False)
    Girl= modules.read(can_vote_girl).sort_values(by="VOTE", ascending=False)
    clr_scrn()
    #Frames
    rtf = Screen()
    TrBoy = Frame(rtf)
    TrBoy.place(relx=0.3, rely=0.5, anchor=CENTER)
    TrGirl= Frame(rtf)
    TrGirl.place(relx=0.7, rely=0.5, anchor=CENTER)
    #View
    modules.TableDis(Boy ,list(Boy.columns) , 11, TrBoy , True, 200)
    modules.TableDis(Girl,list(Girl.columns), 11, TrGirl, True, 200)
    #Labels
    Label(rtf, text="Reuslts", font=(fnt_1, 30)).place(relx=0.01, rely=0.01, anchor=NW)
    Label(rtf, text="BoyCandidates", font=(fnt_1, 25)).place(relx=0.3, rely=0.3, anchor=CENTER)
    Label(rtf, text='GirlCandidates', font=(fnt_1, 25)).place(relx=0.7, rely=0.3, anchor=CENTER)
    BackButton(rtf)


mainwindow()
rtm.mainloop()