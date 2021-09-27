"""
создайте класс `Plane`, наследник `Vehicle`
"""
# - в модуле `plane` создайте класс `Plane`
#     - класс `Plane` должен быть наследником `Vehicle`
#     - добавьте атрибуты `cargo` и `max_cargo` классу `Plane`
#     - добавьте `max_cargo` в инициализатор (переопределите родительский)
#     - объявите метод `load_cargo`, который принимает число, проверяет, что в сумме с текущим `cargo` не будет перегруза, и обновляет значение, в ином случае выкидывает исключение `exceptions.CargoOverload`
#     - объявите метод `remove_all_cargo`, который обнуляет значение `cargo` и возвращает значение `cargo`, которое было до обнуления
from homework_02.base import Vehicle
from homework_02 import exceptions


class Plane(Vehicle):
    cargo = 0
    max_cargo = 0

    def __init__(self, weight, fuel, fuel_consumption, max_cargo):
        self.max_cargo = max_cargo
        super().__init__(weight, fuel, fuel_consumption)

    def load_cargo(self, new_cargo):
        overload = self.cargo + new_cargo
        if overload < self.max_cargo:
            self.cargo = overload
        else:
            raise exceptions.CargoOverload

    def remove_all_cargo(self):
        # with open('temp.txt', 'w') as f:
        #     f.write(str(self.cargo))
        # self.cargo = 0
        # with open('temp.txt') as f:
        #     old_cargo = f.read()
        old_cargo = []
        old_cargo.append(self.cargo)
        self.cargo = 0
        print(old_cargo[0])
        return int(old_cargo[0])
