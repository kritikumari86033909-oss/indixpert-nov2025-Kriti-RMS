import json
import os
from datetime import datetime

class Report:

    def __init__(self):
        self.file_path=os.path.join("App", "database", "orders.json")
        self.report_path = os.path.join("App", "database", "report.json")

    def generate_report(self):

        if not os.path.exists(self.file_path):
            print("no order data found")
            return

        with open(self.file_path, "r")as file:
            try:
                orders = json.load(file)
            except json.JSONDecodeError:
                print("data error")
                return

        if not orders:
            print("no orders available")
            return
        total_orders=len(orders)
        total_earning=0
        today_earning=0

        today_date= datetime.now().strftime("%d-%m-%Y")

        for order in orders:
            bill = order.get("bill", {})

            final_total= bill.get("final_total",order.get("subtotal",0))
            total_earning=total_earning+final_total

            if order.get("date")==today_date:
                today_earning=today_earning+final_total             

        print("\n" + "="*50)
        print(" DAILY REPORT".center(50))
        print("="*50)

        print(f"Total Orders     : {total_orders}")
        print(f"Total Earnings   : ₹{total_earning:.2f}")
        print(f"Today's Earnings : ₹{today_earning:.2f}")

        print("="*50)  

        report_data = {
            "date": today_date,
            "total_orders": total_orders,
            "total_earning": total_earning,
            "today_earning": today_earning
        }
        
        # Load old reports
        if os.path.exists(self.report_path):
            with open(self.report_path, "r") as file:
                try:
                    reports = json.load(file)
                except json.JSONDecodeError:
                    reports = []
        else:
            reports = []

        reports.append(report_data)    

        with open(self.report_path, "w") as file:
            json.dump(reports, file, indent=4)

        print(" Report saved successfully!")        