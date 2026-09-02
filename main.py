import enrollment
import attendance
import sys

def menu():
    while True:
        print("\n=" + "="*20 + "=")
        print ("Welcome to the Student Attendance System")
        print("\n=" + "="*20 + "=")
        print("\nMenu:")
        print("1. Enroll a student")
        print("2. Record attendance")
        print("3. Exit")
        print("\n=" + "="*20 + "=")

        choice = input("Enter your choice: ")

        if choice == '1':
            enrollment.register_face()
            choice = input("Do you want to enroll another student? (y/n): ")
            if choice.lower() != 'y':
                continue
        elif choice == '2':
            attendance.run_attendance()
        elif choice == '3':
            print("Exiting the program.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()