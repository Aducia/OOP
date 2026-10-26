from abc import ABC, abstractmethod


# завдання 1) Початковий клас із порушеннями SOLID - порушує принцип SRP, робить все сам.
class BadOrderManager:
    def __init__(self, items, discount_percent):
        self.items = items
        self.discount_percent = discount_percent

    def calculate_total(self):
        subtotal = sum(item["price"] for item in self.items)
        discount = subtotal * (self.discount_percent / 100)
        return subtotal - discount

    def print_report(self):
        print("До рефакторингу:")
        for item in self.items:
            print(f"Товар: {item['name']} — {item['price']} грн")
        
        subtotal = sum(item["price"] for item in self.items)
        discount_val = subtotal * (self.discount_percent / 100)
        total = subtotal - discount_val

        print(f"\nСума: {subtotal} грн")
        print(f"Знижка: {int(self.discount_percent)}%")
        print(f"До сплати: {int(total)} грн")

    def save_to_database(self):
        print("Замовлення збережено.")

    def send_notification(self):
        print("Повідомлення відправлено.\n")


# Завдання 2) Рефакторинг за "SOLID":

# клас типу SRP: відповідає виключно за зберігання та передачу даних замовлення.
class Order:
    def __init__(self, items):
        self.items = items


# Калькулятор суми замовлення
# SRP: відповідає тільки за бізнес-логіку .
class OrderCalculator:
    def calculate_subtotal(self, order: Order) -> float:
        return sum(item["price"] for item in order.items)


# Абстрактний клас типу OCP для політики знижок: визначає єдиний контракт для знижок, дозволяючи додавати нові 

class IDiscountPolicy(ABC):
    @abstractmethod
    def calculate_discount(self, subtotal: float) -> float:
        pass


# OCP: політика знижок 
class PercentageDiscountPolicy(IDiscountPolicy):
    def __init__(self, percent: float):
        self.percent = percent

    def calculate_discount(self, subtotal: float) -> float:
        return subtotal * (self.percent / 100)


# Абстрактний клас для збереження типу DIP - створює вузький контракт для сховища даних, щоб бізнес-логіка 

class IOrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass


# Абстрактний клас для сповіщень
# DIP та ISP водночас, Належить до DIP, оскільки ізолює бізнес-логіку від конкретних 
# поштових сервісів через абстракцію, і водночас до ISP, оскільки задає 
# вузький і специфічний контракт лише з одним методом notify().
class IOrderNotifier(ABC):
    @abstractmethod
    def notify(self, order: Order):
        pass


#  збереження у БД
class SqlOrderRepository(IOrderRepository):
    def save(self, order: Order):
        print("Замовлення збережено.")


# відправка email-сповіщень
class EmailOrderNotifier(IOrderNotifier):
    def notify(self, order: Order):
        print("Повідомлення відправлено.")


# Сервіс оформлення замовлення 
# SRP: відповідає за виведення чеку, запуск розрахунків, збереження та сповіщення.
class CheckoutService:
    def __init__(
        self, 
        calculator: OrderCalculator, 
        discount_policy: IDiscountPolicy, 
        repository: IOrderRepository, 
        notifier: IOrderNotifier
    ):
        self.calculator = calculator
        self.discount_policy = discount_policy
        self.repository = repository
        self.notifier = notifier

    def process_order(self, order: Order, discount_val: float):
        for item in order.items:
            print(f"Товар: {item['name']} — {item['price']} грн")
        
        subtotal = self.calculator.calculate_subtotal(order)
        discount = self.discount_policy.calculate_discount(subtotal)
        total = subtotal - discount

        print(f"\nСума: {int(subtotal)} грн")
        print(f"Знижка: {int(discount_val)}%")
        print(f"До сплати: {int(total)} грн\n")

        self.repository.save(order)
        self.notifier.notify(order)


if __name__ == "__main__":
    # Демонстрація проблеми 
    bad_items = [
        {"name": "Помада Maybelline superstay", "price": 300},
        {"name": "Туш Maybelline SkyHigh", "price": 550}
    ]
    bad_manager = BadOrderManager(bad_items, 10)
    bad_manager.print_report()
    bad_manager.save_to_database()
    bad_manager.send_notification()

    print("     ***     \n")

    print("Результат після рефакторингу:\n")

    # Демонстрація правильного рішення 
    items = [
        {"name": "Помада Maybelline superstay", "price": 300},
        {"name": "Туш Maybelline SkyHigh", "price": 550}
    ]
    
    order = Order(items)
    
    calculator = OrderCalculator()
    discount_policy = PercentageDiscountPolicy(10)
    repo = SqlOrderRepository()
    notifier = EmailOrderNotifier()
    
    checkout = CheckoutService(calculator, discount_policy, repo, notifier)
    checkout.process_order(order, 10)
