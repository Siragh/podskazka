from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout

class RiskCalculatorApp(App):
    def build(self):
        # Корневой макет с выравниванием содержимого сверху
        root_layout = AnchorLayout(anchor_y="top")
       
        # Внутренний макет
        content_layout = BoxLayout(orientation="vertical", padding=10, spacing=10, size_hint=(None, None))
        content_layout.size = (600, 800)  # Устанавливаем фиксированный размер окна
       
        # Поле для вывода результата (сверху)
        self.result_label_top = Label(
            text="Результаты будут здесь.",
            font_size=46,
            halign="center",  # Выравнивание текста по центру
            valign="middle",
            size_hint=(1, None),
            height=100,
            markup=True  # Включаем разметку
        )
        content_layout.add_widget(self.result_label_top)
       
        # Добавление параметров
        self.capital = 10000
        self.risk_percentage = 0.5
        self.lot_value = self.capital
       
        # Отображение текущих настроек
        content_layout.add_widget(Label(text=f"Текущий капитал: ${self.capital}"))
        content_layout.add_widget(Label(text=f"Риск на сделку: {self.risk_percentage}%"))
        content_layout.add_widget(Label(text=f"Размер лота: ${self.lot_value}\n"))
       
        # Ввод цены стоп-лосса
        content_layout.add_widget(Label(text="Введите цену стоп-лосса ($):"))
        self.stop_loss_input = TextInput(
            multiline=False,
            input_filter="float",
            size_hint=(None, None),
            width=300,  # Устанавливаем ширину
            height=100,  # Устанавливаем высоту
            pos_hint={"center_x": 0.5}  # Центрируем по горизонтали
        )
        content_layout.add_widget(self.stop_loss_input)
       
        # Увеличенная кнопка с зелёным текстом
        self.calc_button = Button(
            text="Рассчитать",
            size_hint=(None, None),  # Отключаем автоматическое растяжение
            width=400,  # Устанавливаем ширину
            height=200,  # Увеличенная высота
            font_size=40,  # Увеличенный размер текста
            bold=True,     # Жирный текст
            pos_hint={"center_x": 0.5}  # Центрируем по горизонтали
        )
        self.calc_button.bind(on_press=self.calculate)
        self.calc_button.color = (0, 1, 0, 1)  # Цвет текста (зелёный)
        content_layout.add_widget(self.calc_button)
       
        # Добавляем всё в корневой макет
        root_layout.add_widget(content_layout)
        return root_layout

    def calculate(self, instance):
        try:
            stop_loss_price = float(self.stop_loss_input.text)
            risk_amount = self.capital * (self.risk_percentage / 100)
            lot_size_btc = self.lot_value / stop_loss_price
            max_buy_price = stop_loss_price + (risk_amount / lot_size_btc)
           
            # Форматируем результат
            self.result_label_top.text = (
                f"[b]Макс. цена покупки:[/b] [color=#FF0000]${max_buy_price:.2f}[/color]\n"
                f"[b]Стоп-лосс:[/b] ${stop_loss_price:.2f}"
            )
        except ValueError:
            self.result_label_top.text = "Ошибка ввода. Проверьте данные."

# Точка входа
if __name__ == "__main__":
    RiskCalculatorApp().run()