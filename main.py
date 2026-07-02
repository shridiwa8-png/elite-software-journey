# 1. Capture user input
clearance_level = input("Enter your clearance tier: ")

# 2. Evaluate the conditions using if/else logic
if clearance_level.lower() == "elite":
    print("Access Granted. Welcome to the international terminal.")
else:
    print("Access Denied. Standard tier limitations applied.")