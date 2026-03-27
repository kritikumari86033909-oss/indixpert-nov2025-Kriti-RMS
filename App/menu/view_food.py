import json
import os

class ViewMenu:

    def view_food(self):

        file_path = os.path.join("App","database","menu.json")

        if not os.path.exists(file_path):
            print("Menu empty")
            return

        with open(file_path,"r") as file:
            try:
                data=json.load(file)

            except json.JSONDecodeError:
                print("menu empty")  
                return  
            
        if not data:
            print("no food item available")
            return    
        
        print("\n" + "="*60)
        print("5 STAR HOTEL MENU ".center(60))
        print("="*60)

        # CATEGORY WISE FILTER
        veg_items = [item for item in data if item["category"] == "veg"]
        nonveg_items = [item for item in data if item["category"] == "non-veg"]

        def print_section(title, items):
            print("\n" + "-"*60)
            print(title.center(60))
            print("-"*60)
            print(f"{'ID':<5}{'DISHES':<25}{'HALF':<10}{'FULL':<10}")
            print("-"*60)

            for item in items:
                short_id = item['id'][:6]
                print(f"{item['id']:<8}{item['name']:<25}{item['half_price']:<10}{item['full_price']:<10}")

        # PRINT SECTIONS
        print_section(" VEG MENU", veg_items)
        print_section(" NON-VEG MENU", nonveg_items)

        print("\n" + "="*60)


        

            