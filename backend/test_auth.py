from getpass import getpass

from backend.auth import register_user, login_user


def main():

    print("==============================")
    print("       PENNYPILOT AUTH")
    print("==============================")

    print("1. Register")
    print("2. Login")

    choice = input("\nEnter choice: ")

    if choice == "1":

        name = input("Enter name: ")
        email = input("Enter email: ")
        password = getpass("Enter password: ")

        success, message = register_user(
            name, email, password
        )

        print("\n", message)

    elif choice == "2":

        email = input("Enter email: ")
        password = getpass("Enter password: ")

        user = login_user(email, password)

        if user:
            print("\nLogin successful!")
            print("Welcome,", user["name"])
            print("User ID:", user["user_id"])
        else:
            print("\nInvalid email or password.")

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()