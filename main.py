from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import RoundedRectangle
from kivy.properties import NumericProperty

class RoundedButton(Button):
    corner_radius = NumericProperty(1)

    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.color = (.51, .54, .59, 1)  # Установка цвета текста

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.corner_radius, ] * 4, background_color = (.12, .72, .88, 1))


class ScheduleApp(App):
    def build(self):
        self.schedule = [[], [], [], [], [], [], []]  # Список событий для каждого дня недели
        self.days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.popup = None  # Создаем атрибут popup

        layout = BoxLayout(orientation='vertical')
        layout.background_color = (.12, .72, .88, 1)

        button_layout = GridLayout(cols=1, spacing=15, padding = 50)
        layout.add_widget(button_layout)

        self.buttons = []  # Список кнопок для каждого дня недели

        for i in range(7):
            day_button = RoundedButton(text=self.days[i], background_color=(1, 1, 1, 1), background_normal = '', font_size = 20)
            day_button.bind(on_release=lambda button, day=self.days[i]: self.show_schedule(day))
            self.buttons.append(day_button)
            button_layout.add_widget(day_button)

        close_button = RoundedButton(text='Выйти',
                              font_size=20,
                              background_color=(.12, .72, .88, 1),
                              background_normal='',)
        close_button.color = (1, 1, 1, 1)
        close_button.bind(on_release=self.stop)
        button_layout.add_widget(close_button)

        return layout

    def show_schedule(self, day):
        day_index = self.days.index(day)
        schedule_text = '\n'.join(self.schedule[day_index])
        if schedule_text == "":
            schedule_text = "Добавьте событие"

        content = BoxLayout(orientation='vertical', padding=10)
        popup_label = ScrollView(size_hint=(1, 0.8))
        schedule_label = Label(text=schedule_text, size_hint=(1, None))
        popup_label.add_widget(schedule_label)
        content.add_widget(popup_label)

        add_event_button = RoundedButton(text="Добавить", size_hint=(1, 0.2), background_normal='')
        add_event_button.bind(on_release=lambda instance: self.add_event(day, content))
        content.add_widget(add_event_button)

        close_button = RoundedButton(text="Закрыть", size_hint=(1, 0.2), background_color=(.12, .72, .88, 1), background_normal='')
        close_button.color = (1, 1, 1, 1)
        close_button.bind(on_release=lambda instance: self.close_event(content, day, content, close_button))
        content.add_widget(close_button)

        self.popup = Popup(title="Расписание на " + day, content=content, size_hint=(0.6, 0.6))
        self.popup.open()

    def add_event(self, day, content):
        day_index = self.days.index(day)

        event_container = BoxLayout(orientation='vertical', spacing=10,)

        event_textinput = TextInput(hint_text="Введите событие")
        event_container.add_widget(event_textinput)
    
        save_event_button = RoundedButton(text="Сохранить", size_hint=(1, 0.2), background_color=(.12, .72, .88, 1), background_normal='')
        save_event_button.color = (1, 1, 1, 1)
        save_event_button.bind(on_release=lambda instance: self.save_event(day_index, event_textinput.text, content, day, event_container, save_event_button))
        event_container.add_widget(save_event_button)

        if len(content.children) >= 4:
            content.remove_widget(content.children[2])  # Удалить кнопку "Добавить событие"

        self.clear_content(content)  # Очистить содержимое
        content.add_widget(event_container)

    def save_event(self, day_index, event, content, day, event_container, save_event_button):
        event_text = event
        self.schedule[day_index].append(event_text)

        schedule_text = '\n'.join(self.schedule[day_index])
        if schedule_text == "":
            schedule_text = "Нет событий"

        self.popup.dismiss()  # Закрыть текущий popup

        self.show_schedule(day)  # Открыть окно дня недели с уже сохраненным событием

    def close_event(self, content, day, event_container, close_button):
        self.popup.dismiss()  # Закрыть текущий Popup

    def clear_content(self, content):
        content.clear_widgets()


if __name__ == "__main__":
    ScheduleApp().run()