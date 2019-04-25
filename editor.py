import os, threading
from time import sleep
from tkinter import *
from tkinter.ttk import *
globals()["homedir"]=os.getcwd()
globals()["Gitfolder"]=os.path.expanduser('~')+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\GitHub, Inc"
globals()["ischecked"]=False

def start():
    main=genwindow("Start",mwidth=600,resize=False)

    globals()["ptext"]=StringVar()
    globals()["progress"]=Progressbar(main,mode="determinate",maximum=9)
    Titletext=Label(main,text="Starting the editor",justify=CENTER)
    progresstext=Label(main,textvariable=ptext,justify=CENTER)
    
    Titletext.pack(pady=30)
    progresstext.pack(pady=10)
    progress.pack(padx=10,fill="x",pady=10)
    
    progress.step(1)

    t1=threading.Thread(target=lambda:load(main),name="load")
    t1.start()

    main.mainloop()

def flipchecked():
    global ischecked
    if ischecked:
        ischecked=False
    else:
        ischecked=True

def fetchfiles(directory=""):
    files=[]
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            files.append(f)
    return files

def loadpages():
    globals()["products"],globals()["categories"],b=[],[],0
    with open(homedir+"\\product.html","r",errors='ignore') as f:
        m=f.read().replace("\t","").replace("  ","")
    for x in m.split("<sub id=")[1:]+[">null<"]:
        categories.append(x.split(">")[1].split("<")[0])

    for x in m.split('<script>')[0].split('<tr>')[2:]:
        try:
            a,loaded,category=x.split("</table>")[0],True,categories[b]
            if "-->" in a:
                loaded=False
            if categories[b+1] in x:
                b+=1

            product=a.split('<a href="')[1].split('" class="t"')[0].replace("/","\\")
            name=a.split('class="t">')[2].split("</a>")[0]
            image='Images/'+splitbetween(a,'Images/',".jpg")+'.jpg'
            short=a.split("<td>")[3].split("</td>")[0]

            with open(homedir+"\\"+product,"r") as f:
                m=f.read()
            a=splitbetween(m,'<img src="../','</h3>').replace("\t","")

            price=splitbetween(splitbetween(a,"<h2>"),"<b>","end")
            description=splitbetween(a,'<h3 align="left">',"end")

            products.append([name,price,short,category,description,image,loaded])
        except:
            pass

def genwindow(title="",width=0,height=0,mwidth=0,mheight=0,posx=0,posy=0,resize=True):
    new=Tk()
    new.title(title)
    if (width>0) and (height>0):
        new.geometry('%dx%d' % (max(width,mwidth+10),max(height,mheight+10)))
    if (mwidth>0) and (mheight>0):
        new.minsize(int(min(width,mwidth)),int(min(height,mheight)))
    if not resize:
        new.resizable(0,0)
    new.geometry("+"+str(posx)+"+"+str(posy))
    settop(new)
    return new

def settop(main=""):
    main.attributes('-topmost', True)
    main.attributes('-topmost', False)

def setscrollbox(window="",default="",width=0,height=0,row=0,column=0,scolumn=0,columnspan=1,rowspan=1,pady=5,padx=5,wtype=0):
    if wtype==2:
        Box=Text(window,width=width,height=height)
    elif wtype==1:
        Box=Canvas(window,width=width,height=height)
    else:
        Box=Listbox(window,width=width,height=height)
    Scroll=Scrollbar(window)
    Box.grid(row=row,column=column,columnspan=columnspan,rowspan=rowspan,pady=pady,padx=padx,sticky=N+S+E+W)
    Scroll.grid(row=row,rowspan=rowspan,column=columnspan+max(column+1,scolumn),pady=pady,padx=padx,sticky=N+S)
    Box.config(yscrollcommand=Scroll.set)
    Scroll.config(command=Box.yview)
    Box.insert(END,"")
    return Box, Scroll

def setentrybox(window="",text="",default="",row=0,column=0,rowspan=1,columnspan=1,padx=5,pady=5):
    ent=Entry(window)
    lab=Label(window,text=text)
    ent.grid(row=row,columnspan=columnspan,column=column+1,padx=padx,pady=pady,sticky=W+E)
    lab.grid(row=row,column=column,pady=pady,padx=padx)
    ent.insert(END,default)
    return ent,lab

def dropdown(window="",text="",default="",options=[],row=0,column=0,columnspan=1,sticky="",dropsticky=""):
    choice=StringVar()
    choices=[default]+options
    text=Label(window,text=text)
    option=OptionMenu(window,choice,*choices)
    text.grid(row=row,column=column,columnspan=columnspan,sticky=sticky)
    option.grid(row=row,column=int(column+columnspan),sticky=dropsticky)
    return choice,text,option

def popup(title="",text="",posx=200,posy=200,resize=False,padx=5,pady=5):
    nothing=genwindow(title=title,posx=posx,posy=posy,resize=resize)
    message,okay=Label(nothing,text=text),Button(nothing,text="Okay",command=nothing.destroy)
    message.pack(pady=pady,padx=padx)
    okay.pack(pady=pady,padx=padx)
    mainloop()

def closepopup(main,entry):
    globals()["inputreturn"]=entry.get()
    main.destroy()

def entrypopup(title="",text="",posx=200,posy=200,resize=False,padx=5,pady=5):
    nothing=genwindow(title=title,posx=posx,posy=posy,resize=resize)
    lab,message,okay=Label(nothing,text=text),Entry(nothing),Button(nothing,text="Okay",command=lambda:closepopup(nothing,message))
    lab.pack(pady=pady,padx=padx)
    message.pack(pady=pady,padx=padx)
    okay.pack(pady=pady,padx=padx)
    mainloop()
    return inputreturn

def splitbetween(text="",start="",end=""):
    if end=="":
        end=start[0]+"/"+start[1:]
    if end=="end":
        a=""
        for x in text.split(start)[1:]:
            a+=x
        return a
    else:
        return text.split(start)[1].split(end)[0]

def savechanges():
    a=1
    ##rembered to fill this with the thingy to make the program save the edits

def updateentries():
    Entries.delete(0,END)
    for x in products:
        Entries.insert(END,str(x[0])+": "+str(x[2]))
    productLabel.configure(text="Products: "+str(len(products)))

def fetchdirectory(ftype=""):
    ftype=ftype.replace(".","")
    from tkinter.filedialog import askopenfilename
    a=""
    while "."+ftype not in a:
        a=askopenfilename(defaultextension=ftype,filetypes=((ftype,"*."+ftype),("All files", "*.*")),title="Select product Image")
    return a

def fetchimage():
    img=fetchdirectory("jpg")
    imageholder.configure(text=img)

def addproduct(tabs=""):
    if "null" in categories:
        categories[categories.index("null")]="Add new Category"
    tab2=Frame(tabs,height=20)
    tabs.add(tab2,text="Add Product")
    tabs.select(tabs.index(tab2))

    Name=setentrybox(tab2,"Name","Insert Name",columnspan=3)[0]

    Price=setscrollbox(tab2,"Insert Price",80,1,1,1,0,3,wtype=2)[0]
    Price_text=Label(tab2,text="Price")
    Price_text.grid(row=1,column=0,pady=5,padx=5)

    Short=setscrollbox(tab2,"Insert Short description",80,1,2,1,0,3,wtype=2)[0]
    Short_text=Label(tab2,text="Short\ndescription")
    Short_text.grid(row=2,column=0,pady=5,padx=5)

    Desc=setscrollbox(tab2,"Insert Long description",80,5,3,1,0,3,wtype=2)[0]
    Desc_text=Label(tab2,text="Long\ndescription")
    Desc_text.grid(row=3,column=0,pady=5,padx=5)

    globals()["img"]=homedir+"\\Images\\not_available.jpg"
    img_text=Label(tab2,text="Image")
    img_text.grid(row=4,column=0,pady=5,padx=5)
    globals()["imageholder"]=Label(tab2,width=100,text=img)
    imageholder.grid(row=4,column=1,pady=5,padx=5)
    imageselect=Button(tab2,text="Select image",width=20,command=fetchimage)
    imageselect.grid(row=4,column=2,pady=5,padx=5)

    Cat_choice,Cat_text,Cat=dropdown(tab2,"Product\ncategory","Select Version",categories,5,0,1,W)

    savebutton=Button(tab2,text="Add Product",width=20,command=lambda:addnewproduct(tab2,Name,Price,Short,Desc,Cat_choice))
    quitbutton=Button(tab2,text="Quit without saving",width=20,command=lambda:tabs.forget(tabs.index(tab2)))
    Separator(tab2,orient=HORIZONTAL).grid(row=6,column=0,columnspan=10,pady=10,sticky=E+W)
    savebutton.grid(row=7,column=1,pady=10,padx=10)
    quitbutton.grid(row=7,column=0,pady=10,padx=10)

def addnewproduct(tab2,name,price,short,long,cat):
    from tkinter import messagebox
    name,price,short,cat,long,newcat,loaded=name.get(),price.get(1.0),short.get(1.0),cat.get(),long.get(1.0),"",True
    if name=="" or name=="Insert Name":
        messagebox.showerror("Error", "Product name not provided")
    elif price=="" or price==" " or price=="\n":
        messagebox.showerror("Error", "Product price not provided")
    elif short=="" or short==" " or short=="\n":
        messagebox.showerror("Error", "Product short description not provided")
    elif long=="" or long==" " or long=="\n":
        messagebox.showerror("Error", "Product description not provided")
    elif cat=="Select Version":
        messagebox.showerror("Error", "Product Category not provided")
    else:
        if cat=="Add new Category":
            while newcat=="":
                newcat=entrypopup("New Category","Category name:")
            categories.append(newcat)
        products.append([name,price,short,newcat,long,img,loaded])
        tabs.forget(tabs.index(tab2))
        updateentries()

def loadeditor():
    global isopen
    Editor=genwindow("Editor",resize=False)

    globals()["tabs"]=Notebook(Editor)
    tab1=Frame(tabs,height=20)
    tabs.add(tab1,text="Main window")
    tabs.grid(row=0,padx=5,pady=5)

    globals()["productLabel"] = Label(tab1,text="Products: "+str(len(products)),width=20)
    AddButton = Button(tab1,text="Add",width=20,command=lambda:addproduct(tabs))
    EditButton = Button(tab1,text="Edit",width=20,command=lambda:editproduct(tabs))
    DeleteButton = Button(tab1,text="Delete",width=20,command=lambda:deleteproduct(tabs))
    QuitButton = Button(tab1,text="Exit",width=20,command=lambda:Editor.destroy())

    productLabel.grid(row=1,column=0,sticky=W,padx=5,pady=5)
    AddButton.grid(row=3,column=0,padx=5,pady=5)
    EditButton.grid(row=4,column=0,padx=5,pady=5)
    DeleteButton.grid(row=5,column=0,padx=5,pady=5)
    QuitButton.grid(row=7,column=0,padx=5,pady=5)

    globals()["Entries"],scroll=setscrollbox(tab1,"",80,10,1,1,2,1,7,5,5,0)
    Entries.bind('<Double-1>', lambda x:EditButton.invoke())
    Entries.select_set(first=0)
    updateentries()

    Editor.mainloop()
    isopen=False

def load(main=""):
    #open github
    ptext.set("Opening GitHub")
    progress.step(1)
    sleep(2)
    os.startfile(Gitfolder+"\\GitHub Desktop")

    #fetch version history
    global ischecked
    ptext.set("Fetch the newest version of the wesbite")
    progress.step(1)
    b = Button(main,text="Continue?",command=flipchecked)
    b.pack(pady=10)
    while not ischecked:
        pass
    ischecked=False
    b.destroy()

    #open data
    ptext.set("Loading object data")
    progress.step(1)
    loadpages()
    sleep(2)

    #launch editor
    ptext.set("Launching editor")
    progress.step(1)
    globals()["isopen"]=True
    t2=threading.Thread(target=loadeditor,name="Editor")
    t2.start()
    while isopen:
        pass

    #save changes
    ptext.set("Saving changes")
    progress.step(1)
    savechanges()
    sleep(2)

    #open github
    ptext.set("Opening GitHub")
    progress.step(1)
    sleep(2)
    os.startfile(Gitfolder+"\\GitHub Desktop")

    #push changes
    ptext.set("Push the changes to GitHub")
    progress.step(1)
    b = Button(main,text="Continue?",command=flipchecked)
    b.pack(pady=10)
    while not ischecked:
        pass
    ischecked=False
    b.destroy()

    #close self
    ptext.set("Closing Program")
    progress.step(1)
    sleep(2)

    main.destroy()

start()
'''loadpages()
loadeditor()'''
