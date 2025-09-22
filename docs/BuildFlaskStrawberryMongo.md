# Build a Basic Flask + Strawberry GraphQL App with MongoDB

This guide walks you through creating a minimal Flask app with GraphQL support using Strawberry, backed by MongoDB.
We define queries and mutations to fetch, add, and delete users and expose them via a `/graphql` endpoint with an interactive GraphiQL interface.

## 1. Create a Basic Flask APP with Strawberry & MongoDB

Create a new Python file, let’s say app.py — 👉 Checkout [app.py]

```python

# Import required modules
from flask import Flask                   # Flask is the web framework for handling HTTP requests
from flask_pymongo import PyMongo        # Flask-PyMongo simplifies working with MongoDB in Flask
import strawberry                        # Strawberry is used to define GraphQL schema and types
from strawberry.flask.views import GraphQLView  # Provides a Flask view for GraphQL endpoints
from bson.objectid import ObjectId       # ObjectId is used to query MongoDB documents by their _id

# ---------------- Flask & Mongo Setup ----------------
app = Flask(__name__)                     # Initialize Flask app
app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"  # MongoDB connection string
mongo = PyMongo(app)                      # Initialize Flask-PyMongo with the Flask app

# Keep a direct PyMongo client for advanced queries if needed
client = mongo.cx                         # Access the underlying PyMongo client
db = client["testdb"]                     # Get reference to the "testdb" database
users_collection = db["users"]            # Get reference to the "users" collection

# ---------------- GraphQL Schema ----------------

# Define a User GraphQL type
@strawberry.type
class User:
    id: strawberry.ID                     # Unique ID of the user (mapped from MongoDB _id)
    name: str                              # User's name
    email: str                             # User's email address

# Define GraphQL queries
@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        """Fetch all users from MongoDB"""
        result = []
        for user in users_collection.find():        # Retrieve all documents from "users" collection
            result.append(User(
                id=str(user["_id"]),               # Convert ObjectId to string for GraphQL
                name=user["name"],
                email=user["email"]
            ))
        return result                              # Return list of User objects

    @strawberry.field
    def user_by_id(self, id: strawberry.ID) -> User | None:
        """Fetch single user by ID"""
        user = users_collection.find_one({"_id": ObjectId(id)})  # Query MongoDB by ObjectId
        if user:
            return User(id=str(user["_id"]), name=user["name"], email=user["email"])
        return None                               # Return None if user not found

# Define GraphQL mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, name: str, email: str) -> User:
        """Insert a new user into MongoDB"""
        user_data = {"name": name, "email": email}        # Create a document dictionary
        inserted = users_collection.insert_one(user_data) # Insert document into MongoDB
        return User(id=str(inserted.inserted_id), name=name, email=email)  # Return the inserted user

    @strawberry.mutation
    def delete_user(self, id: strawberry.ID) -> bool:
        """Delete user by ID"""
        result = users_collection.delete_one({"_id": ObjectId(id)})  # Delete document by _id
        return result.deleted_count > 0       # Return True if a document was deleted, else False

# Create the Strawberry GraphQL schema with Query and Mutation
schema = strawberry.Schema(query=Query, mutation=Mutation)

# ---------------- GraphQL Route ----------------
app.add_url_rule(
    "/graphql",                            # URL endpoint for GraphQL
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True)
    # graphiql=True enables the interactive GraphiQL web interface
)

# Define a simple home route
@app.route("/")
def home():
    return "Flask + Strawberry GraphQL + MongoDB (with flask-pymongo & pymongo)"

# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(debug=True)                     # Run Flask development server with debug mode enabled
```

## 2. High-Level Explanation

### Imports:

- `Flask` handles web requests and routing.

- `PyMongo` connects Flask to MongoDB.

- `strawberry` defines GraphQL schema, types, and resolvers.

- `GraphQLView` exposes GraphQL endpoints with a browser-friendly interface.

- `ObjectId` is needed to query MongoDB documents by `_id`.

### MongoDB Setup

```python
app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"
mongo = PyMongo(app)
client = mongo.cx
db = client["testdb"]
users_collection = db["users"]
```

- `flask_pymongo` simplifies connection to MongoDB.

- `client = mongo.cx` provides a direct PyMongo client for advanced queries.

- `users_collection` is the MongoDB collection used for CRUD operations.

### GraphQL Schema

**User Type**

```python
@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
```

- Defines the `User` type in GraphQL.

- `id` is mapped from MongoDB `_id`.

**Query Type**

```python
@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        ...

```

- `users` returns all users.

- `user_by_id` fetches a single user by their ID.

**Mutation Type**

```python
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, name: str, email: str) -> User:
        ...
```

- `add_user` inserts a new user.

- `delete_user` deletes a user by ID and returns a boolean.

### GraphQL Endpoint

```python
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True)
)
```

- `/graphql` endpoint handles all GraphQL queries and mutations.

- `graphiql=True` provides an interactive web interface to test queries.

### Run Server

```python

if __name__ == "__main__":
    app.run(debug=True)

```

- Starts Flask development server on `http://127.0.0.1:5000`.

- Debug mode enables auto-reload and error details.

## Example GraphQL Queries & Mutations

### Fetch all users:

```graphql
query {
  users {
    id
    name
    email
  }
}
```

### Fetch a user by ID:

```graphql
query {
  userById(id: "64f123abcde456...") {
    id
    name
    email
  }
}
```

### Add a new user:

```graphql
mutation {
  addUser(name: "Alice", email: "alice@example.com") {
    id
    name
    email
  }
}
```

### Delete a user:

```graphql
mutation {
  deleteUser(id: "64f123abcde456...")
}
```

---

**Resources:**

[Strawberry GraphQL Documentation](https://strawberry.rocks/docs)

[Flask-PyMongo Documentation](https://flask-pymongo.readthedocs.io/en/latest/)

[MongoDB Python Docs](https://pymongo.readthedocs.io/en/stable/)

[GraphQL with Flask + Strawberry Tutorial](https://strawberry.rocks/docs/integrations/flask)
