"""
This python file contains widgets that is highly related
with the operation logic and are not suitable to be defined
in kivy file.

Widgets include:
-ResultDialog and ResultDialogButton
-Tables class: ParcelTable, OrderTable
"""

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp


class ResultDialog(MDDialog):
    # Popup Dialog for query result
    def __init__(self, title, text, **kwargs):
        self.title = title
        self.text = text
        self.buttons = [ResultDialogButton(self)]
        super().__init__(**kwargs)


class ResultDialogButton(MDFlatButton):
    # Button in popup dialog
    def __init__(self, dialog, **kwargs):
        self.dialog = dialog
        self.text = "Ok"
        super().__init__(**kwargs)

    def on_release(self):
        self.dialog.dismiss()


class Tables(MDDataTable):
    # Main configuration for tables
    def __init__(self, **kwargs):
        self.rows_num = 200
        self.pos_hint = {'center_y': 0.5, 'center_x': 0.5}
        self.size_hint = (0.9, 0.6)
        self.check = True
        self.use_pagination = True
        super().__init__(**kwargs)


class ParcelTable(Tables):
    # Table for showing parcels
    def __init__(self, table, user="User", **kwargs):
        if user == "User":
            self.column_data = [
                ("ParcelNo", dp(50)),
                ("ParcelName", dp(50)),
                ("ParcelWeight", dp(50)),
                ("OrderNo", dp(50)),
                ("Parcel_Status", dp(50)),
                ("MemberNo", dp(50))
            ]
            self.row_data=[(
                f"{item[0]}",
                f"[font=Font/msyh]{item[1]}[/font]",
                f"{item[2]}",
                f"{item[3]}",
                f"[font=Font/msyh]{item[4]}[/font]",
                f"{item[5]}")
                for item in table
            ]
        else:
            self.column_data = [
                ("ParcelNo", dp(50)),
                ("MemberNo", dp(50)),
                ("ParcelWeight", dp(50)),
                ("ParcelName", dp(50)),
                ("Parcel_InTime", dp(50)),
                ("OrderNo", dp(50)),
                ("RackNo", dp(50)),
                ("Parcel_Status", dp(50))
            ]
            self.row_data=[(
                f"{item[0]}",
                f"{item[1]}",
                f"{item[2]}",
                f"[font=Font/msyh]{item[3]}[/font]",
                f"{item[4]}",
                f"{item[5]}",
                f"{item[6]}",
                f"[font=Font/msyh]{item[7]}[/font]")
                for item in table
            ]
        super().__init__(**kwargs)


class OrderTable(Tables):
    # Table for showing orders
    def __init__(self, table, **kwargs):
        self.column_data = [
            ("OrderNo", dp(50)),
            ("OrderDate", dp(50)),
            ("MemberNo", dp(50)),
            ("ShippingAddress", dp(100)),
            ("PackageQuantity", dp(50)),
            ("OrderStatus", dp(50))
        ]
        self.row_data = [(
            f"{item[0]}",
            f"{item[1]}",
            f"{item[2]}",
            f"{item[3]}",
            f"{item[4]}",
            f"[font=Font/msyh]{item[5]}[/font]")
            for item in table
        ]
        super().__init__(**kwargs)


class PriceTable(MDDataTable):
    # Table for showing price
    def __init__(self, table, table_type, **kwargs):
        self.column_data = [
            ("[font=Font/msyh]合作商名字[/font]", dp(30)),
            ("[font=Font/msyh]计价单位[/font]", dp(30)),
            (f"[font=Font/msyh]从({table_type})[/font]", dp(30)),
            (f"[font=Font/msyh]至({table_type})[/font]", dp(30)),
            (f"[font=Font/msyh]单位首重价格({table_type})[/font]", dp(30)),
            (f"[font=Font/msyh]单位续重价格({table_type})[/font]", dp(30)),
        ]
        self.row_data = [(
            f"[font=Font/msyh]{item[0]}[/font]",
            f"[font=Font/msyh]{item[1]}[/font]",
            f"[font=Font/msyh]{item[2]}[/font]",
            f"[font=Font/msyh]{item[3]}[/font]",
            f"[font=Font/msyh]{item[4]}[/font]",
            f"[font=Font/msyh]{item[5]}[/font]")
            for item in table
        ]
        super().__init__(**kwargs)
