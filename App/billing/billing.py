import json
import os
import uuid
from datetime import datetime
from App.logger import Logger    

class Billing:

    def __init__(self):
        self.logger = Logger()   

    def generate_bill(self, name, phone, address, cart):
        try:
            # -------- DATE & TIME --------
            now = datetime.now()
            date = now.strftime("%d-%m-%Y")
            time = now.strftime("%H:%M:%S")

            # -------- CALCULATE SUBTOTAL & PACKING --------
            subtotal = 0
            total_packing = 0

            for item in cart:
                try:
                    price = float(item.get("price", 0))
                    qty = int(item.get("qty", 1))
                    packing_charge = float(item.get("packing_charge", 0))
                except:
                    price, qty, packing_charge = 0, 1, 0

                item_total = price * qty
                subtotal += item_total
                total_packing += packing_charge * qty

                item["price"] = price
                item["qty"] = qty
                item["packing_charge"] = packing_charge
                item["total"] = item_total + packing_charge

            # -------- DISCOUNT --------
            discount = 0
            apply_discount = input("Apply discount? (yes/no): ").strip().lower()

            if apply_discount == "yes":
                try:
                    percent = float(input("Enter discount %: "))
                    discount = subtotal * percent / 100
                except:
                    print("Invalid discount skipped")

            # -------- GST --------
            gst_percent = 5
            gst = (subtotal - discount) * gst_percent / 100

            # -------- FINAL TOTAL --------
            final_total = subtotal - discount + gst + total_packing

            # -------- PRINT BILL --------
            print("\n" + "="*50)
            print("             5 STAR RESTAURANT".center(50))
            print("="*50)
            print(f"Name    : {name}")
            print(f"Phone   : {phone}")
            print(f"Address : {address}")
            print(f"Date    : {date}")
            print(f"Time    : {time}")
            print("-"*50)
            print(f"{'ITEM':<20}{'QTY':<5}{'PRICE':<8}{'TOTAL':<10}")
            print("-"*50)

            for item in cart:
                print(f"{item['name']:<20}{item['qty']:<5}{item['price']:<8}{item['total']:<10}")

            print("-"*50)
            print(f"Subtotal : ₹{subtotal:.2f}")
            print(f"Discount : -₹{discount:.2f}")
            print(f"GST (5%) : +₹{gst:.2f}")
            print(f"Packing  : ₹{total_packing:.2f}")
            print("-"*50)
            print(f"FINAL TOTAL : ₹{final_total:.2f}")
            print("="*50)

            # -------- PAYMENT --------
            while True:
                print("\nSelect payment method:")
                print("1. Cash")
                print("2. UPI")
                print("3. Card")

                choice = input("Enter choice: ").strip()

                if choice == "1":
                    payment_method = "Cash"
                    print("Payment received in cash")
                    break

                elif choice == "2":
                    payment_method = "UPI"
                    upi_id = input("Enter UPI ID: ")
                    print(f"Payment successful via UPI ({upi_id})")
                    break

                elif choice == "3":
                    payment_method = "Card"
                    print("Processing Card...")
                    print("Payment successful")
                    break

                else:
                    print("Invalid choice!")

            # -------- BILL DATA --------
            bill_data = {
                "order_id": str(uuid.uuid4()),
                "customer_name": name,
                "phone": phone,
                "address": address,
                "cart": cart,
                "subtotal": subtotal,
                "discount": discount,
                "gst": gst,
                "packing": total_packing,
                "final_total": final_total,
                "payment_method": payment_method,
                "date": date,
                "time": time
            }

            # -------- SAVE --------
            self.save_bill(bill_data)

    
            self.logger.log_activity(
                "BILL_GENERATED",
                f"{name} | ₹{final_total} | {payment_method}"
            )

            return final_total, bill_data["order_id"]

        except Exception as e:
            self.logger.log_error(str(e))
            print("Error generating bill")

    def save_bill(self, bill_data):
        file_path = os.path.join("App", "database", "orders.json")
        orders = []

        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    orders = json.load(file)
            except:
                orders = []

        orders.append(bill_data)

        try:
            with open(file_path, "w") as file:
                json.dump(orders, file, indent=4)
        except Exception as e:
            self.logger.log_error(str(e))
            print("Error saving bill")