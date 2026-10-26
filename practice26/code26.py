from abc import ABC, abstractmethod

# "Фабрика" створення посилок
class Parcel(ABC):
    def __init__(self, tracking_number: str, weight: float):
        self.tracking_number = tracking_number
        self.weight = weight

    @abstractmethod
    def get_type_name(self) -> str:
        pass

class SmallParcel(Parcel):
    def get_type_name(self) -> str:
        return "SmallParcel"

class LargeParcel(Parcel):
    def get_type_name(self) -> str:
        return "LargeParcel"

class ParcelFactory:
    @staticmethod
    def create_parcel(parcel_type: str, tracking_number: str, weight: float) -> Parcel:
        if parcel_type == "small":
            return SmallParcel(tracking_number, weight)
        elif parcel_type == "large":
            return LargeParcel(tracking_number, weight)
        else:
            raise ValueError(f"Невідомий тип посилки: {parcel_type}")


# Сповіщення про статус
class Observer(ABC):
    @abstractmethod
    def update(self, status: str):
        pass

class Client(Observer):
    def update(self, status: str):
        print("клієнт", end="")

class Manager(Observer):
    def update(self, status: str):
        print(", менеджер", end="")

class DeliveryTracker:
    def __init__(self, parcel: Parcel):
        self.parcel = parcel
        self._observers = []
        self._status = "Створено"

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def set_status(self, new_status: str):
        self._status = new_status
        self.notify(new_status)

    def notify(self, status: str):
        print(f"Статус: {status}\nObserver повідомив: ", end="")
        for observer in self._observers:
            observer.update(status)
        print()

if __name__ == "__main__":
    print("Служба доставки: FastDelivery")
    print("Посилка: PKG-001")
    print("Вага: 3 кг")

    parcel = ParcelFactory.create_parcel("small", "PKG-001", 3.0)
    print(f"Factory створила: {parcel.get_type_name()}")

    tracker = DeliveryTracker(parcel)
    tracker.attach(Client())
    tracker.attach(Manager())

    tracker.set_status("У дорозі")
