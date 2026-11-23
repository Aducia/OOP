class Ticket:
    def __init__(self, event_name: str, base_price: float) -> None:
        if not event_name.strip():
            raise ValueError("Назва заходу не може бути порожньою")
        if base_price < 0:
            raise ValueError("Базова ціна квитка не може бути від'ємною")
        self.event_name = event_name.strip()
        self.base_price = base_price

    @property
    def ticket_type(self) -> str:
        return "Квиток"

    def calculate_price(self) -> float:
        return self.base_price

    @staticmethod
    def _format_amount(value: float) -> str:
        return f"{int(value)}" if value.is_integer() else f"{value:.2f}"

    def __str__(self) -> str:
        price_str = self._format_amount(self.calculate_price())
        return f"{self.event_name} — {self.ticket_type} — {price_str} грн"


class RegularTicket(Ticket):
    @property
    def ticket_type(self) -> str:
        return "Звичайний квиток"

    def calculate_price(self) -> float:
        return self.base_price


class StudentTicket(Ticket):
    DISCOUNT_RATE = 0.5

    @property
    def ticket_type(self) -> str:
        return "Студентський квиток"

    def calculate_price(self) -> float:
        return self.base_price * (1 - self.DISCOUNT_RATE)


def print_tickets(tickets: list[Ticket]) -> None:
    for ticket in tickets:
        print(ticket)


if __name__ == "__main__":
    event_tickets: list[Ticket] = [
        RegularTicket("Концерт", 200),
        StudentTicket("Концерт", 200),
    ]
    print_tickets(event_tickets)