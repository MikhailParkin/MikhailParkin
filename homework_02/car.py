"""
создайте класс `Car`, наследник `Vehicle`
"""
# - в модуле `car` создайте класс `Car`
#     - класс `Car` должен быть наследником `Vehicle`
#     - добавьте атрибут `engine` классу `Car`
#     - объявите метод `set_engine`, который принимает в себя экземпляр объекта `Engine` и устанавливает на текущий экземпляр `Car`
from homework_02.base import Vehicle
from homework_02.engine import Engine


class Car(Vehicle):

    def __init__(self, weight, fuel, fuel_consumption):
        super().__init__(weight, fuel, fuel_consumption)
        self.engine = None

    def set_engine(self, engine):
        self.engine = engine
