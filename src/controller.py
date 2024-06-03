from flask import g, request
from flask_restx import Resource, Namespace

from src.create_ticket import CreateTicket

create_ticket_ns = Namespace("create_ticket")


class CreateTicketController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ticket_repository = g.get("ticket_repository")
        self._create_ticket = CreateTicket(ticket_repository)

    @create_ticket_ns.doc("Create Ticket")
    def post(self):
        title = request.json.get("title")
        description = request.json.get("description")
        self._create_ticket.execute({"title": title, "description": description})
        return "success", 201


list_tickets_ns = Namespace("list_tickets")


class ListTicketsController(Resource):
    def get(self):
        ticket_repository = g.get("ticket_repository")

        tickets = ticket_repository.list()

        return tickets, 200
