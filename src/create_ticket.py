import uuid


class CreateTicket:
    def __init__(self, ticket_repository):
        self._ticket_repository = ticket_repository

    def execute(self, create_ticket_input):
        create_ticket_input["id"] = str(uuid.uuid4())
        self._ticket_repository.save(create_ticket_input)


