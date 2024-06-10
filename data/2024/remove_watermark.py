import shutil
from math import cos, pi, atan

from PyPDF2 import PdfFileWriter
from PyPDF2.generic import NameObject
from PyPDF2.pdf import ContentStream, PdfFileReader
from PyPDF2.utils import b_


def pdf_remove_watermark(pdf_path, output_path):
    reader = PdfFileReader(pdf_path)
    writer = PdfFileWriter()
    is_modified = False
    for i, page in enumerate(reader.pages):
        content = _build_content_stream(page.get("/Contents"), reader, i)
        if content is None:
            page.compressContentStreams()
            writer.addPage(page)
            continue
        operations = _remove_marked_content_watermark(content.operations)
        operations = _remove_do_type_watermark(operations)
        operations = _remove_rotate_text_watermark(operations)
        if len(operations) != len(content.operations):
            is_modified = True
            content.operations = operations
            page.__setitem__(NameObject("/Contents"), content)
        page.compressContentStreams()
        writer.addPage(page)
    if is_modified:
        with open(output_path, "wb") as fh:
            writer.write(fh)
    else:
        try:
            shutil.copyfile(pdf_path, output_path)
        except shutil.SameFileError:
            pass


def _build_content_stream(contents_ref, pdf_reader, page_index):
    content = None
    try:
        content = ContentStream(contents_ref.getObject(), pdf_reader)
    except Exception as e:
        print('pass invalid page {}: {}'.format(page_index, e))
    return content


def _remove_marked_content_watermark(operations):
    new_operations = []
    i, last_end_index = 0, 0
    while i < len(operations):
        origin_i = i
        start_index, end_index = _search_marked_content_element(operations, i)
        if end_index < 0:
            break
        if start_index < 0:
            new_operations.extend(operations[last_end_index:end_index])
            last_end_index = i = end_index
        if 0 <= start_index < end_index:
            last_end_index = i = end_index + 1
        i = max(i, origin_i + 1)
    new_operations.extend(operations[last_end_index:])
    return new_operations


def _remove_rotate_text_watermark(operations):
    new_operations = []
    last_end_index = 0
    min_cos, max_cos = cos(60 / 180 * pi), cos(30 / 180 * pi)
    i = 0
    while i < len(operations):
        operands, operator = operations[i]
        origin_i = i
        if operator == b_("Tm") and min_cos < _get_rotation_cos(operands) < max_cos:
            for j in range(i + 1, len(operations)):
                next_operands, next_operator = operations[j]
                if next_operator in {b_("Tj"), b_("TJ")}:
                    new_operations.extend(operations[last_end_index:j])
                    last_end_index = j + 1
                elif next_operator in {b_("Tm"), b_("ET")}:
                    i = j
                    break
        i = max(i, origin_i + 1)
    new_operations.extend(operations[last_end_index:])
    return new_operations


def _remove_do_type_watermark(operations):
    new_operations = []
    last_end_index = 0
    i = 0
    while i < len(operations):
        operands, operator = operations[i]
        origin_i = i
        if operator == b_("Do"):
            start_index, end_index = _search_single_do_element(operations, i)
            if end_index <= start_index:
                start_index, end_index = _search_rotate_do_element(operations, i)
            if end_index > start_index:
                new_operations.extend(operations[last_end_index: start_index])
                last_end_index = end_index
                i = end_index
        i = max(i, origin_i + 1)
    new_operations.extend(operations[last_end_index:])
    return new_operations


def _search_marked_content_element(operations, index):
    start_index, end_index = index, index
    operator = operations[start_index][1]
    while operator != b_("BDC"):
        start_index -= 1
        operator = operations[start_index][1] if start_index >= 0 else b_("BDC")
    operator = operations[end_index][1]
    while operator != b_("EMC"):
        if operator == b_("BDC") and start_index < 0:
            break
        end_index += 1
        operator = operations[end_index][1] if end_index < len(operations) else b_("EMC")
    if 0 <= start_index and end_index < len(operations):
        operands, operator = operations[start_index]
        if operator == b_("BDC") and len(operands) >= 2 and isinstance(operands[1], dict) \
                and operands[1].get('/Subtype') == '/Watermark':
            return start_index, end_index
    if start_index < 0 and end_index < len(operations):
        return -1, end_index
    if end_index >= len(operations):
        return start_index, -1
    return -1, -1


def _search_single_do_element(operations, index):
    if 0 < index < len(operations) - 1:
        prev_operation, next_operation = operations[index - 1], operations[index + 1]
        prev_operator, next_operator = prev_operation[1], next_operation[1]
        if prev_operator == b_("q") and next_operator == b_("Q"):
            return index - 1, index + 2
    return 0, 0


def _search_rotate_do_element(operations, index):
    start_index, end_index = index, index
    operator = operations[start_index][1]
    while operator != b_("q"):
        start_index -= 1
        operator = operations[start_index][1] if start_index >= 0 else b_("q")
    operator = operations[end_index][1]
    while operator != b_("Q"):
        end_index += 1
        operator = operations[end_index][1] if end_index < len(operations) else b_("Q")
    if start_index < 0 or end_index >= len(operations):
        return 0, 0
    min_cos, max_cos = cos(60 / 180 * pi), cos(30 / 180 * pi)
    for i in range(index - 1, start_index, -1):
        operands, operator = operations[i]
        if operator == b_("cm"):
            _cos = _get_rotation_cos(operands)
            if min_cos < _cos < max_cos:
                return start_index, end_index + 1
            else:
                break
    return 0, 0


def _get_rotation_cos(operands):
    if len(operands) != 6:
        return 1.0
    if operands[1] == 0 and operands[2] == 0:
        return 1.0
    if operands[0] == 0 and operands[3] == 0:
        return 0.0
    if operands[1] != 0 and operands[3] != 0:
        return cos(atan(operands[1] / operands[3]))
    return 1.0
