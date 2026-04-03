import json
import os
from datetime import datetime, timedelta
from App.logger import Logger 

class Booking:

    def __init__(self):
        self.file_path = os.path.join("App", "database", "booking.json")
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        self.total_tables = 10
        self.seats_per_table = {i: 4 for i in range(1, self.total_tables + 1)}
        self.max_booking_days = 14
        self.valid_slots = ["9-12", "1-3", "3-6", "6-9"]

        self.logger = Logger()   

    # -------- ADD BOOKING --------
    def add_booking(self):
        try:
            name = input("Enter customer name ").strip()
            phone = input("Enter customer number ").strip()

            if not phone.isdigit() or len(phone) != 10:
                print("Invalid phone number")
                return

            date = input("Enter booking date (DD-MM-YYYY): ").strip()

            try:
                booking_date = datetime.strptime(date, "%d-%m-%Y")
            except ValueError:
                print("Invalid date format")
                return

            today = datetime.today()

            if booking_date.date() < today.date():
                print("Booking date cannot be in the past")
                return

            if booking_date.date() > (today + timedelta(days=self.max_booking_days)).date():
                print(f"Booking allowed only within {self.max_booking_days} days")
                return

            print("\nSelect Time slot")
            print("1. 9 AM - 12 PM")
            print("2. 1 PM - 3 PM")
            print("3. 3 PM - 6 PM")
            print("4. 6 PM - 9 PM")

            slot_choice = input("Enter choice: ").strip()

            slot_map = {"1": "9-12", "2": "1-3", "3": "3-6", "4": "6-9"}

            if slot_choice not in slot_map:
                print("Invalid slot")
                return

            time_slot = slot_map[slot_choice]

            data = []
            if os.path.exists(self.file_path):
                try:
                    with open(self.file_path, "r") as file:
                        data = json.load(file)
                except:
                    data = []

            booked_tables = [
                int(b["table"]) for b in data
                if b["date"] == date and b["slot"] == time_slot
            ]

            available_table = [
                i for i in range(1, self.total_tables + 1)
                if i not in booked_tables
            ]

            if not available_table:
                print("No table available")
                return

            print("\nAvailable Tables:")
            for t in available_table:
                print(f"Table {t} - Seats: {self.seats_per_table[t]}")

            table_input = input("Enter table number: ").strip()

            if not table_input.isdigit() or int(table_input) not in available_table:
                print("Invalid table")
                return

            table_number = int(table_input)

            booking = {
                "name": name,
                "phone": phone,
                "table": table_number,
                "date": date,
                "slot": time_slot,
                "seats": self.seats_per_table[table_number]
            }

            data.append(booking)

            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)

            print("Booking added successfully")

            #  LOG
            self.logger.log_activity("BOOKING_ADDED", f"{name}, Table {table_number}, {date}, {time_slot}")

        except Exception as e:
            self.logger.log_error(str(e))

    # -------- VIEW --------
    def view_booking(self):
        try:
            if not os.path.exists(self.file_path):
                print("No bookings found")
                return

            with open(self.file_path, "r") as file:
                bookings = json.load(file)

            print("\n========== BOOKINGS ==========\n")

            for b in bookings:
                print(b)

            self.logger.log_activity("VIEW_BOOKINGS")

        except Exception as e:
            self.logger.log_error(str(e))

    # -------- DELETE --------
    def delete_booking(self):
        try:
            with open(self.file_path, "r") as file:
                bookings = json.load(file)

            phone = input("Enter phone: ")
            date = input("Enter date: ")
            slot = input("Enter slot: ")

            new_data = [
                b for b in bookings
                if not (b["phone"] == phone and b["date"] == date and b["slot"] == slot)
            ]

            with open(self.file_path, "w") as file:
                json.dump(new_data, file, indent=4)

            print("Booking deleted")

            self.logger.log_activity("BOOKING_DELETED", f"{phone}, {date}, {slot}")

        except Exception as e:
            self.logger.log_error(str(e))

    # -------- UPDATE --------
    def update_booking(self):
        try:
            with open(self.file_path, "r") as file:
                bookings = json.load(file)

            phone = input("Enter phone: ")

            found = next((b for b in bookings if b["phone"] == phone), None)

            if not found:
                print("Not found")
                return

            new_date = input("Enter new date: ")
            new_slot = input("Enter new slot: ")

            found["date"] = new_date
            found["slot"] = new_slot

            with open(self.file_path, "w") as file:
                json.dump(bookings, file, indent=4)

            print("Updated")

            self.logger.log_activity("BOOKING_UPDATED", f"{phone}, {new_date}, {new_slot}")

        except Exception as e:
            self.logger.log_error(str(e))

    def customer_history(self):
        try:
            if not os.path.exists(self.file_path):
                print("No customer history found")
                return

            with open(self.file_path, "r") as file:
                data = json.load(file)

            if not data:
                print("No customer history available")
                return
            
            print("\n===== CUSTOMER HISTORY =====\n")
            for b in data:
                print(f"Name: {b.get('name','N/A')}, Phone: {b.get('phone','N/A')}, "
                    f"Table: {b.get('table','N/A')}, Date: {b.get('date','N/A')}, Slot: {b.get('slot','N/A')}")
            print("\n=============================")

            
            self.logger.log_activity("VIEW_CUSTOMER_HISTORY")

        except Exception as e:
            self.logger.log_error(str(e))