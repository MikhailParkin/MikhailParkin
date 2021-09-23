my_numbers = [i for i in range(1, 100)]

ODD = 'ODD'
EVEN = 'EVEN'
PRIME = 'PRIME'


def power_numbers(*args):
    result = []
    for item in args:
        new_item = item ** 2
        result.append(new_item)
    return result


# print(power_numbers(1, 2, 5, 7))


def is_prime(number):
    for i in range(2, number + 1):
        if number % i == 0:
            return i == number


def filter_numbers(my_numbers, type_sort):
    if type_sort == ODD:
        result = []
        for number in my_numbers:
            if number % 2 != 0:
                result.append(number)
    if type_sort == EVEN:
        result = []
        for number in my_numbers:
            if number % 2 == 0:
                result.append(number)
    if type_sort == PRIME:
        result = []
        result = list(filter(is_prime, my_numbers))
    return result


# print(filter_numbers(my_numbers, ODD))
# print(filter_numbers(my_numbers, EVEN))
print(filter_numbers(my_numbers, PRIME))
print(filter_numbers([1, 4, 7, 8, 33], ODD))
