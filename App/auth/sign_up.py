import json
import uuid
import os
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
            # -------NAME-------
            while True:
                name=input("enter your name:").strip()
                check_name=name.replace(" ","")

                if check_name.isalpha():
                    print("valid name")
                    break
                else:
                    print("invalid name! only alphabet allow")
                    

            while True:    
                email=input("enter your email:").strip().lower()

                if not (email.count("@") == 1 and "." in email and email.index("@") < email.rindex(".")):
                    print("invalid email: try again")
                    continue

                # duplicate email check
                duplicate=False
                for user in listdata:      
                    if user["email"]==email:
                        duplicate=True
                        break
                if duplicate:
                    print("email already exists")
                    continue
                else:
                    print("valide email")
                    break            

            while True:

                password=getpass.getpass("enter your password:")

                if len(password)<=8:
                    print("password must be at least 8 characters")

                elif not any(char.isupper() for char in password):
                    print("must cantain 1 uppercase latter")

                elif not any(char.isdigit() for char in password):
                    print("must contain 1 number")

                elif "@" not in password:
                    print("@ symbol zaruri hai")
                    
                else:
                    print("strong password")
                    break 


            while True:                
                mobile_number = input("enter your mobile number:").strip()

                if mobile_number.isdigit() and len(mobile_number) == 10 and mobile_number != "0000000000":
                    print("valid mobile number")
                    break
                else:
                    print("invalid mobile number! must be 10 digit")


            while True:
                adress = input("enter your adress:").strip()
                if len(adress) < 5:
                    print("Invalid address !")
                elif adress.isdigit():
                    print("only number not allowed :")
                else:
                    print("valid address: ")
                    break


            role="staff"
            
            data={
                "id":user_id,
                "name":name,
                "email":email,
                "password":password,
                "mobile" : mobile_number,
                "adress" : adress,
                "role":role
            }  

            listdata.append(data)
            with open(file_path,"w")as file:
                json.dump(listdata, file,indent=4)

            print("Registration successful")

        except Exception as e:
            print("something went wrong:",e)


        
           






