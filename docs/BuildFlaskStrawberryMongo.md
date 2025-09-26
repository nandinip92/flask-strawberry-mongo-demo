# Build a Flask + Strawberry GraphQL App with MongoDB (Separate Files)

This guide walks through creating a **Flask + Strawberry GraphQL project** using **PyMongo** with a clean project structure and separate files for maintainability.

---

## 1. Project Structure

```
flask-strawberry-mongo/
│── app.py                # Flask entry point
│── database.py           # MongoDB connection setup
│── schema.py             # GraphQL schema (Query & Mutation)
│── models/
│    └── user_model.py    # User collection CRUD logic
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```

---

## 32 Create `db.py`

Setup the MongoDB connection using PyMongo.

```python
from pymongo import MongoClient

MONGO_URI = "mongodb://<username>:<password>@localhost:27017"
DB_NAME = "testdb"

client = MongoClient(MONGO_URI)  # Create MongoClient instance
db = client[DB_NAME]             # Select the database
```

---

## 3. Create `models/user_model.py`

CRUD operations for the `users` collection.

```python
from bson.objectid import ObjectId
from db import db

users_collection = db["users"]

def get_all_users():
    return list(users_collection.find())

def get_user_by_id(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})

def add_user(name, email):
    result = users_collection.insert_one({"name": name, "email": email})
    return users_collection.find_one({"_id": result.inserted_id})

def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
```

---

## 4 Create `schema.py`

Define Strawberry GraphQL schema with types, queries, and mutations.

```python
import strawberry
from models.user_model import get_all_users, get_user_by_id, add_user, delete_user

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return [User(id=str(u["_id"]), name=u["name"], email=u["email"]) for u in get_all_users()]

    @strawberry.field
    def user_by_id(self, id: strawberry.ID) -> User | None:
        u = get_user_by_id(id)
        if u:
            return User(id=str(u["_id"]), name=u["name"], email=u["email"])
        return None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, name: str, email: str) -> User:
        u = add_user(name, email)
        return User(id=str(u["_id"]), name=u["name"], email=u["email"])

    @strawberry.mutation
    def delete_user(self, id: strawberry.ID) -> bool:
        return delete_user(id)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

In Strawberry GraphQL, @strawberry.type is a decorator that tells Strawberry:

👉 “Turn this Python class into a GraphQL type.”

**Explaination**

```python
@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
```

- `User` becomes a GraphQL Object Type with fields `id`, `name`, and `email`.
- The `strawberry.ID` type maps to GraphQL’s built-in `ID` scalar.
- `str` maps to the GraphQL String.

Then, when you decorate:

```python
@strawberry.type
class Query:
    ...
```

- This makes `Query` the root query type of your GraphQL schema.
- All `@strawberry.field` methods inside it become GraphQL queries.

and

```python
@strawberry.type
class Mutation:
    ...
```

- Makes `Mutation` the root mutation type.

- All `@strawberry.mutation` methods become GraphQL mutations.


Finally:

```python
schema = strawberry.Schema(query=Query, mutation=Mutation)
```

This wires everything up so your GraphQL API knows what queries and mutations are available.

### 🔑 In short:

`@strawberry.type =` “This class is a GraphQL type.”

Used for data objects (like `User`)

And for root types (like `Query` and `Mutation`)

## 6. Create `app.py`

Flask entry point and GraphQL route.

```python
from flask import Flask
from strawberry.flask.views import GraphQLView
from schema import schema

app = Flask(__name__)

# GraphQL endpoint
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema, graphiql=True)
)

@app.route("/")
def home():
    return "Flask + Strawberry + MongoDB project running!"

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 7. High-Level Explanation

### Imports

- `Flask`: Web framework.
- `pymongo`: Connects to MongoDB.
- `strawberry`: Define GraphQL schema and types.
- `GraphQLView`: Exposes GraphQL endpoint.
- `ObjectId`: Query MongoDB documents by `_id`.

### MongoDB Setup (`db.py`)

- Establishes a MongoClient connection.
- Provides `db` object for accessing collections.

### Models (`models/user_model.py`)

- CRUD functions for the `users` collection.
- Handles conversion between MongoDB documents and Python objects.

### GraphQL Schema (`schema.py`)

- `User` type maps MongoDB `_id` to `id`.
- Queries: `users`, `user_by_id`
- Mutations: `add_user`, `delete_user`

### Flask App (`app.py`)

- Registers `/graphql` endpoint.
- Uses GraphiQL interface for interactive testing.
- Home route confirms server is running.

---

## 8. Example GraphQL Queries & Mutations

**Fetch all users:**

```graphql
query {
  users {
    id
    name
    email
  }
}
```

**Fetch user by ID:**

```graphql
query {
  userById(id: "YOUR_USER_ID") {
    id
    name
    email
  }
}
```

**Add a new user:**

```graphql
mutation {
  addUser(name: "Alice", email: "alice@example.com") {
    id
    name
    email
  }
}
```

**Delete a user:**

```graphql
mutation {
  deleteUser(id: "YOUR_USER_ID")
}
```

---

## 9. Resources

- [Strawberry GraphQL Documentation](https://strawberry.rocks/docs)
- [MongoDB Python Docs (PyMongo)](https://pymongo.readthedocs.io/en/stable/)
- [GraphQL with Flask + Strawberry Tutorial](https://strawberry.rocks/docs/integrations/flask)
