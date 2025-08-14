import json


def main():
    file_name = "orders.json"
    with open(file_name) as fd:
        json_data = json.load(fd)
        res = calculate_spending(json_data)
    print(res)

def calculate_spending(json_data):
    customers = {}
    for order in json_data:
        items = order["items"]
        customer_id = order["customer_id"]

        if not items:
            continue

        for item in items:
            price = calculate_price(item)
            customers[customer_id] = price + customers.get(customer_id,0)

    return sorted(customers.items(), key=lambda kv: kv[1], reverse=True)

def calculate_price(item):
    return item["qty"] * item["price"]

if __name__ == "__main__":
    main()