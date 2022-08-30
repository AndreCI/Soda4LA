from tkinter import *
import numbers

from Utils.constants import DEFAULT_PADDING, TFRAME_STYLE
from Utils.scrollable_frame import ScrollableFrame


class Table():
    def __init__(self, master, col=4, row=4, headers=[], data=None, width=1620, height=300):
        '''
        Create a table instance, passing it master (root), number of columns and number of rows
        as arguments
        '''

        self._master = ScrollableFrame(master, orient='horizontal', width=width, height=height,padding=DEFAULT_PADDING, style=TFRAME_STYLE["PARAMETER_MAPPING"][0])

        self.headers = []
        self.painted_row = None
        if row<1:
            raise ValueError("Tables cannot be created with less than 1 row")
        self._row_number = row
        self._col_number = col

        if data:
            try:
                self.set_table_data(data)
            except:
                pass
        elif headers:
            self.set_table_headers(headers)

        self.cells = []

        self.selected_cell = None
        self.selected_line = None

        self.bind_mouse_button()
        self.create_table()

        if data:
            self.set_data(data)


    def grid(self, **kwargs):
        self._master.grid(**kwargs)

    def pack(self):
        '''
        Pack the table
        '''
        self._master.pack()

    def __str__(self) -> str:
        return f"Rows: {self._row_number}, Cols: {self._col_number}\n{self.cells}"

    def bind_mouse_button(self):
        '''
        Bind mouse input on select (highlight) a cell, row or column
        '''
        self._master.master.bind('<Button-1>', self.select_cell)
        self._master.master.bind('<Double-Button-1>', self.select_col)
        self._master.master.bind('<Triple-Button-1>', self.select_row)

    def create_cell(self, col, row, value=None):
        '''
        Create a cell and append it to the table cells array
        '''
        cell = Cell(self._master.scrollableFrame, col, row + 1)
        if value:
            cell.set_value(value)
        else:
            cell.set_value("{}-{}".format(col, row+1))
        self.cells.append((cell, col, row + 1))

    def create_headers_row(self):
        if not self.headers:
            for col in range(self._col_number):
                self.create_cell(col, -1, f"COL {col}")
        else:
            for col, header in zip(range(self._col_number), self.headers):
                self.create_cell(col, -1, header)
        header_row = self.get_cell_line(0)
        for cell in header_row:
            cell.config(justify=CENTER)

    def create_table(self):
        '''
        Create all the cells
        '''
        self.create_headers_row()
        for row in range(self._row_number):
            for col in range(self._col_number):
                self.create_cell(col, row)

    def get_cell(self, row, col):
        '''
        Giving a row and a col as arguments, it returns the cell in that position
        '''
        return [t[0] for _, t in enumerate(self.cells) if t[1] == col and t[2] == row].pop()

    def get_cell_line(self, n, line_type="ROW"):
        '''
        Returns an array of Cells
        '''
        try:
            if line_type == "ROW":
                return [t[0] for _, t in enumerate(self.cells) if t[2] == n]
            if line_type == "COL":
                return [t[0] for _, t in enumerate(self.cells) if t[1] == n]
        except:
            pass

    def find_widget(self, event):
        '''
        Returns the row and column of the frame where the mouse clicked
        '''
        x = event.x_root - self._master.scrollableFrame.winfo_rootx()
        y = event.y_root - self._master.scrollableFrame.winfo_rooty()
        (col, row) = self._master.scrollableFrame.grid_location(x, y)
        return row, col

    def find_cell(self, event):
        row, col = self.find_widget(event)
        return self.get_cell(row, col)

    def find_row_from_key(self, value, col):
        column = self.get_cell_line(self.headers.index(col), "COL")
        for cell in column:
            try:
                if(int(cell._value.get()) == int(value)):
                    print(cell._pos)
                    return Cell_Line(self._master.scrollableFrame, self.get_cell_line(cell._pos[1], "ROW"))
            except:
                pass
    def find_column(self, col_idx):
        try:
            cell_line = Cell_Line(self._master.scrollableFrame, self.get_cell_line(col_idx, "COL"))
            return cell_line
        except:
            pass

    def find_cell_line(self, event, line_type="ROW"):
        row, col = self.find_widget(event)
        try:
            if line_type == "ROW":
                cell_line = Cell_Line(self._master.scrollableFrame, self.get_cell_line(row, line_type))
            if line_type == "COL":
                cell_line = Cell_Line(self._master.scrollableFrame, self.get_cell_line(col, line_type))
            return cell_line
        except:
            pass

    def focus_selected_cell(self, cell):
        self.selected_cell = cell
        self.selected_cell.focus_cell()

    def unfocus_selected_cell(self):
        self.selected_cell.unfocus_cell()
        self.selected_cell = None

    def select_cell(self, event):
        try:
            cell = self.find_cell(event)
            if self.selected_line:
                self.selected_line.unfocus_cells()
            if not isinstance(self.selected_cell, Cell):
                self.focus_selected_cell(cell)
            elif self.selected_cell == cell:
                self.unfocus_selected_cell()
            else:
                self.unfocus_selected_cell()
                self.focus_selected_cell(cell)
        except:
            pass

    def paint_row(self, value, key, color):
        #self.find_cell()
        #line = Cell_Line(self._master.scrollableFrame, self.get_cell_line(row_idx))
        line = self.find_row_from_key(value, key)
        if line:
            self.painted_row = line
            line.paint_line(color)
            return line

    def paint_col(self, line_name, color):
        line_idx = self.headers.index(line_name)
        line = self.find_column(line_idx)
        line.paint_line(color)

    def focus_selected_line(self, line):
        self.selected_line = line
        self.selected_line.focus_cells()

    def unfocus_selected_line(self):
        self.selected_line.unfocus_cells()
        del self.selected_line
        self.selected_line = None

    def select_row(self, event):
        try:
            row = self.find_cell_line(event)
            if not isinstance(self.selected_line, Cell_Line):
                self.focus_selected_line(row)
            elif self.selected_line == row:
                self.unfocus_selected_line()
            else:
                self.unfocus_selected_line()
                self.focus_selected_line(row)
        except:
            pass

    def select_col(self, event):
        try:
            col = self.find_cell_line(event, line_type="COL")
            if not isinstance(self.selected_line, Cell_Line):
                self.focus_selected_line(col)
            elif self.selected_line == col:
                self.unfocus_selected_line()
            else:
                self.unfocus_selected_line()
                self.focus_selected_line(col)
        except:
            pass

    def insert_cells(self, line, line_type="ROW", header=None):
        '''
        Insert a cell line (column or row) in the specified position
        '''
        try:
            if line_type == "ROW":
                for col in range(self._col_number):
                    self.create_cell(col, line)
                if 0 < line < self._row_number:
                    for (cell, col, row) in self.cells:
                        i = self.cells.index((cell, col, row))
                        if line <= row:
                            _, y = cell.get_pos()
                            cell.set_pos(col, y + 1)
                            self.cells[i] = (cell, col, y + 1)
                        #self.get_cell(line, col).set_value(f"NEW ROW {line}")

            if line_type == "COL":
                if 0 <= line <= self._col_number:
                    for (cell, col, row) in self.cells:
                        i = self.cells.index((cell, col, row))
                        if line <= col:
                            x, _ = cell.get_pos()
                            cell.set_pos(x + 1, row)
                            self.cells[i] = (cell, x + 1, row)

                    if header:
                        self.create_cell(line, -1, header)
                        self.headers.insert(line, header)
                    else:
                        self.create_cell(line, -1, "New column")

                    new_col_header = self.get_cell(0, line)
                    new_col_header.config(justify=CENTER)

                    for row in range(self._row_number):
                        self.create_cell(line, row)

        except:
            print("Error with table, no cells have been added")
            #raise ValueError("Error with table, no cells have been added")
            pass

    def insert_row(self, pos):
        self.insert_cells(pos, line_type="ROW")
        self._row_number += 1

    def insert_col(self, pos, header=None):
        if header not in self.headers:
            self.insert_cells(pos, line_type="COL", header=header)
            self._col_number += 1

    def set_table_headers(self, headers):
        for h in headers:
            self.headers.append(h)
        self._col_number = len(self.headers)

    def set_table_data(self, data):
        for d in data:
            keys = d.keys()
            for k in keys:
                if k not in self.headers:
                    self.headers.append(k)

        self._row_number = len(data)
        self._col_number = len(self.headers)

    def push_row(self, data):
        for cidx in range(self._col_number):
            for ridx in range(1, self._row_number + 1):
                if(ridx < self._row_number):
                    self.get_cell(ridx, cidx).set_value(self.get_cell(ridx +1, cidx)._value.get())
                else:
                    self.get_cell(ridx, cidx).set_value(data[self.headers[cidx]])
        # if(self.painted_row):
        #     for cell in self.get_cell_line(self.painted_row.get_row_nbr() - 1):
        #         cell.paint_cell("blue")
        #     self.painted_row.paint_line("white")


    def set_data(self, data):
        for d in data: # add all unknown headers
            for key in d.keys():
                if key not in self.headers:
                    self.insert_col(self._col_number, key)
        row = 0
        for d in data:
            col = 0
            if(row>=self._row_number):
                self.insert_row(self._row_number)
            for key in d.keys():
                self.get_cell(row + 1, col).set_value(d[key])
                col+=1
            row += 1
        #
        # for h in self.headers: #
        #     col = self.headers.index(h)
        #     for d in data:
        #         for key in d.keys():
        #             if key not in self.headers:
        #                 self.insert_col(self._col_number, key)
        #         row = data.index(d) + 1
        #         if h in d.keys():
        #             pass
        #             self.get_cell(row, col).set_value(d[h])
                # if h not in d.keys():
                #    self.insert_col(1, h)
                # else:
                #    self.get_cell(row, col).set_value(d[h])

    def get_row_data(self, row):
        '''
        Returns a dictionary where the keys are the table headers and its values are the correspondent cell
        '''
        d = {}
        row_cells = self.get_cell_line(row + 1)
        for cell, header in zip(row_cells, self.headers):
            d.setdefault(header, cell.get_value())
        return d

    def get_table_data(self):
        '''
        Returns a list of dictionaries with all the values in the table
        '''
        data = []
        for row in range(self._row_number):
            data.append(self.get_row_data(row))
        return data


class Cell(Entry):
    def __init__(self, master, posx=0, posy=0):
        self._root = master
        Entry.__init__(self, self._root)
        self._value = StringVar()
        self._pos = (posx, posy)
        self.default_color = "white"

        self.grid(column=posx, row=posy)
        self.config(
            state="readonly",
            readonlybackground="white",
            textvariable=self._value,
            cursor="arrow",
            exportselection=0,
            selectbackground="light blue",
            selectforeground="black"
        )

    def paint_cell(self, color="lightgreen"):
        self.default_color = color
        self.config(readonlybackground=color)

    def focus_cell(self):
        self.config(readonlybackground="lightblue")

    def unfocus_cell(self):
        self.config(readonlybackground=self.default_color)

    def set_value(self, value):
        if isinstance(value, numbers.Number):
            self.config(justify=RIGHT)
        else:
            self.config(justify=LEFT)
        self._value.set(value)

    def get_value(self):
        return self._value.get()

    def set_pos(self, posx, posy):
        self._pos = (posx, posy)
        self.grid(column=posx, row=posy)

    def get_pos(self):
        return (self._pos)


class Cell_Line():
    def __init__(self, master, cells):
        self._root = master
        self._cells = cells
        self._length = len(self._cells)

    def get_row_nbr(self):
        return self._cells[0].get_pos()[1]

    def get_col_nbr(self):
        return self._cells[0].get_pos()[0]

    def create_cells(self, i):
        for n in range(self._length):
            cell = Cell(self._root, posx=n, posy=i)
            self._cells.append(cell)

    def get_cells(self):
        return self._cells

    def get_cell(self, i):
        return self._cells[i]

    def paint_line(self, color):
        for cell in self._cells:
            cell.paint_cell(color)

    def focus_cells(self):
        for cell in self._cells:
            cell.focus_cell()

    def unfocus_cells(self):
        for cell in self._cells:
            cell.unfocus_cell()

    # def __del__(self):
    #    print(__class__.__name__, "destroyed")


# Test

def _test():
    d = [
        {"Name": "Juan", "Age": 24},
        {"Age": 33, "Address": "Monteagudo 1175"},
    ]
    h = ["Name", "Age", "ID"]
    root = Tk()
    root.title("Test")
    table = Table(root, data=d)
    #table.set_table_headers(h)
    #table.set_table_data(d)
    #table.set_data(d)
    table.pack()

    root.mainloop()


if __name__ == "__main__":
    _test()