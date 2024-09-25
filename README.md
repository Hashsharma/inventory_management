Apologies for the oversight! Here’s the complete README content with the missing instruction included in the "Create a virtual environment" section. 

```
# Inventory Management System

## Background
The Inventory Management System is designed to help businesses efficiently manage their stock of products. This system provides RESTful API endpoints for creating, reading, updating, and deleting (CRUD) items in the inventory. To enhance performance, frequently accessed items are cached using Redis, and JWT authentication secures access to the API.

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Conclusion](#conclusion)

## Setup Instructions

### Prerequisites
- Python 3.x
- Redis server
- A working installation of pip
- A virtual environment (recommended)

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/inventory-management.git
   cd inventory-management
   ```
#### Use Docker Instead
## Build the Docker Image

To build the Docker image, run the following command in the project root directory:

```bash
docker build -t your_image_name .
```

### Run the Docker Container
After building the image, you can run the container using:

```bash
docker run -p 8000:8000 your_image_name
````
   
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:** Create a `.env` file and add the following configurations:
   ```makefile
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   REDIS_URL=redis://localhost:6379
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the server:**
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Authentication
All endpoints require JWT authentication. Use the Authorization header with the format `<token>`.

### Endpoints

1. **Get All Items**
   - **URL:** `/api/items/all`
   - **Method:** GET
   - **Headers:**
     - Authorization: `<token>`
   
   **Example:**
   ```bash
   curl --location --request GET '127.0.0.1:8000/api/items/all' \
     --header 'Authorization: <your_jwt_token>'
   ```

2. **Add Item**
   - **URL:** `/api/items/add`
   - **Method:** POST
   - **Headers:**
     - Authorization: `<token>`
   
   **Example:**
   ```bash
   curl --location --request POST '127.0.0.1:8000/api/items/add' \
     --header 'Authorization: <your_jwt_token>' \
     --form 'product_name="Laptop Lenovo"' \
     --form 'category="1"' \
     --form 'product_quantity_in_stock="10"' \
     --form 'product_price="100000"' \
     --form 'product_desc="Laptop with i7"'
   ```

3. **Update Item**
   - **URL:** `/api/items/<item_id>`
   - **Method:** PUT
   - **Headers:**
     - Authorization: `<token>`
   
   **Example:**
   ```bash
   curl --location --request PUT '127.0.0.1:8000/api/items/4' \
     --header 'Authorization: <your_jwt_token>' \
     --form 'product_name="Laptop"' \
     --form 'category="1"' \
     --form 'product_quantity_in_stock="20"' \
     --form 'product_price="100000"'
   ```

4. **Delete Item**
   - **URL:** `/api/items/<item_id>`
   - **Method:** DELETE
   - **Headers:**
     - Authorization: `<token>`
   
   **Example:**
   ```bash
   curl --location --request DELETE '127.0.0.1:8000/api/items/4' \
     --header 'Authorization: <your_jwt_token>'
   ```

## Usage Examples

### Retrieve All Items
To get a list of all items in the inventory, use the GET request as shown in the API documentation.

### Add a New Item
To add a new item, make a POST request to the `/api/items/add` endpoint with the required form data.

### Update an Existing Item
To update an existing item, use a PUT request to the appropriate item endpoint with the updated information.

### Delete an Item
To delete an item from the inventory, send a DELETE request to the item’s specific endpoint.

## Conclusion
This Inventory Management System provides a robust way to handle product inventory efficiently. For any issues or contributions, please contact the repository owner or submit a pull request. Happy coding!
```

You can now copy and paste this complete content as needed!