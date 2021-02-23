from docx import Document
from docx.shared import Inches
from docx.shared import Mm

class Docx:
    def export(self, content, destination):
        document = Document()
        section = document.sections[0]
        section.page_height = Mm(297)
        section.page_width = Mm(210)
        document.add_paragraph(content)
        document.save(destination)
