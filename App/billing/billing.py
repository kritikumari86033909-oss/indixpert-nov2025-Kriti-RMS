import json
import os
from datetime import datetime

class Billing:

    def generate_bill(self,name, phone, address, cart, total):

        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")

        # packing system

        total_packing = sum(item["packing_charge"] * item["qty"] for item in cart)

        # -------- DISCOUNT --------
        discount = 0
        apply_discount = input("Apply discount? (yes/no): ").strip().lower()

        if apply_discount == "yes":
            try:
                percent = float(input("Enter discount %: "))
                discount = (total * percent) / 100
            except:
                print("Invalid discount skipped")

        
        # -------- GST --------
        gst_percent= 5
        gst=(total-discount)*gst_percent/100 
        final_total=total - discount + gst+ total_packing

           
        # -------- PRINT BILL --------
        print("\n" + "="*45)
        print("        5 STAR RESTAURANT".center(45))
        print("="*45)

        print(f"Name    : {name}")
        print(f"Phone   : {phone}")
        print(f"Address : {address}")
        print(f"Date    : {date}")
        print(f"Time    : {time}")
        print("-"*45)

        print(f"{'ITEM':<20}{'QTY':<5}{'PRICE':<8}{'TOTAL':<8}")
        print("-"*45)

        for item in cart:
            item_total = item["price"] * item["qty"]   
            print(f"{item['name']:<20}{item['qty']:<5}{item['price']:<8}{item_total:<8}")

        print("-"*45)
        print(f"Subtotal : ₹{total}")
        print(f"Discount : -₹{discount:.2f}")
        print(f"GST (5%) : +₹{gst:.2f}")
        print(f"Packing  : ₹{total_packing}")
        print("-"*45)
        print(f"FINAL TOTAL : ₹{final_total:.2f}")
        print("="*45)

        # -------- PAYMENT --------
        while True:

            print("\nselect payment method")
            print("1. cash")
            print("2. UPI")
            print("3. card")

            choice=(input("Enter choice")).strip()

            if choice == "1":
                payment_method="cash"
                print("payment Received in cash")
                break

            elif choice == "2":
                payment_method="UPI"
                print("scan QR to pay.....")
                upi_id=input("Enter UPI ID: ")
                print("payment Successful via UPI:")
                break

            elif choice =="3":
                payment_method = "Card"
                print("Processing Card...")
                print("Payment Successful ")
                break

            else:
                print("Invalid choice! Please select 1, 2 or 3")
                
        print(f"Payment Method: {payment_method}")

        bill_data={
            "discount": discount,
            "gst":gst,
            "packing":total_packing,
            "final_total":final_total,
            "payment_methode": payment_method
        }
        self.save_bill(bill_data)
        return final_total 

    
    def save_bill(self, bill_data):

        file_path = os.path.join("App", "database", "orders.json")

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    orders = json.load(file)
                except json.JSONDecodeError:
                    orders = []
        else:
            orders = []

        # last order me bill add
        if orders:
            orders[-1]["bill"] = bill_data

        with open(file_path, "w") as file:
            json.dump(orders, file, indent=4)  

            

