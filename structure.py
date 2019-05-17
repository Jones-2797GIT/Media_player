import os
import tkinter.messagebox
from tkinter import filedialog
from tkinter import *
from mutagen.mp3 import MP3
from pygame import mixer
from tkinter import ttk
from ttkthemes import themed_tk as tk
import threading
import time


def browse_file():
    global filePath,paused
    filePath=filedialog.askopenfilename()
    paused=FALSE
    add_to_playlist(filePath)

filelist=[]
def add_to_playlist(fileName):
    fileName=os.path.basename(fileName)
    playlistbox.insert(0, fileName)
    filelist.insert(0,filePath)

def about_us():
    tkinter.messagebox.showinfo("Melody Media Player","This is a project.")

def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused=FALSE

    else:
        try:
            stop_music()
            time.sleep(1)
            selectedSong=playlistbox.curselection()
            selectedSong=int(selectedSong[0])
            playSong=filelist[selectedSong]
            mixer.music.load(playSong)
            mixer.music.play()
            mixer.music.set_volume(0.45)
            statusbar['text'] = "Playing music - " + os.path.basename(playSong)
            show_details(playSong)
        except:
            tkinter.messagebox.showerror("File not found", "Please check the file again. No file uploaded.")

def stop_music():
    global paused
    mixer.music.stop()
    paused=False
    statusbar['text']="Music Stopped"

paused=FALSE
def pause_music():
    global paused
    paused=True
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def set_vol(val):
    if 0==float(val):
        mixer.music.set_volume(float(val) / 100)
        volumeBtn.config(image=mutePhoto)
    elif float(val)<=40:
        mixer.music.set_volume(float(val) / 100)
        volumeBtn.config(image=volume1Photo)
    elif float(val)<=80:
        mixer.music.set_volume(float(val) / 100)
        volumeBtn.config(image=volume2Photo)
    else:
        mixer.music.set_volume(float(val) / 100)
        volumeBtn.config(image=volume3Photo)

def rewind_music():
    stop_music()
    time.sleep(1)
    mixer.music.play()

volume = FALSE
def volume_music():
    global  volume
    if volume:
        mixer.music.set_volume(0.45)
        volumeBtn.config(image=volume1Photo)
        scale.set(45)
        volume=FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.config(image=mutePhoto)
        scale.set(0)
        volume=True

def show_details(playSong):
    fileLabel['text'] = "Playing - " + os.path.basename(playSong)
    a=os.path.splitext(playSong)
    if a[1]=='.mp3':
        audio=MP3(playSong)
        total_length=audio.info.length
    else:
        a=mixer.Sound(playSong)
        total_length=a.get_length()
    mins,secs=divmod(total_length,60)
    dur="{:02d}:{:02d}".format(round(mins),round(secs))
    durationLabel['text'] = "Total Duration : " + dur
    t=threading.Thread(target=running_status,args=(total_length,))
    t.start()

def running_status(current_time):
    global paused
    while current_time and mixer.music.get_busy():
        if paused : continue
        mins, secs = divmod(current_time, 60)
        dur = "{:02d}:{:02d}".format(round(mins), round(secs))
        timeLabel['text'] = "Running Time : " + dur
        time.sleep(1)
        current_time-=1

def on_closing():
    stop_music()
    root.destroy()

def remove_file():
    selectedSong = playlistbox.curselection()
    selectedSong = int(selectedSong[0])
    playlistbox.delete(selectedSong)
    filelist.pop(selectedSong)



root = tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')

menu=Menu(root)

root.config(menu=menu)

fileMenu= Menu(menu,tearoff=0)
menu.add_cascade(label="File",menu=fileMenu)
fileMenu.add_command(label="Open",command=browse_file)
fileMenu.add_command(label="Exit",command=root.destroy)

helpMenu=Menu(menu,tearoff=0)
menu.add_cascade(label="Help",menu=helpMenu)
helpMenu.add_command(label="About Us",command=about_us)

mixer.init()

root.title("Melody")
root.iconbitmap(r"images/Melody.ico")

statusbar=ttk.Label(root,text='Welcome to Melody Music Player',relief=SUNKEN,anchor=W)
statusbar.pack(side=BOTTOM,fill=X)

leftFrame=Frame(root)
leftFrame.pack(side=LEFT)


playlistbox=Listbox(leftFrame)
playlistbox.pack()

addSongbtn=ttk.Button(leftFrame,text="ADD",command=browse_file)
addSongbtn.pack(side=LEFT)

delSongbtn=ttk.Button(leftFrame,text="REMOVE",command=remove_file)
delSongbtn.pack()

rightFrame=Frame(root)
rightFrame.pack(side=LEFT)

topFrame=Frame(rightFrame)
topFrame.pack()

fileLabel = ttk.Label(topFrame, text="Lets make some noise!!!!")
fileLabel.pack(pady=10)

durationLabel= ttk.Label(topFrame, text="Total Duration : --:--")
durationLabel.pack()

timeLabel= ttk.Label(topFrame, text="Running Time : --:--")
timeLabel.pack()

middleFrame=ttk.Frame(rightFrame)
middleFrame.pack()

playPhoto = PhotoImage(file="images/play-button.png")
playBtn = ttk.Button(middleFrame, image=playPhoto, command=play_music)
playBtn.grid(row=0,column=0,padx=10)

stopPhoto = PhotoImage(file="images/stop.png")
stopBtn = ttk.Button(middleFrame, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0,column=1,padx=10)

pausePhoto = PhotoImage(file="images/pause.png")
pauseBtn = ttk.Button(middleFrame, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0,column=2,padx=10)

bottomFrame=Frame(rightFrame)
bottomFrame.pack()

rewindPhoto = PhotoImage(file="images/rewind1.png")
rewindBtn = ttk.Button(bottomFrame, image=rewindPhoto, command=play_music)
rewindBtn.grid(row=0,column=0)

volume1Photo = PhotoImage(file="images/volume1.png")
volume2Photo = PhotoImage(file="images/volume2.png")
volume3Photo = PhotoImage(file="images/volume3.png")
mutePhoto = PhotoImage(file="images/mute.png")
volumeBtn = ttk.Button(bottomFrame, image=volume3Photo, command=volume_music)
volumeBtn.grid(row=0,column=1)

scale=ttk.Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(45)
scale.grid(row=0, column=2,padx=10)

root.protocol("WM_DELETE_WINDOW",on_closing)

root.mainloop()