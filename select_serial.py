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
        self.selector()

    def selector(self):
        if self._height_of_bricks == '65':
            if self._type_of_wall == 'Перегородка':
                catalog = Catalog().get_catalog()
                print(f'width of opening: {self._width_of_opening}')
                for mark, parameters in catalog.items():
                    required_length = self._width_of_opening + 2 * catalog[mark]['minimum support, m']
                    if catalog[mark]['length, m'] > required_length and catalog[mark]['maximum loads, kN/m'] >= 7:
                        quantity = self._width_of_wall // catalog[mark]['width, m']
                        print(f'required_length: {required_length}')
                        print(f'quantity: {quantity}')
                        print(f'mark {mark}, parameters {parameters}')
                        break

                # for iter in nested_dict:
                    # if iter['length, m'] == 2.07:
                    # print(f'iter', iter)
        elif self._height_of_bricks == '88':
            pass
        else:
            print(f'Не правильно введені параметри')


s = SelectSerial('Перегородка', '', '65', '900', '470')