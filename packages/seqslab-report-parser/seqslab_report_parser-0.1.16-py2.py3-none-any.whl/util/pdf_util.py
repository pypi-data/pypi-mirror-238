from typing import Dict, List, Tuple

import fitz


TOLERANCE = 5


def find_first(doc: fitz.Document, word: str) -> (fitz.Page, List):
    (begin, end) = doc.last_location
    for i in range(begin, end + 1):
        page = doc.load_page(i)
        search = page.search_for(word)
        if search:
            return page, search

    return None, None


def find_table_location_list(doc: fitz.Document, upper: str, lower: str, start=0) -> List[Tuple[fitz.Page, fitz.IRect, fitz.IRect]]:
    result = []
    (_, end) = doc.last_location
    for i in range(start, end + 1):
        page = doc.load_page(i)
        search1 = page.search_for(upper)
        search2 = page.search_for(lower)
        if len(search1) > 0 and len(search1) == len(search2):
            result += list(map(lambda r: (page, r[0].irect, r[1].irect), zip(search1, search2)))

    return result


def find_table_location(doc: fitz.Document, upper: str, lower: str, start=0) -> (fitz.Page, fitz.Rect, fitz.Rect):
    (begin, end) = doc.last_location
    for i in range(start, end + 1):
        page = doc.load_page(i)
        search1 = page.search_for(upper)
        search2 = page.search_for(lower)
        if len(search1) > 0:
            top = search1[-1]
        else:
            top = None

        if len(search2) > 0:
            bottom = search2[-1]
        else:
            bottom = None

        if top and bottom:
            return page, top, bottom

    return -1, None, None


def get_single_cell(page: fitz.Page, bbox: (float, float, float, float)) -> List[List[List[str]]]:
    """Returns the parsed table of a page in a PDF / (open) XPS / EPUB document.
    Parameters:
    page: fitz.Page object
    bbox: containing rectangle, List of numbers [xmin, ymin, xmax, ymax]
    Returns single cell
    """

    tab_rect = fitz.Rect(bbox).irect

    if tab_rect.is_empty or tab_rect.is_infinite:
        print('Warning: incorrect rectangle coordinates!')
        return []

    words = page.get_text('words')

    if not words:
        print('Warning: page contains no text')
        return []

    result = []
    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir in tab_rect:
            result.append(w[4])

    return [[result]]


def get_particular_drawing_rect(page: fitz.Page, bbox: (float, float, float, float), func) -> List[fitz.Rect]:
    tab_rect = fitz.Rect(bbox).irect

    if tab_rect.is_empty or tab_rect.is_infinite:
        print('Warning: incorrect rectangle coordinates!')
        return []

    drawings = page.get_drawings()

    if not drawings:
        print('Warning: page contains no drawing')
        return []

    result = []
    for d in drawings:
        ir = d['rect'].irect
        if ir in tab_rect and func(d):
            result.append(d['rect'])

    return result


def parse_table_by_cell(
    page: fitz.Page,
    bbox: (float, float, float, float),
    header_rows: int = 1
) -> List[List[List[str]]]:
    """Returns the parsed table of a page in a PDF / (open) XPS / EPUB document.
    Parameters:
    page: fitz.Page object
    bbox: containing rectangle, List of numbers [xmin, ymin, xmax, ymax]
    Returns the parsed table as a List of Lists of strings.
    The number of rows is determined automatically
    from parsing the specified rectangle.
    """

    tab_rect = fitz.Rect(bbox).irect

    if tab_rect.is_empty or tab_rect.is_infinite:
        print('Warning: incorrect rectangle coordinates!')
        return []

    words = page.get_text('words')

    if not words:
        print('Warning: page contains no text')
        return []

    drawings = page.get_drawings()
    cells = get_tab_cell(drawings, tab_rect, header_rows)

    cell2word = []
    for row in cells:
        d = {r: [] for r in row}
        cell2word.append(d)

    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir in tab_rect:
            for row in cell2word:
                for k, v in row.items():
                    if is_in_cell(ir, k):
                        # row[k].append([ir.x0, ir.y0, ir.x1, ir.y1, w[4]])
                        row[k].append(w[4])

    table = []
    for row in cell2word:
        table.append(list(row.values()))
    for row in table:
        for column in row:
            sentence = ' '.join(column).lower()
            if sentence == 'not detected' \
                    or sentence == 'nd' \
                    or sentence == 'not' \
                    or sentence == 'no fusion gene' \
                    or 'not pass' in sentence:
                return []

    return table


def parse_table_by_header(
    page: fitz.Page,
    bbox: (float, float, float, float),
    headers: List[fitz.IRect],
    header_rows: int = 1,
    additional_words=None
) -> List[List[List[str]]]:
    """Returns the parsed table of a page in a PDF / (open) XPS / EPUB document.
    Parameters:
    page: fitz.Page object
    bbox: containing rectangle, List of numbers [xmin, ymin, xmax, ymax]
    Returns the parsed table as a List of Lists of strings.
    The number of rows is determined automatically
    from parsing the specified rectangle.
    """

    if additional_words is None:
        additional_words = []
    tab_rect = fitz.Rect(bbox).irect

    if tab_rect.is_empty or tab_rect.is_infinite:
        print('Warning: incorrect rectangle coordinates!')
        return []

    if additional_words:
        w = page.get_text('words') + additional_words
        words = sorted(w, key=lambda i: (i[1], i[0]))
    else:
        words = page.get_text('words')

    if not words:
        print('Warning: page contains no text')
        return []

    drawings = page.get_drawings()
    cells = get_tab_cell_by_header(drawings, tab_rect, headers, header_rows)

    cell2word = []
    for row in cells:
        d = {r: [] for r in row}
        cell2word.append(d)

    for w in words:
        ir = fitz.Rect(w[:4]).irect  # word rectangle
        if ir in tab_rect:
            for row in cell2word:
                for k, v in row.items():
                    if is_in_cell(ir, k):
                        # row[k].append([ir.x0, ir.y0, ir.x1, ir.y1, w[4]])
                        row[k].append(w[4])

    table = []
    for row in cell2word:
        table.append(list(row.values()))
    for row in table:
        for column in row:
            sentence = ' '.join(column).lower()
            if sentence == 'not detected' \
                    or sentence == 'nd' \
                    or sentence == 'not' \
                    or sentence == 'no fusion gene' \
                    or 'not pass' in sentence:
                return []

    return table


def get_tab_cell(drawings: List[Dict], tab_rect: fitz.IRect, header_rows: int = 1) -> List[List[fitz.IRect]]:
    xs = get_tab_grid_x(drawings, tab_rect)
    ys = get_tab_grid_y(drawings, tab_rect, header_rows)
    # (x0, y0, x1, y1) (x1, y0, x2, y1) (x2, y0, x3, y1)
    # (x0, y1, x1, y2) (x1, y1, x2, y2) (x2, y1, x3, y2)

    cells = []
    for j in range(1, len(ys)):
        row = []
        for i in range(1, len(xs)):
            bbox = (xs[i - 1], ys[j - 1], xs[i], ys[j])
            row.append(fitz.Rect(bbox).irect)
        cells.append(row)

    return cells


def get_tab_cell_by_header(
    drawings: List[Dict],
    tab_rect: fitz.IRect,
    headers: List[fitz.IRect],
    header_rows: int = 1
) -> List[List[fitz.IRect]]:
    tab = get_tab_grid_x(drawings, tab_rect)
    hs = list(map(lambda i: i.x0, headers[1:]))
    xs = [tab[0]] if tab else [0]
    for h in hs:
        xs.append(h)
    xs.append(tab[-1]) if tab else xs.append(9999)
    ys = get_tab_grid_y(drawings, tab_rect, header_rows)
    # (x0, y0, x1, y1) (x1, y0, x2, y1) (x2, y0, x3, y1)
    # (x0, y1, x1, y2) (x1, y1, x2, y2) (x2, y1, x3, y2)

    cells = []
    for j in range(1, len(ys)):
        row = []
        for i in range(1, len(xs)):
            bbox = (xs[i - 1], ys[j - 1], xs[i], ys[j])
            row.append(fitz.Rect(bbox).irect)
        cells.append(row)

    return cells


def get_tab_grid_x(drawings: List[Dict], tab_rect: fitz.IRect) -> List[int]:
    grid_line_x = set()
    for d in drawings:
        ir = d['rect'].irect
        if ir in tab_rect and ir.x1 - ir.x0 <= 2:
            grid_line_x.add(ir.x0)

    return sorted(grid_line_x)


def get_tab_grid_y(drawings: List[Dict], tab_rect: fitz.IRect, header_rows: int) -> List[int]:
    grid_line_y = set()
    for d in drawings:
        ir = d['rect'].irect
        if ir in tab_rect and ir.y1 - ir.y0 <= TOLERANCE:
            grid_line_y.add(ir.y0)
        elif tab_rect.x0 < ir.x0 and tab_rect.x1 > ir.x1 \
                and abs(ir.y0 - tab_rect.y0) <= TOLERANCE and ir.y1 - ir.y0 <= TOLERANCE:
            grid_line_y.add(ir.y0)

    sorted_grid_line_y = sorted(grid_line_y)
    filtered_grid_line_y = filter_elements(sorted_grid_line_y)
    return filtered_grid_line_y[header_rows:]


def filter_elements(lst: List) -> List:
    filtered_list = [lst[0]] if lst else []  # Initialize the filtered List with the first element

    for index in range(1, len(lst)):
        diff = lst[index] - lst[index - 1]
        if abs(diff) > TOLERANCE:
            filtered_list.append(lst[index])

    return filtered_list


def is_in_cell(rect_a: fitz.IRect, rect_b: fitz.IRect) -> bool:
    if rect_a in rect_b:
        return True
    elif rect_a.x0 >= rect_b.x0 and rect_a.x1 <= rect_b.x1 \
            and (abs(rect_a.y0 - rect_b.y0) <= TOLERANCE or rect_a.y0 >= rect_b.y0) \
            and (abs(rect_a.y1 - rect_b.y1) <= TOLERANCE or rect_a.y1 <= rect_b.y1):
        return True
    else:
        return False


def draw(page, paths, output_file):
    outpdf = fitz.open()
    outpage = outpdf.new_page(width=page.rect.width, height=page.rect.height)
    shape = outpage.new_shape()

    for path in paths:
        # ------------------------------------
        # draw each entry of the 'items' List
        # ------------------------------------
        for item in path['items']:  # these are the draw commands
            if item[0] == 'l':  # line
                shape.draw_line(item[1], item[2])
            elif item[0] == 're':  # rectangle
                shape.draw_rect(item[1])
            elif item[0] == 'qu':  # quad
                shape.draw_quad(item[1])
            elif item[0] == 'c':  # curve
                shape.draw_bezier(item[1], item[2], item[3], item[4])
            else:
                raise ValueError('unhandled drawing', item)
        # ------------------------------------------------------
        # all items are drawn, now apply the common properties
        # to finish the path
        # ------------------------------------------------------
        shape.finish(
            fill=path['fill'],  # fill color
            color=path['color'],  # line color
            dashes=path['dashes'],  # line dashing
            even_odd=path.get('even_odd', True),  # control color of overlaps
            # closePath=path['closePath'],  # whether to connect last and first point
            # lineJoin=path['lineJoin'],  # how line joins should look like
            # lineCap=max(path['lineCap']),  # how line ends should look like
            # width=path['width'],  # line width
            # stroke_opacity=path.get('stroke_opacity', 1),  # same value for both
            fill_opacity=path.get('fill_opacity', 1),  # opacity parameters
        )
    # all paths processed - commit the shape to its page
    shape.commit()
    outpdf.save(output_file)
