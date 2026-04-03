import json
import os
import uuid
from datetime import datetime
from App.billing.billing import Billing
from App.logger import Logger   

class Order:

    def __init__(self):
        self.menu_path = os.path.join("App", "database", "menu.json")
        self.order_path = os.path.join("App", "database", "orders.json")
        self.logger = Logger()   

    def place_order(self):
        try:
            name = input("Enter customer name: ").strip()
            phone = input("Enter phone number: ").strip()
            address = input("Enter customer address: ").strip()

            if not phone.isdigit() or len(phone) != 10:
                print("Invalid phone number")
                self.logger.log_activity("ORDER_FAILED", "Invalid phone")
                return

            if not os.path.exists(self.menu_path):
                print("No menu found")
                self.logger.log_error("Menu file not found")
                return

            with open(self.menu_path, "r") as file:
                try:
                    menu = json.load(file)
                except json.JSONDecodeError:
                    print("Menu empty")
                    self.logger.log_error("Menu file corrupted")
                    return

            if not menu:
                print("No food items available")
                self.logger.log_activity("ORDER_FAILED", "Empty menu")
                return

            # -------- DISPLAY MENU --------
            print("\n" + "="*60)
            print("        5 STAR RESTAURANT MENU")
            print("="*60)

            veg_items = [item for item in menu if item.get("category") == "veg"]
            non_veg_items = [item for item in menu if item.get("category") == "non-veg"]

            def print_items(title, items):
                print(f"\n{title.upper()}")
                print("-"*60)
                print(f"{'ID':<5}{'NAME':<30}{'HALF(₹)':<10}{'FULL(₹)':<10}")
                print("-"*60)
                for item in items:
                    print(f"{item['id']:<5}{item['name']:<30}{item.get('half_price', 'N/A'):<10}{item.get('full_price', 'N/A'):<10}")

            print_items("Veg Items", veg_items)
            print_items("Non-Veg Items", non_veg_items)

            print("\nType 'done' or 0 to finish order")
            cart = []

            # -------- ORDER LOOP --------
            while True:
                search_name = input("\nEnter food name (done to stop): ").strip().lower()

                if search_name in ["done", "0"]:
                    break

                results = [item for item in menu if search_name in item["name"].lower()]

                if not results:
                    print("Item not found, try again")
                    self.logger.log_activity("ORDER_FAILED", f"Item not found: {search_name}")
                    continue

                print("\nSearch Results:")
                print(f"{'ID':<5}{'NAME':<30}{'HALF(₹)':<10}{'FULL(₹)':<10}")
                print("-"*60)

                for item in results:
                    print(f"{item['id']:<5}{item['name']:<30}{item.get('half_price', 'N/A'):<10}{item.get('full_price', 'N/A'):<10}")

                selected_id = input("Enter ID of item to add: ").strip()
                item = next((x for x in results if x["id"] == selected_id), None)

                if not item:
                    print("Invalid ID")
                    self.logger.log_activity("ORDER_FAILED", f"Invalid ID: {selected_id}")
                    continue

                size = input("Enter size (half/full): ").strip().lower()

                if size == "half":
                    price = float(item.get("half_price", 0))
                elif size == "full":
                    price = float(item.get("full_price", 0))
                else:
                    print("Invalid size")
                    self.logger.log_activity("ORDER_FAILED", "Invalid size")
                    continue

                qty = input("Enter quantity: ").strip()

                if not qty.isdigit():
                    print("Quantity must be a number")
                    continue

                qty = int(qty)

                if qty < 1 or qty > 15:
                    print("Quantity must be between 1 and 15")
                    continue

                pack = input("Pack this item? (yes/no): ").strip().lower()

                if pack == "yes":
                    order_type = "takeaway"
                    packing_charge = 10
                else:
                    order_type = "dine in"
                    packing_charge = 0

                item_total = (price * qty) + (packing_charge * qty)

                cart.append({
                    "name": item["name"],
                    "size": size,
                    "price": price,
                    "qty": qty,
                    "type": order_type,
                    "packing_charge": packing_charge,
                    "total": item_total
                })

                print(f"{item['name']} added to cart. Item total: ₹{item_total}")

            if not cart:
                print("No items selected")
                self.logger.log_activity("ORDER_FAILED", "Empty cart")
                return

            # -------- SAVE ORDER --------
            now = datetime.now()
            date = now.strftime("%d-%m-%Y")
            time = now.strftime("%H:%M:%S")

            order_data = {
                "order_id": str(uuid.uuid4()),
                "customer_name": name,
                "phone": phone,
                "date": date,
                "time": time,
                "items": cart,
                "subtotal": sum(item["total"] for item in cart)
            }

            orders = []
            if os.path.exists(self.order_path):
                with open(self.order_path, "r") as file:
                    try:
                        orders = json.load(file)
                    except json.JSONDecodeError:
                        orders = []

            orders.append(order_data)

            with open(self.order_path, "w") as file:
                json.dump(orders, file, indent=4)

            # -------- BILL --------
            bill = Billing()
            final_total, order_id = bill.generate_bill(name, phone, address, cart)

            #  FIX: update correct order
            orders[-1]["order_id"] = order_id
            orders[-1]["final_total"] = final_total

            with open(self.order_path, "w") as file:
                json.dump(orders, file, indent=4)

            print("\nOrder placed successfully!")

            #  SUCCESS LOG
            self.logger.log_activity(
                "ORDER_PLACED",
                f"{name} | Items: {len(cart)} | ₹{final_total}"
            )

        except Exception as e:
            print("Order error:", e)
            self.logger.log_error(str(e))