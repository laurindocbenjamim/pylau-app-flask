# Importing the rewquired libraries

import os

import PyPDF2

class ExtractorFileContent(object):
    """
    This class is used to create speech by generating audio from an
    input text.

    In this class we are using the OpenAI API for speech
     
    """

    NUMBER_OF_PAGES = 0
    PAGES = None
    
    #
    def extract_from_pdf(self,file_path: str):
        """ 
        This metho is used to extract data from a PDF
        """

        if not file_path or '.pdf' not in file_path:
            return  False, "Invalid format"
        
        if not os.path.exists(file_path):
            return False, "File not found"
        
        try:
            pdf_file = open(file_path, 'rb')

            pdf_reader = PyPDF2.PdfReader(pdf_file)

            number_of_pages = len(pdf_reader.pages)

            self.NUMBER_OF_PAGES = number_of_pages
            self.PAGES = pdf_reader

            return True, number_of_pages
        
        except Exception as e:
            False, str(e)

    #
    def read_page_content(self, page_number: int = 0):
        """
        
        """
        if page_number !=0 and not isinstance(page_number, int):
            return False, "Invalid value for [page_number]"
        try:
            page = self.PAGES.pages[page_number]
            text = page.extract_text()           
            return True,text
        except AttributeError as e:
            False, str(e)
        except IndexError as e:
            return False, "Page number not found"
    

    