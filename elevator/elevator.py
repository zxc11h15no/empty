import logging
from abc import ABC, abstractmethod


class Exceptions:
    class RestoreElevatorError(Exception):
        def __init__(self, text):
            self.text = text

    class NumberFloorError(Exception):
        def __init__(self, text):
            self.text = text

    class WeigthCapacityError(Exception):
        def __init__(self, text):
            self.text = text


class Human(ABC):
    def __init__(self, weigth):
        self.weigth = weigth

    @abstractmethod
    def unit_weigth(self):
        pass


class Passenger(Human):
    def __init__(self, weigth, location, floor):
        super().__init__(weigth)
        self.location = location
        self.floor = floor

    def unit_weigth(self):
        return self.weigth

    def unit_location(self):
        return self.location

    def exit_floor(self):
        return self.floor


class Elevator:
    def __init__(self, floors_count, elevator_capacity):
        self.num_break = 0
        self.unit = []
        self.floors_count = floors_count
        self.elevator_capacity = elevator_capacity
        self.weigth = 0
        self.exit_floor = 0
        self.unit_location = 0
        self.waiting_units = []
        self.waiting_count_units = 0
        self.units = []
        self.weigth_units = 0
        self.count_units = 0
        self.elevator_location = 1

    def move(self, number_floor):
        if self.weigth_units <= self.elevator_capacity:
            if self.floors_count >= number_floor > 0:
                self.elevator_location = number_floor
            else:
                logging.critical("A message of CRITICAL severity")
                raise Exceptions.NumberFloorError("Указанный этаж находится вне диапазона этажей этого дома")
        else:
            logging.warning("A WARNING")
            raise Exceptions.WeigthCapacityError("Вес выше допустимого")

    def add_waiting_units(self, unit: Passenger):
        if self.unit_location <= self.floors_count:
            self.exit_floor = unit.exit_floor()  # Этаж на котором пассажир выйдет
            self.weigth = unit.unit_weigth()  # Вес багажа и его пассажира
            self.unit_location = unit.unit_location()  # местоположение ожидающего пассажира
            self.waiting_count_units += 1
            self.waiting_units.append([unit.exit_floor(), unit.unit_weigth(), unit.unit_location()])
            print(f"Этаж на котором человек ожидает лифт: {self.unit_location}\nЭтаж на котором человек выйдет: "
                  f"{self.exit_floor}\nВес пассажира и его багажа, если он есть: {self.weigth}кг\n")
        else:
            logging.critical("A message of CRITICAL severity")
            raise Exceptions.NumberFloorError("Указанный этаж находится вне диапазона этажей этого дома")

    def delete_waiting_units(self):
        i = 0
        while i < self.waiting_count_units:
            if self.elevator_location == self.waiting_units[i][2]:  # сравнение местоположения лифта с
                # местоположением ожидающего пассажира
                self.waiting_count_units -= 1
                self.waiting_units.pop(i)
                print("Очередь уменьшилась на 1\n")
            i += 1

    def add_units(self):
        i = 0
        while i < self.waiting_count_units:
            if self.weigth_units <= self.elevator_capacity:
                if self.weigth_units <= self.elevator_capacity:
                    if self.elevator_location == self.waiting_units[i][2]:  # Сравнение местоположения пассажира с
                        # этажом, на котором он находится
                        self.weigth_units += self.waiting_units[i][1]  # Вес пассажира и его багажа
                        self.count_units += 1
                        self.units.append(self.waiting_units[i])  # Добавление пассажира в список
                        # пассажиров находящихся в лифте
                        print("Человек зашел!\n")
                    i += 1
            else:
                logging.warning("A WARNING")
                raise Exceptions.WeigthCapacityError("Вес выше допустимого")

    def delete_units(self):
        i = 0
        while i < self.count_units:
            if self.elevator_location == self.units[i][0]:  # Сравнение местоположения пассажира с
                # этажом, на котором он выйдет
                self.count_units -= 1
                self.weigth_units -= self.units[i][1]  # Вес пассажира и его багажа
                self.units.pop(i)
                print("Человек вышел!\n")
            i += 1

    def to_ride(self, number_floor, i=0):
        self.move(number_floor)
        print(f'Мы прибыли на {number_floor} этаж\n')
        self.add_units()
        try:
            while i < 100:
                self.delete_waiting_units()
                self.delete_units()
                i += 1
        except:
            pass
        return number_floor

    def check_elevator_condition(self):
        print("Состояние лифта:\n")
        print(f"Этаж на котором находится лифт: {self.elevator_location}\nОбщий вес лифта: {self.weigth_units}\n"
              f"Количество пассажиров в ожидает: {self.waiting_count_units}\nКоличество пассажиров в "
              f"лифте: {self.count_units}\n")


elev = Elevator(10, 1200)
passenger = Passenger(65, 3, 9)

elev.to_ride(5)
elev.add_waiting_units(passenger)
elev.to_ride(3)
elev.to_ride(9)
elev.check_elevator_condition()

