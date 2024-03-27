from GestureController import GestureController
import tkinter as tk 
from PIL import ImageTk, Image



def runvirtualmouse(): 
	gc1 = GestureController() 
	gc1.start() 
root = tk.Tk() 
root.geometry("300x300") 
label = tk.Label(root, text="Welcome to Virtual Mouse", fg="brown",font='TkDefaultFont 16 bold') 
label.grid(row=0, columnspan=5, pady=10, padx=10) 
image = ImageTk.PhotoImage(Image.open("tap.png")) 
img_label = tk.Label(image=image , width=100, height=100, borderwidth=3, relief="solid") 
img_label.grid(row=1, columnspan=5, pady=10, padx=10) 
start_button = tk.Button(root,text=" Track Mouse",fg="white", bg='green', font='Helvetica 12 bold italic ',command= runvirtualmouse , height="4", width="16",activebackground='lightblue') 
start_button.grid(row=3,column=2, pady=10, padx=20) 
root.mainloop() 
label.geometery("400X300") 
root.geometery(row =0,columnspan=5, pady= 10,padx=10) 
root.mainloop()


