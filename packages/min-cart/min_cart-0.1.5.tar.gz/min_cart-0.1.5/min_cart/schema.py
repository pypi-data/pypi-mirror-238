import graphene
from min_cart.apps.cart.graphql.cart import Query as cart_query

class Query(cart_query, graphene.ObjectType, ):
    pass

class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
