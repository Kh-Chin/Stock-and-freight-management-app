import re
import datetime
import pyodbc
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.button import MDRectangleFlatButton
from connection import Connection
from freight_algorithm import small_pack, big_pack
from python_widgets import ResultDialog, ParcelTable, OrderTable, PriceTable


class AppPopup(Popup):
    # Declare a popup class, its attributes and functions will be listed in the kivy file
    pass


class OrderPopup(AppPopup):
    # Declare a popup class, its attributes and functions will be listed in the kivy file
    pass


class SubmitButton(MDRectangleFlatButton):
    # Declare a button class, its attributes and functions will be listed in the kivy file
    pass


class AllButton(Button):
    # Declare a button class, its attributes and functions will be listed in the kivy file
    pass


class HeaderButton(AllButton):
    # Declare a button class, its attributes and functions will be listed in the kivy file
    pass


class StockAndFreightManagementApp(MDApp):
    def __init__(self, **kwargs):
        self.nulls = ("", "None")
        self.Mno = None
        self.Eno = None
        self.latest = False
        self.connection_type = "Guest"
        self.price_table1 = None
        self.price_table2 = None
        self.parcel_data_tables = None
        self.order_data_tables = None
        self.pack_order_table = None
        self.profile_button = None
        self.login_button = None
        self.collect_order_button = None
        self.pay_button = None
        self.pack_order_button = None
        super().__init__(**kwargs)

    def build(self):
        # Init function for kivy app
        # Read kivy layout file
        LabelBase.register(name="msyh", fn_regular="Font/msyh.ttf")
        theme_font_styles.append('msyh')
        self.theme_cls.font_styles["msyh"] = ["msyh"]
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.secondary_hue = "300"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "BlueGray"
        Window.maximize()

        return Builder.load_file("app_hierarchy.kv")

    def sql_query(self, query, *args, popup=False):
        # Handle all SQL query and open popup window after query.
        with Connection() as cursor:
            title = "Result"
            result_table = []
            try:
                cursor.execute(query, args)
                text = "Successful!"
                if cursor.rowcount == -1:
                    result_table = cursor.fetchall()
            except pyodbc.Error as ex:
                text = ex.args[-2] + ex.args[-1]

        if popup:
            self.open_dialog(title, text)

        return result_table

    def open_dialog(self, title, text):
        # Open popup dialog
        ResultDialog(title, text).open()

    def sanitize_input(self, *args):
        args = list(args)
        for i in range(len(args)):
            args[i] = None if args[i].strip() in self.nulls else args[i]
        return args

    def sign_up(self, username, pwd, email, rname, tel, addr):
        # Sign up an user account
        num = str(self.number_counter("signup"))
        mno = "M" + num.zfill(6)
        username, pwd, email, rname, tel, addr = self.sanitize_input(username, pwd, email, rname, tel, addr)
        query = "INSERT INTO Member(MNo,Username,Pwd,Email,Rname,Rtel,RAddress) VALUES(?,?,?,?,?,?,?);"
        self.sql_query(query, mno, username, pwd, email, rname, tel, addr, popup=True)

    def login(self, username, password, employee=False):
        # User and Employee Login
        if not username or not password:
            return
        title = "Login"
        query = "EXEC compare_pwd_employee ?, ?;" if employee else "EXEC compare_pwd_member ?, ?;"
        data = self.sql_query(query, username, password, popup=False)
        if data:
            self.Mno = data[0][0] if not employee else None
            self.Eno = data[0][0] if employee else None
            text = "Welcome!"
            self.connection_type = data[0][1] if employee else 'User'
            self.login_change_header()
            self.root.ids.App_Screen.current = "HomePage"
        else:
            text = "Wrong ID and Password Combination! Please Try Again!"
        self.open_dialog(title, text)

    def login_change_header(self):
        # Change icon after login
        release_type = self.user_info_screen if self.connection_type == "User" else self.employee_info_screen
        self.profile_button = HeaderButton(
            background_color= (0, 0, 0, 1),
            background_normal="Image/Profile1.png",
            background_down="Image/Profile1.png",
            width="170dp",
            on_release=release_type)
        self.root.ids.Header.ids.HeaderFunctionList.remove_widget(self.login_button)
        self.root.ids.Header.ids.HeaderFunctionList.add_widget(self.profile_button)

    def user_info_screen(self, instance):
        # Display user info
        query = "SELECT Username, Email, Rname, Rtel, RAddress, RAddress1, RAddress2 FROM MEMBER WHERE MNo =? "
        info_list = self.sql_query(query, self.Mno, popup=True)[0]
        path = self.root.ids.UserInfoPage.ids
        path.UserInfoMno.text = f"Your Member No: {self.Mno}"
        path.UserInfoUsername.text = f"Username: {info_list[0]}"
        path.UserInfo_Email.text = f"{info_list[1]}"
        path.UserInfo_Receiver.text = f"{info_list[2]}"
        path.UserInfo_Telephone.text = f"{info_list[3]}"
        path.UserInfo_Address.text = f"{info_list[4]}"
        path.UserInfo_Address1.text = f"{info_list[5]}"
        path.UserInfo_Address2.text = f"{info_list[6]}"
        self.root.ids.App_Screen.current = "UserInfoPage"

    def renew_info(self, email, rname, rtel, raddress, raddress1, raddress2, pwd, confirm_pwd):
        # Renew user info
        email, rname, rtel, raddress, raddress1, raddress2, pwd, confirm_pwd = self.sanitize_input(email, rname, rtel, raddress, raddress1, raddress2, pwd, confirm_pwd)
        query = "EXEC renew_user ?, ?, ?, ?, ?, ?, ?, ?;"
        if pwd == confirm_pwd:
            self.sql_query(query, self.Mno, email, pwd, rname, rtel, raddress, raddress1, raddress2, popup=True)
        else:
            title = "Error"
            text = "Two passwords that you entered are not the same!"
            self.open_dialog(title, text)

    def log_out(self):
        # Log out
        self.Mno = None
        self.Eno = None
        self.latest = False
        self.connection_type = "Guest"
        self.root.ids.Header.ids.HeaderFunctionList.remove_widget(self.profile_button)
        self.root.ids.Header.ids.HeaderFunctionList.add_widget(self.login_button)
        title = "Log out"
        text = "Log out successful!"
        self.open_dialog(title, text)
        self.root.ids.App_Screen.current = "HomePage"

    def employee_info_screen(self, instance):
        # Display employee info
        info_list = self.sql_query("SELECT Username, Etype FROM Employee WHERE ENo =? ", self.Eno, popup=False)[0]
        path = self.root.ids.EmployeeInfoPage.ids
        path.EmployeeInfoEno.text = f"Your Employee No: {self.Eno}"
        path.EmployeeInfoUsername.text = f"Username: {info_list[0]}"
        path.EmployeeInfoEtype.text = f"Type:{info_list[1]}"
        self.root.ids.App_Screen.current = "EmployeeInfoPage"

    def load_price(self):
        # Load every price of freight option
        if self.price_table1:
            return
        table1 = self.sql_query("SELECT * FROM SeaFreight_SmallParcel;", popup=False)
        table2 = self.sql_query("SELECT * FROM SeaFreight_LargeParcel;", popup=False)
        self.price_table1 = PriceTable(table=table1, table_type="kg")
        self.price_table2 = PriceTable(table=table2, table_type="m3")
        path = self.root.ids.PricePage.ids
        path.SmallPackPriceHolder.add_widget(self.price_table1)
        path.BigPackPriceHolder.add_widget(self.price_table2)

    def key_in_parcel(self, pno, pname):
        self.sql_query("EXEC insert_parcel ?, ?, ?, ?;", pno, self.Mno, pname, "未入库", popup=True)
        self.latest = False
        self.root.Parcel_In_Window.dismiss()

    def employee_key_in_parcel(self, pno, pweight, prack):
        query = "EXEC employee_insert_parcel ?, ?, ?, ?, ?;"
        self.sql_query(query, pno, pweight, datetime.datetime.now(), prack, "已入库", popup=True)
        self.root.Employee_Parcel_In_Window.dismiss()

    def reload_parcel(self):
        # Reload parcel information
        table = []
        if self.connection_type == "User":
            table = self.sql_query("SELECT * FROM Parcel_View WHERE MNo = ?;", self.Mno, popup=True)
        elif self.connection_type in ("Employee", "Manager"):
            table = self.sql_query("SELECT * FROM Parcel;", popup=True)
        return table

    def load_parcel(self):
        # Load parcel page
        if self.connection_type not in ("User", "Employee", "Manager"):
            return
        if not self.latest:
            table = self.reload_parcel()
            self.parcel_data_tables = ParcelTable(table, user=self.connection_type)
        self.root.ids.CheckParcelPage.ids.ParcelListButton.disabled = True if self.connection_type != "User" else False
        self.root.ids.CheckParcelPage.ids.ParcelList.add_widget(self.parcel_data_tables)

    def load_order(self):
        # Load all order information
        table = []
        self.collect_order_button = SubmitButton(text="收齐订单", on_press=self.collect_order)
        self.pay_button = SubmitButton(text="付款", on_press=self.pay)
        self.pack_order_button = SubmitButton(text="包装订单", on_press=self.order_popup)
        if self.connection_type == "User":
            query = "SELECT OrderNo,OrderDate, MNo, ShipAddress, PackageQuantity, Ostatus FROM Orders WHERE MNo = ?;"
            table = self.sql_query(query, self.Mno, popup=True)
            self.root.ids.LogisticsPage.ids.OrderListButtonHolder1.add_widget(self.pay_button)
        elif self.connection_type in ("Employee", "Manager"):
            query = "SELECT OrderNo,OrderDate, MNo, ShipAddress, PackageQuantity, Ostatus FROM Orders;"
            table = self.sql_query(query, popup=True)
            self.root.ids.LogisticsPage.ids.OrderListButtonHolder1.add_widget(self.collect_order_button)
            self.root.ids.LogisticsPage.ids.OrderListButtonHolder2.add_widget(self.pack_order_button)
        self.order_data_tables = OrderTable(table=table)
        self.root.ids.LogisticsPage.ids.OrderList.add_widget(self.order_data_tables)

    def create_order(self):
        # Create an order
        table = self.parcel_data_tables.get_row_checks()
        if len(table) > 0 and all(re.findall("已入库", item[-2]) for item in table):
            num = str(self.number_counter(counter_type="order"))
            ono = "MY" + num.zfill(11)
            address = self.sql_query("SELECT RAddress FROM MEMBER WHERE MNo = ?", self.Mno, popup=False)[0][0]
            query = "INSERT INTO Orders (OrderNo, OrderDate, MNo, ShipAddress, PackageQuantity, OStatus) VALUES(?,?,?,?,?,?);"
            self.sql_query(query, ono, datetime.datetime.now(), self.Mno, address, len(table), "待处理", popup=True)
            for item in table:
                self.sql_query("UPDATE Parcel SET OrderNo=?,PStatus=? WHERE PNo=?", ono, "待收齐", item[0], popup=False)
            self.latest = False
        else:
            title = "Error"
            text = "You can only create order with parcels which are already in the Warehouse!"
            self.open_dialog(title, text)

    def pay(self, instance):
        # User payment
        table = self.order_data_tables.get_row_checks()
        if len(table) and all(re.findall("待付款", item[-1]) for item in table):
            for item in table:
                self.sql_query("UPDATE Orders SET OStatus =? WHERE OrderNo=?;", "待运输", item[0], popup=False)
                self.sql_query("UPDATE Parcel SET PStatus=? WHERE OrderNo=?;", "已包装", item[0], popup=True)

        else:
            title = "Error"
            text = "You can only pay for the packed order!"
            self.open_dialog(title, text)

    def collect_order(self, instance):
        # Employee has done collecting all the parcel for the orders, and is waiting for packaging
        if self.connection_type in ("Employee", "Manager"):
            table = self.order_data_tables.get_row_checks()
            if len(table) and all(re.findall("待处理", item[-1]) for item in table):
                for item in table:
                    self.sql_query("UPDATE Parcel SET PStatus=? WHERE OrderNo=?", "待包装", item[0], popup=False)
                    self.sql_query("UPDATE Orders SET OStatus=? WHERE OrderNo=?", "待包装", item[0], popup=True)
                self.latest = False
            else:
                title = "Error"
                text = "Unable to collect the order!"
                self.open_dialog(title, text)

    def order_popup(self, instance):
        # Open popup window to fill in the order packing details
        if self.connection_type in ("Employee", "Manager"):
            self.pack_order_table = self.order_data_tables.get_row_checks()
            if len(self.pack_order_table) == 1 and re.findall("待包装", self.pack_order_table[0][-1]):
                OrderPopup().open()
            else:
                title = "Error"
                text = "Unable to pack the order! You can only choose one order at a time!"
                self.open_dialog(title, text)

    def pack_order(self, weight, length, width, height):
        # Pack all parcels in order
        ono = self.pack_order_table[0][0]
        m3, price, priceID = self.calculate(weight, length, width, height, calc_type="order")
        query = "UPDATE Orders SET OWeight_kg =?, OVolume_M3 =?, Freight =?, PriceID =?, OStatus =? WHERE OrderNo=?;"
        self.sql_query(query, weight, m3, price, priceID, "待付款", ono, popup=False)
        self.sql_query("UPDATE Parcel SET PStatus=? WHERE OrderNo=?", "已包装", ono, popup=True)
        self.latest = False

    def number_counter(self, counter_type):
        # Generate ID for user and order
        counter = -1
        counters, = self.sql_query("SELECT * FROM Generator", popup=False)
        if counter_type == "signup":
            counter = counters[0]
            counter += 1
            self.sql_query("UPDATE Generator SET MNo_Generator = ?", counter, popup=False)
        if counter_type == "order":
            counter = counters[1]
            counter += 1
            self.sql_query("UPDATE Generator SET OrderNo_Generator = ?", counter, popup=False)
        return counter

    def calculate(self, weight, length, width, height, calc_type="calculator"):
        # Calculate price for freight
        weight = float(weight)
        length = float(length)
        width = float(width)
        height = float(height)
        m3 = length * width * height / 100000
        small_pack_price, price_ID1 = small_pack(weight, width, height, length)
        big_pack_price, price_ID2 = big_pack(m3)
        if calc_type == "calculator":
            self.root.ids.CalculatePage.ids.Fee1.text = str(small_pack_price)
            self.root.ids.CalculatePage.ids.Fee2.text = str(big_pack_price)
        elif calc_type == "order":
            price = big_pack_price if small_pack_price > big_pack_price else small_pack_price
            price_id = price_ID2 if small_pack_price > big_pack_price else price_ID1
            return m3, price, price_id


if __name__ == "__main__":
    StockAndFreightManagementApp().run()
