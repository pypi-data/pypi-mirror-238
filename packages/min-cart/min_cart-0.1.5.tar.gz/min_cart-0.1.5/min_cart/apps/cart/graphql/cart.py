import graphene
from graphene import Field
from graphene import relay



class CartNode(graphene.ObjectType):
    """Cart node for graphql api"""

    total_price = graphene.String()

    def resolve_total_price(self, info):
        return "0.0"


class Query(graphene.ObjectType):
    """Query definitions"""
    cart = Field(
        CartNode,
        description="Endpoint for fetching basket")

    def resolve_cart(self, info):
        return CartNode()