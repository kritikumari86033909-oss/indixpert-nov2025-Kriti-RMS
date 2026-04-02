import json
import os
from datetime import datetime
from App.menu.manage_menu import ManageMenu
from App.booking.table_booking import Booking
from App.report.project_info import Report

class AdminDashboard:

    def __init__(self):
        self.order_path = os.path.join("App", "database", "orders.json")
    def admin_menu(self):

        menu=ManageMenu()

        while True:
            
            print("\n" + "="*45)
            print("              ADMIN DASHBOARD              ")
            print("="*45)
            print("1 - MANAGE MENU")
            print("2 - VIEW ORDER")
            print("3 - TABLE BOOKING")
            print("4 - REPORT")
            print("5 - DELETE ORDER")
            print("6 - TODAY's SALES")
            print("7 - LOGOUT")
            print("="*45)
         
            choice = input("Enter your choice: ").strip()

            if not choice.isdigit():
                print("please enter number only")
                continue
            
            # -------- MENU MANAGEMENT --------    
            if choice == "1":

                while True:

                    print("\n" + "="*45)
                    print("               MENU MANAGEMENT               ")
                    print("="*45)
                    print("1 Add item")
                    print("2 View menu")
                    print("3 Update item")
                    print("4 Delete item")
                    print("5 Back")
                    print("="*45)
                    
                    option = input("Enter choice: ").strip()

                    if not option.isdigit():
                        print("please enter number only")
                        continue

                    if option == "1":
                        menu.add_food()

                    elif option == "2":
                        menu.view_menu()

                    elif option == "3":
                        menu.update_food()

                    elif option == "4":
                        menu.delete_food()

                    elif option == "5":
                    
                        break

                    else:
                        print("invailed choice")
                    
            elif choice == "2":
                self.view_orders()
                
            elif choice == "3":
                booking=Booking()

                while True:

                    print("\n" + "="*45)
                    print("                 BOOKING MENU                 ")
                    print("="*45)
                    print("1 Add Booking")
                    print("2 View Booking")
                    print("3 Delete Booking")
                    print("4 Update Booking")
                    print("5 Customer History")
                    print("6 Back")
                    print("="*45)


                    opt = input("Enter choice: ").strip()


                    if opt == "1":
                        booking.add_booking()

                    elif opt == "2":
                        booking.view_booking()

                    elif opt == "3":
                        booking.delete_booking()

                    elif opt == "4":
                        booking.update_booking()

                    elif opt == "5":
                        booking.customer_history()

                    elif opt == "6":
                        break

                    else:
                        print("Invalid choice")
                   
            elif choice == "4":
                report = Report()
                report.generate_report()
                

            elif choice == "5":
                self.delete_order()
            

            elif choice == "6":
                self.today_sales()
        
                
            elif choice == "7":
                print("Logout Successfuly")
                break

            else:
                print("Invalid Choice")

    def view_orders(self):

        if not os.path.exists(self.order_path):
            print("no ordered founr")
            return
        
        with open(self.order_path, "r") as file:
            try:
                orders=json.load(file)
            except:
                print("No data found")
                return

        if not orders:
            print("No orders available")
            return     

        print("\n========ORDER HISTORY========")

        for order in orders: 
            print(f"Order ID: {order.get('order_id')}")
            print(f"Subtotal: ₹{order.get('subtotal')}")
            print("-" * 50)
            print(f"{'ITEM':<25}{'QTY':<10}{'PRICE':<10}")
            print("-" * 50)  

            for item in order.get("items", []):
                print(f"{item['name']:<25}{item['qty']:<10}{item['total']:<10}")

            print("-" * 50)

     # -------- DELETE ORDER --------
    def delete_order(self):

        if not os.path.exists(self.order_path):
            print("No orders found")
            return

        
        with open(self.order_path, "r") as file:
            try:
                orders = json.load(file)
            except:
                print("no data found")
                return    

        order_id = input("Enter Order ID to delete: ").strip()

        new_orders = []
        for i in orders:
            if i["order_id"]!=order_id:
                new_orders.append(i)


        if len(orders) == len(new_orders):
            print("Order ID not found")
            return


        with open(self.order_path, "w") as file:
            json.dump(new_orders, file, indent=4)

        print("Order deleted successfully") 


    def sales_report(self):

        if not os.path.exists(self.order_path):
            print("No data found") 
            return

        with open(self.order_path, "r") as file:
            try:
                orders=json.load(file)
            except:
                print("Error recording data")
                return

        total_orders= len(orders)
        total_sales=0
        
        for order in orders:
            total_sales = total_sales+order.get("subtotal", 0)

    
        print("\n===== SALES REPORT =====")
        print(f"Total Orders: {total_orders}")
        print(f"Total Sales: ₹{total_sales}")  

    
    # -------- TODAY SALES --------
    def today_sales(self):

        if not os.path.exists(self.order_path):
            print("No orders found")
            return
        
        today = datetime.now().strftime("%d-%m-%Y")
        try:
            with open(self.order_path, "r") as file:
                orders = json.load(file)
        except:
            print("no data found")   
            return     

        today_orders = []

        for o in orders:
            if o.get("date") == today:
                today_orders.append(o)

        total = 0
        for o in today_orders:
            total = total+o.get("subtotal", 0)        

        print("\n===== TODAY SALES =====")
        print("Orders Today:", len(today_orders))
        print("Today's Revenue: ₹", total)
                       
    

                