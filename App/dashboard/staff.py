from App.menu.view_menu import ViewMenu
from App.order.order_item import Order
from App.booking.table_booking import Booking

class StaffDashboard:

    def staff_menu(self):

        view = ViewMenu()
        order = Order()
        booking = Booking()

        while True:

            print("\n===== STAFF DASHBOARD =====")
            print("1 - VIEW MENU")
            print("2 - ORDER")
            print("3 - BOOKING")
            print("4 - BACK")

            choice = input("Enter your choice: ")

            if choice == "1":
                view.view_menu() 

            elif choice == "2":
                order.place_order()

            elif choice == "3":
                
                while True:
                    print("\n===== BOOKING MENU =====")
                    print("1 - Add Booking")
                    print("2 - View Booking")
                    print("3 - Cancel Booking")
                    print("4 -  Back")

                    opt = input("Enter choice: ").strip()

                    if opt == "1":
                        booking.add_booking()

                    elif opt == "2":
                        booking.view_booking()

                    elif opt =="3":
                        booking.delete_booking()    

                    elif opt == "4":
                        break

                    else:
                        print("Invalid choice")            

            elif choice == "4":
                print("Going Back")
                break

            else:
                print("Invalid Choice")