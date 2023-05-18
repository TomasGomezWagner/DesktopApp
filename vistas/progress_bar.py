import os
import customtkinter
import glob
from tkinter import ttk
from generales.settings import MENSAJES
from generales.alertas import Alerts
from dppsv.pdf_datos import PdfData
from dppsv.funciones_principales import igual_o_diferente
from dppsv.get_info import Datos 


class TopLevelProgressBar(customtkinter.CTk):
    def __init__(self, rc, pdfs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rc             = rc
        self.pdfs           = pdfs
        self.algun_pdf_mal  = False
        self.datos          = Datos() 

        self.pb = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            length=280,
            maximum=self.get_maximum(),
        )
        self.pb.pack(padx=20, pady=20)
        
        self.value_label = customtkinter.CTkLabel(self, text=self.update_progress_label())
        self.value_label.pack()
        
        self.progress()


    def update_progress_label(self,):
        return f"Procesado: {self.pb['value']} de {int(self.get_maximum())}"


    def progress(self,) -> None: 
        """
        Funcion principal de la vista. Cuando ejecuta get_pdf_data se va actualizando la\n
        barra de progreso mientras se leen los datos de los pdf. Cuando termina lanza la \n
        alerta con la info correspondiente a lo generado.
        """ 
        tipo_proceso    = igual_o_diferente(self.rc, self.pdfs)
        datos_para_txt  = self.get_pdf_data()
        
        self.datos.generar_archivo_de_salida(self.rc, datos_para_txt)
        self.datos.renombrar_archivos_txt(self.rc, tipo_proceso)
        self.datos.pasar_a_carpeta_temp(self.rc)
        self.destroy()
        
        if self.algun_pdf_mal:
            Alerts.informacion_dppsv(
                MENSAJES[tipo_proceso] + MENSAJES['pdf_con_errores'],
                self.rc
            )
        else:
            Alerts.informacion_dppsv(MENSAJES[tipo_proceso], self.rc)
            

    def get_maximum(self,) -> float:
        """Obtiene la cantidad total de los pdf a modificar para utilizar en la barra de progreso"""
        
        cantidad_total = 0
        carpeta = glob.glob(os.path.join(self.pdfs, '*.pdf')) 

        for pdf in carpeta:
            cantidad_total += 1
        return float(cantidad_total)
    

    def get_pdf_data(self,) ->list:
        """
        Crea un objeto PdfData que devuelve una lista con los datos del pdf leido.\n
        Los datos pueden estar completos o no, luego en la alerta se informara si hubo 
        alguno con error.\n
        Al terminar de procesar el pdf aumenta la barra de progreso.
        """
        datos = []
        archivos = glob.glob(os.path.join(self.pdfs,'*.pdf'))

        for pdf in archivos:
            if self.pb['value'] < self.get_maximum():
                data = PdfData(pdf)
                datos.append(data.data)
                self.update()
                self.pb['value'] += 1
                self.value_label.configure(text=self.update_progress_label())
                if not data.is_good:
                    self.algun_pdf_mal = True

        return datos
    

if __name__ == '__main__':
    asd = TopLevelProgressBar(r'C:\Users\hcapra\Desktop\arreglo_csv\archivos_fuente\devolucion_dppsv\1000015845')
    asd.mainloop()
    