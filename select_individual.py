from math import sqrt, pi, ceil

test_dict = {'Б-1': ['Несуча стіна', 'Опирання з однієї сторони', '4300', '500', '200']}
test_dict2 = {'Б-1': ['Несуча стіна', 'Опирання з двох сторін', '900', '250', '510']}
test_dict3 = {'Б-1': ['Перегородка', 'Перегородка', '900', '250', '510']}


class SelectIndividual:

    def __init__(self, request_dict: dict):
        self._keys = request_dict.keys()
        for _ in self._keys:
            self._mark = _
            break
        self._type_of_wall = request_dict[self._mark][0]
        self._type_of_construction_wall = request_dict[self._mark][1]
        self._beam_length = int(request_dict[self._mark][2]) / 1000 + 0.25 * 2
        self._height_of_beam = int(request_dict[self._mark][3]) / 1000
        self._width_of_wall = int(request_dict[self._mark][4]) / 1000
        self._result_dict = request_dict
        """
        {
        'Б-1': ['Несуча стіна', 'Опирання з однієї сторони', '4300', '500', '200'],
        '1': ['3', '14', 'A500C', 'Lenght'],
        '2': ['2', '6', 'A240C', 'Lenght'],
        '3': ['quantity', '8', 'A400C', 'Lenght'],
        }
        """
        self._calculate_max_loads()
        self._calculation()
        self._calculate_position_1()
        self._calculate_position_2()
        self._calculate_position_3()
        print(self._result_dict)

    def _calculate_ksi(self, a_m):
        D = 6.25 - 12.5 * a_m
        if D > 0:
            ksi_1 = (2.5 + sqrt(D)) / 2
            ksi_2 = (2.5 - sqrt(D)) / 2
            return min(ksi_1, ksi_2)
        elif D == 0:
            ksi = 2.5 / 2
            return ksi
        else:
            raise Exception(ValueError)

    def _calculate_dzetha(self, ksi):
        return 1 - 0.4 * ksi

    def _select_diameter(self, A_s):
        result = (0, 0, 12000)  # (diameter, quantity, A)
        temp_result = []
        diameters = [6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40]
        quantity = range(1, 10)
        for d in diameters:
            for n in quantity:
                A = n * pi * d ** 2 / 4
                if A_s * 10 ** 6 < A < A_s * 10 ** 6 * 1.3:
                    temp_result.append((n, d, A))
        if len(temp_result) == 0:
            result = (2, 6, 2 * pi * 6 ** 2 / 4)
        for i in temp_result:
            if i[2] < result[2]:
                result = i
        return result

    def _calculation(self):
        M = self.max_loads * (self._beam_length - 0.25) ** 2 / 8
        a = 0.03
        f_cd = 14500  # kN/m2
        f_yd = 435000  # A500C kN/m2
        d = self._height_of_beam - a
        a_m = M / (f_cd * self._width_of_wall * (d ** 2))
        ksi = self._calculate_ksi(a_m)
        dzetha = self._calculate_dzetha(ksi)
        A_s = M / (dzetha * f_yd * d)
        return self._select_diameter(A_s)


    def _calculate_max_loads(self):
        if self._type_of_wall == 'Несуча стіна' and self._type_of_construction_wall == 'Опирання з однієї сторони':
            load_from_slab = 14
            payloads = 9
            load_from_the_wall = (self._beam_length - 0.25) ** 2 / 2 * self._width_of_wall * 17.64
        elif self._type_of_wall == 'Несуча стіна' and self._type_of_construction_wall == 'Опирання з двох сторін':
            load_from_slab = 28
            payloads = 18
            load_from_the_wall = (self._beam_length - 0.25) ** 2 / 2 * self._width_of_wall * 17.64
        else:
            load_from_slab = 0
            payloads = 0
            load_from_the_wall = (self._beam_length - 0.25) ** 2 / 2 * self._width_of_wall * 17.64
        self.max_loads = load_from_slab * 1.1 + payloads * 1.2 + load_from_the_wall * 1.1
        return self.max_loads

    def _calculate_position_1(self):
        count = self._calculation()[0]
        diameter = self._calculation()[0]
        reinforcement_class = "A500C"
        length = round(self._beam_length - 0.06, 3)
        self._result_dict["1"] = [count, diameter, reinforcement_class, length]

    def _calculate_position_2(self):
        count = 2
        diameter = 6
        reinforcement_class = "A500C"
        length = round(self._beam_length - 0.06, 3)
        self._result_dict["2"] = [count, diameter, reinforcement_class, length]

    def _calculate_position_3(self):
        length = self._beam_length - 0.06 - 0.1
        segment1 = length / 5
        segment2 = length - 2 * segment1
        count = self._beam_length - 0.06 - 0.1
        print(segment1)
        print(segment2)

        pass


if __name__ == "__main__":
    s1 = SelectIndividual(test_dict)
    s2 = SelectIndividual(test_dict2)
    s3 = SelectIndividual(test_dict3)
    print(s1._type_of_wall)
    print(s2._type_of_wall)
    print(s3._type_of_wall)
