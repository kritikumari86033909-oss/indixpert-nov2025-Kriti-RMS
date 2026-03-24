from App.auth.sign_up import reg_user
from App.auth.sign_in import Login
from App.dashboard.user_manage_dashboard import UserDashboard


class UserManag:
    def menu(self):

        while True:
            print("\n" + "-"*40)
            print("|{:^38}|".format("5 STAR REGISTRATION MENU"))
            print("-"*40)
            print("| 1. SIGNUP                        |")
            print("| 2. LOGIN                         |")
            print("| 3. EXIT                          |")
            print("-"*40)
            

            try:
                choice = input("enter your choice!")

                if not choice.isdigit():
                    print("please enter numbers only!")
                    continue

                choice = int(choice)

            except ValueError as e:
                print(e)
                continue


            if choice == 1:
                obj = reg_user()
                obj.register()

            elif choice == 2:
                obj = Login()
                role = obj.sign_in()   # role return

                 
                if role == "admin":
                    from App.dashboard.admin import AdminDashboard
                    obj = AdminDashboard()
                    obj.admin_menu()

                elif role == "staff":
                    from App.dashboard.staff import StaffDashboard
                    obj = StaffDashboard()
                    obj.staff_menu()

                elif role is None:
                    # login failed → kuch mat karo (loop continue)
                    continue

                else:
                    print(" Invalid role detected")

            elif choice == 3:
                print(" Thank you!")
                break

            else:
                print(" Invalid choice (1-3 only)")
            #     if role:
            #         dash = UserDashboard()
            #         dash.dashboard(role)   # dashboard open

            # elif choice == 3:
            #     print("Thank You! Exiting...")
            #     break

            # else:
            #     print("invalid choice please try again!")