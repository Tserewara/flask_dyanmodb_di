class TicketRepositoryDynamoDB:
    def __init__(self, dynamodb_client, table_name="TicketTable"):
        self.dynamodb_client = dynamodb_client
        self.table_name = table_name
        self.table = self.dynamodb_client.Table(self.table_name)

    def save(self, ticket):
        """
        Save a ticket to the DynamoDB table.

        Parameters:
        ticket (dict): A dictionary containing ticket details with keys 'id', 'title', and 'description'.
        """
        self.table.put_item(Item=ticket)
        print(f"Ticket with id {ticket['id']} saved successfully.")

    def list(self):
        """
        List all tickets from the DynamoDB table.

        Returns:
        list: A list of dictionaries, each representing a ticket.
        """
        response = self.table.scan()
        tickets = response.get('Items', [])
        return tickets
