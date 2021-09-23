"""
Объявите следующие исключения:
- LowFuelError
- NotEnoughFuel
- CargoOverload
"""


class Error(Exception):
    pass


class LowFuelError(Error):
    pass


class NotEnoughFuel(Error):
    pass


class CargoOverload(Error):
    pass
