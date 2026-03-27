from App.dashboard.admin import AdminDashboard
from App.dashboard.staff import StaffDashboard

class UserDashboard:

    def dashboard(self, role):

        if role == "admin":
            admin = AdminDashboard()
            admin.admin_menu()

        elif role == "staff":
            staff = StaffDashboard()
            staff.staff_menu()

        else:
            print("Invalid role")