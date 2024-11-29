from fastapi import FastAPI
from database import engine
from models import Base
from routers import products, categories
import uvicorn
# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

@app.get("/")
def root():
    return {"message": "Welcome to the Product Service!"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001)


# Great! Let's dive into the Product Service for your ecommerce microservices architecture. The Product Service will manage the products available in your ecommerce system.

# Key Features for the Product Service
# Here’s a list of functionalities we can implement for the Product Service:

# CRUD Operations for Products:
# Create a new product.
# Retrieve product details (by ID or name).
# List all products with optional filters (e.g., category, price range).
# Update product details.
# Delete a product.

# Inventory Management:
# Add or remove stock for a product.
# Track available quantity.

# Product Categories:
# Associate products with categories (e.g., Electronics, Apparel).

# Search and Filter:
# Enable search by name or category.
# Filter by price range or stock availability.

# Optional Features:
# Support for product images.
# Track product ratings and reviews.