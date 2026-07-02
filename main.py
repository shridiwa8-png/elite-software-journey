## 1. Gather profile attributes
visitor_name = input("Enter traveler name: ")
clearance_tier = input("Enter membership tier (Elite / Executive / Standard): ").strip().lower()

print("\n--- Processing Terminal Credentials ---")

# 2. Complex evaluation using multi-tier logic
if clearance_tier == "elite":
    print(f"Welcome back, {visitor_name}. Premium International Lounge door is unlocked.")
elif clearance_tier == "executive":
    print(f"Welcome, {visitor_name}. Regional Business Lounge door is unlocked.")
elif clearance_tier == "standard":
    print(f"Pass verified, {visitor_name}. Proceeding to main boarding terminal.")
else:
    print(f"Warning: {clearance_tier.upper()} is an invalid tier. Security desk notified.")