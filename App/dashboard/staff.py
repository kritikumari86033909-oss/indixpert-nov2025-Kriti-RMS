from App.menu.view_food import ViewMenu
from App.order.order import Order
from App.dashboard.admin import AdminDashboard
from App.booking.table_booking import Booking

class StaffDashboard:

    def staff_menu(self):

        view = ViewMenu()
        order = Order()
        admin = AdminDashboard()   # booking reuse

        while True:

            print("\n===== STAFF DASHBOARD =====")
            print("1 - view menu")
            print("2 - order")
            print("3 - booking")
            print("4 - back")

            choice = input("Enter your choice: ")

            if choice == "1":
                view.view_food() 

            elif choice == "2":
                order.place_order()

            elif choice == "3":
                booking = Booking()

                while True:
                    print("\n===== BOOKING MENU =====")
                    print("1 Add Booking")
                    print("2 View Booking")
                    print("3 Back")

                    opt = input("Enter choice: ").strip()

                    if opt == "1":
                        booking.add_booking()

                    elif opt == "2":
                        booking.view_booking()

                    elif opt == "3":
                        break

                    else:
                        print("Invalid choice")

            elif choice == "4":
                print("Going Back")
                break

            else:
                print("Invalid Choice")