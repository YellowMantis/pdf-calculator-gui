import os
import sys
import tkinter as tk
from tkinter import filedialog
from TkinterDnD2 import TkinterDnD, DND_FILES
from PyPDF2 import PdfReader
import customtkinter as ctk
from PIL import Image, ImageTk



def count_pages_in_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            return len(pdf_reader.pages)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return 0

def count_pages_in_directory(directory_path):
    total_pages = 0
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                total_pages += count_pages_in_pdf(file_path)
    return total_pages

class DragAndDropApp():
    def __init__(self, root):
        
        self.root = root
        self.root.title("Pdf Page Calculator")
        self.current_directory_path = None  
        self.starting_cost = tk.StringVar(value="133")
        self.cost_per_page = tk.StringVar(value="0.25")
        self.root.minsize(500, 600)
        self.root.maxsize(700,700)
        self.root.configure(bg="#1E2637")
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        self.file_icon = self.load_icon(os.path.join(base_path, "icons", "folder_icon.png"))
        self.pages_icon = self.load_icon(os.path.join(base_path, "icons", "pdf_icon.png"))
        self.cost_icon = self.load_icon(os.path.join(base_path, "icons", "shekel_icon.png"))
        self.tk_icon_image = self.load_icon(os.path.join(base_path, "icons", "download_icon2.png"))
        
        self.create_ui()

    def create_ui(self):

        ctk.set_appearance_mode("light")


        input_frame1 = tk.Frame(self.root, bg="#1E2637")
        input_frame1.pack(pady=5)

        self.starting_cost_label = tk.Label(input_frame1, text="Starting Cost:", font=("Roboto", 12), background="#1E2637", fg="#71D4FF")
        self.starting_cost_entry = ctk.CTkEntry(input_frame1, textvariable=self.starting_cost, font=("Roboto", 14), width=100)
        self.starting_cost_entry.bind("<FocusOut>", self.update_cost)


        self.starting_cost_label.pack(side="left", padx=5,pady=(10,10))
        self.starting_cost_entry.pack(side="left", padx=5)


        input_frame2 = tk.Frame(self.root, bg="#1E2637")
        input_frame2.pack(pady=5)

        self.cost_per_page_label = tk.Label(input_frame2, text="Cost per Page:", font=("Roboto", 12), background="#1E2637", fg="#71D4FF")
        self.cost_per_page_entry = ctk.CTkEntry(input_frame2, textvariable=self.cost_per_page, font=("Roboto", 14), width=100)
        self.cost_per_page_entry.bind("<FocusOut>", self.update_cost)

        self.cost_per_page_label.pack(side="left", padx=1,pady=(10,10))
        self.cost_per_page_entry.pack(side="left", padx=5,pady=10)


        self.browse_button = ctk.CTkButton(self.root, text="Upload File", command=self.browse_file, corner_radius=10, fg_color="#FE7060", font=('Roboto', 14, 'bold'))
        self.browse_button.pack(pady=5)



        canvas_height = 250
        canvas_width = 300
        border_width = 6
        dash_length = 40
        self.canvas = tk.Canvas(self.root, height=canvas_height, width=canvas_width, bg="#3D4861", highlightthickness=0,highlightbackground="#3F98D9",highlightcolor="#1E2637")
        self.canvas.create_line(1, 0, 1, canvas_height, dash=(dash_length, dash_length), width=border_width, fill="#EFEEEE")#down
        self.canvas.create_line(1, 1, canvas_width, 1, dash=(dash_length, dash_length), width=border_width, fill="#EFEEEE")#right
        self.canvas.create_line(canvas_width-2, 0, canvas_width-2, canvas_height-1, dash=(dash_length, dash_length), width=border_width, fill="#EFEEEE")#down
        self.canvas.create_line(0, canvas_height-1, canvas_width, canvas_height-1, dash=(dash_length, dash_length), width=border_width, fill="#EFEEEE")#right
        label_text = "Choose a file or drop it here"
        label_font = ("Roboto", 14)
        label_color = "#FFFFFF"
        self.choose_label = self.canvas.create_text(
            canvas_width // 2,
            canvas_height // 2,
            text=label_text,
            font=label_font,
            fill=label_color,
            tags="drag_label"
        )
    
        self.canvas.pack(pady=10)

        self.file_icon_label = self.create_icon_label(self.file_icon, "Folder name:   ")
        self.pages_icon_label = self.create_icon_label(self.pages_icon, "Total pages:    ")
        self.cost_icon_label = self.create_icon_label(self.cost_icon, "Cost/payment:")
        self.create_icon_label2(self.tk_icon_image,"Choose a file or drag it here", )
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self.on_drop)
   
    def create_icon_label2(self, icon_image, text):
        icon_frame = tk.Frame(self.canvas, bg="#3D4861")
        
        text_label = tk.Label(icon_frame, text=text, font=("Roboto", 14), bg="#3D4861", fg="#FFFFFF")
        text_label.pack(side="top", pady=(0, 5)) 
        
        
        icon_label = tk.Label(icon_frame, image=icon_image, bg="#3D4861")
        icon_label.pack(side="bottom", pady=(0,50),padx=10)  
        
        
        canvas_center_x = self.canvas.winfo_width() // 2
        canvas_center_y = self.canvas.winfo_height() // 2
        
        offset_x = 150  # Adjust this value to move horizontally
        offset_y = 80   # Adjust this value to move vertically
        
        x_position = canvas_center_x + offset_x
        y_position = canvas_center_y + offset_y
        
        # Place the icon_frame inside the canvas
        self.canvas.create_window(x_position, y_position, window=icon_frame, tags="drag_label")



    def update_cost(self, event=None):
        directory_path = self.current_directory_path 

        if directory_path:
            self.process_directory(directory_path)
    
    def create_icon_label(self, icon, text):
        label_frame = tk.Frame(self.root, bg="#1E2637")
        icon_label = tk.Label(label_frame, image=icon, bg="#1E2637")
        text_label = tk.Label(label_frame, text=text, font=("Roboto", 12), background="#1E2637", fg="#71D4FF")
        value_label = tk.Label(label_frame, text="", font=("Roboto", 12), background="#1E2637", fg="#FFFFFF",width='17')

        icon_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
        text_label.grid(row=0, column=1, sticky="w")  # Stick to the left side
        value_label.grid(row=0, column=2, sticky="w")  # Stick to the right side

        label_frame.pack(pady=10)
        return value_label

    def load_icon(self, filename):
        icon_image = Image.open(filename)
        tk_image = ImageTk.PhotoImage(icon_image)
        return tk_image

    def browse_file(self):
        file_path = filedialog.askdirectory()
        print(file_path)
        if file_path:
            self.process_directory(file_path)

    def on_drop(self, event):
        try:
            file_path = event.data.strip('{}')
            if not file_path:
                return

            if os.path.isdir(file_path):
                self.process_directory(file_path)
        except Exception as e:
            print(f"Error processing dropped directory: {e}")

    def process_directory(self, directory_path):
        self.current_directory_path = directory_path

        num_pages = count_pages_in_directory(directory_path)
        starting_cost = float(self.starting_cost.get())
        cost_per_page = float(self.cost_per_page.get())
        cost = starting_cost + max(0, num_pages - 10) * cost_per_page

        file= os.path.basename(directory_path)
        self.update_value_label(self.file_icon_label, f"{file}")
        self.update_value_label(self.pages_icon_label, f"{num_pages}")
        self.update_value_label(self.cost_icon_label, f"{cost:.2f}₪")

    def update_value_label(self, label, text,width=0):
        padded_text = f"{text:<{width}}"  
        
        label["text"] =  padded_text
    
    def on_enter(self, event):
        self.canvas.itemconfigure("drag_label", state=tk.HIDDEN)
        


    def on_leave(self, event):
        self.canvas.itemconfigure("drag_label", state=tk.NORMAL)
        self.canvas.config(bg="#3D4861")  

if __name__ == "__main__":
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    icon_path = os.path.join(base_path, "icons", "lucky_icon.ico")

    root = TkinterDnD.Tk()

    app = DragAndDropApp(root)
    tk_icon_image = app.load_icon(icon_path)

    root.iconphoto(True, tk_icon_image)
    root.mainloop()