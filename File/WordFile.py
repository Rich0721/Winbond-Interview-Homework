
import shutil
import subprocess
from PyPDF2 import PdfReader

from constants import LIBREOFFICE_PATH, TMP_FOLDER

from .File import File
import os


class WordFile(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__doc_to_pdf()

    @property
    def pages(self) -> int:
        return self.attributes.get("pages")

    @pages.setter
    def pages(self, value:int):
        self.attributes["pages"] = value

    def __doc_to_pdf(self):
        doc_path = self.attributes.get("full_path")

        if not os.path.exists(TMP_FOLDER):
            os.makedirs(TMP_FOLDER)

        try:
            
            subprocess.run([
                LIBREOFFICE_PATH,
                "--headless",
                "--convert-to", "pdf",
                doc_path.replace("/", "\\"),
                "--outdir", TMP_FOLDER
            ], check=True)

            base = os.path.splitext(os.path.basename(doc_path))[0]
            pdf_file = os.path.join(TMP_FOLDER, base + ".pdf")
            self.__set_page_count(pdf_file)

        finally:
            # 轉換完成後刪除暫存資料夾
            shutil.rmtree(TMP_FOLDER, ignore_errors=True)


    def __set_page_count(self, pdf_file: str) -> int:
        reader = PdfReader(pdf_file)
        self.pages = len(reader.pages)
    
    def to_string(self, size: str) -> str:
        return f"{self.name}{self.extension} [Word檔] (頁數: {self.pages}, 大小: {size})"
    
    def to_xml(self, size: str) -> str:
        return f"<{self.name}_{self.extension[1:]}> 頁數:{self.pages}, 大小:{size} </{self.name}_{self.extension[1:]}>"