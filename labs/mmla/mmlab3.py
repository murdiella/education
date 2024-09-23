from random import choice, randint
from abc import abstractmethod, ABCMeta
from copy import copy


class Collection(metaclass=ABCMeta):
    """Абстрактный класс с коллекцией"""

    @abstractmethod
    def __init__(self):
        """Конструктор абстрактного класса с коллекцией"""

        self.data = {}
        pass

    @abstractmethod
    def create_iterator(self):
        """Абстрактный метод создания итератора"""

        pass


class ConcreteCollection(Collection):
    """Класс конкретной коллекции"""

    def __init__(self, size: int = 20):
        """Конструктор конкретной коллекции"""

        super().__init__()
        self.iterator = None
        self.template = {
            'light AC': {'tank volume': None,
                         'total days idle': None,
                         'current day': None,
                         'location': None,
                         'type': 'AC'},
            'transport AC': {'tank volume': None,
                             'total days idle': None,
                             'current day': None,
                             'location': None,
                             'cargo weight': None,
                             'type': 'cargo'},
            'passenger AC': {'tank volume': None,
                             'total days idle': None,
                             'current day': None,
                             'location': None,
                             'sitting places': None,
                             'passengers': None,
                             'type': 'passenger'},
            'light HC': {'tank volume': None,
                         'total days idle': None,
                         'current day': None,
                         'location': None,
                         'type': 'AC'},
            'battle HC': {'tank volume': None,
                          'total days idle': None,
                          'current day': None,
                          'location': None,
                          'rockets total': None,
                          'type': 'battle'},
            'battle AC': {'tank volume': None,
                          'total days idle': None,
                          'current day': None,
                          'location': None,
                          'rockets total': None,
                          'type': 'battle'},
            'fuel tank': {'tank volume': None,
                          'total days idle': None,
                          'current day': None,
                          'location': None,
                          'target location': None,
                          'refuel status': None,
                          'type': 'cargo'},
            'bus': {'tank volume': None,
                    'location': None,
                    'sitting places': None,
                    'passengers': None,
                    'target location': None,
                    'type': 'ground transport'}
        }
        self.bounds = {
            'tank volume': [0, 50],
            'total days idle': [0, 10],
            'current day': [0, 10],
            'location': [0, 200],
            'cargo weight': [0, 50],
            'sitting places': [0, 50],
            'passengers': [0, 50],
            'rockets total': [0, 6],
            'refuel status': [0, 1],
            'target location': [0, 200]
        }

        self.__generate_collection(size)

    # PROTECTED емое
    def __generate_collection(self, size=20):
        """Метод создания случайно сгенерированной коллекции"""

        locations_used = []
        curr_id = 1

        for _ in range(size):
            temp = choice(list(self.template))
            new = {temp: {}}

            # в данном фрагменте кода ваши глаза спасет только Иисус
            for key, value in self.template[temp].items():
                if key != 'type' and key != 'target location' and key != 'location':
                    low = self.bounds[key][0]
                    high = self.bounds[key][1]
                    new_value = randint(low, high)
                    new[temp].update({key: new_value})

                elif key == 'location':
                    low = self.bounds[key][0]
                    high = self.bounds[key][1]
                    new_value = randint(low, high)
                    if len(locations_used) != 200:
                        while new_value in locations_used:  # reroll gambling
                            new_value = randint(low, high)
                    else:
                        raise Exception('Предел мест на парковке достигнут')
                    locations_used.append(new_value)
                    new[temp].update({key: new_value})

                elif key == 'target location':
                    try:
                        new_value = int(choice(locations_used))
                        new[temp].update({key: new_value})
                    # если вдруг зароллили первым бензовоз, то он стоит на месте (таргет = собственная позиция)
                    except IndexError:
                        new_value = new[temp].get('location')
                        new[temp].update({key: new_value})

                # лол аче
                elif key == 'type':
                    new[temp].update({key: self.template[temp]['type']})

            replacer = next(iter(new))
            new[replacer + f' #{curr_id}'] = new.pop(replacer)  # шаманство с ID, иначе словарь просто переписывается
            curr_id += 1

            self.data.update(new)

    def create_iterator(self):
        """Метод создания конкретного итератора"""

        self.iterator = ConcreteIterator(collection=self)  # я себя таким гением почувствовал когда это написал


class Iterator(metaclass=ABCMeta):
    """Абстрактный класс итератора"""

    @abstractmethod
    def __init__(self):
        """Конструктор абстрактного итератора"""

        pass

    @abstractmethod
    def get_next(self):
        """Абстрактный метод для получения следующего объекта коллекции"""

        pass

    @abstractmethod
    def has_more(self):
        """Абстрактный метод для получения информации о содержании большего числа объектов в коллекции"""

        pass


class ConcreteIterator(Iterator):
    """Класс конкретного итератора"""

    def __init__(self, collection: Collection):
        """Конструктор конкретного итератора"""

        super().__init__()
        self.collection = collection
        self.data = {}
        self.iterable = None  # я создал итератор внутри итератора ВАУ

    def get_next(self):
        """Метод для получения следующего объекта конкретной коллекции"""

        if self.iterable is None:
            self.iterable = iter(self.collection.data.items())

        key, value = next(self.iterable)

        return {key: value}

    def has_more(self):
        """Метод для получения информации о содержании большего числа объектов в конкретной коллекции"""

        if self.iterable is None:
            self.iterable = iter(self.collection.data.items())

        temp_iterable = copy(self.iterable)  # теневая магия

        try:
            next(temp_iterable)
        except StopIteration:
            return False
        else:
            return True

    def _get_all(self):
        """Метод для получения всех объектов коллекции"""

        while self.has_more():
            self.data.update(self.get_next())

    def get_with(self, title: str):
        """Метод для получения всех объектов с требуемым полем"""

        if self.data == {}:
            self._get_all()

        output = {}
        for key in self.data:
            if title in self.data[key]:
                output.update({key: self.data[key]})  # это вообще кринж, словари упоротые AF

        return output

    def sort_by(self, title: str, ascending: bool = False):
        """Метод для сортировки полученной коллекции"""

        if self.data == {}:
            self._get_all()

        output = self.get_with(title)
        # следующая строка писалась на следующих гео. координатах: 28°23'57.5"N 14°09'21.4"W
        output = {key: value for key, value in sorted(output.items(), key=lambda x: x[1][title], reverse=not ascending)}

        return output

    def get_by_rule(self, title: str, rule: str, border):
        """Метод для отображения определенных объектов коллекции"""

        if self.data == {}:
            self._get_all()

        match rule:
            case '>':
                output = self.get_with(title)
                output = {key: value for key, value in output.items() if value[title] > int(border)}
            case '<':
                output = self.get_with(title)
                output = {key: value for key, value in output.items() if value[title] < int(border)}
            case '=':
                output = self.get_with(title)
                output = {key: value for key, value in output.items() if value[title] == border}
            case '>=':
                output = self.get_with(title)
                output = {key: value for key, value in output.items() if value[title] >= int(border)}
            case '=<':
                output = self.get_with(title)
                output = {key: value for key, value in output.items() if int(border) >= value[title]}
            case '!=':
                output = self.get_with(title)
                output = {key: value for key, value in output.items() if value[title] != border}
            case _:
                raise ValueError('Неверное условие')

        return output

    def get_by_type(self, desired_type: str):
        """Метод для отображения определенных типов транспорта коллекции"""

        if self.data == {}:
            self._get_all()

        output = {}
        temp = self.get_with('type')
        for key, value in temp.items():
            if desired_type == value['type']:
                output.update({key: value})

        return output


def format_data(dictionary: dict):
    """Метод для форматированного вывода данных"""

    for key in dictionary:
        print('{' + f'{key}: ' + str(dictionary[key]) + '}')


def main():
    collection_size = 20
    collection = ConcreteCollection(collection_size)
    collection.create_iterator()

    print(f'Original data: {collection.data}\n')
    # collection.iterator._get_all()
    # res = collection.iterator.get_with('refuel status')
    # res = collection.iterator.sort_by('location')
    # res = collection.iterator.get_by_type('cargo')
    res = collection.iterator.get_by_rule('current day', '<', 7)
    format_data(res)


if __name__ == "__main__":
    main()
