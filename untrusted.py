import tkinter as tk
import tkinter.messagebox

class CircleGridApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Circle Grid Generator for Untrusted Advice")

        self.label_m = tk.Label(self.master, text="Enter m (rows):")
        self.label_m.pack()

        self.entry_m = tk.Entry(self.master)
        self.entry_m.pack()

        self.label_n = tk.Label(self.master, text="Enter n (columns):")
        self.label_n.pack()

        self.entry_n = tk.Entry(self.master)
        self.entry_n.pack()

        self.canvas = tk.Canvas(self.master, width=1900, height=1000, bg='white')
        self.canvas.pack()

        self.generate_button = tk.Button(self.master, text="Generate Grid", command=self.generate_grid)
        self.generate_button.pack()

        self.m = 0  # number of rows (m)
        self.n = 0  # number of columns (n)
        self.circle_radius = 20  # radius of each circle
        self.circle_spacing = 40  # spacing between circles
        self.start_x = 0  # starting x position of the grid
        self.start_y = 0  # starting y position of the grid
        self.highlighted_circle = None  # currently highlighted circle
        self.space_pressed = False  # flag to track if spacebar is pressed
        self.circles = [] # ids of all circles
        self.filled_circles = set()  # set to store indices of filled circles
        self.neighboring_dots = {}  # dictionary to store dot IDs of neighboring circles
        self.familiar_nodes = set()  # set to store familiar nodes
        self.colors = ["#75dfff", "#3a93ca", "#184c8d", "#090949"] # the color of the node when visited for the 1st, 2nd, 3rd, 4th (or more) times
        self.colors_green = ["#008000", "#005d0c", "#003b0c", "#003300"] # the color if v_0 is visited multiple times

        self.master.bind("<Left>", lambda event: self.move_highlighted_circle(event, -1, 0))
        self.master.bind("<Right>", lambda event: self.move_highlighted_circle(event, 1, 0))
        self.master.bind("<Up>", lambda event: self.move_highlighted_circle(event, 0, -1))
        self.master.bind("<Down>", lambda event: self.move_highlighted_circle(event, 0, 1))
        self.master.bind("<space>", self.fill_highlighted_circle)
        self.master.bind("<Return>", self.generate_grid)
        self.master.bind("<KeyRelease>", self.remove_spaces)

    def generate_grid(self, event=None):
        try:
            self.m = int(self.entry_m.get())
            self.n = int(self.entry_n.get())
        except ValueError:
            tkinter.messagebox.showerror("Error", "Please enter valid integers for m and n.")
            return
        
        self.canvas.delete("all")
        self.space_pressed = False
        self.filled_circles.clear()
        self.neighboring_dots = {}
        self.familiar_nodes.clear()
        self.circles.clear()

        # Calculate dimensions for grid of circles
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        total_width = self.n * (2 * self.circle_radius + self.circle_spacing) - self.circle_spacing
        total_height = self.m * (2 * self.circle_radius + self.circle_spacing) - self.circle_spacing

        if total_width > canvas_width or total_height > canvas_height:
            tkinter.messagebox.showerror("Error", "Grid is too large for canvas. Please reduce the number of rows or columns.")
            return
        
        self.start_x = (canvas_width - total_width) / 2
        self.start_y = (canvas_height - total_height) / 2

        for row in range(self.m):
            for col in range(self.n):
                x = self.start_x + col * (2 * self.circle_radius + self.circle_spacing) + self.circle_radius
                y = self.start_y + row * (2 * self.circle_radius + self.circle_spacing) + self.circle_radius
                circle = self.canvas.create_oval(x - self.circle_radius, y - self.circle_radius,
                                                 x + self.circle_radius, y + self.circle_radius,
                                                 outline='black', width=2, fill='white')
                self.circles.append(circle)
                
        self.highlight_circle(self.circles[0])

    def highlight_circle(self, circle):
        self.canvas.itemconfigure(circle, width=4)
        self.highlighted_circle = circle
        new_familiars = self.mark_neighboring_circles(self.circles.index(circle))
        return new_familiars

    def unhighlight_circle(self, circle):
        self.canvas.itemconfigure(circle, width=2)
        self.highlighted_circle = None

    def fill_highlighted_circle(self, event):
        if self.highlighted_circle and not self.space_pressed:
            self.canvas.itemconfigure(self.highlighted_circle, fill=self.colors_green[0])
            self.space_pressed = True
            index = self.circles.index(self.highlighted_circle)
            self.filled_circles.add((index, self.colors_green[0]))
            
            new_familiars = self.mark_neighboring_circles(index)


    def move_highlighted_circle(self, event, dx, dy):
        if self.highlighted_circle is None:
            return
        
        current_index = self.circles.index(self.highlighted_circle)
        current_row = current_index // self.n
        current_col = current_index % self.n

        new_row = (current_row + dy) % self.m
        new_col = (current_col + dx) % self.n

        new_index = new_row * self.n + new_col

        self.update_neighboring_dots()
        self.unhighlight_circle(self.highlighted_circle)
        new_familiars = self.highlight_circle(self.circles[new_index])

        if self.space_pressed:
            arrow_id = self.draw_arrow(current_index, new_index)
            found=False
            for circle in self.filled_circles:
                if circle[0] == new_index: # have visited the node before
                    if circle[1] in self.colors:
                        self.filled_circles.add((new_index, self.colors[self.colors.index(circle[1])+1])) 
                        self.filled_circles.remove(circle)
                        self.canvas.itemconfigure(self.circles[new_index], fill=self.colors[self.colors.index(circle[1])+1])
                    else:
                        self.filled_circles.add((new_index, self.colors_green[self.colors_green.index(circle[1])+1]))
                        self.filled_circles.remove(circle)
                        self.canvas.itemconfigure(self.circles[new_index], fill=self.colors_green[self.colors_green.index(circle[1])+1])
                    found = True
                    break
            if not found: #visited the node for the 1st time
                self.filled_circles.add((new_index, self.colors[0]))
                self.canvas.itemconfigure(self.circles[new_index], fill=self.colors[0])
        

    def draw_arrow(self, start_index, end_index):
        start_x, start_y = self.get_circle_center(start_index)
        end_x, end_y = self.get_circle_center(end_index)

        if start_index % self.n == 0 and end_index % self.n == self.n - 1:  # Left to right edge
            control_x = start_x + (end_x - start_x) / 2  # Control point to create a curve
            control_y = start_y - (self.circle_spacing * 2)
        elif start_index % self.n == self.n - 1 and end_index % self.n == 0:  # Right to left edge
            control_x = start_x + (end_x - start_x) / 2  # Control point to create a curve
            control_y = start_y - (self.circle_spacing * 2)
        elif start_index // self.n == 0 and end_index // self.n == self.m - 1:  # Top to bottom edge
            control_x = start_x - (self.circle_spacing * 2)
            control_y = start_y + (end_y - start_y) / 2  # Control point to create a curve
        elif start_index // self.n == self.m - 1 and end_index // self.n == 0:  # Bottom to top edge
            control_x = start_x - (self.circle_spacing * 2)
            control_y = start_y + (end_y - start_y) / 2  # Control point to create a curve
        else:
            control_x = (start_x + end_x) / 2
            control_y = (start_y + end_y) / 2
        line_id = self.canvas.create_line(start_x, start_y, control_x, control_y, end_x, end_y, fill='black', width=2, arrow='last', smooth=1)
        
        return line_id


    def get_circle_center(self, index):
        col = index % self.n
        row = index // self.n
        x = self.start_x + col * (2 * self.circle_radius + self.circle_spacing) + self.circle_radius
        y = self.start_y + row * (2 * self.circle_radius + self.circle_spacing) + self.circle_radius
        return x, y

    def mark_neighboring_circles(self, index):
        if not self.space_pressed:
            return
        
        row = index // self.n
        col = index % self.n

        neighbors = [
            ((row-1) % self.m, col),  # Up (wrap-around)
            ((row+1) % self.m, col),  # Down (wrap-around)
            (row, (col-1) % self.n),  # Left (wrap-around)
            (row, (col+1) % self.n),  # Right (wrap-around)
        ]
        new_familiars=[]
        for r, c in neighbors:
            neighbor_index = r * self.n + c
            if not any(neighbor_index == circle for circle in self.filled_circles) and neighbor_index not in self.familiar_nodes:
                x, y = self.get_circle_center(neighbor_index)
                dot_id = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='orange')
                self.neighboring_dots[neighbor_index] = dot_id
                self.familiar_nodes.add(neighbor_index)
                new_familiars.append([neighbor_index, dot_id])
        return new_familiars

    def update_neighboring_dots(self):
        for index, dot_id in self.neighboring_dots.items():
            self.canvas.itemconfigure(dot_id, fill='black')

    def reset_highlighted_circle(self):
        if self.highlighted_circle:
            self.unhighlight_circle(self.highlighted_circle)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.filled_circles.clear()
        self.space_pressed = False
        
    def remove_spaces(self, event):
        content_n = self.entry_n.get()
        content_m = self.entry_m.get()
        new_content_n = content_n.replace(" ", "")
        new_content_m = content_m.replace(" ", "")
        if content_n != new_content_n:
            self.entry_n.delete(0, tk.END)
            self.entry_n.insert(0, new_content_n)
        if content_m != new_content_m:
            self.entry_m.delete(0, tk.END)
            self.entry_m.insert(0, new_content_m)
            
   
if __name__ == "__main__":
    root = tk.Tk()
    app = CircleGridApp(root)
    root.mainloop()
