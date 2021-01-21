from serial_beam import Catalog

class SelectSerial():

    def __init__(self, type_of_wall: str,
                 type_of_construction_wall: str,
                 height_of_bricks: str,
                 width_of_opening,
                 width_of_wall):
        self._type_of_wall = type_of_wall
        self._type_of_construction_wall = type_of_construction_wall
        self._height_of_bricks = height_of_bricks
        self._width_of_opening = int(width_of_opening) / 1000
        self._width_of_wall = int(width_of_wall) / 1000
        self._result_dict = {}
        self.selector()

    def selector(self):
        catalog = Catalog().get_catalog()
        print(f'width of opening: {self._width_of_opening}')
        if self._height_of_bricks == '65':
            if self._type_of_wall == 'Перегородка':
                for mark, parameters in catalog.items():
                    required_length = self._width_of_opening + 2 * catalog[mark]['minimum support, m']
                    if required_length <= catalog[mark]['length, m'] < 2 * required_length \
                            and catalog[mark]['maximum loads, kN/m'] >= 0:
                        quantity = self._width_of_wall // catalog[mark]['width, m']
                        print(f'required_length: {required_length}')
                        print(f'quantity: {quantity}')
                        print(f'mark {mark}, parameters {parameters}')
                        return

            elif self._type_of_wall == 'Самонесуча стіна':
                for mark, parameters in catalog.items():
                    required_length = self._width_of_opening + 2 * catalog[mark]['minimum support, m']
                    if required_length <= catalog[mark]['length, m'] < 2 * required_length \
                            and catalog[mark]['maximum loads, kN/m'] >= 7.85:
                        quantity = self._width_of_wall // catalog[mark]['width, m']
                        print(f'required_length: {required_length}')
                        print(f'quantity: {quantity}')
                        print(f'mark {mark}, parameters {parameters}')
                        break

            elif self._type_of_wall == 'Несуча стіна':
                for mark, parameters in catalog.items():
                    required_length = self._width_of_opening + 2 * catalog[mark]['minimum support, m']
                    if required_length <= catalog[mark]['length, m'] < 2 * required_length \
                            and catalog[mark]['maximum loads, kN/m'] >= 27.5:
                        quantity = self._width_of_wall // catalog[mark]['width, m']
                        print(f'required_length: {required_length}')
                        print(f'quantity: {quantity}')
                        print(f'mark {mark}, parameters {parameters}')
                        break

        elif self._height_of_bricks == '88':
            pass
        else:
            print(f'Не правильно введені параметри')


    def get_result_dict(self):
        return self._result_dict

s = SelectSerial('Перегородка', '', '65', '1200', '80')
# s2 = SelectSerial('Самонесуча стіна', '', '65', '1200', '510')
# s3 = SelectSerial('Несуча стіна', '', '65', '2100', '510')