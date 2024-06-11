import time

class Field:

    def __init__(self, size):
        self.filling = [[' '] * size for _ in range(size)]
        self.game_switch = True

    def put(self, cell_x, cell_y, symbol):
        self.filling[cell_x][cell_y] = symbol

    def get(self, cell_x, cell_y):
        if 0 <= cell_x < SIZE and 0 <= cell_y < SIZE:
            return self.filling[cell_x][cell_y]
        else:
            return ' '


def winner_determination(field, cell_x, cell_y):
    symbol = field.get(cell_x, cell_y)
    directions = [[1, 0], [0, 1], [1, 1], [1, -1]]  # these directions correspond to the directions on the plane
    length = 3

    for direction in directions:
        for left_cells in range(length):
            for i in range(-left_cells, length - left_cells):
                if field.get(cell_x + i * direction[1], cell_y + i * direction[0]) != symbol:
                    break
            else:
                for edge in [-left_cells - 1, length - left_cells]:
                    if field.get(cell_x + edge * direction[1], cell_y + edge * direction[0]) == symbol:
                        break
                else:
                    right_cells = length - left_cells - 1
                    return symbol, direction, left_cells, right_cells

    return False


def line_x(i):
    return FIELD_PADDING + TITLE_Y / 2 + i * FIELD_SIZE / SIZE


def line_y(i):
    return FIELD_PADDING + TITLE_Y + i * FIELD_SIZE / SIZE


def preparation(canvas):
    text = canvas.create_text(SCREEN_SIZE / 2, TITLE_Y, text="Let's play!")

    field = canvas.create_rectangle(FIELD_PADDING + TITLE_Y / 2, FIELD_PADDING + TITLE_Y,
                                    FIELD_PADDING + TITLE_Y / 2 + FIELD_SIZE, FIELD_PADDING + TITLE_Y + FIELD_SIZE,
                                    fill=COLOR_FIELD, outline="")

    for i in range(1, SIZE):
        line = canvas.create_line(line_x(i), line_y(0), line_x(i), line_y(SIZE),
                                  fill=COLOR_LINES, width=2)

    for j in range(1, SIZE):
        line = canvas.create_line(line_x(0), line_y(j), line_x(SIZE), line_y(j),
                                  fill=COLOR_LINES, width=2)


def painting_cross(canvas, center_x, center_y):
    global FIGURES_SIZE
    line = canvas.create_line(center_x - FIGURES_SIZE, center_y - FIGURES_SIZE,
                              center_x + FIGURES_SIZE, center_y + FIGURES_SIZE,
                              fill=COLOR_CROSS, width=2.5)
    line = canvas.create_line(center_x - FIGURES_SIZE, center_y + FIGURES_SIZE,
                              center_x + FIGURES_SIZE, center_y - FIGURES_SIZE,
                              fill=COLOR_CROSS, width=2.5)


def painting_circle(canvas, center_x, center_y):
    global FIGURES_SIZE
    circle = canvas.create_oval(center_x - FIGURES_SIZE, center_y - FIGURES_SIZE,
                                center_x + FIGURES_SIZE, center_y + FIGURES_SIZE,
                                outline=COLOR_CIRCLE, width=2.5)


def win_sign(canvas, info_list):
    symbol = info_list[0]
    color_text = COLOR_CROSS if symbol == 'X' else COLOR_CIRCLE
    win_label = Label(root, text=f'{symbol} wins!',
                      bg=COLOR_FIELD,
                      height=3,
                      width=20,
                      fg=color_text,
                      font=('Helvetica', 24),
                      relief=RAISED,
                      )
    win_label.place(relx=0.5, rely=0.5, anchor='center')

def win_line(canvas, info_list, cell_x, cell_y):
    symbol, direction, left_cells, right_cells = info_list

    tail = 0.6
    left_cells += tail
    right_cells += tail
    color_line = COLOR_CROSS if symbol == 'X' else COLOR_CIRCLE

    canvas.create_line(cell_x - direction[0] * left_cells * CELLS_SIZE,
                       cell_y - direction[1] * left_cells * CELLS_SIZE,
                       cell_x + direction[0] * right_cells * CELLS_SIZE,
                       cell_y + direction[1] * right_cells * CELLS_SIZE,
                       fill='black', width=3)

def write_slogan():
    label = Label(root, text='Па-ма-ги-те!')
    label.pack()

def ask_sign(canvas):
    button = Button(root, text="YES",
                       command=write_slogan)
    button.pack(side=LEFT)
    slogan = Button(root, text="NO",
                       command=quit)
    slogan.pack(side=RIGHT)


def process_mouse(event):
    if game_field.game_switch:
        for i in range(SIZE):
            if line_x(i) < event.x < line_x(i + 1):
                for j in range(SIZE):
                    if line_y(j) < event.y < line_y(j + 1):
                        if game_field.filling[j][i] == ' ':
                            center_x = (line_x(i) + line_x(i + 1)) / 2
                            center_y = (line_y(j) + line_y(j + 1)) / 2

                            global move_count

                            if move_count % 2 == 0:
                                painting_cross(canvas, center_x, center_y)
                                game_field.filling[j][i] = 'X'
                            else:
                                painting_circle(canvas, center_x, center_y)
                                game_field.filling[j][i] = 'O'

                            move_count += 1

                            win_info = winner_determination(game_field, j, i)

                            if win_info:
                                game_field.game_switch = False
                                root.after(300, lambda: win_line(canvas, win_info, center_x, center_y))
                                # ask_sign(canvas)

                            break


def process_key(event):
    if event.keysym == "Escape":
        root.quit()
        return


from tkinter import *

SCREEN_SIZE = 600
FIELD_PADDING = 30
TITLE_Y = 25

FIELD_SIZE = SCREEN_SIZE - 2 * FIELD_PADDING - TITLE_Y

SIZE = 15
CELLS_SIZE = FIELD_SIZE / SIZE
FIGURES_SIZE = FIELD_SIZE / SIZE * 0.35

COLOR_FIELD = '#7ac5cd'
COLOR_LINES = '#98f5ff'
COLOR_CROSS = '#FFeF00'
COLOR_CIRCLE = '#EB4C42'

root = Tk()
root.title("TIC TAC TOE")

canvas = Canvas(root, width=SCREEN_SIZE, height=SCREEN_SIZE)
canvas.pack()

preparation(canvas)

move_count = 0
game_field = Field(SIZE)

root.bind("<Key>", process_key)
root.bind("<Button-1>", process_mouse)

root.mainloop()
