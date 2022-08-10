import tkinter as tk
from datetime import datetime, date
from tkinter import filedialog


def check_date():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    today = date.today()
    # try:
    with open(file_path, "r") as f:
        file_str = f.read()
        license_date = date(int(file_str[0:4]), int(file_str[5:7]), int(file_str[8:10]))
        day_diff = (today - license_date).days
        if -1 < day_diff < 15:
            return "Success"
        else:
            return "Date Expired"
    # except Exception as e:
    #     raise e
    #     return "Invalid file"
