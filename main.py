import streamlit as st
from tabulate import tabulate
import json
import os

class LaundryItem:
    def __init__(self, name, weight, price):
        self.name = name
        self.weight = weight
        self.price = price

    def to_dict(self):
        return {"name": self.name, "weight": self.weight, "price": self.price}

class LaundryOrder:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_total_weight(self):
        total_weight = sum(item.weight for item in self.items)
        return total_weight
    
    def calculate_total_price(self):
        total_price = sum(item.price for item in self.items)
        return total_price
    
    def search_item(self, search_name):
        found_items = [item for item in self.items if item.name == search_name]
        return found_items

    def to_dict(self):
        return {"items": [item.to_dict() for item in self.items]}

def save_orders(orders, filename="laundry_orders.json"):
    with open(filename, "w") as file:
        json.dump([order.to_dict() for order in orders], file, indent=1)

def load_orders(filename="laundry_orders.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            orders_data = json.load(file)
        orders = [LaundryOrder() for _ in range(len(orders_data))]
        for order, order_data in zip(orders, orders_data):
            order.items = [LaundryItem(**item_data) for item_data in order_data["items"]]
        return orders
    else:
        return []

def main():
    st.title("Aplikasi Laundry Barokah")
    laundry_orders = load_orders()

    menu_options = {
        "men-0": "Tambah Item Laundry",
        "men-1": "Lihat Pesanan",
        "men-2": "Hitung Total Berat",
        "men-3": "Hitung Total Harga",
        "men-4": "Cari Item Laundry",
        "men-5": "Keluar"
    }

    menu_keys = menu_options.keys()
    menu_values = menu_options.values()

    choice = st.sidebar.selectbox("Menu", menu_values, key="pemuda tersesat")

    if choice == "Tambah Item Laundry":
        name = st.text_input("Masukkan nama item:")
        weight = st.number_input("Masukkan berat item (kg):")

        if st.button("Tambahkan Item"):
            price = int(10000 * weight)
            item = LaundryItem(name, weight, price)
            laundry_order = LaundryOrder()
            laundry_order.add_item(item)
            laundry_orders.append(laundry_order)
            save_orders(laundry_orders)
            st.success("Item ditambahkan ke pesanan.")

    elif choice == "Lihat Pesanan":
        st.subheader("Detail Pesanan:")
        table_data = []
        for order_num, laundry_order in enumerate(laundry_orders, 1):
            for i, item in enumerate(laundry_order.items, 1):
                table_data.append([order_num, item.name, item.weight, item.price])
        
        headers = ["No.", "Nama Item", "Berat (kg)", "Total Harga"]
        st.text(tabulate(table_data, headers=headers, tablefmt="grid"))

    # Add the rest of your menu options here...
    # Add these sections to your existing code

    elif choice == "Hitung Total Berat":
        total_weight = sum(order.calculate_total_weight() for order in laundry_orders)
        st.info(f"Total Berat Pesanan: {total_weight} kg")

    elif choice == "Hitung Total Harga":
        total_price = sum(order.calculate_total_price() for order in laundry_orders)
        st.info(f"Total Harga Pesanan Rp: {int(total_price)}")

    elif choice == "Cari Item Laundry":
        search_name = st.text_input("Masukkan nama item yang dicari:")
        found_items = [
            item for order in laundry_orders
            for item in order.items
            if search_name.lower() in item.name.lower()
        ]

        if found_items:
            st.subheader("Item ditemukan:")
            table_data = []
            for i, found_item in enumerate(found_items, 1):
                table_data.append([i, found_item.name, found_item.weight, found_item.price])

            headers = ["No.", "Nama Item", "Berat (kg)", "Total Harga"]
            st.text(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            st.warning("Item tidak ditemukan.")

    elif choice == "Keluar":
        st.success("Terima kasih. Program selesai.")
        # You can optionally exit the program here, but for Streamlit, it's not necessary.
        # st.stop()


if __name__ == "__main__":
    main()
