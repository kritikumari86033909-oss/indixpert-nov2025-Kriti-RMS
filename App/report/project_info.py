import json
import os
from datetime import datetime, timedelta
from App.logger import Logger 

class Report:

    def __init__(self):
        self.file_path = os.path.join("App", "database", "orders.json")
        self.report_path = os.path.join("App", "database", "report.json")
        self.logger = Logger()   

    # -------- LOAD DATA --------
    def load_orders(self):
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            self.logger.log_error(str(e))   
            return []

    # -------- FILTER --------
    def filter_orders(self, period):
        orders = self.load_orders()
        filtered = []

        today = datetime.now()

        for order in orders:
            try:
                if "date" not in order:
                    continue

                order_date = datetime.strptime(order["date"], "%d-%m-%Y")

                if period == "daily":
                    if order_date.date() == today.date():
                        filtered.append(order)

                elif period == "weekly":
                    start = today - timedelta(days=7)
                    if start.date() <= order_date.date() <= today.date():
                        filtered.append(order)

                elif period == "monthly":
                    if order_date.month == today.month and order_date.year == today.year:
                        filtered.append(order)

                elif period == "yearly":
                    if order_date.year == today.year:
                        filtered.append(order)

            except Exception as e:
                self.logger.log_error(str(e))   
                continue

        return filtered

    # -------- GENERATE REPORT --------
    def generate_report(self, period="daily", report_type="Order"):
        try:
            orders = self.filter_orders(period)

            if not orders:
                print("No data found for this period")
                return

            total_orders = 0
            total_earning = 0
            today_earning = 0
            total_packing = 0
            total_discount = 0

            today_date = datetime.now().strftime("%d-%m-%Y")

            for order in orders:
                try:
                    total_orders += 1

                    bill = order.get("bill", {})

                    if "final_total" in bill:
                        final_total = float(bill.get("final_total", 0))
                        total_packing += float(bill.get("packing", 0))
                        total_discount += float(bill.get("discount", 0))

                    elif "final_total" in order:
                        final_total = float(order.get("final_total", 0))
                        total_packing += float(order.get("packing", 0))
                        total_discount += float(order.get("discount", 0))

                    elif "subtotal" in order:
                        final_total = float(order.get("subtotal", 0))

                    else:
                        final_total = 0

                    total_earning += final_total

                    if order.get("date") == today_date:
                        today_earning += final_total

                except Exception as e:
                    self.logger.log_error(str(e))
                    continue

            # -------- PRINT --------
            print("\n" + "="*50)
            print(f"{report_type.upper()} {period.upper()} REPORT")
            print("="*50)

            print(f"Total Orders     : {total_orders}")
            print(f"Total Earnings   : ₹{total_earning:.2f}")
            print(f"Today's Earnings : ₹{today_earning:.2f}")
            print(f"Total Packing    : ₹{total_packing:.2f}")
            print(f"Total Discount   : ₹{total_discount:.2f}")

            print("="*50)

            # -------- REPORT DATA --------
            report_data = {
                "report_type": report_type,
                "period": period,
                "date": datetime.now().strftime("%d-%m-%Y"),
                "time": datetime.now().strftime("%H:%M:%S"),
                "total_orders": total_orders,
                "total_earning": round(total_earning, 2),
                "today_earning": round(today_earning, 2),
                "total_packing": round(total_packing, 2),
                "total_discount": round(total_discount, 2)
            }

            # -------- SAVE --------
            self.save_report(report_data)

            print("Report saved successfully!")

            #  LOG SUCCESS
            self.logger.log_activity(
                "REPORT_GENERATED",
                f"{period} | Orders: {total_orders} | Earnings: {total_earning}"
            )

        except Exception as e:
            self.logger.log_error(str(e))

    # -------- SAVE FUNCTION --------
    def save_report(self, report_data):

        reports = []

        if os.path.exists(self.report_path):
            try:
                with open(self.report_path, "r") as file:
                    reports = json.load(file)
            except:
                reports = []

        # duplicate remove
        reports = [r for r in reports if not (
            r.get("date") == report_data["date"] and
            r.get("period") == report_data["period"] and
            r.get("report_type") == report_data["report_type"]
        )]

        reports.append(report_data)

        try:
            with open(self.report_path, "w") as file:
                json.dump(reports, file, indent=4)
        except Exception as e:
            print(f"Error saving report: {e}")
            self.logger.log_error(str(e))   


# -------- MENU SYSTEM --------
def report_menu():

    report = Report()

    while True:
        print("\n========== REPORT MENU ==========")
        print("1. Daily Report")
        print("2. Weekly Report")
        print("3. Monthly Report")
        print("4. Yearly Report")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            report.generate_report("daily")

        elif choice == "2":
            report.generate_report("weekly")

        elif choice == "3":
            report.generate_report("monthly")

        elif choice == "4":
            report.generate_report("yearly")

        elif choice == "5":
            break

        else:
            print("Invalid choice")


# RUN
if __name__ == "__main__":
    report_menu()