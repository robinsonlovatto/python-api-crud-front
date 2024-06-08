import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

st.image("logo.png", width=200)

st.title("Products Management")


# Displays detailed error messages
def show_response_message(response):
    if response.status_code == 200:
        st.success("Operation finished succesfully!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                # whether the error is a list, extract each message
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"] for error in data["detail"]])
                    st.error(f"Error: {errors}")
                else:
                    # display the error message
                    st.error(f"Error: {data['detail']}")
        except ValueError:
            st.error("Unhandled error. It was not possible to identify the error message.")


# Add a new product
with st.expander("Add product"):
    with st.form("new_product"):
        name = st.text_input("Product Name")
        description = st.text_area("Product Description")
        price = st.number_input("Price", min_value=0.01, format="%f")
        category = st.selectbox(
            "Category",
            ["Eletronics", "Furniture", "Clothes", "Shoes"],
        )
        supplier_email = st.text_input("Supplier e-mail")
        submit_button = st.form_submit_button("Add product")

        if submit_button:
            response = requests.post(
                "http://backend:8000/products/",
                json={
                    "name": name,
                    "description": description,
                    "price": price,
                    "category": category,
                    "supplier_email": supplier_email,
                },
            )
            show_response_message(response)

# See the products
with st.expander("Check the products"):
    if st.button("Show all products"):
        response = requests.get("http://backend:8000/products/")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame(product)

            df = df[
                [
                    "id",
                    "name",
                    "description",
                    "price",
                    "category",
                    "supplier_email",
                    "created_at",
                ]
            ]

            # displays the dataframe with no index
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Get product details
with st.expander("Get Product Details"):
    get_id = st.number_input("Product Id", min_value=1, format="%d")
    if st.button("Search Product"):
        response = requests.get(f"http://backend:8000/products/{get_id}")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame([product])

            df = df[
                [
                    "id",
                    "name",
                    "description",
                    "price",
                    "category",
                    "supplier_email",
                    "created_at",
                ]
            ]

            # displays the dataframe with no index
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Delete product
with st.expander("Delete Product"):
    delete_id = st.number_input("Product Id to delete", min_value=1, format="%d")
    if st.button("Delete Product"):
        response = requests.delete(f"http://backend:8000/products/{delete_id}")
        show_response_message(response)

# Edit Product
with st.expander("Edit Product"):
    with st.form("update_product"):
        update_id = st.number_input("Product Id to edit", min_value=1, format="%d")
        new_name = st.text_input("New Product Name")
        new_description = st.text_area("New Product Description")
        new_price = st.number_input(
            "New Price",
            min_value=0.01,
            format="%f",
        )
        new_category = st.selectbox(
            "New Category",
            ["Eletronics", "Furniture", "Clothes", "Shoes"]
        )
        new_email = st.text_input("New Supplier E-mail")

        update_button = st.form_submit_button("Edit Product")

        if update_button:
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_description:
                update_data["description"] = new_description
            if new_price > 0:
                update_data["price"] = new_price
            if new_email:
                update_data["supplier_email"] = new_email
            if new_category:
                update_data["category"] = new_category

            if update_data:
                response = requests.put(
                    f"http://backend:8000/products/{update_id}", json=update_data
                )
                show_response_message(response)
            else:
                st.error("No data provided to edit.")