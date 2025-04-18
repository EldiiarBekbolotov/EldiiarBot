import tkinter as tk
window = tk.Tk()
window.title("My GUI App")
window.geometry("400x300")  # Set window size
label = tk.Label(window, text="Hello, Tkinter!")
label.pack()  # Add label to window

button = tk.Button(window, text="Click Me", command=lambda: label.config(text="Button Clicked!"))
button.pack()  # Add button to window
window.mainloop()  # Starts the GUI event loop