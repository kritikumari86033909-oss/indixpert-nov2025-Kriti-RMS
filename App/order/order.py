import json
import os
import uuid
from datetime import datetime
from App.billing.billing import Billing

class Order:

    def __init__(self):
        self.menu_path = os.path.join("App", "database", "menu.json")
        self.order_path = os.path.join("App", "database", "orders.json")

    def place_order(self):

        name = input("Enter customer name: ").strip()
        phone = input("Enter phone number: ").strip()
        address= input("enter customer address: ").strip()
        
        if not phone.isdigit() or len(phone) != 10:
            print("invalid phone number")
            return
        
        if not os.path.exists(self.menu_path):
            print("No menu found")
            return

        with open(self.menu_path, "r") as file:
            try:
                menu = json.load(file)
            except json.JSONDecodeError:
                print("Menu empty")
                return
        if not menu:
            print("no food items available")
            return    
        
        
        print("\n" + "="*60)
        print("      5 STAR RESTAURENT MENU ")
        print("="*60)
        veg_items=[]
        non_veg_items=[]

        for item in menu:
            if item["category"]== "veg":
                veg_items.append(item)
            else:
                non_veg_items.append(item)

        # ------VEG------          
        print("\n VEG ITEMS")
        print("-"*60)
        print(f"{"ID" :<5}{"NAME":<30}{"HALF(₹)":<10}{"FULL(₹)":<10}")

        for item in veg_items:
            print(f"{item["id"]:<5}{item["name"]:<30}{item["half_price"]:<10}{item["full_price"]:<10}") 

        # -------- NON-VEG --------
        print("\n NON-VEG ITEM")
        print("-"*60)
        print(f"{'ID':<5}{'NAME':<30}{'HALF (₹)':<10}{'FULL (₹)':<10}")
        print("-"*60)

        for item in non_veg_items:
            print(f"{item['id']:<5}{item['name']:<30}{item['half_price']:<10}{item['full_price']:<10}")


        print("\nType 'done' or 0 to finish order")
        cart=[]
        total = 0

        
        # -------- ORDER LOOP --------
        while True:
            food_id = input("Enter Food ID : ").strip()

            if food_id in ["0", "done", "q"]:
                break

            found = None
            for item in menu:
                if item["id"] == food_id:
                    found = item
                    break

            if not found:
                print("Invalid Food ID")
                continue

            size= input("Enter size (half/full): ").strip().lower()
            if size == "half":
                price = int(found.get ("half_price", 0))
            elif size == "full":
                price = int(found.get("full_price", 0))
 
            else:
                print("Invalid size")
                continue   
            
            # QUANTITY    
            qty = input("Enter quantity: ").strip()
            if not qty.isdigit():
                print("Quantity must be number")
                continue

            qty = int(qty)
              # TAKEAWAY / DINE-IN
            pack=input("pack this item? (yes/no): ").strip().lower()
            if pack == "yes":
                order_type= "takeaway"
                packing_charge= 10
            else:
                order_type="dine in"
                packing_charge=0

            item_total = (price * qty) + packing_charge
            total += item_total

            cart.append({
                "name" : found.get("name"),
                "size": size,
                "price" : price,
                "qty" :  qty,
                "type": order_type,
                "packing_charge": packing_charge,
                "total" :item_total
        
            })

        
            print(" Item added to cart")

        if not cart:
            print(" No items selected")
            return
        
        # -------- DATE TIME --------
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")
                
        # -------- SAVE ORDER --------
        order_data = {
            "order_id": str(uuid.uuid4()),
            "customer_name":name,
            "phone": phone,
            "date": date,
            "time": time,
            "items": cart,
            "subtotal": total
            
        } 

        if os.path.exists(self.order_path):
            with open(self.order_path, "r") as file:
                try:
                    orders = json.load(file)
                except:
                    orders = []
        else:
            orders = []

        orders.append(order_data)

        with open(self.order_path, "w") as file:
            json.dump(orders, file, indent=4)  

        
        bill=Billing()
        bill.generate_bill(name, phone, address, cart, total)
         

        
              
 
            

