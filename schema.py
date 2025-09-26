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
