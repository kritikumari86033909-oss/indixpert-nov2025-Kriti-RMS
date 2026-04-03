import json
import os

class AddMenu:

    def add_food(self):

        file_path = os.path.join("App","database","menu.json")

        # -------- NAME VALIDATION --------
        name = input("Enter food name: ").strip()
        
        if not all(char.isalpha() or char.isspace() for char in name):
            print("invalid name only alphabets and space allowed")
            return
        
        # -------- CATEGORY VALIDATION --------
        category = input("Enter category(veg/non-veg) : ").strip().lower()

        if category != "veg" and category != "non-veg":
            print("invalid category! ")

        else:
            print("Valid category")    
        

        # -------- PRICE VALIDATION --------
        try:
            half_price=int(input("enter half price:").strip())
            full_price=int(input("enter full price:").strip())

            if half_price <=0 or full_price <=0:
                print("price must be greater than 0")
                return
            
            if full_price <= half_price:
                print("full price must be greater than half price")
                return
            
        except ValueError:
            print("price must be a number")
            return  

        data = []
        if os.path.exists(file_path):
            with open(file_path, "r")as file:
                try:
                    data = json.load(file) 

                except json.JSONDecodeError:
                    data=[]

        # -------- DUPLICATE NAME CHECK --------
        for item in data:
            if item["name"].strip().lower() == name.lower():
                print("Food already exists") 
                return
                        
        if data:
            last_id = int(data[-1]["id"])
            new_id = str(last_id + 1)
        else:
            new_id = "1"
            
        # -------- CREATE FOOD ITEM --------
        food_item={

            "id": new_id,
            "name": name,
            "category": category,
            "half_price": half_price,
            "full_price": full_price
        }

        data.append(food_item)

        # -------- save DATA --------
        try:
            with open(file_path, "w")as file:
                json.dump(data, file,indent=4)
        except Exception as e:
            print("error saving data:",e)
            return
        

        print("FOOD ADDED SUCCESSFULY")

           

