from scraper import Scraper
    
import tkinter as tk
from tkinter import ttk
import time


def process_data(field, area, city, country):
    sc = Scraper()
    link = sc.link_constructor(field, area, city, country)
    sc.pipeline(link)

# Function to handle the button click event
def scrape_details():
    # Get the data from the input fields
    field = entries["Field"].get()
    # area = entries["Area"].get()
    area = None
    city = entries["City"].get()
    country = entries["State"].get()
    
    # Change label to show "Collecting Data"
    status_label.config(text="Collecting Data", foreground="orange")
    root.update_idletasks()
    
    # Call the function to process the data
    process_data(field, area, city, country)
    
    # Change label to show "Results Gathered"
    status_label.config(text="Scrape Complete", foreground="green")
    
    
root = tk.Tk()
root.title("Data Scraper")
root.geometry("300x300")
root.configure(bg="#f0f0f0")

# Set a consistent style
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12, "bold"), background="#4CAF50", foreground="white")

# Create and place input fields and labels
# labels = ["Field", "Area", "City", "Country"]
labels = ["Field","City", "State"]
entries = {}

for i, label_text in enumerate(labels):
    label = ttk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
    
    entry = ttk.Entry(root, width=30)
    entry.grid(row=i, column=1, padx=10, pady=10)
    entries[label_text] = entry

# Create and place the button
# scrape_button = ttk.Button(root, text="Scrape Details", command=scrape_details)
# scrape_button.grid(row=len(labels), columnspan=2, pady=20)
# Create a custom style for the button
# Create and place the button using tk.Button
scrape_button = tk.Button(root, text="Scrape Details", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=scrape_details)
scrape_button.grid(row=len(labels), columnspan=2, pady=20)

# Create and place the status label
status_label = ttk.Label(root, text="", font=("Helvetica", 12, "italic"))
status_label.grid(row=len(labels) + 1, columnspan=2, pady=10)

# Start the main event loop
root.mainloop()