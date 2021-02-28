from fpdf import FPDF
from collections import Counter
from datetime import datetime
from select_individual import SelectIndividual
from math import pi, ceil, floor


class MakePDF(FPDF):


    def __init__(self, result_dict: dict, filename: str):
        super().__init__()
        try:
            self._result = SelectIndividual(result_dict)
            self._result_dict = self._result.get_result_dict()
            print(self._result_dict)
            self.annotation = "Даний підбір виконано автоматично. Для підтвердження підбору зверніться у проектну організацію"
            self.title1 = "З/б балка Б-1. Опалубне креслення"
            self.title2 = "З/б балка Б-1. Армування"
            self.title3 = "Специфікація"
            self.scale = 10
            self.count_of_lines = 11
            self.form3 = FPDF(orientation="L", unit="mm", format="A3")
            self.form3.add_page()
            self.form3.add_font("iso", "", "static/ISOCPEUR/ISOCPEUR.ttf", uni=True)
            self._draw_form_3()
            self._draw_specification(self._result_dict, 20, 184, self.title3)
            self._make()
            self.form3.output(f"static/{filename}")
        except:
            self._make_error()

    def _make_error(self):
        print('error')
        raise Exception
        # return "Помилка! З даними параметрами неможливо виконати розрахунок. Збільшіть висоту перерізу."

    def _make(self):
        self._draw_beam(36, 30)
        self._draw_rainforcment(36, 110)

    def _draw_beam(self, x, y):
        x0 = x
        y0 = y
        l = (int(self._result_dict["Б-1"][2]) + 500) / self.scale
        h = int(self._result_dict["Б-1"][3]) / self.scale
        b = int(self._result_dict["Б-1"][4]) / self.scale
        self.form3.set_font("iso", "", 14)
        self.form3.text(x0 + l / 2.5, y0 - 5, self.title1)
        self.form3.set_line_width(0.5)
        self.form3.rect(x0, y0, l, h)
        self._dim_h(x0, y0 + h, l)
        self._dim_v(x0, y0, h)
        if l > 250:
            self.form3.rect(x0 + l + 16, y0, b, h)
            self._dim_h(x0 + l + 16, y0 + h, b)
        else:
            self.form3.rect(x0 + l + 30, y0, b, h)
            self._dim_h(x0 + l + 30, y0 + h, b)

    def _draw_rainforcment(self, x, y):
        x0 = x
        y0 = y
        l = (int(self._result_dict["Б-1"][2]) + 500) / self.scale
        h = int(self._result_dict["Б-1"][3]) / self.scale
        b = int(self._result_dict["Б-1"][4]) / self.scale
        self.form3.set_font("iso", "", 14)
        self.form3.text(x0 + l / 2.35, y0 - 5, self.title2)
        diam_pos1 = self._result_dict["1"][1] / self.scale
        diam_pos2 = self._result_dict["2"][1] / self.scale
        diam_pos3 = self._result_dict["3"][1] / self.scale
        diam_pos4 = self._result_dict["4"][1] / self.scale
        a = diam_pos1 / 2 + 20 / self.scale
        self.form3.set_line_width(0.05)
        self.form3.rect(x0, y0, l, h)
        pos1_l = int(self._result_dict["1"][3] / self.scale * 1000)
        pos2_l = int(self._result_dict["2"][3] / self.scale * 1000)
        self.form3.set_line_width(0.5)
        self.form3.line(x0 + 30 / self.scale, y0 + h - a, x0 + 30 / self.scale + pos1_l, y0 + h - 30 / self.scale)
        self.form3.line(x0 + 30 / self.scale, y0 + a, x0 + 30 / self.scale + pos2_l, y0 + 30 / self.scale)
        pos3_data = self._result.get_distance_position_3_4()

        def draw_pos3(x, y):
            self.form3.line(
                x,
                y + a - diam_pos2 / 2 - diam_pos3 / 2,
                x,
                y + h - a + diam_pos2 / 2 + diam_pos3 / 2,
            )

        draw_pos3(x0 + (30 + 50) / self.scale, y0)
        draw_pos3(x0 + (30 + 50) / self.scale + pos3_data[1] * 1000 / self.scale, y0)
        draw_pos3(x0 + l - (30 + 50) / self.scale - pos3_data[1] * 1000 / self.scale, y0)
        draw_pos3(x0 + l - (30 + 50) / self.scale, y0)
        mid_dist_temp = round((pos2_l * self.scale - (50 + pos3_data[1] * 1000) * 2 - pos3_data[3] * 1000) / 2)
        mid_dist = mid_dist_temp / self.scale
        draw_pos3(x0 + 30 / self.scale + (50 + pos3_data[1] * 1000) / self.scale + mid_dist, y0)
        draw_pos3(x0 + 30 / self.scale + (50 + pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + mid_dist, y0)
        s = (b - 2 * a) / (self._result_dict["1"][0] - 1)
        if l > 250:
            self.form3.set_line_width(0.05)
            self.form3.rect(x0 + l + 16, y0, b, h)
            self.form3.set_line_width(0.5)
            self.form3.line(
                x0 + l + 16 + a - (diam_pos3 + diam_pos1) / 2,
                y0 + 10 / self.scale,
                x0 + l + 16 + a - (diam_pos3 + diam_pos1) / 2,
                y0 + h - 10 / self.scale
            )
            self.form3.line(
                x0 + l + 16 + b - a + (diam_pos3 + diam_pos1) / 2,
                y0 + 10 / self.scale,
                x0 + l + 16 + b - a + (diam_pos3 + diam_pos1) / 2,
                y0 + h - 10 / self.scale
            )
            self.form3.line(
                x0 + l + 16 + 10 / self.scale,
                y0 + a - (diam_pos3 + diam_pos2) / 2,
                x0 + l + 16 + b - 10 / self.scale,
                y0 + a - (diam_pos3 + diam_pos2) / 2
            )
            self.form3.line(
                x0 + l + 16 + 10 / self.scale,
                y0 + h - a + (diam_pos3 + diam_pos1) / 2,
                x0 + l + 16 + b - 10 / self.scale,
                y0 + h - a + (diam_pos3 + diam_pos1) / 2
            )
            self.form3.set_line_width(0.05)
            self.form3.ellipse(x0 + l + 16 + a - diam_pos1 / 2, y0 + a - diam_pos2 / 2, diam_pos2, diam_pos2, "FD")
            self.form3.ellipse(x0 + l + 16 - a + diam_pos1 / 2 + b - diam_pos2, y0 + a - diam_pos2 / 2, diam_pos2, diam_pos2, "FD")
            for i in range(self._result_dict["1"][0]):
                self.form3.ellipse(x0 + l + 16 + a - diam_pos1 / 2 + s * i, y0 + h - a - diam_pos1 / 2, diam_pos1, diam_pos1, "FD")
        else:
            self.form3.set_line_width(0.05)
            self.form3.rect(x0 + l + 30, y0, b, h)
            self.form3.set_line_width(0.5)
            self.form3.line(
                x0 + l + 30 + a - (diam_pos3 + diam_pos1) / 2,
                y0 + 10 / self.scale,
                x0 + l + 30 + a - (diam_pos3 + diam_pos1) / 2,
                y0 + h - 10 / self.scale
            )
            self.form3.line(
                x0 + l + 30 + b - a + (diam_pos3 + diam_pos1) / 2,
                y0 + 10 / self.scale,
                x0 + l + 30 + b - a + (diam_pos3 + diam_pos1) / 2,
                y0 + h - 10 / self.scale
            )
            self.form3.line(
                x0 + l + 30 + 10 / self.scale,
                y0 + a - (diam_pos3 + diam_pos2) / 2,
                x0 + l + 30 + b - 10 / self.scale,
                y0 + a - (diam_pos3 + diam_pos2) / 2
            )
            self.form3.line(
                x0 + l + 30 + 10 / self.scale,
                y0 + h - a + (diam_pos3 + diam_pos1) / 2,
                x0 + l + 30 + b - 10 / self.scale,
                y0 + h - a + (diam_pos3 + diam_pos1) / 2
            )
            self.form3.set_line_width(0.05)
            self.form3.ellipse(x0 + l + 30 + a - diam_pos1 / 2, y0 + a - diam_pos2 / 2, diam_pos2, diam_pos2, "FD")
            self.form3.ellipse(x0 + l + 30 - a + diam_pos1 / 2 + b - diam_pos2, y0 + a - diam_pos2 / 2, diam_pos2, diam_pos2, "FD")
            for i in range(self._result_dict["1"][0]):
                self.form3.ellipse(x0 + l + 30 + a - diam_pos1 / 2 + s * i, y0 + h - a - diam_pos1 / 2, diam_pos1, diam_pos1, "FD")
        self._dim_h(x0, y0 + h, 30 / self.scale, -2.5)
        self._dim_h(x0 + 30 / self.scale, y0 + h, 50 / self.scale, 4)
        self._dim_h(
            x0 + 30 / self.scale + 50 / self.scale,
            y0 + h,
            pos3_data[1] * 1000 / self.scale,
            -5,
            f"{pos3_data[0] - 1}x100={(pos3_data[0] - 1) * 100}"
        )
        self._dim_h(
            x0 + 30 / self.scale + 50 / self.scale + pos3_data[1] * 1000 / self.scale,
            y0 + h,
            mid_dist
        )
        self._dim_h(
            x0 + 30 / self.scale + 50 / self.scale + pos3_data[1] * 1000 / self.scale + mid_dist,
            y0 + h,
            pos3_data[3] * 1000 / self.scale,
            -5,
            f"{pos3_data[2] - 1}x200={(pos3_data[2] - 1) * 200}"
        )
        self._dim_h(
            x0 + 30 / self.scale + 50 / self.scale + pos3_data[1] * 1000 / self.scale + mid_dist + pos3_data[3] * 1000 / self.scale,
            y0 + h,
            mid_dist
        )
        self._dim_h(
            x0 + 30 / self.scale + 50 / self.scale + pos3_data[1] * 1000 / self.scale + 2 * mid_dist + pos3_data[3] * 1000 / self.scale,
            y0 + h,
            pos3_data[1] * 1000 / self.scale,
            -5,
            f"{pos3_data[0] - 1}x100={(pos3_data[0] - 1) * 100}"
        )
        self._dim_h(
            x0 + 30 / self.scale + 50 / self.scale + 2 * pos3_data[1] * 1000 / self.scale + 2 * mid_dist + pos3_data[3] * 1000 / self.scale,
            y0 + h,
            50 / self.scale,
            -3
        )
        self._dim_h(
            x0 + 30 / self.scale + 2 * 50 / self.scale + 2 * pos3_data[1] * 1000 / self.scale + 2 * mid_dist + pos3_data[3] * 1000 / self.scale,
            y0 + h,
            30 / self.scale,
            3
        )
        self._dim_v(x0, y0, a, 3)
        self._dim_v(x0, y0 + a, h - 2 * a)
        self._dim_v(x0, y0 - a + h, a, -3)
        if l > 250:
            self._dim_h(x0 + l + 16, y0 + h, a, -3)
            if self._result_dict['1'][0] > 2:
                self._dim_h(
                    x0 + l + 16 + a,
                    y0 + h,
                    b - 2 * a,
                    -1,
                    f" "
                )
                self.form3.set_line_width(0.05)
                self.form3.line(x0 + l + 16 + b / 2, y0 + h + 8, x0 + l + 16 + b / 2, y0 + h + 13)
                self.form3.line(x0 + l + 16 + b / 2, y0 + h + 13, x0 + l + 16 + b / 2 + 15, y0 + h + 13)
                self.form3.text(
                    x0 + l + 16 + b / 2 + 1,
                    y0 + h + 12.5,
                    f"{self._result_dict['1'][0] - 1}x"
                    f"{int(round((b - 2 * a) * self.scale / (self._result_dict['1'][0] - 1), 0))}="
                    f"{int(round((b - 2 * a) * self.scale, 0))}")
            else:
                self._dim_h(
                    x0 + l + 16 + a,
                    y0 + h,
                    b - 2 * a,
                    -1,
                    f"{int(round((b - 2 * a) * self.scale / (self._result_dict['1'][0] - 1), 0))}"
                )
            self._dim_h(x0 + l + 16 - a + b, y0 + h, a, 3.5)
            self._dim_v(x0 + l + 16, y0, a, 3)
            self._dim_v(x0 + l + 16, y0 + a, h - 2 * a)
            self._dim_v(x0 + l + 16, y0 - a + h, a, -3)
        else:
            self._dim_h(x0 + l + 30, y0 + h, a, -3)
            if self._result_dict['1'][0] > 2:
                self._dim_h(
                    x0 + l + 30 + a,
                    y0 + h,
                    b - 2 * a,
                    -1,
                    " "  #f"{self._result_dict['1'][0] - 1}x{int(round((b - 2 * a) * self.scale / (self._result_dict['1'][0] - 1), 0))}"
                )
                self.form3.set_line_width(0.05)
                self.form3.line(x0 + l + 30 + b / 2, y0 + h + 8, x0 + l + 30 + b / 2, y0 + h + 13)
                self.form3.line(x0 + l + 30 + b / 2, y0 + h + 13, x0 + l + 30 + b / 2 + 15, y0 + h + 13)
                self.form3.text(
                    x0 + l + 30 + b / 2 + 1,
                    y0 + h + 12.5,
                    f"{self._result_dict['1'][0] - 1}x"
                    f"{int(round((b - 2 * a) * self.scale / (self._result_dict['1'][0] - 1), 0))}="
                    f"{int(round((b - 2 * a) * self.scale, 0))}")
            else:
                self._dim_h(
                    x0 + l + 30 + a,
                    y0 + h,
                    b - 2 * a,
                    0,
                    f"{int(round((b - 2 * a) * self.scale / (self._result_dict['1'][0] - 1), 0))}"
                )
            self._dim_h(x0 + l + 30 - a + b, y0 + h, a, 3.5)
            self._dim_v(x0 + l + 30, y0, a, 3)
            self._dim_v(x0 + l + 30, y0 + a, h - 2 * a)
            self._dim_v(x0 + l + 30, y0 - a + h, a, -3)
        self.form3.set_line_width(0.05)
        self.form3.set_font("iso", "", 11)
        self.form3.line(x0 + l / 2 + 5, y0 + a, x0 + l / 2 + 5, y0 + a + 5)
        self.form3.line(x0 + l / 2 + 5, y0 + a + 5, x0 + l / 2 + 8, y0 + a + 5)
        self.form3.text(x0 + l / 2 + 6, y0 + a + 4.5, "2")
        self.form3.line(x0 + l / 2 - 5, y0 + h - a, x0 + l / 2 - 5, y0 + h - a - 5)
        self.form3.line(x0 + l / 2 - 5, y0 + h - a - 5, x0 + l / 2 - 2, y0 + h - a - 5)
        self.form3.text(x0 + l / 2 - 4, y0 + h - a - 5.5, "1")
        self.form3.line(x0 + 80 / self.scale, y0 + h / 2, x0 + 80 / self.scale + 8, y0 + h / 2)
        self.form3.text(x0 + 80 / self.scale + 6, y0 + h / 2 - 0.5, "3")
        self.form3.line(
            x0 + (80 + pos3_data[1] * 1000) / self.scale,
            y0 + h / 2,
            x0 + (80 + pos3_data[1] * 1000) / self.scale - 8,
            y0 + h / 2
        )
        self.form3.text(x0 + (80 + pos3_data[1] * 1000) / self.scale - 7, y0 + h / 2 - 0.5, "3")
        self.form3.line(
            x0 + (80 + pos3_data[1] * 1000) / self.scale + mid_dist,
            y0 + h / 2,
            x0 + (80 + pos3_data[1] * 1000) / self.scale + mid_dist + 8,
            y0 + h / 2
        )
        self.form3.text(x0 + (80 + pos3_data[1] * 1000) / self.scale + mid_dist + 6, y0 + h / 2 - 0.5, "3")
        self.form3.line(
            x0 + (80 + pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + mid_dist,
            y0 + h / 2,
            x0 + (80 + pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + mid_dist - 8,
            y0 + h / 2
        )
        self.form3.text(x0 + (80 + pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + mid_dist -7, y0 + h / 2 - 0.5, "3")
        self.form3.line(
            x0 + (80 + pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + 2 * mid_dist,
            y0 + h / 2,
            x0 + (80 + pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + 2 * mid_dist + 8,
            y0 + h / 2
        )
        self.form3.text(x0 + (80 + pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + 2 * mid_dist + 6, y0 + h / 2 - 0.5, "3")
        self.form3.line(
            x0 + (80 + 2 * pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + 2 * mid_dist,
            y0 + h / 2,
            x0 + (80 + 2 * pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + 2 * mid_dist - 8,
            y0 + h / 2
        )
        self.form3.text(x0 + (80 + 2 * pos3_data[1] * 1000 + pos3_data[3] * 1000) / self.scale + 2 * mid_dist - 7, y0 + h / 2 - 0.5, "3")
        if l > 250:
            for i in range(self._result_dict["1"][0]):
                self.form3.line(
                    x0 + l + 16 + a + s * i,
                    y0 + h - a,
                    x0 + l + 16 + a + 2,
                    y0 + h - a - 5
                )
            self.form3.line(
                x0 + l + 16 + a + 2,
                y0 + h - a - 5,
                x0 + l + 16 + a + 5,
                y0 + h - a - 5
            )
            self.form3.text(x0 + l + 16 + a + 3, y0 + h - a - 5.5, "1")
            self.form3.line(
                x0 + l + 16 + a - diam_pos2 / 2,
                y0 + a,
                x0 + l + 16 + a - diam_pos2 / 2 - 2,
                y0 + a - 5
            )
            self.form3.line(
                x0 + l + 16 + a - diam_pos2 / 2 - 2,
                y0 + a - 5,
                x0 + l + 16 + a - diam_pos2 / 2 - 5,
                y0 + a - 5
            )
            self.form3.text(x0 + l + 16 + a - diam_pos2 / 2 - 4, y0 + a - 5.5, "2")
            self.form3.line(
                x0 + l + 16 - a + b - diam_pos2 / 2 + diam_pos1 / 2,
                y0 + a,
                x0 + l + 16 - a + b - diam_pos2 / 2 + diam_pos1 / 2 + 2,
                y0 + a - 5
            )
            self.form3.line(
                x0 + l + 16 - a + b - diam_pos2 / 2 + diam_pos1 / 2 + 2,
                y0 + a - 5,
                x0 + l + 16 - a + b - diam_pos2 / 2 + diam_pos1 / 2 + 5,
                y0 + a - 5
            )
            self.form3.text(x0 + l + 16 - a + b - diam_pos2 / 2 + diam_pos1 / 2 + 3, y0 + a - 5.5, "2")
            self.form3.line(
                x0 + l + 16 + a - (diam_pos3 / 2 + diam_pos1 / 2),
                y0 + h / 2,
                x0 + l + 16 + a - (diam_pos3 / 2 + diam_pos1 / 2) - 6,
                y0 + h / 2
            )
            self.form3.text(x0 + l + 16 + a - (diam_pos3 / 2 + diam_pos1 / 2) - 5, y0 + h / 2 - 0.5, "3")
            self.form3.line(
                x0 + l + 16 - a + (diam_pos3 / 2 + diam_pos1 / 2) + b,
                y0 + h / 2,
                x0 + l + 16 - a + (diam_pos3 / 2 + diam_pos1 / 2) + b + 8,
                y0 + h / 2
            )
            self.form3.text(x0 + l + 16 - a + (diam_pos3 + diam_pos1) / 2 + b + 6, y0 + h / 2 - 0.5, "3")
            self.form3.line(
                x0 + l + 16 + b / 2,
                y0 + a - (diam_pos4 + diam_pos2) / 2,
                x0 + l + 16 + b / 2 - 2,
                y0 + a - (diam_pos4 + diam_pos2) / 2 - 5
            )
            self.form3.line(x0 + l + 16 + b / 2 - 2, y0 + a - (diam_pos4 + diam_pos2) / 2 - 5, x0 + l + 16 + b / 2 + 1, y0 + a - (diam_pos4 + diam_pos2) / 2 - 5)
            self.form3.text(x0 + l + 16 + b / 2 - 1, y0 + a - (diam_pos4 + diam_pos2) / 2 - 5.5, "4")
            self.form3.line(
                x0 + l + 16 + 3,
                y0 + h - a + (diam_pos4 + diam_pos1) / 2,
                x0 + l + 16 - 2,
                y0 + h - a + (diam_pos4 + diam_pos1) / 2 + 5
            )
            self.form3.line(
                x0 + l + 16 - 2,
                y0 + h - a + (diam_pos4 + diam_pos1) / 2 + 5,
                x0 + l + 16 - 5,
                y0 + h - a + (diam_pos4 + diam_pos1) / 2 + 5
            )
            self.form3.text(x0 + l + 16 - 4, y0 + h - a + (diam_pos4 + diam_pos1) / 2 + 4.5, "4")
        else:
            for i in range(self._result_dict["1"][0]):
                self.form3.line(
                    x0 + l + 30 + a + s * i,
                    y0 + h - a,
                    x0 + l + 30 + a + 2,
                    y0 + h - a - 5
                )
            self.form3.line(
                x0 + l + 30 + a + 2,
                y0 + h - a - 5,
                x0 + l + 30 + a + 5,
                y0 + h - a - 5
            )
            self.form3.text(x0 + l + 30 + a + 3, y0 + h - a - 5.5, "1")
            self.form3.line(
                x0 + l + 30 + a - diam_pos2 / 2,
                y0 + a,
                x0 + l + 30 + a - diam_pos2 / 2 - 2,
                y0 + a - 5
            )
            self.form3.line(
                x0 + l + 30 + a - diam_pos2 / 2 - 2,
                y0 + a - 5,
                x0 + l + 30 + a - diam_pos2 / 2 - 5,
                y0 + a - 5
            )
            self.form3.text(x0 + l + 30 + a - diam_pos2 / 2 - 4, y0 + a - 5.5, "2")
            self.form3.line(
                x0 + l + 30 - a + b - diam_pos2 / 2 + diam_pos1 / 2,
                y0 + a,
                x0 + l + 30 - a + b - diam_pos2 / 2 + diam_pos1 / 2 + 2,
                y0 + a - 5
            )
            self.form3.line(
                x0 + l + 30 - a + b - diam_pos2 / 2 + diam_pos1 / 2 + 2,
                y0 + a - 5,
                x0 + l + 30 - a + b - diam_pos2 / 2 + diam_pos1 / 2 + 5,
                y0 + a - 5
            )
            self.form3.text(x0 + l + 30 - a + b - diam_pos2 / 2 + diam_pos1 / 2 + 3, y0 + a - 5.5, "2")
            self.form3.line(
                x0 + l + 30 + a - (diam_pos3 / 2 + diam_pos1 / 2),
                y0 + h / 2,
                x0 + l + 30 + a - (diam_pos3 / 2 + diam_pos1 / 2) - 6,
                y0 + h / 2
            )
            self.form3.text(x0 + l + 30 + a - (diam_pos3 / 2 + diam_pos1 / 2) - 5, y0 + h / 2 - 0.5, "3")
            self.form3.line(
                x0 + l + 30 - a + (diam_pos3 / 2 + diam_pos1 / 2) + b,
                y0 + h / 2,
                x0 + l + 30 - a + (diam_pos3 / 2 + diam_pos1 / 2) + b + 8,
                y0 + h / 2
            )
            self.form3.text(x0 + l + 30 - a + (diam_pos3 + diam_pos1) / 2 + b + 6, y0 + h / 2 - 0.5, "3")
            self.form3.line(
                x0 + l + 30 + b / 2,
                y0 + a - (diam_pos4 + diam_pos2) / 2,
                x0 + l + 30 + b / 2 - 2,
                y0 + a - (diam_pos4 + diam_pos2) / 2 - 5
            )
            self.form3.line(x0 + l + 30 + b / 2 - 2, y0 + a - (diam_pos4 + diam_pos2) / 2 - 5, x0 + l + 30 + b / 2 + 1, y0 + a - (diam_pos4 + diam_pos2) / 2 - 5)
            self.form3.text(x0 + l + 30 + b / 2 - 1, y0 + a - (diam_pos4 + diam_pos2) / 2 - 5.5, "4")
            self.form3.line(
                x0 + l + 30 + 3,
                y0 + h - a + (diam_pos4 + diam_pos1) / 2,
                x0 + l + 30 - 2,
                y0 + h - a + (diam_pos4 + diam_pos1) / 2 + 5
            )
            self.form3.line(
                x0 + l + 30 - 2,
                y0 + h - a + (diam_pos4 + diam_pos1) / 2 + 5,
                x0 + l + 30 - 5,
                y0 + h - a + (diam_pos4 + diam_pos1) / 2 + 5
            )
            self.form3.text(x0 + l + 30 - 4, y0 + h - a + (diam_pos4 + diam_pos1) / 2 + 4.5, "4")

    def _dim_h(self, x, y, l, x_text=0.0, text=""):
        x0 = x
        y0 = y
        x_t = x0 + x_text + l / 2 - 2
        if len(text) == 0:
            dim_text = str(int(l * self.scale))
        else:
            dim_text = text
        self.form3.set_line_width(0.05)
        self.form3.line(x0 - 2, y0 + 8, x0 + l + 2, y0 + 8)
        self.form3.line(x0, y0 + 2, x0, y0 + 10)
        self.form3.line(x0 + l, y0 + 2, x0 + l, y0 + 10)
        self.form3.set_line_width(0.5)
        self.form3.line(x0 - 0.9, y0 + 8.9, x0 + 0.9, y0 + 7.1)
        self.form3.line(x0 + l - 0.9, y0 + 8.9, x0 + l + 0.9, y0 + 7.1)
        self.form3.set_font("iso", "", 11)
        self.form3.text(x_t, y0 + 7.5, dim_text)

    def _dim_v(self, x, y, l, x_text=0.0, text=""):
        x0 = x
        y0 = y
        x_t = x0 + x_text - l / 2 - 2
        self.form3.rotate(90, x0, y0)
        if len(text) == 0:
            dim_text = str(int(l * self.scale))
        else:
            dim_text = text
        self.form3.set_line_width(0.05)
        self.form3.line(x0 + 2, y0 - 8, x0 - l - 2, y0 - 8)
        self.form3.line(x0, y0 - 2, x0, y0 - 10)
        self.form3.line(x0 - l, y0 - 2, x0 - l, y0 - 10)
        self.form3.set_line_width(0.5)
        self.form3.line(x0 + 0.9, y0 - 8.9, x0 - 0.9, y0 - 7.1)
        self.form3.line(x0 - l + 0.9, y0 - 8.9, x0 - l - 0.9, y0 - 7.1)
        self.form3.set_font("iso", "", 11)
        self.form3.text(x_t, y0 - 8.5, dim_text)
        self.form3.rotate(0)

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
        self.form3.set_font("iso", "", 11)
        self.form3.text(233, y0 + 255.75, "Зм.")
        self.form3.text(240.75, y0 + 255.75, "Кільк.")
        self.form3.text(252, y0 + 255.75, "Арк.")
        self.form3.text(260.5, y0 + 255.75, "№док.")
        self.form3.text(273, y0 + 255.75, "Підпис")
        self.form3.text(286, y0 + 255.75, "Дата")
        self.form3.text(231, y0 + 260.75, "Виконав")
        self.form3.text(251, y0 + 260.75, "Бережний")
        self.form3.text(367, y0 + 260.75, "Стадія")
        self.form3.text(382.5, y0 + 260.75, "Аркуш")
        self.form3.text(396.25, y0 + 260.75, "Аркушів")
        self.form3.text(296, y0 + 275.75, self.title1)
        self.form3.text(296, y0 + 280.75, self.title2)
        self.form3.text(296, y0 + 285.75, self.title3)
        self.form3.set_font("iso", "", 14)
        self.form3.text(370, y0 + 268.75, "ЕП")
        self.form3.text(386.5, y0 + 268.75, "1")
        self.form3.text(401.5, y0 + 268.75, "1")
        self.form3.text(336, y0 + 238.25, str(datetime.utcnow().strftime("%Y—%m—%d %H:%M")))
        self.form3.image("static/images/logo_dark.png", 366.25, y0 + 273.25, 42.5, 12.5)
        
    def _draw_specification(self, result_dict: dict, x=230, y=30, title: str = "Специфікація"):
        x0 = x
        y0 = y
        self.form3.set_line_width(0.5)
        self.form3.line(x0 + 0, y0 + 0, x0 + 180, y0 + 0)
        self.form3.line(x0 + 0, y0 + 15, x0 + 180, y0 + 15)
        self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + self.count_of_lines * 8)
        self.form3.line(x0 + 15, y0 + 0, x0 + 15, y0 + 15 + self.count_of_lines * 8)
        self.form3.line(x0 + 75, y0 + 0, x0 + 75, y0 + 15 + self.count_of_lines * 8)
        self.form3.line(x0 + 135, y0 + 0, x0 + 135, y0 + 15 + self.count_of_lines * 8)
        self.form3.line(x0 + 145, y0 + 0, x0 + 145, y0 + 15 + self.count_of_lines * 8)
        self.form3.line(x0 + 160, y0 + 0, x0 + 160, y0 + 15 + self.count_of_lines * 8)
        self.form3.line(x0 + 180, y0 + 0, x0 + 180, y0 + 15 + self.count_of_lines * 8)
        y = y0 + 23
        self.form3.set_line_width(0.05)
        i = 0
        while i < self.count_of_lines:
            self.form3.set_font("iso", "", 11)
            self.form3.line(x0 + 0, y, x0 + 180, y)
            i += 1
            y += 8
        self.form3.set_font("iso", "", 14)
        self.form3.text(x0 + 85, y0 - 5, title)
        self.form3.set_font("iso", "", 11)
        self.form3.text(x0 + 5, y0 + 9.25, "Поз.")
        self.form3.text(x0 + 35, y0 + 9.25, "Позначення")
        self.form3.text(x0 + 94, y0 + 9.25, "Найменування")
        self.form3.text(x0 + 135.5, y0 + 9.25, "Кільк.")
        self.form3.text(x0 + 145.3, y0 + 7.25, "Маса од.,")
        self.form3.text(x0 + 151, y0 + 11, "кг")
        self.form3.text(x0 + 163, y0 + 9.25, "Примітка")
        self.form3.set_font("iso", "U", 11)
        self.form3.text(x0 + 88, y0 + 20.25 + 0 * 8, "Залізобетонні вироби")
        self.form3.text(x0 + 90, y0 + 20.25 + 2 * 8, "Арматурні вироби")
        self.form3.text(x0 + 96, y0 + 20.25 + 7 * 8, "Матеріали")
        self.form3.set_font("iso", "", 11)
        mark = []
        for key in result_dict.keys():
            mark.append(key)
        text0 = f"Залізобетонна балка {mark[0]}"
        mass = (int(self._result_dict[mark[0]][2]) + 500) * int(self._result_dict[mark[0]][3]) * int(self._result_dict[mark[0]][4]) * 2500 / 1e9
        self.form3.text(x0 + 4, y0 + 20.25 + 1 * 8, mark[0])
        self.form3.text(x0 + 76, y0 + 20.25 + 1 * 8, text0)
        self.form3.text(x0 + 139, y0 + 20.25 + 1 * 8, '1')
        self.form3.text(x0 + 148.5, y0 + 20.25 + 1 * 8, str(mass))
        i = 3
        for p in mark[1:]:
            diameter = self._result_dict[p][1]
            cl = self._result_dict[p][2]
            length = int(self._result_dict[p][3] * 1000)
            quantity = self._result_dict[p][0]
            text1 = f"∅{diameter}{cl}; L={length}"
            mass = round(pi * (diameter / 1000) ** 2 / 4 * 7850 * length / 1000, 3)
            total_mass = f"{round(mass * quantity, 3)} кг"
            self.form3.text(x0 + 6.5, y0 + 20.25 + i * 8, p)
            self.form3.text(x0 + 16, y0 + 20.25 + i * 8, "ДСТУ 3760:2019")
            self.form3.text(x0 + 76, y0 + 20.25 + i * 8, text1)
            self.form3.text(x0 + 139, y0 + 20.25 + i * 8, f"{quantity}")
            self.form3.text(x0 + 148.5, y0 + 20.25 + i * 8, f"{mass}")
            self.form3.text(x0 + 162.5, y0 + 20.25 + i * 8, f"{total_mass}")
            i += 1
        volume = (int(self._result_dict[mark[0]][2]) + 500) * int(self._result_dict[mark[0]][3]) * int(self._result_dict[mark[0]][4]) / 1e9
        self.form3.text(x0 + 16, y0 + 20.25 + 8 * 8, "ДСТУ Б В.2.7-176:2008")
        self.form3.text(x0 + 76, y0 + 20.25 + 8 * 8, "Бетон класу С20/25")
        self.form3.text(x0 + 162.5, y0 + 20.25 + 8 * 8, f"{volume}")
        self.form3.text(x0 + 171, y0 + 20.25 + 8 * 8, f"м")
        self.form3.set_font("iso", "", 7)
        self.form3.text(x0 + 173, y0 + 19.25 + 8 * 8, "3")


if __name__ == "__main__":
    test_dict = {
        'Б-1': ['Несуча стіна', 'Опирання з однієї сторони', '900', '250', '510']
    }
    filename = "files/result_test.pdf"
    s = MakePDF(test_dict, filename)