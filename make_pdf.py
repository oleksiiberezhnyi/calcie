from fpdf import FPDF
from collections import Counter
from datetime import datetime
from serial_beam import Catalog



result_dict = {
    'ПР-1': [
        {'5ПБ30-37': {
            'length, m': 2.98,
            'width, m': 0.25,
            'height, m': 0.22,
            'maximum loads, kN/m': 37.3,
            'minimum support, m': 0.23,
            'volume, m3': 0.164,
            'weight, kN': 4.018
        }
        },
        {'3ПБ39-8': {
            'length, m': 3.89,
            'width, m': 0.12,
            'height, m': 0.22,
            'maximum loads, kN/m': 7.85,
            'minimum support, m': 0.21,
            'volume, m3': 0.103,
            'weight, kN': 2.523
        }
        },
        {'3ПБ39-8': {
            'length, m': 3.89,
            'width, m': 0.12,
            'height, m': 0.22,
            'maximum loads, kN/m': 7.85,
            'minimum support, m': 0.21,
            'volume, m3': 0.103,
            'weight, kN': 2.523
        }
        }
    ],
    'ПР-2': [
        {'5ПБ21-27': {
            'length, m': 2.07,
            'width, m': 0.25,
            'height, m': 0.22,
            'maximum loads, kN/m': 27.5,
            'minimum support, m': 0.17,
            'volume, m3': 0.114,
            'weight, kN': 2.793
        }
        },
        {'3ПБ21-8': {
            'length, m': 2.07,
            'width, m': 0.12,
            'height, m': 0.22,
            'maximum loads, kN/m': 7.85,
            'minimum support, m': 0.17,
            'volume, m3': 0.055,
            'weight, kN': 1.347
        }
        }
    ],
    'ПР-3': [
        {'1ПБ13-1': {
            'length, m': 1.29,
            'width, m': 0.12,
            'height, m': 0.065,
            'maximum loads, kN/m': 1.47,
            'minimum support, m': 0.1,
            'volume, m3': 0.01,
            'weight, kN': 0.245
        }
        }
    ],
    'ПР-4': [
        {'1ПБ13-1': {
            'length, m': 1.29,
            'width, m': 0.12,
            'height, m': 0.065,
            'maximum loads, kN/m': 1.47,
            'minimum support, m': 0.1,
            'volume, m3': 0.01,
            'weight, kN': 0.245
        }
        }
    ],
    'ПР-5': [
        {'1ПБ13-1': {
            'length, m': 1.29,
            'width, m': 0.12,
            'height, m': 0.065,
            'maximum loads, kN/m': 1.47,
            'minimum support, m': 0.1,
            'volume, m3': 0.01,
            'weight, kN': 0.245
        }
        }
    ],
    'ПР-6': [
        {'5ПБ30-37': {
            'length, m': 2.98,
            'width, m': 0.25,
            'height, m': 0.22,
            'maximum loads, kN/m': 37.3,
            'minimum support, m': 0.23,
            'volume, m3': 0.164,
            'weight, kN': 4.018
        }
        },
        {'3ПБ39-8': {
            'length, m': 3.89,
            'width, m': 0.12,
            'height, m': 0.22,
            'maximum loads, kN/m': 7.85,
            'minimum support, m': 0.21,
            'volume, m3': 0.103,
            'weight, kN': 2.523
        }
        },
        {'3ПБ39-8': {
            'length, m': 3.89,
            'width, m': 0.12,
            'height, m': 0.22,
            'maximum loads, kN/m': 7.85,
            'minimum support, m': 0.21,
            'volume, m3': 0.103,
            'weight, kN': 2.523
        }
        }
    ]
}

class MakePDF(FPDF):
    annotation = 'Даний підбір виконано автоматично. Для підтвердження підбору зверніться у проектну організацію'
    title1 = 'Специфікація пакетів перемичок'
    title2 = 'Специфікація елементів перемичок'
    title3 = 'Відомість перемичок'

    def __init__(self, result_dict: dict, filename: str):
        super().__init__()
        count_of_lines = len(result_dict)
        if count_of_lines > 10:
            count_of_lines = 10
        self.form3 = FPDF(orientation='L', unit='mm', format='A3')
        self.form3.add_page()
        self._draw_form_3()
        self._draw_specification_for_package(result_dict, 20, 30, self.title1)
        self._count_dict = dict()
        self._calculation_count(result_dict)
        self._draw_specification_for_element(self._count_dict, 20, 30 + 15 + (count_of_lines + 2) * 8 + 20, self.title2)
        self._draw_statement(count_of_lines, 230, 30, self.title3)
        self.make(result_dict)
        self._annotation(text=self.annotation)
        self.form3.output(f'static/{filename}')

    def _calculation_count(self, result_dict: dict):
        temp_list = []
        position = 1
        for value in result_dict.values():
            for element in value:
                for elem in element.keys():
                    temp_list.append(elem)
        for k, v in Counter(temp_list).items():
            self._count_dict[k] = {'count': v, 'position': position}
            position += 1
        return self._count_dict

    def make(self, result_dict: dict):
        n = 0
        for mark, parameters_list in result_dict.items():
            self.make_package_of_serial_beam(parameters_list, mark, n)
            n += 1

    def make_package_of_serial_beam(self, package: list, mark: str, n):
        scale = 20
        i = n
        if i < 5:
            x0 = 265
            y0 = 67 + 4 * 8 * i
            self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
            self.form3.set_font('iso', '', 11)
            self.form3.text(x0 - 29, y0 - 5, mark)
            for nested_dict in package:
                position = str(self._count_dict.get(list(nested_dict.keys())[0])['position'])
                self._draw_serial_beam(list(nested_dict.keys())[0], x0, y0, position)
                x0 += nested_dict[list(nested_dict.keys())[0]]['width, m'] * 1000 / scale + 10 / scale
        else:
            x0 = 355
            y0 = 67 + 4 * 8 * (i - 5)
            self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
            self.form3.set_font('iso', '', 11)
            self.form3.text(x0 - 29, y0 - 5, mark)
            for nested_dict in package:
                position = str(self._count_dict.get(list(nested_dict.keys())[0])['position'])
                self._draw_serial_beam(list(nested_dict.keys())[0], x0, y0, position)
                x0 += nested_dict[list(nested_dict.keys())[0]]['width, m'] * 1000 / scale + 10 / scale
        i += 1

    def _draw_serial_beam(self, mark: str, x=260, y=70, position: str = '00'):
        x0 = x
        y0 = y
        scale = 20
        if mark[0] == '1':
            b = 120/scale
            h = 65/scale
        elif mark[0] == '2':
            b = 120/scale
            h = 140/scale
        elif mark[0] == '3':
            b = 120/scale
            h = 220/scale
        elif mark[0] == '4':
            b = 120/scale
            h = 290/scale
        elif mark[0] == '5':
            b = 250/scale
            h = 220/scale
        else:
            return f'Помилка перерізу балки'
        self.form3.set_line_width(0.5)
        self.form3.rect(x0, y0, b, -h)
        self.form3.set_line_width(0.05)
        self.form3.line(x0, y0, x0 + b, y0 - h)
        self.form3.line(x0 + b, y0, x0, y0 - h)
        self.form3.line(x0 + b / 2, y0 - h + 1.25, x0 + b / 4, y0 - h - 5)
        self.form3.line(x0 + b / 4, y0 - h - 5, x0 + b / 4 + 4, y0 - h - 5)
        self.form3.ellipse(x0 + b / 2 - 0.5, y0 - h + 0.75, 1, 1, 'F')
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_font('iso', '', 11)
        self.form3.text(x0 + b / 4 + 0.5, y0 - h - 5.5, position)

    def _draw_form_3(self, y=0):
        y0 = y
        self.form3.set_line_width(0.5)
        self.form3.rect(20, y0 + 10, 390, y0 + 277)
        self.form3.rect(230, y0 + 232, 180, y0 + 55)
        self.form3.line(240, y0 + 232, 240, y0 + 257)
        self.form3.line(250, y0 + 232, 250, y0 + 287)
        self.form3.line(260, y0 + 232, 260, y0 + 257)
        self.form3.line(270, y0 + 232, 270, y0 + 287)
        self.form3.line(285, y0 + 232, 285, y0 + 287)
        self.form3.line(295, y0 + 232, 295, y0 + 287)
        self.form3.line(365, y0 + 257, 365, y0 + 287)
        self.form3.line(380, y0 + 257, 380, y0 + 272)
        self.form3.line(395, y0 + 257, 395, y0 + 272)
        self.form3.line(295, y0 + 242, 410, y0 + 242)
        self.form3.line(230, y0 + 252, 295, y0 + 252)
        self.form3.line(230, y0 + 257, 410, y0 + 257)
        self.form3.line(365, y0 + 262, 410, y0 + 262)
        self.form3.line(295, y0 + 272, 410, y0 + 272)
        self.form3.set_line_width(0.05)
        self.form3.line(230, y0 + 237, 295, y0 + 237)
        self.form3.line(230, y0 + 242, 295, y0 + 242)
        self.form3.line(230, y0 + 247, 295, y0 + 247)
        self.form3.line(230, y0 + 262, 295, y0 + 262)
        self.form3.line(230, y0 + 267, 295, y0 + 267)
        self.form3.line(230, y0 + 272, 295, y0 + 272)
        self.form3.line(230, y0 + 277, 295, y0 + 277)
        self.form3.line(230, y0 + 282, 295, y0 + 282)
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_font('iso', '', 11)
        self.form3.text(233, y0 + 255.75, 'Зм.')
        self.form3.text(240.75, y0 + 255.75, 'Кільк.')
        self.form3.text(252, y0 + 255.75, 'Арк.')
        self.form3.text(260.5, y0 + 255.75, '№док.')
        self.form3.text(273, y0 + 255.75, 'Підпис')
        self.form3.text(286, y0 + 255.75, 'Дата')
        self.form3.text(231, y0 + 260.75, 'Виконав')
        self.form3.text(251, y0 + 260.75, 'Бережний')
        self.form3.text(367, y0 + 260.75, 'Стадія')
        self.form3.text(382.5, y0 + 260.75, 'Аркуш')
        self.form3.text(396.25, y0 + 260.75, 'Аркушів')
        self.form3.text(296, y0 + 275.75, self.title1)
        self.form3.text(296, y0 + 280.75, self.title2)
        self.form3.text(296, y0 + 285.75, self.title3)
        self.form3.set_font('iso', '', 14)
        self.form3.text(370, y0 + 268.75, 'ЕП')
        self.form3.text(386.5, y0 + 268.75, '1')
        self.form3.text(401.5, y0 + 268.75, '1')
        self.form3.text(336, y0 + 238.25, str(datetime.utcnow().strftime('%Y—%m—%d %H:%M')))
        self.form3.image('static/images/logo_dark.png', 366.25, y0 + 273.25, 42.5, 12.5)
        
    def _draw_specification_for_package(self, result_dict: dict, x=230, y=30, title: str = 'Специфікація'):
        keys_list =[]
        for key in result_dict.keys():
            keys_list.append(key)
        count_of_lines = len(result_dict) + 2
        x0 = x
        y0 = y
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_line_width(0.5)
        self.form3.line(x0 + 0, y0 + 0, x0 + 180, y0 + 0)
        self.form3.line(x0 + 0, y0 + 15, x0 + 180, y0 + 15)
        self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 15, y0 + 0, x0 + 15, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 75, y0 + 0, x0 + 75, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 135, y0 + 0, x0 + 135, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 145, y0 + 0, x0 + 145, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 160, y0 + 0, x0 + 160, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 180, y0 + 0, x0 + 180, y0 + 15 + count_of_lines * 8)
        y = y0 + 23
        i = 0
        self.form3.set_line_width(0.05)
        while i < count_of_lines:
            try:
                text = f'Збірна перемичка {keys_list[i]}'
                self.form3.set_font('iso', '', 11)
                self.form3.text(x0 + 4, y0 + 20.25 + i * 8, keys_list[i])
                self.form3.text(x0 + 76, y0 + 20.25 + i * 8, text)
                self.form3.text(x0 + 139, y0 + 20.25 + i * 8, '1')
            except IndexError:
                pass
            self.form3.set_font('iso', '', 11)
            self.form3.line(x0 + 0, y, x0 + 180, y)
            i += 1
            y += 8
        self.form3.set_font('iso', '', 14)
        self.form3.text(x0 + 65, y0 - 5, title)
        self.form3.set_font('iso', '', 11)
        self.form3.text(x0 + 5, y0 + 9.25, 'Поз.')
        self.form3.text(x0 + 35, y0 + 9.25, 'Позначення')
        self.form3.text(x0 + 94, y0 + 9.25, 'Найменування')
        self.form3.text(x0 + 135.5, y0 + 9.25, 'Кільк.')
        self.form3.text(x0 + 145.3, y0 + 7.25, 'Маса од.,')
        self.form3.text(x0 + 151, y0 + 11, 'кг')
        self.form3.text(x0 + 163, y0 + 9.25, 'Примітка')

    def _draw_specification_for_element(self, count_dict: dict, x=230, y=30, title: str = 'Специфікація'):
        catalog = Catalog()
        keys_list = []
        for key in count_dict.keys():
            keys_list.append(key)
        count_of_lines = len(count_dict) + 2
        x0 = x
        y0 = y
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_line_width(0.5)
        self.form3.line(x0 + 0, y0 + 0, x0 + 180, y0 + 0)
        self.form3.line(x0 + 0, y0 + 15, x0 + 180, y0 + 15)
        self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 15, y0 + 0, x0 + 15, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 75, y0 + 0, x0 + 75, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 135, y0 + 0, x0 + 135, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 145, y0 + 0, x0 + 145, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 160, y0 + 0, x0 + 160, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 180, y0 + 0, x0 + 180, y0 + 15 + count_of_lines * 8)
        y = y0 + 23
        i = 0
        self.form3.set_line_width(0.05)
        while i < count_of_lines:
            try:
                self.form3.set_font('iso', '', 11)
                self.form3.text(x0 + 6.5, y0 + 20.25 + i * 8,
                    str(count_dict[keys_list[i]]['position'])
                )
                self.form3.text(x0 + 16, y0 + 20.25 + i * 8,
                    'ДСТУ Б В.2.6-55:2008'
                )
                self.form3.text(x0 + 76, y0 + 20.25 + i * 8, keys_list[i])
                self.form3.text(x0 + 139, y0 + 20.25 + i * 8,
                    str(count_dict[keys_list[i]]['count'])
                )
                self.form3.text(x0 + 146.5, y0 + 20.25 + i * 8,
                    str(round(catalog.get_weight(keys_list[i]) * 1000 / 9.8, 3))
                )
                self.form3.text(x0 + 161, y0 + 20.25 + i * 8,
                    f"{str(round(catalog.get_weight(keys_list[i]) * 1000 / 9.8 * count_dict[keys_list[i]]['count'], 3))} кг"
                )
            except IndexError:
                pass
            self.form3.line(x0 + 0, y, x0 + 180, y)
            i += 1
            y += 8
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_font('iso', '', 14)
        self.form3.text(x0 + 65, y0 - 5, title)
        self.form3.set_font('iso', '', 11)
        self.form3.text(x0 + 5, y0 + 9.25, 'Поз.')
        self.form3.text(x0 + 35, y0 + 9.25, 'Позначення')
        self.form3.text(x0 + 94, y0 + 9.25, 'Найменування')
        self.form3.text(x0 + 135.5, y0 + 9.25, 'Кільк.')
        self.form3.text(x0 + 145.3, y0 + 7.25, 'Маса од.,')
        self.form3.text(x0 + 151, y0 + 11, 'кг')
        self.form3.text(x0 + 163, y0 + 9.25, 'Примітка')

    def _draw_statement(self, count_of_lines: int, x=230, y=30, title: str = 'Відомість'):
        x0 = x
        y0 = y
        self.form3.set_line_width(0.5)
        self.form3.line(x0 + 0, y0 + 0, x0 + 90, y0 + 0)
        self.form3.line(x0 + 0, y0 + 15, x0 + 90, y0 + 15)
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        if count_of_lines <= 5:
            self.form3.set_font('iso', '', 14)
            self.form3.text(x0 + 25, y0 - 5, title)
            self.form3.set_font('iso', '', 11)
            self.form3.text(x0 + 5, y0 + 9.25, 'Марка')
            self.form3.text(x0 + 42, y0 + 9.25, 'Схема перерізу')
            self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + count_of_lines * 8 * 4)
            self.form3.line(x0 + 20, y0 + 0, x0 + 20, y0 + 15 + count_of_lines * 8 * 4)
            self.form3.line(x0 + 90, y0 + 0, x0 + 90, y0 + 15 + count_of_lines * 8 * 4)
        elif 5 < count_of_lines <= 10:
            self.form3.set_font('iso', '', 14)
            self.form3.text(x0 + 70, y0 - 5, title)
            self.form3.set_font('iso', '', 11)
            self.form3.text(x0 + 5, y0 + 9.25, 'Марка')
            self.form3.text(x0 + 42, y0 + 9.25, 'Схема перерізу')
            self.form3.text(x0 + 95, y0 + 9.25, 'Марка')
            self.form3.text(x0 + 132, y0 + 9.25, 'Схема перерізу')
            self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 20, y0 + 0, x0 + 20, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 90, y0 + 0, x0 + 90, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 90, y0 + 0, x0 + 180, y0 + 0)
            self.form3.line(x0 + 90, y0 + 15, x0 + 180, y0 + 15)
            self.form3.line(x0 + 110, y0 + 0, x0 + 110, y0 + 15 + (count_of_lines - 5) * 8 * 4)
            self.form3.line(x0 + 180, y0 + 0, x0 + 180, y0 + 15 + (count_of_lines - 5) * 8 * 4)
        # else:
        #     self.form3.set_font('iso', '', 14)
        #     self.form3.text(x0 + 70, y0 - 5, title)
        #     self.form3.set_font('iso', '', 11)
        #     self.form3.text(x0 + 5, y0 + 9.25, 'Марка')
        #     self.form3.text(x0 + 42, y0 + 9.25, 'Схема перерізу')
        #     self.form3.text(x0 + 95, y0 + 9.25, 'Марка')
        #     self.form3.text(x0 + 132, y0 + 9.25, 'Схема перерізу')
        #     self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + 5 * 8 * 4)
        #     self.form3.line(x0 + 20, y0 + 0, x0 + 20, y0 + 15 + 5 * 8 * 4)
        #     self.form3.line(x0 + 90, y0 + 0, x0 + 90, y0 + 15 + 5 * 8 * 4)
        #     self.form3.line(x0 + 90, y0 + 0, x0 + 180, y0 + 0)
        #     self.form3.line(x0 + 90, y0 + 15, x0 + 180, y0 + 15)
        #     self.form3.line(x0 + 110, y0 + 0, x0 + 110, y0 + 15 + 5 * 8 * 4)
        #     self.form3.line(x0 + 180, y0 + 0, x0 + 180, y0 + 15 + 5 * 8 * 4)
        self.form3.set_line_width(0.05)
        y = y0 + 47
        i = 0
        while i < count_of_lines and i < 5:
            self.form3.line(x0 + 0, y, x0 + 90, y)
            i += 1
            y += 8 * 4
        y = y0 + 47
        while count_of_lines > i >= 5 and i < 10:
            self.form3.line(x0 + 90, y, x0 + 180, y)
            i += 1
            y += 8 * 4

    def _annotation(self, text: str = 'Примітка', x=30, y=257):
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_font('iso', '', 11)
        self.form3.text(x, y, text)

if __name__ == '__main__':
    MakePDF(result_dict, 'files/result_test.pdf')