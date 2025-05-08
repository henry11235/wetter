import tkinter as tk

root = tk.Tk()
root.title("Wetter App")
root.geometry("400x300")
root.update_idletasks()  # Make sure window is updated
root.geometry("400x300")  # Force geometry again after window is created

if __name__ == "__main__":
    root.mainloop()
