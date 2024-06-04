class Field:

    def __init__(self, size):
        self.filling = [[' '] * size for _ in range(size)]

    def record(self, cell_x, cell_y, symbol):
        self.filling[cell_x][cell_y] = symbol

    def read(self, cell_x, cell_y):
        return self.filling[cell_x][cell_y]


def line_x(i):
    return FIELD_PADDING + TITLE_Y / 2 + i * FIELD_SIZE / SIZE


def line_y(i):
    return FIELD_PADDING + TITLE_Y + i * FIELD_SIZE / SIZE

def preparation(canvas):

    text = canvas.create_text(SCREEN_SIZE/2, TITLE_Y, text="Let's play!")

    field = canvas.create_rectangle(FIELD_PADDING + TITLE_Y / 2, FIELD_PADDING + TITLE_Y,
                                    FIELD_PADDING + TITLE_Y / 2 + FIELD_SIZE, FIELD_PADDING + TITLE_Y + FIELD_SIZE ,
                                    fill=COLOR_FIELD, outline="")

    for i in range(0, SIZE):
        line = canvas.create_line(line_x(i), line_y(0), line_x(i), line_y(SIZE),
                                    fill=COLOR_LINES, width=2)

    for j in range(0, SIZE):
        line = canvas.create_line(line_x(0), line_y(j), line_x(SIZE), line_y(j),
                                  fill=COLOR_LINES, width=2)

    for i in range(SIZE):
        for j in range(SIZE):
            center_x = (line_x(i) + line_x(i + 1)) / 2
            center_y = (line_y(j) + line_y(j + 1)) / 2
            painting_сircle(canvas, center_x, center_y)


def painting_cross(canvas, center_x, center_y):
    global FIGURES_SIZE
    line = canvas.create_line(center_x - FIGURES_SIZE, center_y - FIGURES_SIZE,
                              center_x + FIGURES_SIZE, center_y + FIGURES_SIZE,
                              fill=COLOR_CROSS, width=2.5)
    line = canvas.create_line(center_x - FIGURES_SIZE, center_y + FIGURES_SIZE,
                              center_x + FIGURES_SIZE, center_y - FIGURES_SIZE,
                              fill=COLOR_CROSS, width=2.5)

def painting_сircle(canvas, center_x, center_y):
    global FIGURES_SIZE
    circle = canvas.create_oval(center_x - FIGURES_SIZE, center_y - FIGURES_SIZE,
                                center_x + FIGURES_SIZE, center_y + FIGURES_SIZE,
                                outline=COLOR_CIRCLE, width=2)

def process_mouse(event):
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
                            painting_сircle(canvas, center_x, center_y)
                            game_field.filling[j][i] = 'O'

                        move_count += 1

                        break


def process_key(event):
    if event.keysym == "Escape":
        root.quit()
        return

from tkinter import *

SCREEN_SIZE = 600
FIELD_PADDING = 30
TITLE_Y = 20

FIELD_SIZE = SCREEN_SIZE - 2 * FIELD_PADDING - TITLE_Y

SIZE = 52
FIGURES_SIZE = 1 # FIELD_SIZE / SIZE * 0.35


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

# k = 2
# b1 = 10
# b2 = 13
# x0 = 40
# x1 = 500
#
# canvas.create_line(x0, k * x0 + b1, x1, k * x1 + b1, fill=COLOR_LINES, width=0.1)
# canvas.create_line(x0, k * x0 + b2, x1, k * x1 + b2, fill=COLOR_LINES, width=0.1)

# canvas.create_line(line_x(0), line_y(0) + 10, line_x(0), line_y(SIZE) - 10, fill=COLOR_LINES, width=20)
# canvas.create_line(line_x(0) + 10, line_y(0), line_x(0) + 10, line_y(SIZE), width=1)
#
# # canvas.create_oval(175, 100, 100, 175, width = 3)
# canvas.create_oval(100 - 5, 100 - 5, 100 + 5, 100 + 5, width = 2)

win_label = Label(root, text=f'x wins!',
                bg = COLOR_FIELD,
                height = 3,
                width = 20,
                fg = COLOR_LINES,
                # justify = CENTER,
                relief = RAISED,
                # underline = 0,
                # wraplength = 250
                )

win_label.place(relx=0.5, rely=0.5, anchor='center')
# win_label.pack()

root.mainloop()