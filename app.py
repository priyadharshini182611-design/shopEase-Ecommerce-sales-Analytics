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

# =========================
# STYLING
# =========================

st.markdown("""
<style>

.main {
    background-color: #ffffff;
}

/* Shop title */
.shop-title {
    font-size: 38px;
    font-weight: bold;
    color: #222222 !important;
    margin-bottom: 0px;
}

/* Subtitle */
.shop-subtitle {
    font-size: 18px;
    color: #555555 !important;
    margin-bottom: 25px;
}

/* Product card */
.product-card {
    padding: 20px;
    border: 1px solid #eeeeee;
    border-radius: 15px;
    background-color: #ffffff;
    margin-bottom: 15px;
}

/* PRODUCT NAME - DARK */
.product-name {
    color: #111111 !important;
    font-size: 22px;
    font-weight: 700;
}

/* PRODUCT CATEGORY - DARK */
.product-category {
    color: #333333 !important;
    font-size: 16px;
    font-weight: 500;
}

/* PRODUCT DESCRIPTION - DARK */
.product-description {
    color: #333333 !important;
    font-size: 15px;
}

/* PRICE - DARK */
.price {
    font-size: 22px;
    font-weight: bold;
    color: #111111 !important;
}

/* Banner */
.banner {
    padding: 25px;
    border-radius: 15px;
    background-color: #f5f5f5;
    margin-bottom: 25px;
}

.banner h1 {
    color: #111111 !important;
}

.banner p {
    color: #333333 !important;
}

/* Buttons */
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =========================
# PRODUCTS
# =========================

products = [

    {
        "id": 1,
        "name": "Elegant Silk Saree",
        "category": "Sarees",
        "price": 899,
        "icon": "👗",
        "description": "Beautiful traditional silk saree suitable for special occasions."
    },

    {
        "id": 2,
        "name": "Designer Handbag",
        "category": "Bags",
        "price": 599,
        "icon": "👜",
        "description": "Stylish and spacious handbag for everyday use."
    },

    {
        "id": 3,
        "name": "Printed Cotton Kurti",
        "category": "Kurtis",
        "price": 499,
        "icon": "👚",
        "description": "Comfortable printed cotton kurti with a modern design."
    },

    {
        "id": 4,
        "name": "Party Wear Saree",
        "category": "Sarees",
        "price": 1099,
        "icon": "🥻",
        "description": "Trendy party wear saree with an elegant look."
    },

    {
        "id": 5,
        "name": "Casual Shoulder Bag",
        "category": "Bags",
        "price": 449,
        "icon": "🎒",
        "description": "Compact shoulder bag perfect for casual outings."
    },

    {
        "id": 6,
        "name": "Floral Kurti",
        "category": "Kurtis",
        "price": 549,
        "icon": "👕",
        "description": "Comfortable floral kurti for daily and casual wear."
    }
]


# =========================
# SESSION STATE
# =========================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None


# =========================
# SAVE ORDER
# =========================

def save_order(order):

    file_exists = os.path.exists(SALES_FILE)

    with open(
        SALES_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

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
                "Total"
            ])

        writer.writerow([
            str(order["order_id"]),
            order["date"],
            order["customer"],
            order["phone"],
            order["address"],
            order["product"],
            order["category"],
            order["price"],
            order["quantity"],
            order["total"]
        ])


# =========================
# HEADER
# =========================

st.markdown(
    '<div class="shop-title">🛍️ ShopEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="shop-subtitle">Smart E-Commerce Store with Python Sales Analytics</div>',
    unsafe_allow_html=True
)


# =========================
# SEARCH
# =========================

search = st.text_input(
    "🔍 Search products",
    placeholder="Search sarees, bags, kurtis..."
)


# =========================
# NAVIGATION
# =========================

nav_cols = st.columns(6)

with nav_cols[0]:

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):

        st.session_state.page = "Home"


with nav_cols[1]:

    if st.button(
        "👗 Sarees",
        use_container_width=True
    ):

        st.session_state.page = "Sarees"


with nav_cols[2]:

    if st.button(
        "👜 Bags",
        use_container_width=True
    ):

        st.session_state.page = "Bags"


with nav_cols[3]:

    if st.button(
        "👚 Kurtis",
        use_container_width=True
    ):

        st.session_state.page = "Kurtis"


with nav_cols[4]:

    if st.button(
        "🛒 Cart",
        use_container_width=True
    ):

        st.session_state.page = "Cart"


with nav_cols[5]:

    if st.button(
        "📦 Orders",
        use_container_width=True
    ):

        st.session_state.page = "Orders"


st.divider()


# =========================
# SHOW PRODUCTS
# =========================

def show_products(product_list):

    if search:

        product_list = [

            p for p in product_list

            if search.lower() in p["name"].lower()
            or search.lower() in p["category"].lower()

        ]

    if not product_list:

        st.warning("No products found.")

        return


    for i in range(
        0,
        len(product_list),
        3
    ):

        cols = st.columns(3)


        for col, p in zip(
            cols,
            product_list[i:i + 3]
        ):

            with col:

                # Product icon/card

                st.markdown(
                    f"""
                    <div class="product-card">

                        <div style="
                            font-size:70px;
                            text-align:center;
                        ">
                            {p["icon"]}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # PRODUCT NAME

                st.markdown(
                    f"""
                    <div class="product-name">
                        {p["name"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # CATEGORY

                st.markdown(
                    f"""
                    <div class="product-category">
                        Category: {p["category"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # PRICE

                st.markdown(
                    f"""
                    <div class="price">
                        ₹{p["price"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # DESCRIPTION

                st.markdown(
                    f"""
                    <div class="product-description">
                        {p["description"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                c1, c2 = st.columns(2)


                with c1:

                    if st.button(
                        "View",
                        key=f"view_{p['id']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_product = p

                        st.session_state.page = "Product"


                with c2:

                    if st.button(
                        "Add 🛒",
                        key=f"add_{p['id']}",
                        use_container_width=True
                    ):

                        st.session_state.cart.append({
                            "product": p,
                            "quantity": 1
                        })

                        st.success(
                            "Added to cart!"
                        )


# =========================
# HOME PAGE
# =========================

if st.session_state.page == "Home":

    st.markdown(
        """
        <div class="banner">

            <h1>
                Welcome to ShopEase 🛍️
            </h1>

            <p>
                Discover stylish sarees, trendy bags
                and beautiful kurtis at affordable prices.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.subheader(
        "✨ Featured Products"
    )

    show_products(products)


# =========================
# CATEGORY PAGES
# =========================

elif st.session_state.page in [
    "Sarees",
    "Bags",
    "Kurtis"
]:

    category = st.session_state.page

    st.title(
        f"{category} Collection"
    )


    category_products = [

        p for p in products

        if p["category"] == category

    ]


    show_products(
        category_products
    )


# =========================
# PRODUCT DETAILS
# =========================

elif st.session_state.page == "Product":

    p = st.session_state.selected_product


    if p is not None:

        st.title(
            p["name"]
        )


        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:120px;
            ">
                {p["icon"]}
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
            <div class="product-name">
                {p["name"]}
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
            <div class="product-category">
                Category: {p["category"]}
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
            <div class="price">
                ₹{p["price"]}
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            f"""
            <div class="product-description">
                {p["description"]}
            </div>
            """,
            unsafe_allow_html=True
        )


        st.write(
            "### Product Features"
        )


        st.write(
            "✔ Good quality product"
        )

        st.write(
            "✔ Affordable price"
        )

        st.write(
            "✔ Suitable for everyday use"
        )

        st.write(
            "✔ Easy online ordering"
        )


        c1, c2, c3 = st.columns(3)


        with c1:

            if st.button(
                "🛒 Add to Cart",
                use_container_width=True
            ):

                st.session_state.cart.append({
                    "product": p,
                    "quantity": 1
                })

                st.success(
                    "Product added to cart!"
                )


        with c2:

            if st.button(
                "❤️ Wishlist",
                use_container_width=True
            ):

                if p not in st.session_state.wishlist:

                    st.session_state.wishlist.append(p)

                    st.success(
                        "Added to wishlist!"
                    )


        with c3:

            if st.button(
                "⬅️ Back",
                use_container_width=True
            ):

                st.session_state.page = "Home"


    else:

        st.warning(
            "Product not found."
        )


# =========================
# CART PAGE
# =========================

elif st.session_state.page == "Cart":

    st.title(
        "🛒 Shopping Cart"
    )


    if not st.session_state.cart:

        st.info(
            "Your cart is empty."
        )


        if st.button(
            "🛍️ Continue Shopping"
        ):

            st.session_state.page = "Home"


    else:

        grand_total = 0


        for index, item in enumerate(
            st.session_state.cart
        ):

            p = item["product"]

            quantity = item["quantity"]

            item_total = (
                p["price"] * quantity
            )


            grand_total += item_total


            col1, col2, col3, col4 = st.columns(
                [3, 1, 1, 1]
            )


            with col1:

                st.markdown(
                    f"""
                    <div class="product-name">
                        {p['icon']} {p['name']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.caption(
                    f"₹{p['price']} × {quantity}"
                )


            with col2:

                if st.button(
                    "➖",
                    key=f"minus_{index}"
                ):

                    if item["quantity"] > 1:

                        item["quantity"] -= 1

                    else:

                        st.session_state.cart.pop(
                            index
                        )

                    st.rerun()


            with col3:

                st.write(
                    f"Qty: {quantity}"
                )


                if st.button(
                    "➕",
                    key=f"plus_{index}"
                ):

                    item["quantity"] += 1

                    st.rerun()


            with col4:

                st.write(
                    f"₹{item_total}"
                )


                if st.button(
                    "🗑️ Remove",
                    key=f"remove_{index}"
                ):

                    st.session_state.cart.pop(
                        index
                    )

                    st.rerun()


            st.divider()


        st.subheader(
            f"Grand Total: ₹{grand_total}"
        )


        if st.button(
            "💳 Proceed to Checkout",
            use_container_width=True
        ):

            st.session_state.page = "Checkout"


# =========================
# CHECKOUT
# =========================

elif st.session_state.page == "Checkout":

    st.title(
        "💳 Checkout"
    )


    if not st.session_state.cart:

        st.warning(
            "Your cart is empty."
        )


        if st.button(
            "Go Shopping"
        ):

            st.session_state.page = "Home"


    else:

        st.subheader(
            "Customer Details"
        )


        customer_name = st.text_input(
            "Full Name"
        )


        phone = st.text_input(
            "Phone Number"
        )


        address = st.text_area(
            "Delivery Address"
        )


        st.subheader(
            "Order Summary"
        )


        checkout_total = 0


        for item in st.session_state.cart:

            p = item["product"]

            quantity = item["quantity"]

            total = (
                p["price"] * quantity
            )


            checkout_total += total


            st.markdown(
                f"""
                <div class="product-description">
                    {p['icon']} {p['name']} × {quantity}
                    = ₹{total}
                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown(
            f"### Total Amount: ₹{checkout_total}"
        )


        if st.button(
            "✅ Place Order",
            use_container_width=True
        ):

            if (
                not customer_name
                or not phone
                or not address
            ):

                st.error(
                    "Please fill all customer details."
                )


            else:

                order_id = datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                )


                for item in st.session_state.cart:

                    p = item["product"]

                    quantity = item["quantity"]


                    order = {

                        "order_id": order_id,

                        "date": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                        "customer": customer_name,

                        "phone": phone,

                        "address": address,

                        "product": p["name"],

                        "category": p["category"],

                        "price": p["price"],

                        "quantity": quantity,

                        "total": (
                            p["price"] * quantity
                        )
                    }


                    save_order(order)


                st.session_state.cart = []


                st.success(
                    f"🎉 Order placed successfully! "
                    f"Order ID: {order_id}"
                )


                st.session_state.page = "Orders"


# =========================
# WISHLIST
# =========================

elif st.session_state.page == "Wishlist":

    st.title(
        "❤️ My Wishlist"
    )


    if not st.session_state.wishlist:

        st.info(
            "Your wishlist is empty."
        )


    else:

        for p in st.session_state.wishlist:

            st.markdown(
                f"""
                <div class="product-name">
                    {p['icon']} {p['name']}
                </div>

                <div class="price">
                    ₹{p['price']}
                </div>
                """,
                unsafe_allow_html=True
            )


            if st.button(
                "🛒 Add to Cart",
                key=f"wishlist_cart_{p['id']}"
            ):

                st.session_state.cart.append({
                    "product": p,
                    "quantity": 1
                })


                st.success(
                    "Added to cart!"
                )


# =========================
# ORDERS
# =========================

elif st.session_state.page == "Orders":

    st.title(
        "📦 My Orders"
    )


    if not os.path.exists(
        SALES_FILE
    ):

        st.info(
            "No orders placed yet."
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
                "No orders placed yet."
            )


        else:

            st.success(
                f"You have placed "
                f"{df['Order ID'].nunique()} order(s)."
            )


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


# =========================
# ANALYTICS
# =========================

elif st.session_state.page == "Analytics":

    st.title(
        "📊 Sales Analytics"
    )


    if not os.path.exists(
        SALES_FILE
    ):

        st.info(
            "No sales data available yet."
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
                "No sales data available yet."
            )


        else:

            df["Price"] = pd.to_numeric(
                df["Price"],
                errors="coerce"
            )


            df["Quantity"] = pd.to_numeric(
                df["Quantity"],
                errors="coerce"
            )


            df["Total"] = pd.to_numeric(
                df["Total"],
                errors="coerce"
            )


            total_sales = df["Total"].sum()


            total_orders = (
                df["Order ID"].nunique()
            )


            products_sold = (
                df["Quantity"].sum()
            )


            average_order_value = (

                total_sales / total_orders

                if total_orders > 0

                else 0

            )


            best_product = (

                df.groupby("Product")["Quantity"]

                .sum()

                .idxmax()

            )


            c1, c2, c3, c4, c5 = st.columns(5)


            with c1:

                st.metric(
                    "💰 Total Sales",
                    f"₹{total_sales:,.0f}"
                )


            with c2:

                st.metric(
                    "📦 Total Orders",
                    total_orders
                )


            with c3:

                st.metric(
                    "🛍️ Products Sold",
                    int(products_sold)
                )


            with c4:

                st.metric(
                    "🏆 Best Product",
                    best_product
                )


            with c5:

                st.metric(
                    "📈 Average Order",
                    f"₹{average_order_value:,.0f}"
                )


            st.divider()


            # PRODUCT SALES

            st.subheader(
                "🛍️ Product-wise Sales"
            )


            product_sales = (

                df.groupby("Product")["Total"]

                .sum()

                .sort_values(
                    ascending=False
                )

            )


            st.bar_chart(
                product_sales
            )


            # CATEGORY SALES

            st.subheader(
                "📂 Category-wise Sales"
            )


            category_sales = (

                df.groupby("Category")["Total"]

                .sum()

                .sort_values(
                    ascending=False
                )

            )


            st.bar_chart(
                category_sales
            )


            # QUANTITY SOLD

            st.subheader(
                "📦 Quantity Sold by Product"
            )


            quantity_sales = (

                df.groupby("Product")["Quantity"]

                .sum()

                .sort_values(
                    ascending=False
                )

            )


            st.bar_chart(
                quantity_sales
            )


            # SALES TREND

            st.subheader(
                "📈 Sales Trend"
            )


            df["Date"] = pd.to_datetime(
                df["Date"],
                errors="coerce"
            )


            daily_sales = (

                df.groupby(
                    df["Date"].dt.date
                )["Total"]

                .sum()

            )


            st.line_chart(
                daily_sales
            )


            # SALES DATA

            st.subheader(
                "📋 Sales Data"
            )


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


            # DOWNLOAD

            csv_data = df.to_csv(
                index=False
            ).encode("utf-8")


            st.download_button(
                "⬇️ Download Sales Data",
                data=csv_data,
                file_name="sales_data.csv",
                mime="text/csv",
                use_container_width=True
            )
