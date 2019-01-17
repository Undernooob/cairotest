import cairo
import yaml
import textwrap as tw
import webcolors as wcol

# initialization
all_objects, all_blocks, rows_height, object_matrix = [], [], [], []
temp = 0
x = []
y = []
c = 0


# def get_color(obj_list):
#     tupl = wcol.name_to_rgb(obj_list.get('block')[0].get('color'))
#     ctx.set_source_rgba(tupl[0] / 256, tupl[1] / 256, tupl[2] / 256, 0.7)


# file_path = input("Enter .yaml file path: ")
# font_size = int(input("Enter font size in pt (default: 13): "))
# if font_size <= 8:
#     font_size = 13
file_path = "structure.yaml"
font_size = 13


def read_file(file_path):
    stream = open(file_path, 'r')
    for data in yaml.load_all(stream):
        if data.get('Structure') != None:
            struct = data.get('Structure')
        elif data.get('Structure') == None:
            block_list = (data.get('Blocks'))
            object_list = (data.get('Objects'))
    return struct, block_list, object_list


def get_size_for_font(struct):
    WIDTH, HEIGHT = struct.get('size')
    # Need to do
    return 13


def get_matrix_size(struct):
    Width, Height = struct.get('size')
    Height = Height - (font_size + 4) * 3  # Вычитаем из высоты изображения высоту для имени концепции
    Width = Width - (font_size + 2) * 11  # Вычитаем из ширины изображения ширину столбца для обозначения семестра
    comments = struct.get('comments')[:-1].split('\n')
    comments_count = len(comments)
    Height = Height - font_size * 1.2 * comments_count  # Вычитаем из высоты изображения высоту для имени концепции
    return Width, Height


def sems_stretching(object_list, object_matrix, elems_matrix):  # one block
    for k in object_list:
        sem = k.get('sems')
        block = k.get('block')
        if len(block) == 1 and len(sem) > 1:
            max_x = 0
            max_w = 0
            max_y = 0
            max_h = 0
            for j in sem:
                if len(object_matrix[j - 1][block[0].get('number') - 1]) > 1:
                    x = 1
                    w = 1
                    y = 1
                    h = 1
                    for v in object_matrix[j - 1][block[0].get('number') - 1]:
                        if v.get('name') != k.get('name'):
                            if min(v.get('sems')) <= sem[0]:
                                y += 1
                                max_y = max(max_y, y)
                            if max(v.get('sems')) >= sem[-1]:
                                h += 1
                                max_h = max(max_h, h)
                            if v.get('block')[0].get('number') <= block[0].get('number'):
                                x += 1
                                max_x = max(max_x, x)
                            if v.get('block')[-1].get('number') > block[0].get('number'):
                                w += 1
                                max_w = max(max_w, w)
            k.update([['x', max_x], ['w', max_w]])
            k.update([['y', max_y], ['h', max_h]])


def block_stretching(object_list, object_matrix):
    for k in object_list:
        sem = k.get('sems')
        block = k.get('block')
        if len(block) > 1 and len(sem) == 1:
            max_x = 0
            max_w = 0
            min_y = 0
            for j in range(len(block)):
                if len(object_matrix[sem[0] - 1][block[j].get('number') - 1]) > 1:
                    for v in object_matrix[sem[0] - 1][block[j].get('number') - 1]:
                        if v.get('name') != k.get('name'):
                            if v.get('sems')[0] == sem[0] and 'y' in list(v.keys()):
                                y = v.get('y') - 1
                                min_y = min(min_y, y)
                            if v.get('sems')[-1] == sem[0] and 'h' in list(v.keys()):
                                y = v.get('h') + 1
                                min_y = max(min_y, y)
                            # if len(v.get('sems')) > 1:
                            #     if (v.get('block')[0].get('number') == block[0].get('number')
                            #             and ):  # first block
                            #         x += 1
                            #         max_x = max(max_x, x)
                    if max_x == 0:
                        max_x = 1
                    if min_y == 0:
                        min_y = 1
                    if max_w == 0:
                        max_w = 1
            k.update([['x', max_x],['y', min_y], ['w', max_w]])
    print(object_matrix[2][0][0])


def block_and_sems_stretching(object_list, object_matrix, elems_matrix):
    for k in object_list:
        sem = k.get('sems')
        block = k.get('block')
        if len(block) > 1 and len(sem) == 2:
            max_x = 0
            max_w = 0
            max_y = 0
            max_h = 0
            for j in range(len(block)):
                for i in [0, 1]:
                    if len(object_matrix[sem[i] - 1][block[j].get('number') - 1]) > 1:
                        x = 1
                        w = 1
                        y = 1
                        h = 1
                        for v in object_matrix[sem[i] - 1][block[j].get('number') - 1]:
                            if v.get('name') != k.get('name'):
                                if len(v.get('sems')) > 1:
                                    if v.get('block')[0].get('number') <= block[0].get('number'):  # first block
                                        x += 1
                                        max_x = max(max_x, x)
                                    if v.get('block')[-1].get('number') >= block[0].get('number'):  # last block
                                        w += 1
                                        max_w = max(max_w, w)
                                if min(v.get('sems')) <= sem[i] and i == 0:
                                    y += 1
                                    max_y = max(max_y, y)
                                if max(v.get('sems')) >= sem[i] and i == 1:
                                    h += 1
                                    max_h = max(max_h, h)
                k.update([['x', max_x], ['w', max_w]])
                k.update([['y', max_y], ['h', max_h]])
        elif len(block) == 2 and len(sem) > 1:
            max_x = 0
            max_w = 0
            max_y = 0
            max_h = 0
            for i in [0, 1]:
                for j in sem:
                    if len(object_matrix[j - 1][block[i].get('number') - 1]) > 1:
                        x = 1
                        w = 1
                        y = 1
                        h = 1
                        for v in object_matrix[j - 1][block[i].get('number') - 1]:
                            if v.get('name') != k.get('name'):
                                if min(v.get('sems')) <= sem[0]:
                                    y += 1
                                    max_y = max(max_y, y)
                                if max(v.get('sems')) >= sem[-1]:
                                    h += 1
                                    max_h = max(max_h, h)
                                if v.get('block')[0].get('number') <= block[i].get('number') and i == 0:
                                    x += 1
                                    max_x = max(max_x, x)
                                if v.get('block')[-1].get('number') >= block[i].get('number') and i == 1:
                                    w += 1
                                    max_w = max(max_w, w)
                k.update([['x', max_x], ['w', max_w]])
                k.update([['y', max_y], ['h', max_h]])
    return elems_matrix


def get_matrix_coords(struct, object_matrix, elems_matrix):
    block_count = struct.get('block_count')
    sems_count = struct.get('sems_count')
    font_size = get_size_for_font(struct)
    Width, Height = get_matrix_size(struct)
    elems_matrix = block_and_sems_stretching(object_list, object_matrix, elems_matrix)
    sems_stretching(object_list, object_matrix, elems_matrix)
    block_stretching(object_list, object_matrix)
    print(object_matrix[3][0][2])

def get_object_matrix(object_list):
    block_count = struct.get('block_count')
    sems_count = struct.get('sems_count')
    object_matrix = []
    elems_matrix = []
    for i in range(sems_count):
        object_matrix.append([])
        elems_matrix.append([])
        for j in range(block_count):
            object_matrix[i].append([])
            elems_matrix[i].append(0)
            for k in range(len(object_list)):
                if i+1 in object_list[k].get('sems'):
                    for block in range(len(object_list[k].get('block'))):
                        if j + 1 == object_list[k].get('block')[block].get('number'):
                            object_matrix[i][j].append(object_list[k])
                            elems_matrix[i][j] += 1
    return object_matrix, elems_matrix


struct, block_list, object_list = read_file(file_path)
print(struct)
object_matrix, elems_matrix = get_object_matrix(object_list)
print(elems_matrix)
get_matrix_coords(struct, object_matrix, elems_matrix)

# block_list, object_list = [], []
#
# stream = open(file_path, 'r')
# for data in yaml.load_all(stream):
#     if data.get('Structure') != None:
#         struct = data.get('Structure')
#         count = struct.get('block_count')
#         sems_count = struct.get('sems_count')
#
#         rows_height = [0] * sems_count
#         object_matrix = [[0] * count for i in range(sems_count)]
#         WIDTH, HEIGHT = struct.get('size')
#         sym_count_in_line = int(WIDTH/count/font_size)
#         wrapper = tw.TextWrapper(break_long_words=False, width=sym_count_in_line - 10)
#     else:
#         i = 0
#         block_list.append(data.get('Block'))
#         object_list.append(data.get('Objects'))
#         tmp = [0] * sems_count
#         last_block_in_iter = len(object_list) - 1
#         while i != len(object_list[last_block_in_iter]):
#             tmp_lst = wrapper.wrap(object_list[last_block_in_iter][i].get('name'))
#             sem = object_list[last_block_in_iter][i].get('sems')[0] - 1
#             tmp[sem] += (len(tmp_lst) + 2) * font_size
#             object_matrix[sem][last_block_in_iter] += 1
#             all_objects.append(tmp_lst)
#             i += 1
#         rows_height = list(map(lambda a, b: max(a, b), rows_height, tmp))
#
#
# surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
# ctx = cairo.Context(surface)
# ctx.set_source_rgb(0.4, 0.1, 0.9)
# ctx.select_font_face('Lucida Console', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
# ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)  # transparent black
# ctx.rectangle(0, 0, WIDTH, HEIGHT)
# ctx.fill()
# ctx.set_font_size(font_size + 4)  # Прибавляем 4, чтобы преобразовать пункты в пиксели
# cols_width = int((WIDTH - 11 * font_size) / count)
#
#
# ctx.set_source_rgb(0, 0, 0)
# for i in range(len(rows_height)):
#     temp += rows_height[i]
#     ctx.move_to(0, temp)
#     ctx.line_to(WIDTH, temp)
#     y.append(temp)
# ctx.stroke()
# ctx.set_dash([14.0, 6.0])
# for i in range(count):
#     x.append(11 * font_size + cols_width * i)
#     ctx.move_to(x[i], 0)
#     ctx.line_to(x[i], HEIGHT)
# y = [0] + y
# print(block_list)
# print(object_list)
# # ctx.set_line_width(1)
# ctx.stroke()
# ctx.set_dash([1.0, 0])
#
# for i in range(len(x)):
#     for j in range(len(y) - 1):
#         tmp_coord = 0
#         if object_matrix[j][i] != 0:
#             for k in range(object_matrix[j][i]):
#                 rect_y_corner = tmp_coord
#                 for n in range(len(all_objects[c])):
#                     ctx.move_to(x[i] + font_size, y[j] + font_size * 2 + k * (font_size * 2.2) + n * (font_size + 2) + tmp_coord)
#                     ctx.show_text(str(all_objects[c][n]))
#                 tmp_coord += n * (font_size + 2)
#                 get_color(object_list[i][object_matrix[j][i] - 1])
#                 ctx.rectangle(x[i] + int(font_size/2), y[j] + font_size - 3 + k * (font_size * 2.2) + rect_y_corner, cols_width - font_size, (n + 1) * (font_size + 7))
#                 ctx.set_line_join(cairo.LINE_JOIN_ROUND)
#                 ctx.fill()
#                 ctx.set_source_rgb(0, 0, 0)
#                 ctx.stroke()
#                 if n == 0:
#                     temp_n = 1
#                 c += 1
#
# ctx.stroke()
#
#
# surface.write_to_png("example.png")  # Output to PNG