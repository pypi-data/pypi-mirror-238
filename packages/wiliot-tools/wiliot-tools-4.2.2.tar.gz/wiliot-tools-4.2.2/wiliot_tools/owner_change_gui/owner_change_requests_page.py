import threading
import customtkinter as ctk
import pandas as pd
from wiliot_tools.owner_change_gui.owner_change_utils import show_img


class OwnerChangeRequests(ctk.CTkFrame):
    def __init__(self, parent, show_page_callback):
        super().__init__(parent)
        self.parent = parent
        self.show_page_callback = lambda: show_page_callback(self)

        label = ctk.CTkLabel(self, text="Owner Change Requests", font=("Arial", 28, "bold"))
        label.pack(pady=50)
        if self.parent.requests_df is None:
            try:
                self.parent.requests_df = pd.read_csv('data/requests.csv', index_col=0, dtype=str)
            except FileNotFoundError:
                self.parent.requests_df = pd.DataFrame(columns=self.parent.requests_cols)
        # df = self.parent.df
        self.tree = self.parent.create_tree_view(self, self.parent.requests_df, equal_width=False)
        self.tree.tag_configure('red', foreground='#d44e2a')
        self.tree.tag_configure('green', foreground='#39a987')
        self.tree.tag_configure('yellow', foreground='#FFBF00')
        self.tree.tag_configure('orange', foreground='orange')
        self.tree.pack(pady=20, padx=20)
        self.color_requests()

        btn = ctk.CTkButton(master=self, text="Request Details", command=self.request_details, width=220,
                            font=('Helvetica', 14))
        btn.place(x=self.parent.W / 2 - 110, y=self.parent.H - 150)

        self.delete_btn = ctk.CTkButton(master=self, text="Delete Selected", command=lambda: self.delete(), width=220,
                                        font=('Helvetica', 14))
        self.delete_btn.place(x=50, y=self.parent.H - 150)

        self.delete_btn = ctk.CTkButton(master=self, text="Delete All", command=lambda: self.delete(all=True),
                                        width=220,
                                        font=('Helvetica', 14))
        self.delete_btn.place(x=50, y=self.parent.H - 100)

        btn = ctk.CTkButton(self, text="Create Request (Multiple Reels)", command=self.show_page_callback, width=220)
        btn.place(x=self.parent.W - 270, y=self.parent.H - 100)

        btn = ctk.CTkButton(self, text="Create Request (One Reel)",
                            command=lambda: self.parent.show_send_request_one_reel_page(self),
                            width=220)
        btn.place(x=self.parent.W - 270, y=self.parent.H - 150)
        show_img(self)
        self.after(1, self.refresh)

    def request_details(self):
        items = self.tree.selection()
        if len(items) == 0:
            self.parent.show_error_popup("No Request Was Selected!")
            return
        item = items[0]
        if self.tree.item(item, "values")[3] != 'processed':
            self.parent.show_error_popup("The Request has not been Processed Yet!")
            return
        request_id = self.tree.item(item, "values")[0]
        self.parent.show_request_details_page(request_id, self)

    def color_requests(self):
        for i, item in enumerate(self.tree.get_children()):
            values = self.tree.item(item, "values")
            if values[3] in ('not-started', 'processing'):
                self.tree.item(item, tags=('yellow',))
            elif values[3] == 'failed':
                self.tree.item(item, tags=('red',))
            elif values[3] == 'processed' and int(values[6]) == int(values[4]):
                self.tree.item(item, tags=('red',))
            elif values[3] == 'processed' and int(values[6]) > 0:
                self.tree.item(item, tags=('orange',))
            elif values[3] == 'processed':
                self.tree.item(item, tags=('green',))

    def sync(self):
        self.parent.requests_df = pd.DataFrame(
            [self.tree.item(item, "values") for item in self.tree.get_children()],
            columns=self.parent.requests_cols
        )

    def update_requests(self):
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values[3] in ('not-started', '-', 'processing'):
                response, status_code = self.parent.get_request_status(values[0])
                if status_code == 200:
                    new_values = list(response.values())[:7] + [values[7]]
                    new_values = ['-' if str(v) == 'None' else v for v in new_values]
                    self.update_item(item, new_values)
                else:
                    values = list(values)
                    values[3] = 'failed'
                    self.update_item(item, values)
                    print(f"API Response {status_code}, Response: {response}")

        self.color_requests()
        self.sync()
        self.parent.save_data()

    def refresh(self):
        print('Refreshing Requests!')
        threading.Thread(target=self.update_requests).start()
        self.after(30000, self.refresh)

    def update_item(self, item_id, new_values):
        self.tree.item(item_id, values=new_values)

    def delete(self, all=False):
        if all:
            items = self.tree.get_children()
        else:
            items = self.tree.selection()
            if len(items) == 0:
                self.parent.show_error_popup("No Request Was Selected!")
                return
        for item in items:
            self.tree.delete(item)
        self.sync()
