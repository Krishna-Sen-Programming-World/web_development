# # cd .\project
# # python -m streamlit run .\restaurant_ui.py

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px  # For the pie chart


API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Hypermarket Inventory and Sales Management System", layout="wide")
st.title("🛒 Hypermarket Inventory and Sales Management System")

st.sidebar.header("Configuration & Navigation")
api_url = st.sidebar.text_input("FastAPI base URL", API_BASE_URL)

section = st.sidebar.radio("Choose View", [
    "Products 🛒",
    "Sales 💳",
    "List & Charts 📊",
])
def show_response(resp: requests.Response, method: str, endpoint: str):
    try:
        j = resp.json()
        if 'message' in j:
            st.success(j['message'])  
            
    except Exception:
        st.error("Failed to parse response")  
        

    with st.expander("Show Response"):

        st.text(f"➡ {method} {endpoint} (status {resp.status_code})")
        

        try:
            st.json(resp.json())  
        except Exception:
            st.text(resp.text) 


def fetch_products(category=None):
    url = f"{api_url}/products"
    params = {}
    if category:
        params['category'] = category
    
    try:
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return pd.DataFrame(resp.json())
        else:
            st.error(f"Failed to fetch products: {resp.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()


def fetch_sales():
    resp = requests.get(f"{api_url}/sales")
    if resp.status_code == 200:
        return pd.DataFrame(resp.json())
    else:
        st.error(f"Failed to fetch sales: {resp.status_code}")
        return pd.DataFrame()


if section == "Products 🛒":
    st.header("🧾 Products Management")

    tab_list, tab_create, tab_update, tab_patch, tab_delete = st.tabs([
        "List 📋", "Create ➕", "Full Update (PUT) 🔄",
        "Partial Update (PATCH) ✏️", "Delete 🗑️"
    ])

    with tab_list:
        st.subheader("All Products")

        category_filter = st.text_input("Search by Category (optional)", "", key="category_filter_input")

        category = category_filter.strip() if category_filter else None

        if "products_data" not in st.session_state or category != st.session_state.category:
            st.session_state.products_data = None
            st.session_state.category = category
        
        if st.button("Refresh List 🔄"):
            st.session_state.products_data = fetch_products(category)
        
        if st.session_state.products_data is not None:
            df = st.session_state.products_data

            if not df.empty:
                if 'id' in df.columns:
                    cols = ['id'] + [col for col in df.columns if col != 'id']
                    df = df[cols]
                
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No products available.")

    with tab_create:
        st.subheader("Create New Product")
        with st.form("create_product"):
            name = st.text_input("Product Name")
            price = st.number_input("Price (INR)",
                                    min_value=0.0,
                                    step=0.01,
                                    format="%.2f")
            stock = st.number_input("Stock", min_value=0, step=1, format="%d")
            category = st.text_input("Category (optional)")
            submitted = st.form_submit_button("Create Product ➕")

        if submitted:
            payload = {
                "name": name,
                "price": price,
                "stock": int(stock),
                "category": category or None
            }
            try:
                resp = requests.post(f"{api_url}/products", json=payload)
                show_response(resp, "POST", "/products")
            except Exception as e:
                st.error(f"Error: {e}")

    with tab_update:
        st.subheader("Full Update (Replace All Fields)")
        pid = st.number_input("Product ID to Replace",
                              min_value=1,
                              step=1,
                              format="%d")
        with st.form("put_product"):
            name2 = st.text_input("New Name")
            price2 = st.number_input("New Price",
                                     min_value=0.0,
                                     step=0.01,
                                     format="%.2f")
            stock2 = st.number_input("New Stock",
                                     min_value=0,
                                     step=1,
                                     format="%d")
            category2 = st.text_input("New Category")
            put_submit = st.form_submit_button("Update Product 🔄")

        if put_submit:
            payload = {
                "name": name2,
                "price": price2,
                "stock": int(stock2),
                "category": category2 or None
            }
            try:
                endpoint = f"/products/{int(pid)}"
                resp = requests.put(f"{api_url}{endpoint}", json=payload)
                if resp.status_code == 404:
                    st.error(f"❌ Product with ID {pid} not found!")
                show_response(resp, "PUT", endpoint)

            except Exception as e:
                st.error(f"Error: {e}")

    with tab_patch:
        st.subheader("Partial Update (Update Selected Fields)")
        pid2 = st.number_input("Product ID to Update",
                               min_value=1,
                               step=1,
                               format="%d",
                               key="ppid")
        st.write("Select fields to update")
        patch_payload = {}
        if st.checkbox("Change Name"):
            new_name = st.text_input("New Name", key="patch_name")
            if new_name:
                patch_payload["name"] = new_name
        if st.checkbox("Change Price"):
            new_price = st.number_input("New Price",
                                        min_value=0.0,
                                        step=0.01,
                                        format="%.2f",
                                        key="patch_price")
            patch_payload["price"] = new_price
        if st.checkbox("Change Stock"):
            new_stock = st.number_input("New Stock",
                                        min_value=0,
                                        step=1,
                                        format="%d",
                                        key="patch_stock")
            patch_payload["stock"] = int(new_stock)
        if st.checkbox("Change Category"):
            new_cat = st.text_input("New Category", key="patch_cat")
            patch_payload["category"] = new_cat

        if st.button("Apply Partial Update ✏️"):
            if not patch_payload:
                st.warning("No fields selected to update.")
            else:
                try:
                    endpoint = f"/products/{int(pid2)}"
                    resp = requests.patch(f"{api_url}{endpoint}",
                                          json=patch_payload)

                    if resp.status_code == 404:
                        st.error(f"❌ Product with ID {pid2} not found!")
                    show_response(resp, "PATCH", endpoint)

                except Exception as e:
                    st.error(f"Error: {e}")

    with tab_delete:
        st.subheader("Delete product")

        pid3 = st.number_input("Product ID to delete",
                               min_value=1,
                               step=1,
                               format="%d",
                               key="delpid")

        confirm_delete = st.checkbox("I confirm I want to delete this product",
                                     key="confirm_delete")

        if confirm_delete:
            if st.button("Delete product 🗑️"):
                try:
                    endpoint = f"/products/{int(pid3)}"
                    resp = requests.delete(f"{api_url}{endpoint}")

                    if resp.status_code == 404:
                        st.error(f"❌ Product with ID {pid3} not found!")


                    show_response(resp, "DELETE", endpoint)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning(
                "Please confirm the deletion by checking the box above.")





elif section == "Sales 💳":
    st.header("💳 Sales Management")

    tab_s_list, tab_s_create = st.tabs(["List 📋", "Create Sale ➕"])

    with tab_s_list:
        st.subheader("All Sales")
        if st.button("Refresh Sales List 🔄"):
            sdf = fetch_sales()
            if not sdf.empty:
                st.dataframe(sdf, use_container_width=True)
            else:
                st.write("No sales records available.")
                st.dataframe(sdf.columns.to_frame().T, use_container_width=True)  # Show only column names




    with tab_s_create:
        st.subheader("Create New Sale")
        prod_df = fetch_products()
        if prod_df.empty:
            st.warning("No products available. Create products first.")
        else:
            prod_options = {
                row['name'] + f" (id={row['id']}, stock={row['stock']})":
                int(row['id'])
                for _, row in prod_df.iterrows()
            }
            
            sel = st.selectbox("Select Product", list(prod_options.keys()))
            selected_pid = prod_options[sel]
            
            selected_product = prod_df.loc[prod_df['id'] == selected_pid].iloc[0]
            price = selected_product['price']
            stock = selected_product['stock']
            
            st.write(f"**Price**: ₹{price:.2f}")
            
            qty = st.number_input("Quantity",
                                min_value=1,
                                value=1,
                                step=1)
            
            total_cost = price * qty
            st.write(f"**Total Cost**: ₹{total_cost:.2f}")

            if st.button("Create Sale 💳"):
                payload = {
                    "product_id": int(selected_pid),
                    "quantity": int(qty)
                }
                try:

                    resp = requests.post(f"{api_url}/sales", json=payload)
                    if resp.status_code == 400:
                        st.error(f"Transaction failed: {resp.json()['detail']}")
                    show_response(resp, "POST", "/sales")
                except Exception as e:
                    st.error(f"Error: {e}")






elif section == "List & Charts 📊":
    st.header("📈 Sales Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    prod_df = fetch_products()
    sdf = fetch_sales()

    if sdf.empty or prod_df.empty:
        st.warning("No data available to generate the dashboard.")
    else:
        total_sales = sdf['total_amount'].sum()
        total_quantity = sdf['quantity'].sum()
        total_products = len(prod_df)
        total_categories = prod_df['category'].nunique()
        container = st.container(border=True)

        with container:

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Sales", f"₹{total_sales:,.2f}")
            with col2:
                st.metric("Total Quantity Sold", f"{total_quantity:,}")
            with col3:
                st.metric("Total Products", f"{total_products:,}")
            with col4:
                st.metric("Total Categories", f"{total_categories:,}")



    st.subheader("Sales Breakdown by Product")
    chart_type = st.selectbox("Select Chart Type", ["Pie", "Bar", "Line"], key="chart_type")

    if st.button("Generate Chart 📊"):
        if not sdf.empty:
            grouped = sdf.groupby('product_id').agg({
                'total_amount': 'sum',
                'quantity': 'sum'
            }).reset_index()

            grouped = grouped.merge(prod_df[['id', 'name']], left_on='product_id', right_on='id', how='left')

            st.write("Aggregated Sales Data")
            st.dataframe(grouped, use_container_width=True)

            chart_df = pd.DataFrame({
                'product_name': grouped['name'],
                'Metric': grouped["total_amount"]
            })
            chart_df = chart_df.set_index('product_name')

            if chart_type == 'Bar':
                st.write("### Bar Chart")
                fig = px.bar(chart_df, x=chart_df.index, y='Metric', title='Sales Distribution by Product')
                fig.update_layout(
                    xaxis_title="Product Name",
                    yaxis_title="Total Sales Amount (INR)"
                )
                st.plotly_chart(fig)

            elif chart_type == 'Line':
                st.write("### Line Chart")
                fig = px.line(chart_df, x=chart_df.index, y='Metric', title='Sales Distribution by Product')
                fig.update_layout(xaxis_title="Product Name", yaxis_title="Total Sales Amount (INR)")
                st.plotly_chart(fig)

            elif chart_type == 'Pie':
                st.write("### Pie Chart")
                fig = px.pie(grouped, names='name', values='total_amount', title='Sales Distribution by Product')
                st.plotly_chart(fig)

        else:
            st.warning("No data available to generate the selected chart.")

