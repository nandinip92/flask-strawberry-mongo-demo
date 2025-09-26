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
    app.run(debug=True,  port=5050)