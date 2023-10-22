import rembg
import os
import socket
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        bg_color = "black"  # Hex color code for dark gray
        self.root.configure(bg=bg_color)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Calculate the x and y coordinates for centering the window
        x_coordinate = (screen_width - 1100) // 2
        y_coordinate = (screen_height - 550) // 2
        # Set initial geometry and position the window
        self.root.geometry(f"1100x550+{x_coordinate}+{y_coordinate}")
        self.selected_image = None
        self.processed_image_path = None
        if self.is_online():
            self.setup_online_ui()
        else:
            self.setup_offline_ui()
        
        
        
        
    def setup_online_ui(self):
        # Buttons
        self.select_button = tk.Button(root, text="Select Image", command=self.select_image, font=("times new roman", 15))
        self.select_button.pack(side="bottom", anchor="center", pady=150)
        self.settings_button = tk.Menubutton(root, text="⚙", font=("times new roman", 15))
        self.settings_menu = tk.Menu(self.settings_button, tearoff=0)
        self.settings_menu.add_command(label="Select folder", font=("times new roman", 15), command=self.select_folder_and_process)
        self.settings_button.config(menu=self.settings_menu)
        self.settings_button.pack(side="top",anchor="se",pady=20)
        self.next_button = tk.Button(root, text="Next", command=self.process_and_display_image, font=("times new roman", 15))
        self.next_button.pack(side="top")
        self.next_button.pack_forget()
        self.save_button = tk.Button(root, text="Save", command=self.save_image, font=("times new roman", 15))
        self.save_button.pack(side="top")
        self.save_button.pack_forget()
        self.back_button = tk.Button(root, text="Back", command=self.go_back, font=("times new roman", 15))
        self.back_button.pack(side="top")
        self.back_button.pack_forget()


        self.image_label = tk.Label(root)
        self.image_label.pack_forget()
        # Progress Bar
        self.progress_bar = None
        self.progress_generator = None
    def is_online(self):
        try:
        # Try to connect to Google's DNS server
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            return False
        
    def setup_offline_ui(self):
    # Set up the offline UI elements
        offline_label = tk.Label(self.root, text="Offline Mode", font=("times new roman", 20))
        offline_label.pack(side="top", pady=100)

        
    def select_folder_and_process(self):
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if image_files:
                self.back_button.pack_forget()
                self.save_button.pack_forget()
                self.root.after(1000, lambda: self.process_images_in_folder(folder_path, image_files, 0))
    
    def process_images_in_folder(self, folder_path, image_files, index):
        if index >= len(image_files):
            self.progress_bar.pack_forget()
            self.save_button.pack_forget()
            messagebox.showinfo("Batch Processing Complete", "all images save go to your selected folder.")
            return

        file_name = image_files[index]
        file_path = os.path.join(folder_path, file_name)
        input_image = Image.open(file_path)
        input_image.thumbnail((400, 400))  # Resize image to fit the window
        
        self.selected_image = input_image
        self.display_image()
        self.process_and_display_image()
        self.back_button.pack_forget()
        self.save_button.pack_forget()
        self.select_button.pack_forget()
        # Schedule the next image processing
        self.root.after(1000, lambda: self.process_images_in_folder(folder_path, image_files, index + 1))

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.selected_image = Image.open(file_path)
            self.selected_image.thumbnail((400, 400))  # Resize image to fit the window
            self.display_image()
            self.next_button.pack()
            self.select_button.pack_forget()
            self.settings_button.pack_forget()

    def display_image(self):
        if self.selected_image:
            img_tk = ImageTk.PhotoImage(self.selected_image)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
            self.image_label.pack()

    def process_and_display_image(self):
        if not self.selected_image:
            return

        self.progress_bar = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress_bar.pack()
        self.progress_bar.start()
        self.root.after(1000, self.complete_processing)

    def complete_processing(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
    
        self.process_image()
        #messagebox.showinfo("Background Removed", "Background has been successfully removed.")
        self.display_processed_image()
        self.save_button.pack()  # Show the "Save" button
        self.next_button.pack_forget()  # Hide the "Next" button
        self.back_button.pack()
    def process_image(self):
        if not self.selected_image:
            return

        img_name = os.path.basename(self.selected_image.filename)

        with open(self.selected_image.filename, 'rb') as f:
            input_data = f.read()

        self.processed_image_path = os.path.join(os.path.dirname(self.selected_image.filename), img_name.split('.')[0] + '_trulloy.png')

        subject = rembg.remove(input_data)
        with open(self.processed_image_path, 'wb') as output_file:
            output_file.write(subject)

    def display_processed_image(self):
        if not self.processed_image_path:
            return

        processed_image = Image.open(self.processed_image_path)
        processed_image.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(processed_image)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk
    

    def save_image(self):
        if not self.processed_image_path:
            return

        output_folder = filedialog.askdirectory(title="Select Your Output Folder")
        if output_folder:
            img_name = os.path.basename(self.processed_image_path)
            new_output_path = os.path.join(output_folder, img_name)
            os.rename(self.processed_image_path, new_output_path)
            messagebox.showinfo("Image Saved", "Image saved successfully.")
            self.processed_image_path = None  # Reset processed_image_path
            self.save_button.pack_forget()
            self.back_button.pack()
            
    def go_back(self):
        if self.processed_image_path:
            os.remove(self.processed_image_path)  # Remove the processed image
            self.processed_image_path = None

        self.selected_image = None
        self.display_image()
        self.next_button.pack_forget()
        self.save_button.pack_forget()
        self.back_button.pack_forget()
        self.select_button.pack(side="top")


    def on_closing(self):
        if self.processed_image_path:
            os.remove(self.processed_image_path)  # Remove the processed image
            self.processed_image_path = None
        self.root.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Call on_closing() when the window is closed
    root.mainloop()