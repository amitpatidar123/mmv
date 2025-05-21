import tkinter as tk
from tkinter import messagebox

class MemoryBlock:
    def __init__(self, start, size, process=None):
        self.start = start
        self.size = size
        self.process = process  # None means free

class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.blocks = [MemoryBlock(0, total_memory)]

    def allocate(self, process_name, size):
        for i, block in enumerate(self.blocks):
            if block.process is None and block.size >= size:
                new_block = MemoryBlock(block.start, size, process_name)
                remaining = block.size - size

                if remaining > 0:
                    self.blocks[i] = MemoryBlock(block.start + size, remaining)
                    self.blocks.insert(i, new_block)
                else:
                    block.process = process_name
                return True
        return False

    def deallocate(self, process_name):
        for block in self.blocks:
            if block.process == process_name:
                block.process = None
        self.merge_free_blocks()

    def merge_free_blocks(self):
        i = 0
        while i < len(self.blocks) - 1:
            if self.blocks[i].process is None and self.blocks[i + 1].process is None:
                self.blocks[i].size += self.blocks[i + 1].size
                del self.blocks[i + 1]
            else:
                i += 1

class MemoryVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Management Visualizer")
        self.geometry("600x400")

        self.manager = MemoryManager(400)  # 400 units of memory

        self.canvas = tk.Canvas(self, bg="white", height=200)
        self.canvas.pack(pady=20, fill=tk.X)

        frame = tk.Frame(self)
        frame.pack()

        tk.Label(frame, text="Process Name:").grid(row=0, column=0)
        self.process_name_entry = tk.Entry(frame)
        self.process_name_entry.grid(row=0, column=1)

        tk.Label(frame, text="Size:").grid(row=1, column=0)
        self.size_entry = tk.Entry(frame)
        self.size_entry.grid(row=1, column=1)

        tk.Button(frame, text="Allocate", command=self.allocate).grid(row=2, column=0, pady=10)
        tk.Button(frame, text="Deallocate", command=self.deallocate).grid(row=2, column=1)

        self.draw_memory()

    def allocate(self):
        name = self.process_name_entry.get()
        try:
            size = int(self.size_entry.get())
            if self.manager.allocate(name, size):
                self.draw_memory()
            else:
                messagebox.showerror("Error", "Not enough memory!")
        except ValueError:
            messagebox.showerror("Error", "Invalid size input!")

    def deallocate(self):
        name = self.process_name_entry.get()
        self.manager.deallocate(name)
        self.draw_memory()

    def draw_memory(self):
        self.canvas.delete("all")
        x = 10
        height = 50
        total_width = 580

        for block in self.manager.blocks:
            width = (block.size / self.manager.total_memory) * total_width
            color = "lightgreen" if block.process else "lightgrey"
            self.canvas.create_rectangle(x, 20, x + width, 20 + height, fill=color)
            label = block.process if block.process else "Free"
            self.canvas.create_text(x + width / 2, 45, text=label)
            x += width

if __name__ == "__main__":
    app = MemoryVisualizer()
    app.mainloop()
