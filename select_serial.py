from serial_beam import Catalog


class SelectSerial:

    def __init__(self, request_list: list):
        self._type_of_wall = request_list[0]
        self._type_of_construction_wall = request_list[1]
        self._height_of_bricks = int(request_list[2])
        self._width_of_opening = int(request_list[3]) / 1000
        self._width_of_wall = int(request_list[4]) / 1000
        self._result_list = []
        if self._height_of_bricks == 65:
            self._catalog = Catalog().get_catalog(65)
        elif self._height_of_bricks == 88:
            self._catalog = Catalog().get_catalog(88)
        self._selector()

    def _selector(self):
        if self._type_of_wall == 'Перегородка':
            self._calculation_partition_wall()
        elif self._type_of_wall == 'Самонесуча стіна':
            self._calculation_construction_wall_non_load()
        elif self._type_of_wall == 'Несуча стіна'\
                and self._type_of_construction_wall == 'Опирання з однієї сторони':
            self._calculation_construction_wall_one_side()
        elif self._type_of_wall == 'Несуча стіна'\
                and self._type_of_construction_wall == 'Опирання з двох сторін':
            self._calculation_construction_wall_two_side()

    def _calculation_partition_wall(self):
        if self._width_of_wall < 0.120:
            return self._result_list
        else:
            for mark, parameters in self._catalog.items():
                required_length = self._width_of_opening + 2 * self._catalog[mark]['minimum support, m']
                if required_length <= self._catalog[mark]['length, m'] < 2 * required_length \
                        and self._catalog[mark]['maximum loads, kN/m'] >= 0 \
                        and self._catalog[mark]['width, m'] <= self._width_of_wall:
                    self._result_list.append({mark: parameters})
                    self._width_of_wall -= self._catalog[mark]['width, m']
                    return self._calculation_partition_wall()

    def _calculation_construction_wall_non_load(self):
        if self._width_of_wall < 0.120:
            return self._result_list
        else:
            for mark, parameters in self._catalog.items():
                required_length = self._width_of_opening + 2 * self._catalog[mark]['minimum support, m']
                if required_length <= self._catalog[mark]['length, m'] < 2 * required_length \
                        and self._catalog[mark]['maximum loads, kN/m'] >= 7 \
                        and self._catalog[mark]['width, m'] <= self._width_of_wall:
                    self._result_list.append({mark: parameters})
                    self._width_of_wall -= self._catalog[mark]['width, m']
                    return self._calculation_construction_wall_non_load()

    def _calculation_construction_wall_two_side(self):
        if self._width_of_wall < 0.120:
            return self._result_list
        else:
            for mark, parameters in self._catalog.items():
                required_length = self._width_of_opening + 2 * self._catalog[mark]['minimum support, m']
                if required_length <= self._catalog[mark]['length, m'] < 2 * required_length \
                        and self._catalog[mark]['maximum loads, kN/m'] >= 25 \
                        and self._catalog[mark]['width, m'] <= self._width_of_wall:
                    self._result_list.append({mark: parameters})
                    self._width_of_wall -= 2 * self._catalog[mark]['width, m']
                    self._calculation_construction_wall_non_load()
                    self._result_list.append({mark: parameters})

    def _calculation_construction_wall_one_side(self):
        if self._width_of_wall < 0.120:
            return self._result_list
        else:
            for mark, parameters in self._catalog.items():
                required_length = self._width_of_opening + 2 * self._catalog[mark]['minimum support, m']
                if required_length <= self._catalog[mark]['length, m'] < 2 * required_length \
                        and self._catalog[mark]['maximum loads, kN/m'] >= 27.5 \
                        and self._catalog[mark]['width, m'] <= self._width_of_wall:
                    self._result_list.append({mark: parameters})
                    self._width_of_wall -= self._catalog[mark]['width, m']
                    self._calculation_construction_wall_non_load()

    def get_result(self):
        return self._result_list


class SelectIndividual:

    def __init__(self, request_list: list):
        self._type_of_wall = request_list[0]
        self._type_of_construction_wall = request_list[1]
        self._height_of_beam = request_list[2]
        self._width_of_opening = int(request_list[3]) / 1000
        self._width_of_wall = int(request_list[4]) / 1000
        self._result_list = []
        self._selector()

    def _selector(self):
        if self._type_of_wall == 'Несуча стіна' and self._type_of_construction_wall == 'Опирання з однієї сторони':
            max_loads = 0
        elif self._type_of_wall == 'Несуча стіна' and self._type_of_construction_wall == 'Опирання з двох сторін':
            max_loads = 0
        else:
            max_loads = 17.64 * self._width_of_wall * self._width_of_opening


if __name__ == '__main__':

    s1 = SelectSerial(['Перегородка', 'Немає', '65', '1000', '120'])
    s2 = SelectSerial(['Самонесуча стіна', 'Немає', '65', '1200', '510'])
    s3 = SelectSerial(['Несуча стіна', 'Опирання з однієї сторони', '65', '2100', '510'])
    s4 = SelectSerial(['Несуча стіна', 'Опирання з двох сторін', '88', '2100', '640'])
    print(s1.get_result())
    print(s2.get_result())
    print(s3.get_result())
    print(s4.get_result())
