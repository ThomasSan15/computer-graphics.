import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def abrir_imagen():
    ruta = filedialog.askopenfilename(
        
        title= "Seleccione una imagen",
        filetypes= [("Imagenes", "*.png;*.jpg;*jpeg")]
    )
    
    if not ruta:
        return
    
    
    img = Image.open(ruta)
    img_res = img.resize((400,400))
    
    img = ImageTk.PhotoImage(img_res)
    
    lbl.config(image=img)
    lbl.image(img)

root = tk.Tk()

root.title("Visualizador de imagenes")
root.geometry("700x500")
res_img = root.resizable(False,False)
boton = tk.Button(root, text= "Abrir imagen",command=abrir_imagen)
boton.place(x=10,y=10)

lbl = tk.Label(root)
lbl.place(x=40,y=40)
root.mainloop()