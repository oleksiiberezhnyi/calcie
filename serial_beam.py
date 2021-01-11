class Catalog:

    def __init__(self): # mark, l, w, h, max_loads, min_support):
        self.read_from_file()
        self._len = 0
        # self._mark = mark
        # self._length = l
        # self._width = w
        # self._height = h
        # self._max_loads = max_loads
        # self._min_support = min_support
        # self._volume = self._length * self._width * self._height
        # self._mass = 2500 * self._volume  # 2500 kg/m3

    def read_from_file(self, file='files/catalog_serial.csv'):
        self.catalog = dict()
        with open(file, 'r') as f:
            file_lines = f.readlines()
            for line in file_lines:
                parameters_list = line.split(';')
                mark = parameters_list[0]
                length = float(parameters_list[1])
                width = float(parameters_list[2])
                height = float(parameters_list[3])
                max_loads = float(parameters_list[4])
                min_support = float(parameters_list[5])
                volume = round(length * width * height, 3)
                weight = round(24.5 * volume, 3)  # 24.5 kN/m3

                self.catalog[mark] = {'length, m': length,
                                 'width, m': width,
                                 'height, m': height,
                                 'maximum loads, kN/m': max_loads,
                                 'minimum support, m': min_support,
                                 'volume, m3': volume,
                                 'weight, kN': weight
                                 }
        return self.catalog

    def search(self, l, loads):
        pass

    def __len__(self):
        for _ in self.catalog.keys():
            self._len += 1
        return self._len


    def __iter__(self):
        return self

    def __next__(self):
        iter_dict = dict()
        if self._len == 0:
            raise StopIteration
        else:
            for k, v in self.catalog.items():
                iter_dict[k] = v
                self._len -= 1
            return iter_dict


def selection(opening_length, loads):
    length_list = [1.03, 1.29, 1.55, 1.68, 1.81,
                   1.94, 2.07, 2.2, 2.46, 2.59,
                   2.72, 2.85, 2.98, 3.11, 3.37,
                   3.63, 3.89, 4.41, 4.8, 5.96
                   ]

    with open('static/files/catalog_serial.csv', 'r') as f:
        file_lines = f.readlines()
        for line in file_lines:
            parameters_list = line.split(';')
            mark = parameters_list[0]
            length = float(parameters_list[1])
            width = float(parameters_list[2])
            height = float(parameters_list[3])
            max_loads = float(parameters_list[4])
            min_support = float(parameters_list[5])
            volume = round(length * width * height, 3)
            weight = round(24.5 * volume, 3)  # 24.5 kN/m3



f = Catalog()
print(len(f))
for i in f:
    print(i)
