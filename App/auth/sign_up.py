import json
import uuid
import os
import re
import getpass

file_path= os.path.join("App","database","users.json")

listdata=[]

if os.path.exists(file_path):
    with open(file_path,"r") as file:
        try:
            listdata=json.load(file)
        except json.JSONDecodeError:
            listdata=[]    

class reg_user:

    def register(self):
        try:
            user_id=str(uuid.uuid4())
            while True:
                name=input("enter your name:").strip()
                check_name=name.replace(" ","")

                if check_name.isalpha():
                    print("valid name")
                    break
                else:
                    print("invalid name! only alphabet allow")
                    return
            while True:    
                email=input("enter your email:").lower()

                if "@" in email and "." in email:
                    print("valid email")
                else:
                    print("invalid email:")
                    return


                # duplicate email check
                duplicate=False
                for user in listdata:      
                    if user["email"]==email:
                        duplicate=True
                        break
                if duplicate:
                    print("email already exists")
                else:
                    print("valide email")
                    break            


            while True:

                password=getpass.getpass("enter your password:")

                if len(password)<6:
                    print("password must be at least 6 characters")

                elif not any(char.isupper() for char in password):
                    print("must cantain 1 uppercase latter")

                elif not any(char.isdigit() for char in password):
                    print("must contain 1 number")

                else:
                    print("strong password")
                    break            
                            
                  
            role="staff"
            
            data={
                "id":user_id,
                "name":name,
                "email":email,
                "password":password,
                "role":role
            }  

            listdata.append(data)
            with open(file_path,"w")as file:
                json.dump(listdata, file,indent=4)

            print("Registration successful")

        except Exception as e:
            print("something went wrong:",e)


        
           






