import os
import fitz

class PdfData:

    def __init__(self, pdf) -> None:
        self.pdf = pdf
        self.is_good = self.is_good_pdf()
        
        if self.is_good_pdf():
            self.data = self.get_pdf_data()
        else:
            self.data = self.get_pdf_data_incomplete()


    def buscar_mes(self, mes:str) -> str:
        meses = {
            'ene': '01',
            'feb': '02',
            'mar': '03',
            'abr': '04',
            'may' : '05',
            'jun' : '06',
            'jul' : '07',
            'ago' : '08',
            'sep': '09',
            'oct' : '10',
            'nov' : '11',
            'dic' : '12',
            }

        if mes in meses:
            return(meses[mes])
        
    def get_pdf_name(self,):
        padre, archivo = os.path.split(self.pdf)
        return archivo
        

    def formatear_fecha(self, fecha:str):
        
        nueva_fecha = []
        for item in fecha:
            if not item == '':
                nueva_fecha.append(item)
        nueva_fecha[1] = self.buscar_mes(nueva_fecha[1])

        return f'{nueva_fecha[0]}-{nueva_fecha[1]}-{nueva_fecha[2]}'
    

    def get_pdf_data(self,):

        try:
            doc = fitz.Document(self.pdf)
            page = doc[0]

            text = page.get_textpage('text')

            full_dict = text.extractDICT()
            
            for item in full_dict['blocks']:
                for line in item['lines']:
                    for span in line['spans']:
                        
                        if span['origin'] == (309.0, 591.5):     #cantidad UF
                            cantidad_uf = span['text'].split(' ')[-1]
                            
                        
                        if span['origin'] == (462.82000732421875, 591.5):     #valor UF
                            valor_uf = span['text'].split(' ')[-1].replace('$', '')
                            
                             
                        if span['origin'] == (82.31800079345703, 951.1799926757812): #fecha emision
                            fecha_emision = span['text'].split('-')
                            fecha_emision = self.formatear_fecha(fecha_emision) 
                            
                        
                        if span['origin'] == (127.0, 970.5399780273438):    #vto
                            fecha_vencimiento = span['text'].replace('/', '-')
                            


            pdf_data = [
                self.get_pdf_name(),
                valor_uf,
                cantidad_uf,
                str(float(valor_uf)*float(cantidad_uf)),
                str(float(cantidad_uf)/2),
                str(float(cantidad_uf)/2*float(valor_uf)),
                fecha_emision,
                fecha_vencimiento,
            ]
        
            return pdf_data
        
        except:
            return [self.get_pdf_name(), '0', '0', '0', '0', '0', '', '']
    
        
    
    def get_pdf_data_incomplete(self,):
        return [self.get_pdf_name(), '0', '0', '0', '0', '0', '', '']


    def is_good_pdf(self,):

        try:
            fitz.Document(self.pdf)
            return True
        except:
            return False















if __name__ == '__main__':

    pdf = r'C:\Users\hcapra\Desktop\1000015648\02-029-00191821-3-00_029018895583_27597039.pdf'
    #pdf = r'C:\Users\hcapra\Desktop\arreglo_csv\archivos_fuente\devolucion_dppsv\1000015845\02-148-00023781-3-00_148019630267_RN16419925.pdf'
    data = PdfData(pdf)
    print(data.data)

    # import glob
    #pdf = r'E:\148-EXALTACION DE LA CRUZ RN (148)\1000015845\02-148-00025118-1-00_148019629931_RN15918139.pdf'
    # pdf = r'C:\Users\hcapra\Desktop\arreglo_csv\archivos_fuente\devolucion_dppsv\1000015845\02-148-00023781-3-00_148019630267_RN16419925.pdf'
    # doc = fitz.Document(pdf)
    # page = doc[0]

    # text = page.get_textpage('text')

    # full_dict = text.extractDICT()
    # print(full_dict)
    # data = PdfData(pdf)
    # print(data.data)
    # carpeta = glob.glob(os.path.join(r'C:\Users\hcapra\Desktop\arreglo_csv\archivos_fuente\devolucion_dppsv\1000015845', '*.pdf')) 
    # i=0
    # data_lista = []
    # for item in carpeta:
    #     if i == 3:
    #         break

    #     print(item)
    #     data = PdfData(item)
    #     print(data.data)
    #     data_lista.append(data.data)
        

    #     #i += 1

    # print(data_lista)

        


