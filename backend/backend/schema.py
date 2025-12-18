# backend/schema.py
import graphene
from scanner.schema import Query as ScannerQuery, Mutation as ScannerMutation
from emails.schema import Mutation as EmailMutation

class Query(ScannerQuery, graphene.ObjectType):
    pass

class Mutation(ScannerMutation, EmailMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
