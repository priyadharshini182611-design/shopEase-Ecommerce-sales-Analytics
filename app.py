import streamlit as st
import csv
import os
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="ShopEase",
    page_icon="🛍️",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SALES_FILE = os.path.join(DATA_DIR, "sales_data.csv")

os.makedirs(DATA_DIR, exist_ok=True)

st.markdown("""
<style>
.main {
    background-color: #fafafa;
}

.store-banner {
    padding: 22px;
    border-radius: 15px;
    background: white;
    border: 1px solid #e5e5e5;
    margin-bottom: 20px;
    text-align: center;
}

.store-banner h1 {
    margin-bottom: 5px;
}

.store-banner p {
    margin-top: 0;
    color: #666666;
}

.product-card {
    padding: 18px;
    border: 1px solid #e5e5e5;
    border-radius: 15px;
    background: white;
    margin-bottom: 12px;
}

div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

div[data-testid="stMetric"] {
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    padding: 12px;
    background: white;
}
</style>
""", unsafe_allow_html=True)

products = [
    {
        "id": 1,
        "name": "Designer Saree",
        "category": "Sarees",
        "price": 799,
        "description": "Beautiful designer saree for everyday and special occasions."
    },
    {
        "id": 2,
        "name": "Ladies Handbag",
        "category": "Bags",
        "price": 599,
        "description": "Stylish and spacious handbag for daily use."
    },
    {
        "id": 3,
        "name": "Cotton Kurti",
        "category": "Kurtis",
        "price": 699,
        "description": "Comfortable cotton kurti with a simple modern design."
    },
    {
        "id": 4,
        "name": "Printed Saree",
        "category": "Sarees",
        "price": 899,
        "description": "Trendy printed saree with an elegant design."
    },
    {
        "id": 5,
        "name": "Fashion Handbag",
        "category": "Bags",
        "price": 749,
        "description": "Modern handbag suitable for casual and office use."
    },
    {
        "id": 6,
        "name": "Casual Kurti",
        "category": "Kurtis",
        "price": 549,
        "description": "Soft and comfortable kurti for daily wear."
    }
]

defaults = {
    "page": "Home",
    "cart": [],
    "wishlist": [],
    "selected_product": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def save_order(name, phone, address, cart):
    new_file = not os.path.exists(SALES_FILE)

    order_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(SALES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if new_file:
            writer.writerow([
                "Order ID",
                "Date",
                "Customer Name",
                "Phone",
                "Address",
                "Product",
                "Category",
                "Price",
                "Quantity",
                "Amount"
            ])

        for item in cart:
            product = item["product"]
            quantity = item["quantity"]

            writer.writerow([
                order_id,
                date,
                name,
                phone,
                address,
                product["name"],
                product["category"],
                product["price"],
                quantity,
                product["price"] * quantity
            ])


st.markdown("""
<div class="store-banner">
    <h1>🛍️ ShopEase</h1>
    <p>Smart E-Commerce Store with Python Sales Analytics</p>
</div>
""", unsafe_allow_html=True)

search = st.text_input(
    "🔍 Search Products",
    placeholder="Search for saree, bag, kurti..."
)

nav = st.columns(5)

nav_items = [
    ("🏠 Home", "Home"),
    ("🛒 Cart", "Cart"),
    ("❤️ Wishlist", "Wishlist"),
    ("📦 Orders", "Orders"),
    ("📊 Analytics", "Analytics")
]

for col, (label, page) in zip(nav, nav_items):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.page = page
            st.rerun()

st.divider()
# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    st.subheader("🛍️ Shop by Category")

    category_cols = st.columns(3)

    for col, label, category in zip(
        category_cols,
        ["👗 Sarees", "👜 Bags", "👚 Kurtis"],
        ["Sarees", "Bags", "Kurtis"]
    ):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.page = category
                st.rerun()

    st.divider()

    shown_products = products

    if search:
        search_text = search.lower()

        shown_products = [
            product
            for product in products
            if search_text in product["name"].lower()
            or search_text in product["category"].lower()
        ]

    st.subheader("⭐ Featured Products")

    if not shown_products:
        st.warning("No products found.")

    for i in range(0, len(shown_products), 3):

        cols = st.columns(3)

        for col, product in zip(
            cols,
            shown_products[i:i + 3]
        ):

            with col:

                icon = (
                    "👗"
                    if product["category"] == "Sarees"
                    else "👜"
                    if product["category"] == "Bags"
                    else "👚"
                )

                st.markdown(
                    f"""
                    <div class="product-card">
                        <h1 style="text-align:center;">
                            {icon}
                        </h1>
                        <h3>{product['name']}</h3>
                        <p>{product['description']}</p>
                        <h3>💰 ₹{product['price']}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "View Product",
                    key=f"home_{product['id']}",
                    use_container_width=True
                ):
                    st.session_state.selected_product = product
                    st.session_state.page = "Product"
                    st.rerun()


# =========================================================
# CATEGORY PAGES
# =========================================================

elif st.session_state.page in [
    "Sarees",
    "Bags",
    "Kurtis"
]:

    category = st.session_state.page

    st.subheader(f"{category} Collection")

    category_products = [
        product
        for product in products
        if product["category"] == category
    ]

    for product in category_products:

        c1, c2 = st.columns([1, 2])

        with c1:

            icon = (
                "👗"
                if category == "Sarees"
                else "👜"
                if category == "Bags"
                else "👚"
            )

            st.markdown(
                f"""
                <div class="product-card"
                     style="text-align:center;">
                    <h1 style="font-size:70px;">
                        {icon}
                    </h1>
                    <h3>{product['category']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"### {product['name']}"
            )

            st.write(product["description"])

            st.write(
                f"💰 **₹{product['price']}**"
            )

            if st.button(
                "View Product",
                key=f"category_{product['id']}"
            ):

                st.session_state.selected_product = product
                st.session_state.page = "Product"
                st.rerun()

        st.divider()


# =========================================================
# PRODUCT DETAILS
# =========================================================

elif st.session_state.page == "Product":

    product = st.session_state.selected_product

    if product:

        c1, c2 = st.columns(2)

        with c1:

            icon = (
                "👗"
                if product["category"] == "Sarees"
                else "👜"
                if product["category"] == "Bags"
                else "👚"
            )

            st.markdown(
                f"""
                <div class="product-card"
                     style="text-align:center;">
                    <h1 style="font-size:120px;">
                        {icon}
                    </h1>
                    <h2>{product['category']}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.subheader(product["name"])

            st.write(
                f"## 💰 ₹{product['price']}"
            )

            st.write(
                f"**Category:** {product['category']}"
            )

            st.write(product["description"])

            st.divider()

            if st.button(
                "🛒 Add to Cart",
                use_container_width=True
            ):

                found = next(
                    (
                        item
                        for item in st.session_state.cart
                        if item["product"]["id"]
                        == product["id"]
                    ),
                    None
                )

                if found:
                    found["quantity"] += 1

                else:
                    st.session_state.cart.append(
                        {
                            "product": product,
                            "quantity": 1
                        }
                    )

                st.success(
                    "Product added to cart!"
                )

            if st.button(
                "❤️ Add to Wishlist",
                use_container_width=True
            ):

                already_exists = any(
                    item["id"] == product["id"]
                    for item in st.session_state.wishlist
                )

                if not already_exists:

                    st.session_state.wishlist.append(
                        product
                    )

                    st.success(
                        "Added to wishlist!"
                    )

                else:

                    st.info(
                        "Product already in wishlist."
                    )

            if st.button(
                "⬅️ Back to Home",
                use_container_width=True
            ):

                st.session_state.page = "Home"
                st.rerun()
                # =========================================================
# CART
# =========================================================

elif st.session_state.page == "Cart":

    st.subheader("🛒 My Cart")

    if not st.session_state.cart:

        st.info("Your cart is empty.")

    else:

        total = 0

        for i, item in enumerate(st.session_state.cart):

            product = item["product"]
            quantity = item["quantity"]

            c1, c2, c3 = st.columns([1, 2, 2])

            with c1:

                icon = (
                    "👗"
                    if product["category"] == "Sarees"
                    else "👜"
                    if product["category"] == "Bags"
                    else "👚"
                )

                st.markdown(
                    f"<h1 style='text-align:center'>{icon}</h1>",
                    unsafe_allow_html=True
                )

            with c2:

                st.write(f"### {product['name']}")
                st.write(f"₹{product['price']}")
                st.write(
                    f"Quantity: **{quantity}**"
                )

            with c3:

                a, b, c = st.columns(3)

                with a:

                    if st.button(
                        "➕",
                        key=f"plus_{i}"
                    ):

                        item["quantity"] += 1
                        st.rerun()

                with b:

                    if st.button(
                        "➖",
                        key=f"minus_{i}"
                    ):

                        if item["quantity"] > 1:
                            item["quantity"] -= 1

                        st.rerun()

                with c:

                    if st.button(
                        "❌",
                        key=f"remove_{i}"
                    ):

                        st.session_state.cart.pop(i)
                        st.rerun()

            total += product["price"] * quantity

            st.divider()

        st.subheader(
            f"Total Amount: ₹{total}"
        )

        if st.button(
            "✅ Proceed to Checkout",
            use_container_width=True
        ):

            st.session_state.page = "Checkout"
            st.rerun()


# =========================================================
# CHECKOUT
# =========================================================

elif st.session_state.page == "Checkout":

    st.subheader("🧾 Checkout")

    if not st.session_state.cart:

        st.warning("Your cart is empty.")

    else:

        total = sum(
            item["product"]["price"]
            * item["quantity"]
            for item in st.session_state.cart
        )

        st.write("### 🛍️ Order Summary")

        for item in st.session_state.cart:

            product = item["product"]
            quantity = item["quantity"]

            st.write(
                f"**{product['name']}** × {quantity} "
                f"= ₹{product['price'] * quantity}"
            )

        st.divider()

        st.subheader(
            f"Total: ₹{total}"
        )

        st.write("### Delivery Details")

        name = st.text_input(
            "Customer Name"
        )

        phone = st.text_input(
            "Phone Number"
        )

        address = st.text_area(
            "Delivery Address"
        )

        if st.button(
            "🛍️ Place Order",
            use_container_width=True
        ):

            if name and phone and address:

                save_order(
                    name,
                    phone,
                    address,
                    st.session_state.cart
                )

                st.session_state.cart = []

                st.session_state.page = "Orders"

                st.rerun()

            else:

                st.warning(
                    "Please fill all delivery details."
                )


# =========================================================
# WISHLIST
# =========================================================

elif st.session_state.page == "Wishlist":

    st.subheader("❤️ My Wishlist")

    if not st.session_state.wishlist:

        st.info(
            "Your wishlist is empty."
        )

    else:

        for product in st.session_state.wishlist:

            c1, c2 = st.columns([1, 3])

            with c1:

                icon = (
                    "👗"
                    if product["category"] == "Sarees"
                    else "👜"
                    if product["category"] == "Bags"
                    else "👚"
                )

                st.markdown(
                    f"""
                    <h1 style="text-align:center">
                        {icon}
                    </h1>
                    """,
                    unsafe_allow_html=True
                )

            with c2:

                st.write(
                    f"### {product['name']}"
                )

                st.write(
                    f"₹{product['price']}"
                )

                st.write(
                    product["description"]
                )

            st.divider()


# =========================================================
# ORDERS
# =========================================================

elif st.session_state.page == "Orders":

    st.subheader("📦 My Orders")

    if os.path.exists(SALES_FILE):

        orders_df = pd.read_csv(
            SALES_FILE,
            dtype={
                "Order ID": str,
                "Phone": str
            }
        )

        if not orders_df.empty:

            orders_df["Amount"] = pd.to_numeric(
                orders_df["Amount"],
                errors="coerce"
            ).fillna(0)

            orders_df["Quantity"] = pd.to_numeric(
                orders_df["Quantity"],
                errors="coerce"
            ).fillna(0)

            grouped_orders = orders_df.groupby(
                "Order ID",
                sort=False
            )

            for i, (order_id, group) in enumerate(
                grouped_orders,
                1
            ):

                customer_name = str(
                    group["Customer Name"].iloc[0]
                )

                order_date = str(
                    group["Date"].iloc[0]
                )

                item_count = int(
                    group["Quantity"].sum()
                )

                order_total = group["Amount"].sum()

                st.write(
                    f"### 📦 Order #{i}"
                )

                st.write(
                    f"**Customer:** {customer_name}"
                )

                st.write(
                    f"**Order Date:** {order_date}"
                )

                st.write(
                    f"**Items:** {item_count}"
                )

                st.write(
                    f"**Total:** ₹{order_total:,.0f}"
                )

                st.write(
                    "**Status:** ✅ Order Placed"
                )

                with st.expander(
                    "View Order Details"
                ):

                    for _, row in group.iterrows():

                        st.write(
                            f"• {row['Product']} × "
                            f"{int(row['Quantity'])} = "
                            f"₹{float(row['Amount']):,.0f}"
                        )

                st.divider()

        else:

            st.info(
                "No orders placed yet."
            )

    else:

        st.info(
            "No orders placed yet."
        )
        # =========================================================
# ANALYTICS
# =========================================================

elif st.session_state.page == "Analytics":

    st.subheader("📊 Sales Data Analytics")

    st.write(
        "Python and Pandas are used to analyse "
        "sales data collected from customer orders."
    )

    if not os.path.exists(SALES_FILE):

        st.info(
            "No sales data available yet. "
            "Place an order first."
        )

    else:

        df = pd.read_csv(
            SALES_FILE,
            dtype={
                "Order ID": str,
                "Phone": str
            }
        )

        if df.empty:

            st.info(
                "No sales records available."
            )

        else:

            for column in [
                "Price",
                "Quantity",
                "Amount"
            ]:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).fillna(0)

            total_sales = df["Amount"].sum()

            total_products = df["Quantity"].sum()

            total_orders = df["Order ID"].nunique()

            average_order_value = (
                total_sales / total_orders
                if total_orders
                else 0
            )

            product_quantity = (
                df.groupby("Product")["Quantity"]
                .sum()
                .sort_values(ascending=False)
            )

            product_sales = (
                df.groupby("Product")["Amount"]
                .sum()
                .sort_values(ascending=False)
            )

            category_sales = (
                df.groupby("Category")["Amount"]
                .sum()
                .sort_values(ascending=False)
            )

            # ---------------- METRICS ----------------

            st.subheader(
                "📌 Key Sales Metrics"
            )

            a, b, c, d = st.columns(4)

            a.metric(
                "💰 Total Sales",
                f"₹{total_sales:,.0f}"
            )

            b.metric(
                "📦 Total Orders",
                total_orders
            )

            c.metric(
                "🛍️ Products Sold",
                int(total_products)
            )

            d.metric(
                "⭐ Best-Selling Product",
                product_quantity.index[0]
            )

            st.divider()

            # ---------------- AVERAGE ORDER ----------------

            st.subheader(
                "💵 Average Order Value"
            )

            st.write(
                f"₹{average_order_value:,.2f}"
            )

            st.divider()

            # ---------------- PRODUCT SALES ----------------

            st.subheader(
                "🏆 Product-wise Sales"
            )

            st.bar_chart(
                product_sales
            )

            st.divider()

            # ---------------- CATEGORY SALES ----------------

            st.subheader(
                "📂 Category-wise Sales"
            )

            st.bar_chart(
                category_sales
            )

            st.divider()

            # ---------------- QUANTITY ----------------

            st.subheader(
                "📦 Quantity Sold by Product"
            )

            st.bar_chart(
                product_quantity
            )

            st.divider()

            # ---------------- SALES TREND ----------------

            st.subheader(
                "📅 Sales Trend"
            )

            df["Date"] = pd.to_datetime(
                df["Date"],
                errors="coerce"
            )

            daily_sales = (
                df.groupby(
                    df["Date"].dt.date
                )["Amount"]
                .sum()
            )

            st.line_chart(
                daily_sales
            )

            st.divider()

            # ---------------- DATA TABLE ----------------

            st.subheader(
                "📋 Sales Data"
            )

            st.dataframe(
                df.astype({
                    "Order ID": str,
                    "Phone": str
                }),
                use_container_width=True
            )

            st.download_button(
                "⬇️ Download Sales Data",
                df.to_csv(index=False),
                "sales_data.csv",
                "text/csv"
            )