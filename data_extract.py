"""extract pdf file content into a new text files that will be stored in a new folder"""
import PyPDF2 as pdf
import os


source_pdf_path = r'C:\Users\MLoong\Downloads\CUAD_v1\full_contract_pdf\Part_I\Service'
dest_path = r'C:\Users\MLoong\Downloads\CUAD_v1\txt_files'


class PDFExtract:
    def __init__(self, pdf_file_path, txt_file_path=None) -> None:
        self.pdf_file_path = pdf_file_path
        self.txt_file_path = txt_file_path if txt_file_path else dest_path
        if not os.path.exists(self.txt_file_path):
            os.makedirs(self.txt_file_path, exist_ok=True)
        
    def _get_pdf_file_list(self):
        files = [x for x in os.listdir(self.pdf_file_path) if x.endswith('.pdf')]
        return files
    
    def _extract_one_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as f:
            reader = pdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def _dump_text_to_local(self, text, file_name):
        if file_name.endswith('.pdf'):
            file_name = file_name.split('.')[0] + '.txt'
        dest_txt_path = os.path.join(self.txt_file_path, file_name)
        with open(dest_txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def extract_files(self):
        files = self._get_pdf_file_list()
        for file_name in files:
            print("start to process file: {}".format(file_name))
            file_path = os.path.join(self.pdf_file_path, file_name)
            text = self._extract_one_pdf(file_path=file_path)
            self._dump_text_to_local(text, file_name=file_name)
        
        

if __name__ == "__main__":
    pdf_extraxt = PDFExtract(source_pdf_path)
    pdf_extraxt.extract_files()
    
        
