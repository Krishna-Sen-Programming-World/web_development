# cd .\project
# uvicorn backend:app --reload
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from datetime import datetime
import psycopg2
import os




DB_NAME = "restaurant.db"

def get_conn():
    # Use the DATABASE_URL environment variable from Render
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            category TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            sale_date TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()



init_db()




class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None

class ProductRead(ProductBase):
    id: int

class SaleBase(BaseModel):
    product_id: int
    quantity: int

class SaleRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_amount: float
    sale_date: str


app = FastAPI()




@app.post("/products")
def create_product(product: ProductBase):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products (name, price, stock, category)
        VALUES (?, ?, ?, ?)
    """, (product.name, product.price, product.stock, product.category))
    
    conn.commit()
    pid = cur.lastrowid
    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    row = cur.fetchone()
    conn.close()

    return {
        "message": "Product created successfully.",
        "product": ProductRead(**row)
    }

    # return ProductRead(**row)




@app.get("/products")
def list_products(category: Optional[str] = Query(None, alias="category")):
    conn = get_conn()
    cur = conn.cursor()

    if category:
        cur.execute("SELECT * FROM products WHERE category=?", (category,))
    else:
        cur.execute("SELECT * FROM products")

    rows = cur.fetchall()
    conn.close()

    return [ProductRead(**row) for row in rows]


@app.get("/products/{pid}")
def get_product(pid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(404, "Product not found")
    return ProductRead(**row)


@app.put("/products/{pid}")
def update_product(pid: int, data: ProductBase):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    if not cur.fetchone():
        raise HTTPException(404, "Product not found")

    cur.execute("""
        UPDATE products SET name=?, price=?, stock=?, category=?
        WHERE id=?
    """, (data.name, data.price, data.stock, data.category, pid))

    conn.commit()
    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    row = cur.fetchone()
    conn.close()
    return {
        "message": f"Product with ID {pid} has been updated successfully.",
        "product": ProductRead(**row)
    }

    # return ProductRead(**row)

@app.patch("/products/{pid}")
def patch_product(pid: int, data: ProductUpdate):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(404, "Product not found")

    updated = dict(row)
    payload = data.model_dump(exclude_unset=True)
    updated.update(payload)

    cur.execute("""
        UPDATE products SET name=?, price=?, stock=?, category=?
        WHERE id=?
    """, (updated["name"], updated["price"], updated["stock"], updated["category"], pid))

    conn.commit()
    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    row = cur.fetchone()
    conn.close()
    return {
        "message": f"✅ Product with ID {pid} has been partially updated successfully.",
        "product": ProductRead(**row)
    }

    # return ProductRead(**row)

@app.delete("/products/{pid}")
def delete_product(pid: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    product = cur.fetchone()
    
    if not product:
        raise HTTPException(404, detail="Product not found")

    cur.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    cur.execute("DELETE FROM sales WHERE product_id=?", (pid,))
    conn.commit()
    
    conn.close()
    
    return {"message": f"Product with id {pid} and its related sales have been deleted."}




@app.post("/sales")
def create_sale(sale: SaleBase):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM products WHERE id=?", (sale.product_id,))
    product = cur.fetchone()

    if not product:
        raise HTTPException(404, "Product not found")


    if product["stock"] == 0:
        raise HTTPException(
            status_code=400,
            detail="Product is out of stock."
        )

    # if product["stock"] < sale.quantity:
        # raise HTTPException(400, "Not enough stock")

    if sale.quantity > product["stock"]:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stock. Available: {product['stock']}, requested: {sale.quantity}"
        )


    total = product["price"] * sale.quantity

    cur.execute("""
        INSERT INTO sales (product_id, quantity, total_amount, sale_date)
        VALUES (?, ?, ?, ?)
    """, (sale.product_id, sale.quantity, total, datetime.now().isoformat()))

    cur.execute("""
        UPDATE products SET stock = stock - ?
        WHERE id = ?
    """, (sale.quantity, sale.product_id))

    conn.commit()

    sid = cur.lastrowid
    cur.execute("SELECT * FROM sales WHERE id=?", (sid,))
    row = cur.fetchone()
    conn.close()
    return{
        "message": f"✅ Transaction successful.",
        "product":SaleRead(**row)
    }

@app.get("/sales")
def list_sales():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    rows = cur.fetchall()
    conn.close()
    return [SaleRead(**row) for row in rows]




