import graphene
from apps.cart.graphql.cart import Query as cart_query

class Query(orders_schema.Query, cart_query):
    pass

class Mutation(orders_schema.mutation):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
