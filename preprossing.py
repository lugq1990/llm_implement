# used for NLP preprocessing that could be used for batch and new query
"""spacy pretrained model downlaod: 
python -m spacy download en_core_web_sm
"""
import spacy
import re
import os


class NLPProcessor:
    def __init__(self, model_name="en_core_web_sm"):
        self.nlp = spacy.load(model_name, disable=["parser", "ner"])
        
    def _remove_symbols(self, text):
         text = re.sub(r'[^\w]', ' ', text)
         text = re.sub(' +', ' ', text)
         return text

    def tokenize(self, text):
        doc = self.nlp(text)
        tokens = [token.text for token in doc]
        return tokens

    def remove_stopwords(self, tokens):
        doc = self.nlp(" ".join(tokens))
        filtered_tokens = [token.text for token in doc if not token.is_stop]
        return filtered_tokens

    def lemmatize(self, tokens):
        doc = self.nlp(" ".join(tokens))
        lemmas = [token.lemma_ for token in doc]
        return lemmas
    

    def preprocess_text(self, text):
        text = self._remove_symbols(text)
        tokens = self.tokenize(text)
        filtered_tokens = self.remove_stopwords(tokens)
        lemmas = self.lemmatize(filtered_tokens)
        preprocessed_text = " ".join(lemmas)
        return preprocessed_text


import PyPDF2

def extract_paragraphs_from_pdf(pdf_path):
    paragraphs = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        num_pages = pdf_reader.getNumPages()
        
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text = page.extractText()
            paragraphs.extend(text.split('\n\n'))
    
    # Filter out empty paragraphs
    paragraphs = [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]
    return paragraphs

# sample to use to extract paragraph from pdf
if __name__ == "__main__":
    pdf_file_path = "path_to_your_legal_contract.pdf"
    extracted_paragraphs = extract_paragraphs_from_pdf(pdf_file_path)
    for i, paragraph in enumerate(extracted_paragraphs, start=1):
        print(f"Paragraph {i}: {paragraph}")
        

class FileProcess:
    def __init__(self, txt_file_path) -> None:
        self.txt_file_path = txt_file_path
        
    def _list_txt_files(self):
        file_list = [x for x in os.listdir(self.txt_file_path) if x.endswith('.txt')]
        return file_list
    
    def _load_txt_file(self, file_name):
        # each file with each line will be a record.
        with open(os.path.join(self.txt_file_path, file_name), 'r', encoding='utf-8') as f:
            #data_list = f.readlines()
            data = f.read()
        # change the split logic with `\n\n` for paragpragh, noted -> this isn't as expected.
        data_list = data.split('\n')
        return data_list
    
    def _dump_processed_text(self, text_list, file_name):
        processed_txt_path = os.path.join(self.txt_file_path, 'mid_date')
        if not os.path.exists(processed_txt_path):
            os.makedirs(processed_txt_path, exist_ok=True)
        mid_file_path = os.path.join(processed_txt_path, file_name)
        with open(mid_file_path, 'w') as f:
            for text in text_list:
                f.write(text + '\n') 
     
    @staticmethod       
    def _filter_text(text, n_words=10):
        if len(text.split()) < n_words:
            return ''
        return text
        
    def process(self):
        # process each txt file and dump them into a processed folder.
        processor = NLPProcessor()
        file_list = self._list_txt_files()
        for file_name in file_list:
            data_list = self._load_txt_file(file_name=file_name)
            processed_list = [processor.preprocess_text(text) for text in data_list]
            processed_list = [self._filter_text(text) for text in processed_list]
            processed_list = [x for x in processed_list if x != '']
            self._dump_processed_text(processed_list, file_name=file_name)
            

if __name__ == '__main__':
    processing = NLPProcessor()
    text = "This is a sample sentence. It showcases NLP preprocessing techniques."
    print(processing.preprocess_text(text))

    txt_file_path = r'C:\Users\MLoong\Downloads\CUAD_v1\txt_files'
    file_process = FileProcess(txt_file_path).process()