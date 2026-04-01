import json
import os
from datetime import datetime

class Booking:

    def __init__(self):
        self.file_path = os.path.join("App", "database", "booking.json")

    def add_booking(self):

        name = input("Enter customer name ").strip()
        phone = input("Enter customer number ").strip()

        if not phone.isdigit() or len(phone) != 10:
            print(" Invailed  phone number: ")
            return

        date = input("Enter booking date (DD-MM-YYYY: )").strip()

        try:
            datetime.strptime(date, "%d-%m-%Y")
        except:
            print("Invalide date format")
            return
         
        # -------- TIME SLOT --------
        print("\nSelect Time slot")
        print("1. 9 AM - 12 PM")
        print("2. 1 PM - 3 PM")
        print("3. 3 PM - 6 PM")

        slot_choice = input("Enter choice: ").strip()

        if slot_choice == "1":
            time_slot = "9-12"
        elif slot_choice == "2":
           time_slot = "1-3"    
        elif slot_choice == "3":
            time_slot = "3-6"
        else:
            print("Invalide time slot")
            return
        
        data=[]
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    data = json.load(file)
                except:
                    data=[]

        # -------- AVAILABLE TABLES -------- 
        total_tables = 10
        booked_tables = []

        for b in data:
            if b["date"] == date and b["slot"] == time_slot:
                booked_tables.append(b["table"])

        available_table = []

        for i in range(1, total_tables + 1):
            if i not in booked_tables:
                available_table.append(i)
                      

        if not available_table:
            print("no table available in this slot ")
            return

        print("\nAvailable Tables:", ", ".join(available_table)) 

        table = input("Enter table number from available tables: ").strip()

        if table not in available_table:
            print("please select from available tables only  ")
            return               

        booking = {
            "name": name,
            "phone": phone,
            "table": table,
            "date": date,
            "slot": time_slot
        }
        data.append(booking)
    
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

        print("Booking added successfully ")

    # -------- VIEW --------
    def view_booking(self):

        if not os.path.exists(self.file_path):
            print("No bookings found")
            return

        with open(self.file_path, "r") as file:
            bookings = json.load(file)

        print("\n===== BOOKINGS =====")

        for b in bookings:
            print(f"{b['name']} | {b['phone']} | Table {b['table']} | {b['date']} | Slot: {b['slot']}")

    # -------- DELETE --------
    def delete_booking(self):

        if not os.path.exists(self.file_path):
            print("No bookings found")
            return

        with open(self.file_path, "r") as file:
            bookings = json.load(file)

        phone = input("Enter phone number to delete booking: ").strip()

        new_data = [b for b in bookings if b["phone"] != phone]

        with open(self.file_path, "w") as file:
            json.dump(new_data, file, indent=4)

        print("Booking deleted successfully ")

    # -------- UPDATE BOOKING --------
    def update_booking(self):

        if not os.path.exists(self.file_path):
            print("No bookings found")
            return

        with open(self.file_path, "r") as file:
            bookings = json.load(file)

        phone = input("Enter phone number: ").strip()

        found = None
        for b in bookings:
            if b["phone"] == phone:
                found = b
                break

        if not found:
            print("Booking not found")
            return

        print("Current Booking:", found)

        new_date = input("Enter new date (DD-MM-YYYY): ").strip()
        new_slot = input("Enter new slot (9-12 / 1-3 / 3-6): ").strip()

        found["date"] = new_date
        found["slot"] = new_slot

        with open(self.file_path, "w") as file:
            json.dump(bookings, file, indent=4)

        print("Booking updated successfully ")  


    # -------- CUSTOMER HISTORY --------
    def customer_history(self):

        if not os.path.exists(self.file_path):
            print("No bookings found")
            return

        with open(self.file_path, "r") as file:
            bookings = json.load(file)

        phone = input("Enter phone number: ").strip()

        print("\n===== CUSTOMER BOOKING HISTORY =====")

        found = False

        for b in bookings:
            if b["phone"] == phone:
                print(f"{b['name']} | Table {b['table']} | {b['date']} | Slot {b['slot']}")
                found = True   

        if not found:
            print("No booking found for this customer")               
        




        

  





