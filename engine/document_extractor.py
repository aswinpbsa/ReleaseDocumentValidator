import zipfile
import xml.etree.ElementTree as ET


class DocumentExtractor:

    def extract(self, filepath):

        with zipfile.ZipFile(filepath, "r") as doc:

            xml = doc.read("word/document.xml")

            images = [
                file
                for file in doc.namelist()
                if file.startswith("word/media/")
            ]

        root = ET.fromstring(xml)

        namespace = {
            "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        }

        paragraphs = []

        for p in root.findall(".//w:p", namespace):

            text = ""

            for t in p.findall(".//w:t", namespace):

                if t.text:
                    text += t.text

            if text.strip():
                paragraphs.append(text.strip())

        # Read all tables
        tables = []

        for tbl in root.findall(".//w:tbl", namespace):

            table = []

            for row in tbl.findall(".//w:tr", namespace):

                cells = []

                for cell in row.findall("./w:tc", namespace):

                    value = ""

                    for t in cell.findall(".//w:t", namespace):

                        if t.text:
                            value += t.text

                    cells.append(value.strip())

                if cells:
                    table.append(cells)

            if table:
                tables.append(table)

        return {

            "paragraphs": paragraphs,

            "tables": tables,

            "imageCount": len(images)

        }