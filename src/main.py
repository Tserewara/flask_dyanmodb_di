import boto3
from flask import Flask, request, g
from flask_restx import Api

from src.controller import create_ticket_ns, CreateTicketController, list_tickets_ns, ListTicketsController
from src.create_ticket import CreateTicket
from src.ticket_repository import TicketRepositoryDynamoDB


def create_dependencies():

    ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

    ticket_repository = TicketRepositoryDynamoDB(ddb)

    return {
        "ticket_repository": ticket_repository
    }


# class TicketRepository:
#     def __init__(self):
#         self._tickets = []
#
#     def save(self, ticket):

#         self._tickets.append({
#             "id": ticket.get("id"),
#             "title": ticket.get("title"),
#             "description": ticket.get("description")
#         })
#
#     def list(self):
#         return self._tickets


def create_app(dependencies):
    app = Flask(__name__)
    api = Api(app)

    app.config['dependencies'] = dependencies

    @app.before_request
    def before_request():
        # Make dependencies available in the request context
        g.ticket_repository = app.config['dependencies']['ticket_repository']

    api.add_namespace(create_ticket_ns)
    create_ticket_ns.add_resource(CreateTicketController, "")

    api.add_namespace(list_tickets_ns)
    list_tickets_ns.add_resource(ListTicketsController, "")

    return app


app = create_app(create_dependencies())


if __name__ == '__main__':
    app.run(debug=True)
