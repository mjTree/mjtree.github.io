# coding:utf-8
# time: 2023/9/11 3:19 下午
import fitz
from fitz.fitz import Document as MupdfDocument

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextBoxHorizontal
from document_structure import Page, Character, TextRange, Element, Document


class PdfParse:

    def __init__(self, parse_pdf_path):
        self.parse_pdf_path = parse_pdf_path

    def gen_document_by_pdfminer(self):
        page_list = []
        for page_idx, lt_page in enumerate(extract_pages(self.parse_pdf_path)):
            element_list = []
            for lt_text_box in lt_page._objs:
                if not isinstance(lt_text_box, LTTextBoxHorizontal):
                    continue
                for lt_text_line in lt_text_box._objs:
                    text_range_chars = []
                    for lt_char in lt_text_line._objs:
                        if not isinstance(lt_char, LTChar):
                            continue
                        # 过滤pdf可视界面外的字符
                        if lt_char.x0 >= 0 and lt_char.y0 >= 0 and lt_char.width > 0 and lt_char.height > 0:
                            text_range_chars.append(Character(
                                round(lt_char.x0, 2),
                                round(lt_page.height - lt_char.y0 - lt_char.height, 2),
                                round(lt_char.width, 2),
                                round(lt_char.height, 2),
                                page_idx + 1,
                                lt_char._text,
                                lt_char.fontname,
                            ))
                    if text_range_chars:
                        text_range = TextRange(text_range_chars)
                        element_list.append(Element([text_range], element_type='paragraph'))
            page_list.append(Page(lt_page.width, lt_page.height, page_idx + 1, element_list))
        return Document(page_list)

    def gen_document_by_pymupdf(self):
        page_list = []
        mupdf_document = MupdfDocument(self.parse_pdf_path)
        for mupdf_page in mupdf_document:
            element_list = []
            # TODO: 待实现
            page = Page(mupdf_page.rect.width, mupdf_page.rect.height, mupdf_page.number, element_list)
            page_list.append(page)
        return Document(page_list)


if __name__ == '__main__':
    input_path = '/Users/mjtree/PycharmProjects/dg_document/tests/test_data/pdf/merged_table.pdf'
    pdf_parse: PdfParse = PdfParse(input_path)
    document_1 = pdf_parse.gen_document_by_pdfminer()
    # document_2 = pdf_parse.gen_document_by_pymupdf()
    print()
