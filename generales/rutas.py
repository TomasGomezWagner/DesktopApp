from tkinter import filedialog

def examinar(textvariable):
    resultado = filedialog.askopenfilename()
    print(resultado)
    return textvariable.set(resultado)
    

def examinar_carpeta(textvariable):
    resultado = filedialog.askdirectory()
    print(resultado)
    return textvariable.set(resultado)

