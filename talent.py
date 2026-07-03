import json, os, datetime

DATA_FILE = "repairs.json"
SHOP_NUMBER = "0777647498"
SHOP_NAME = "Harare Phone Repairs"

# ========== DATA ==========
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ========== PRICE LIST FOR EVERY PHONE ==========
PRICES = {
    "Screen": {"iPhone": 45, "Samsung": 40, "Huawei": 35, "Tecno": 25, "Infinix": 25, "Xiaomi": 30, "Other": 30},
    "Battery": {"iPhone": 25, "Samsung": 20, "Huawei": 18, "Tecno": 15, "Infinix": 15, "Xiaomi": 16, "Other": 15},
    "Charging Port": {"Other": 10},
    "Camera": {"Other": 12},
    "Software": {"Other": 8},
    "Water Damage": {"Other": 20}
}

BRANDS = ["iPhone", "Samsung", "Huawei", "Tecno", "Infinix", "Xiaomi", "Nokia", "Vivo", "Oppo", "Realme", "Other"]
SERVICES = list(PRICES.keys())

# ========== FUNCTIONS ==========
def add_repair():
    data = load_data()
    print("\n=== New Repair ===")
    customer = input("Customer name: ").strip()
    phone = input("Phone number: ").strip()
    
    print("Brands:", ", ".join(BRANDS))
    brand = input("Phone brand: ").strip().title()
    if brand not in BRANDS: brand = "Other"
    
    model = input("Phone model e.g. A54, iPhone 13: ").strip()
    
    print("Services:", ", ".join(SERVICES))
    service = input("Service needed: ").strip().title()
    if service not in SERVICES: 
        print("Invalid service")
        return
    
    price = PRICES[service].get(brand, PRICES[service]["Other"])
    print(f"Price: ${price}")
    
    repair = {
        "id": len(data) + 1,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "customer": customer,
        "phone": phone,
        "brand": brand,
        "model": model,
        "service": service,
        "price": price,
        "status": "Received"
    }
    data.append(repair)
    save_data(data)
    print_receipt(repair)
    print("✅ Saved!")

def view_repairs():
    data = load_data()
    if not data:
        print("No repairs yet.")
        return
    print("\nID | Date | Customer | Phone | Brand | Service | $ | Status")
    print("-"*80)
    for r in data:
        print(f"{r['id']} | {r['date']} | {r['customer']} | {r['phone']} | {r['brand']} | {r['service']} | ${r['price']} | {r['status']}")

def update_status():
    data = load_data()
    view_repairs()
    try:
        rid = int(input("\nEnter repair ID to update: "))
        for r in data:
            if r["id"] == rid:
                print(f"Current status: {r['status']}")
                r["status"] = input("New status [Received/Repairing/Done/Collected]: ").strip().title()
                save_data(data)
                print("✅ Updated")
                return
        print("ID not found")
    except: print("Invalid ID")

def search_by_phone():
    data = load_data()
    num = input("Enter customer phone: ").strip()
    results = [r for r in data if num in r["phone"]]
    if not results: print("No records found")
    for r in results:
        print(f"{r['id']} | {r['customer']} | {r['brand']} {r['model']} | {r['service']} | ${r['price']} | {r['status']}")

def print_receipt(r):
    print("\n" + "="*40)
    print(f" {SHOP_NAME}")
    print(f" Tel: {SHOP_NUMBER}")
    print("="*40)
    print(f"Receipt #{r['id']}")
    print(f"Date: {r['date']}")
    print(f"Customer: {r['customer']}")
    print(f"Phone: {r['brand']} {r['model']}")
    print(f"Service: {r['service']}")
    print(f"Total: ${r['price']}")
    print(f"Status: {r['status']}")
    print("="*40)
    print("WhatsApp us: 0777647498\n")

def total_sales():
    data = load_data()
    total = sum(r["price"] for r in data if r["status"] in ["Done", "Collected"])
    print(f"\n💰 Total Collected: ${total}")
    print(f"Total Jobs: {len(data)}")

# ========== MENU ==========
def main():
    while True:
        print(f"\n=== {SHOP_NAME} | {SHOP_NUMBER} ===")
        print("1. Add New Repair")
        print("2. View All Repairs") 
        print("3. Update Status")
        print("4. Search by Phone")
        print("5. Total Sales")
        print("6. Exit")
        choice = input("Choose: ").strip()
        
        if choice == "1": add_repair()
        elif choice == "2": view_repairs()
        elif choice == "3": update_status()
        elif choice == "4": search_by_phone()
        elif choice == "5": total_sales()
        elif choice == "6": break
        else: print("Invalid")

if __name__ == "__main__":
    main()
