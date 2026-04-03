import json
import os
import getpass
from App.logger import Logger    

class Login:

    def __init__(self):
        self.file_path = os.path.join("App", "database", "users.json")
        self.logger = Logger()   

    def sign_in(self):

        attempts = 3   

        while attempts > 0:
            try:

                if not os.path.exists(self.file_path):
                    print("No users found, please signup first")

                    #  LOG
                    self.logger.log_activity("LOGIN_FAILED", "No users file found")

                    return None

                # Read file
                with open(self.file_path, "r") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        print("File is empty or corrupted")

                        #  LOG
                        self.logger.log_error("Users file corrupted")

                        return None

                email = input("Enter email: ").strip().lower()
                password = getpass.getpass("Enter password: ").strip()

                # Login check
                for user in data:
                    if user["email"] == email:

                        if user["password"] == password:
                            role = user.get("role", "staff")
                            role = role.strip().lower()

                            print("Login Successful!")
                            print("ROLE:", role)

                            #  SUCCESS LOG
                            self.logger.log_activity(
                                "LOGIN_SUCCESS",
                                f"{email} | role: {role}"
                            )

                            return role

                        else:
                            #  WRONG PASSWORD LOG
                            self.logger.log_activity(
                                "LOGIN_FAILED",
                                f"{email} wrong password"
                            )

                            break   # email mil gaya but password galat

                #  Wrong credentials
                attempts -= 1
                print(f"Invalid email or password. Attempts left: {attempts}")

                #  LOG (invalid attempt)
                self.logger.log_activity(
                    "LOGIN_FAILED",
                    f"{email} invalid attempt | attempts left: {attempts}"
                )

            except FileNotFoundError:
                print("File not found")

                #  LOG
                self.logger.log_error("Users file not found")

                return None

            except Exception as e:
                print("Something went wrong:", e)

                #  ERROR LOG
                self.logger.log_error(str(e))

                return None

        print("Too many failed attempts! Try again later.")

        # FINAL FAIL LOG
        self.logger.log_activity(
            "LOGIN_BLOCKED",
            "Too many failed attempts"
        )

        return None