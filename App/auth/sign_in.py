import json
import os
import getpass

class Login:

    def __init__(self):
        self.file_path = os.path.join("App", "database", "users.json")

    def sign_in(self):

        attempts = 3   

        while attempts > 0:
            try:

                if not os.path.exists(self.file_path):
                    print("No users found, please signup first")
                    return None

                # Read file
                with open(self.file_path, "r") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        print(" File is empty or corrupted")
                        return None

                email = input("Enter email: ").strip()
                password = getpass.getpass("Enter password: ").strip()

                # Login check
                for user in data:
                    if user["email"] == email and user["password"] == password:
                        role=user.get("role","staff")
                        role=role.strip().lower()

                        print(" Login Successful!")
                        print("DEBUG ROLE:", role)
                        return role

                #  Wrong credentials
                attempts = attempts - 1
                print(f" Invalid email or password. Attempts left: {attempts}")

            except FileNotFoundError:
                print(" File not found")
                return None

            except Exception as e:
                print(" Something went wrong:", e)
                return None

        print(" Too many failed attempts! Try again later.")
        return None