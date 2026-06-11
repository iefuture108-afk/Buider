import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="CarryMe Store",
    page_icon="👜",
    layout="wide"
)

# 2. Mock Product Data
PRODUCTS = [
    {
        "id": 1,
        "name": "Classic Leather Tote",
        "price": 120.00,
        "desc": "Spacious everyday carry made from premium full-grain leather.",
        "img": "💼"
    },
    {
        "id": 2,
        "name": "Canvas Adventure Backpack",
        "price": 85.00,
        "desc": "Water-resistant canvas with heavy-duty straps for rugged travel.",
        "img": "🎒"
    },
    {
        "id": 3,
        "name": "Minimalist Crossbody Bag",
        "price": 45.00,
        "desc": "Sleek, compact design perfect for carrying just the essentials.",
        "img": "👛"
    },
    {
        "id": 4,
        "name": "Urban Sling Pack",
        "price": 60.00,
        "desc": "Quick-access shoulder pack designed for modern city commuters.",
        "img": "🧳"
    }
]

# 3. Initialize Shopping Cart Session State
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Helper functions to manage cart actions
def add_to_cart(prod_id):
    if prod_id in st.session_state.cart:
        st.session_state.cart[prod_id] += 1
    else:
        st.session_state.cart[prod_id] = 1

def remove_from_cart(prod_id):
    if prod_id in st.session_state.cart:
        del st.session_state.cart[prod_id]

# 4. Main Application UI Layout
st.title("👜 CarryMe Store")
st.write("Welcome to the ultimate collection of premium carry gear.")
st.divider()

# Create layout columns: Left for Products, Right for Cart Sidebar
col_products, col_cart = st.columns([3, 1.2], gap="large")

# --- LEFT COLUMN: PRODUCT GRID ---
with col_products:
    st.subheader("Our Collection")
    
    # Render products in a clean 2x2 responsive grid
    grid_cols = st.columns(2)
    
    for idx, item in enumerate(PRODUCTS):
        # Alternate between the two grid columns
        with grid_cols[idx % 2]:
            with st.container(border=True):
                st.large_caption(f"{item['img']} Item #{item['id']}")
                st.subheader(item["name"])
                st.write(f"**Price:** ${item['price']:.2f}")
                st.write(item["desc"])
                
                # Unique key for each button to avoid session conflicts
                st.button(
                    f"Add to Cart", 
                    key=f"add_{item['id']}", 
                    on_click=add_to_cart, 
                    args=(item['id'],),
                    type="primary"
                )

# --- RIGHT COLUMN: SHOPPING CART SIDEBAR ---
with col_cart:
    st.subheader("🛒 Your Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is currently empty.")
    else:
        grand_total = 0.0
        
        # Display each item added to the cart
        for prod_id, quantity in list(st.session_state.cart.items()):
            # Find product details by ID
            item = next((p for p in PRODUCTS if p["id"] == prod_id), None)
            if item:
                item_total = item["price"] * quantity
                grand_total += item_total
                
                with st.container(border=True):
                    st.markdown(f"**{item['name']}**")
                    st.write(f"Qty: {quantity} × ${item['price']:.2f}")
                    st.write(f"Subtotal: **${item_total:.2f}**")
                    
                    st.button(
                        "Remove", 
                        key=f"rem_{prod_id}", 
                        on_click=remove_from_cart, 
                        args=(prod_id,),
                        type="secondary",
                        help="Remove item from cart"
                    )
        
        st.divider()
        st.metric(label="Total Amount Due", value=f"${grand_total:.2f}")
        
        # Checkout Actions
        checkout_clicked = st.button("Proceed to Checkout", use_container_width=True, type="primary")
        if checkout_clicked:
            st.success("🎉 Order placed successfully! Thank you for shopping with CarryMe.")
            st.session_state.cart = {} # Clear cart after successful checkout
