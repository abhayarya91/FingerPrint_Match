import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import Label, Button, StringVar

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at {image_path} could not be loaded. Check the file path.")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    size = (256, 256)
    image_resized = cv2.resize(gray_image, size)
    return image_resized

def compute_histogram(image):
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
    return histogram

def compare_histograms(hist1, hist2):
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return correlation

def compare_fingerprints(image_path1, image_path2):
    img1 = preprocess_image(image_path1)
    img2 = preprocess_image(image_path2)
    hist1 = compute_histogram(img1)
    hist2 = compute_histogram(img2)
    correlation = compare_histograms(hist1, hist2)
    threshold = 0.7
    return correlation > threshold

class FingerprintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fingerprint Matcher")
        self.root.config(bg="#e6f7ff")  # Light blue background

        # Set the size of the window (5 cm x 5 cm ≈ 189 pixels x 189 pixels)
        self.root.geometry("189x189")
        
        self.file_path1 = ""
        self.file_path2 = ""

        # Create GUI elements with updated styles
        self.label1 = Label(root, text="Select the first fingerprint image:", bg="#e6f7ff", font=("Arial", 12, "bold"))
        self.label1.pack(pady=5)
        
        self.button1 = Button(root, text="Browse Image 1", command=self.load_image1, bg="#4da6ff", fg="white", font=("Arial", 10, "bold"))
        self.button1.pack(pady=3)

        self.label2 = Label(root, text="Select the second fingerprint image:", bg="#e6f7ff", font=("Arial", 12, "bold"))
        self.label2.pack(pady=5)

        self.button2 = Button(root, text="Browse Image 2", command=self.load_image2, bg="#4da6ff", fg="white", font=("Arial", 10, "bold"))
        self.button2.pack(pady=3)

        self.compare_button = Button(root, text="Compare", command=self.compare_images, bg="#0066cc", fg="white", font=("Arial", 12, "bold"))
        self.compare_button.pack(pady=10)

        self.result_var = StringVar()
        self.result_label = Label(root, textvariable=self.result_var, bg="#e6f7ff", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=5)

    def load_image1(self):
        self.file_path1 = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.file_path1:
            self.label1.config(text=f"Selected Image 1: {self.file_path1.split('/')[-1]}", fg="green")
        else:
            self.label1.config(text="No Image 1 Selected", fg="red")

    def load_image2(self):
        self.file_path2 = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.file_path2:
            self.label2.config(text=f"Selected Image 2: {self.file_path2.split('/')[-1]}", fg="green")
        else:
            self.label2.config(text="No Image 2 Selected", fg="red")

    def compare_images(self):
        if not self.file_path1 or not self.file_path2:
            messagebox.showwarning("Warning", "Please select both images.")
            return

        try:
            if compare_fingerprints(self.file_path1, self.file_path2):
                self.result_var.set("The fingerprints are likely the same.")
                self.result_label.config(fg="green")
            else:
                self.result_var.set("The fingerprints are likely different.")
                self.result_label.config(fg="red")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = FingerprintApp(root)
    root.mainloop()
