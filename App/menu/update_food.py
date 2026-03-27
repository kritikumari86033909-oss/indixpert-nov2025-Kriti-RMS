import json
import os

class UpdateMenu:

    def update_food(self):

        file_path = os.path.join("App","database","menu.json")

        # -------- FILE CHECK --------
        if not os.path.exists(file_path):
            print("menu file nhi mili")
            return

        # -------- LOAD DATA --------
        with open(file_path,"r") as file:
            try:
                data=json.load(file)

            except json.JSONDecodeError:
                print("menu empty")  
                return 

        if not data:
            print("no food item available")
            return
             
        food_id=input("enter food id to update:").strip()


        # -------- SEARCH --------
        food_item=None
        
        for food in data:
            if food.get("id") == food_id:
                food_item=food
                break

        if not food_item:
                print("food not found") 
                return   
        print("Food found! Enter new details")
        name=input("Enter new name: ").strip()
        if name and name.replace(" ", "").isalpha():
            food_item["name"] = name


                # CATEGORY
        category=input("Enter category (veg/non-veg): ").strip().lower()
        if category in ["veg", "non-veg"]:
            food_item["category"] = category

        try:
            half_price = int(input("Enter new half price: "))
            full_price = int(input("Enter new full price: "))

            if half_price >0 and full_price >0:
                food_item["half_price"] = half_price
                food_item["full_price"] = full_price

            if full_price <= half_price:
                print("full price must be greater than half price")
                return    
            else:
                print("price must be greater than 0 ")

        except ValueError:
            print("Invalid price")
            return
                
                        
        # -------- SAVE --------
        with open(file_path,"w") as file:
            json.dump(data,file,indent=4)

        print("FOOD UPDATE SUCCESSFULY")
                

        