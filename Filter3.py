from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
import glob
import os
import random

root = Tk()
root.title("ANIME FILTER by Suyash")
root.geometry('600x550+250+100')


wallpaper = PhotoImage(file="animes\\extra\\wall.png")

w = wallpaper.width()
h = wallpaper.height()

cv = Canvas(width=w, height=h)
cv.pack(side='top', fill='both', expand='yes')
cv.create_image(0, 0, image=wallpaper, anchor='nw')

head = Label(cv,text="Anime Filter",fg="white",bg="red",font=('comic sans',30))
head.place(x=200,y=10)

display = Label(cv,relief=GROOVE,bd=10)
display.place(x=60,y=70)



cap = cv2.VideoCapture(0)


def stops():
	global shuffle 
	global imga 
	global frame
	global aa
	shuffle = False
	aa = random.choice(animeList)
	imga = cv2.imread(aa)
	
def reseter():
	global shuffle
	shuffle = True

button = PhotoImage(file="animes\\extra\\btn.png")
stop = Button(cv,text="STOP",image=button,fg="white",command=stops,compound=CENTER,font=('Ninja naruto',20),relief=FLAT,bg='green')
stop.place(x=150,y=450)

reset = Button(cv,text="reset",image=button,fg="white",command=reseter,compound=CENTER,font=('Ninja naruto',20),relief=FLAT,bg='green')
reset.place(x=350,y=450)

shuffle = True


### Anime List
animeList= glob.glob(os.path.join("animes\\*.png"))

# Black Background
blk = cv2.imread("animes\\extra\\black.png")

imga = cv2.imread("animes\\extra\\menu.png")


# Create the haar cascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# function for video streaming
def video_stream():
	global shuffle 
	global imga

	global aa
	if shuffle == True:
		a = random.choice(animeList)
		imga = cv2.imread(a)
	

	img = imga

	_, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	

	# Detect faces in the image
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
		#flags = cv2.CV_HAAR_SCALE_IMAGE
	)

	

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		#cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
				
		
		Boardwidth = w+20
		Boardheight = Boardwidth*0.56
		
				
				
		animeBoard = cv2.resize(img,(int(Boardwidth),int(Boardheight)))
		bg =cv2.resize(blk,(int(Boardwidth),int(Boardheight)))

		animeb = cv2.add(animeBoard,bg)                        
		imgX=x
		imgY=y-150
		try:
			frame[ imgY:imgY+int(Boardheight) , imgX:imgX+int(Boardwidth) ] = animeb
		except:
			pass


		if shuffle == False:
			cv2.putText(frame,f"{(os.path.basename(aa).replace('.png',''))}",(x,y+10),cv2.FONT_HERSHEY_SIMPLEX ,1,(0, 0, 255),3)




	framereal = cv2.resize(frame,(480,350))
		
	aimg = cv2.cvtColor(framereal,cv2.COLOR_BGR2RGB)
	img = Image.fromarray(aimg)
	imgtk = ImageTk.PhotoImage(img)

	display.imgtk = imgtk
	display.config(image=imgtk)
	display.after(1, video_stream) 

	


	
		

video_stream()

root.mainloop()
