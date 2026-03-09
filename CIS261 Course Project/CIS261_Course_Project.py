# Darius Bell - CIS261 - Course Project Phase 4 #
FILE_NAME = "user_login.txt"

def load_user_ids():
    user_ids = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) >= 1:
                    user_ids.append(parts[0])
    except FileNotFoundError:
        pass

    return user_ids

def add_users():
    user_ids = load_user_ids()

    file = open(FILE_NAME, "a")
    while True:
        user_id = input("Enter user ID (or type 'End' to finish): ")

        if user_id == "End":
            break
        if user_id in user_ids:
            print("User ID already exists.")
            continue
        password = input("Enter password: ")
        authorization = input("Enter authorization (Admin/User): ")

        if authorization not in ["Admin", "User"]:
            print("Authorization must be Admin or User.")
            continue
        file.write(f"{user_id}|{password}|{authorization}\n")
        user_ids.append(user_id)

    file.close()

def display_users():
    print("\nStored Users:\n")
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                user_id, password, authorization = line.strip().split("|")
                print("User ID:", user_id,
                      "Password:", password,
                      "Authorization:", authorization)
    except FileNotFoundError:
        print("No user file found.")


def main():
    add_users()
    display_users()


main()

FILE_NAME = "user_login.txt"

class Login:
    def __init__(self, user_id, password, authorization):
        self.user_id = user_id
        self.password = password
        self.authorization = authorization


def get_users():
    users = []

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                user_id, password, authorization = line.strip().split("|")
                users.append([user_id, password, authorization])
    except FileNotFoundError:
        print("User file not found.")

    return users

def login_process():
    users = get_users()

    entered_user_id = input("Enter user ID: ")
    entered_password = input("Enter password: ")

    matching_user = None

    for user in users:
        if user[0] == entered_user_id:
            matching_user = user
            break

    if matching_user is None:
        print("User ID does not exist.")
        return

    if matching_user[1] != entered_password:
        print("Incorrect password.")
        return

    login_user = Login(matching_user[0], matching_user[1], matching_user[2])

    print("\nLogin successful.\n")

    if login_user.authorization == "Admin":
        print("User ID:", login_user.user_id)
        print("Password:", login_user.password)
        print("Authorization:", login_user.authorization)
        print()

        print("All User Records:")
        for user in users:
            print("User ID:", user[0], "Password:", user[1], "Authorization:", user[2])

    elif login_user.authorization == "User":
        print("User ID:", login_user.user_id)
        print("Password:", login_user.password)
        print("Authorization:", login_user.authorization)

def main():
    login_process()
main()