import json
import os

class DeleteMenu:

    def delete_food(self):

        file_path = os.path.join("App","database","menu.json")
        # -------- FILE CHECK --------
        if not os.path.exists(file_path):
            print("menu file nhi mili")
            return
        

        with open(file_path,"r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print("Menu empty ")
                return

        if not data:
            print("No food items available")
            return
        
        food_id=input("Enter food IDto delete: ").strip()
        new_data = []
        found=False
        for food in data:
            if food.get("id") == food_id:
                found=True
            else:
                new_data.append(food)

        if not found:
            print("Food not found")
            return
        # -------- CONFIRMATION --------    
        confirm = input("Are you sure? (Yes/no): ").strip().lower()
        if confirm != "yes":
            print("Delete cancelled")
            return
        

        with open(file_path,"w") as file:
            json.dump(new_data,file,indent=4)

        print("FOOD DELETE SUCCESSFULY")
        