from PIL import Image, ImageTk
import json
import customtkinter as ctk
import pandas as pd


def col_width():
    with open("resources/columns_width.json", "r") as json_file:
        cols_width = json.load(json_file)
    return cols_width


def show_img(frame):
    try:
        image = Image.open("resources/wiliot.png")
        image = image.resize((150, 75))
        tk_image = ImageTk.PhotoImage(image)
        image_label = ctk.CTkLabel(frame, text="", image=tk_image)
        image_label.image = tk_image
        image_label.place(x=1020, y=0)
    except:
        print("image was not found")


def can_be_int(value):
    try:
        val = int(value)
        return val < 10000
    except ValueError:
        return False


def create_tags_df(request_df):
    rows = []
    for i, row in request_df.iterrows():
        for x in range(int(row['First Tag']), int(row['Last Tag']) + 1):
            rows.append(row['Ex. ID Prefix'] + "T" + str(x).zfill(4))
    rows = set(rows)
    return pd.DataFrame([[row] for row in rows], columns=['tagId']).sort_values('tagId')


def verify_file(df):
    if not all((df['Ex. ID Prefix'].str.len() >= 4)):
        raise ValueError(f"Not all values for column 'Ex. ID Prefix' are correct\n"
                         "please verify that all values at least 4 letters")

    if not df['First Tag'].apply(can_be_int).all():
        raise ValueError(f"Not all values for column 'First Tag' are numbers and under 10000")

    if not df['Last Tag'].apply(can_be_int).all():
        raise ValueError(f"Not all values for column 'Last Tag' are numbers and under 10000")

    if not df['To Owner'].apply(lambda x: x != "").all():
        raise ValueError(f"To Owner column has empty values")

    for i, row in df.iterrows():
        if str(row['First Tag']).zfill(4) > str(row['Last Tag']).zfill(4):
            raise ValueError(f"First Tag is bigger than Last Tag\n"
                             f"({row['Ex. ID Prefix']}, {row['First Tag']}, {row['Last Tag']})")
