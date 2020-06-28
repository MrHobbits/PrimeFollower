import json

def load_users():
    # this will load the usernames we need to check for follower counts
    with open('users.log', 'r') as f:
        return json.load(f)

def save_users(users):
    # this will save our list of users
    with open('users.log', 'w') as f:
        json.dump(users, f)

def main():
    while True:
        users = load_users()

        menu = "\nEnter your selection\n1. Add user\n2. View users\n3. Quit"
        print(menu)
        menu_choice = input("Enter operation: ")
        if menu_choice == "1":
            new_user = input("Enter twitter username: ")
            users[new_user] = 0
            save_users(users)
            print(f"Added {new_user} to the list.")
        elif menu_choice == "2":
            users = load_users()
            usernum = 1
            for user in users:
                print(f"{usernum}. {user}")
                usernum += 1
        elif menu_choice == "3":
            quit()

if __name__ == "__main__":
    main()
