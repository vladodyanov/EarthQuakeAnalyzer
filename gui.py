import wx
from datetime import datetime, timedelta
from data_fetcher import fetch_earthquake_data
from data_processor import process_data
from analyzer import analyze_and_visualize, depth_magnitude_correlation


class ResultDialog(wx.Dialog):
    def __init__(self, parent, title, message, statistics):
        super().__init__(parent, title=title, size=(500, 500))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        message_ctrl = wx.TextCtrl(panel, value=message, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(message_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        btn_charts = wx.Button(panel, label="Диаграми")
        btn_charts.Bind(wx.EVT_BUTTON, self.on_charts)
        hbox.Add(btn_charts, proportion=1, flag=wx.EXPAND | wx.RIGHT, border=5)

        btn_stats = wx.Button(panel, label="Статистика")
        btn_stats.Bind(wx.EVT_BUTTON, lambda event: self.on_statistics(event, statistics))
        hbox.Add(btn_stats, proportion=1, flag=wx.EXPAND | wx.LEFT, border=5)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def on_charts(self, event):
        self.EndModal(wx.ID_OK)

    def on_statistics(self, event, statistics):
        dlg = wx.MessageDialog(self, statistics, "Статистика", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class SeismicAnalysisApp(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Анализ на сеизмична активност')
        panel = wx.Panel(self)

        wx.StaticText(panel, label="Начална дата (ГГГГ-ММ-ДД):", pos=(10, 10))
        self.start_date = wx.TextCtrl(panel, pos=(10, 30), size=(150, 25))

        wx.StaticText(panel, label="Крайна дата (ГГГГ-ММ-ДД):", pos=(10, 60))
        self.end_date = wx.TextCtrl(panel, pos=(10, 80), size=(150, 25))

        wx.StaticText(panel, label="Минимален магнитуд (0.0 до 10.0):", pos=(10, 110))
        self.magnitude = wx.TextCtrl(panel, pos=(10, 130), size=(150, 25))

        wx.StaticText(panel, label="Континент:", pos=(10, 160))
        self.continent = wx.ComboBox(panel, pos=(10, 180), size=(150, 25),
                                     choices=['Всички', 'Африка', 'Антарктика', 'Азия',
                                              'Европа', 'Северна Америка', 'Океания',
                                              'Южна Америка'],
                                     style=wx.CB_READONLY)

        analyze_button = wx.Button(panel, label='Анализирай', pos=(10, 210), size=(150, 25))
        analyze_button.Bind(wx.EVT_BUTTON, self.on_analyze)

        # Стойности по подразбиране
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        self.start_date.SetValue(week_ago.strftime("%Y-%m-%d"))
        self.end_date.SetValue(today.strftime("%Y-%m-%d"))
        self.magnitude.SetValue("5.0")
        self.continent.SetValue('Всички')

        self.SetSize((300, 300))
        self.Centre()
        self.Show()

    def on_analyze(self, event):
        # Валидация на входните данни
        try:
            start_date = self.validate_date(self.start_date.GetValue(), "Начална дата")
            end_date = self.validate_date(self.end_date.GetValue(), "Крайна дата")
            magnitude = self.validate_magnitude(self.magnitude.GetValue())
            continent = self.continent.GetValue()

            if start_date > end_date:
                raise ValueError("Началната дата трябва да бъде преди крайната дата")

        except ValueError as e:
            wx.MessageBox(str(e), "Грешка", wx.OK | wx.ICON_ERROR)
            return

        # Извличане и обработка на данните
        data = fetch_earthquake_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), magnitude)
        df = process_data(data)

        # Филтриране по континент
        if continent != 'Всички':
            df = df[df['continent'] == continent]

        # Анализ и визуализация
        (result, top_earthquakes, most_affected_region, affected_region_count, correlation,
         seismic_hazard_assessment, aftershocks_analysis, map_image, activity_change_analysis) = analyze_and_visualize(
            df, start_date, end_date,
            magnitude)

        # Корелация
        correlation_explanation = depth_magnitude_correlation(correlation)

        # Резултати
        message = (f"Анализ за периода: {start_date.strftime('%Y-%m-%d')} до {end_date.strftime('%Y-%m-%d')}\n"
                   f"Минимален магнитуд: {magnitude}\n"
                   f"Избран континент: {continent}\n\n"
                   f"{result}\n\n"
                   f"Корелация между дълбочина и магнитуд:\n"
                   f"{correlation_explanation}\n\n"
                   f"{activity_change_analysis}\n\n"
                   f"Анализ на афтършокове (вторични земетресения):\n"
                   f"{aftershocks_analysis}\n")

        statistics = (f"Най-засегнат регион: {most_affected_region} (брой земетресения: {affected_region_count})\n"
                      f"{seismic_hazard_assessment}\n"
                      f"Земетресения с най-висок магнитуд:\n{top_earthquakes}")

        dlg = ResultDialog(self, "Резултати от анализа", message, statistics)
        if dlg.ShowModal() == wx.ID_OK:
            self.show_images()
        dlg.Destroy()

    def validate_date(self, date_string, field_name):
        try:
            return datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"{field_name} трябва да бъде във формат ГГГГ-ММ-ДД")

    def validate_magnitude(self, magnitude_string):
        try:
            magnitude = float(magnitude_string)
            if magnitude < 0.0 or magnitude > 10.0:
                raise ValueError()
            return magnitude
        except ValueError:
            raise ValueError("Магнитудът трябва да бъде число между 0.0 и 10.0")

    def show_images(self):
        image1 = wx.Image('earthquakes_over_time.png', wx.BITMAP_TYPE_PNG)
        image2 = wx.Image('magnitude_distribution.png', wx.BITMAP_TYPE_PNG)
        image4 = wx.Image('world_map.png', wx.BITMAP_TYPE_PNG)

        frame1 = wx.Frame(None, -1, 'Земетресения във времето')
        wx.StaticBitmap(frame1, -1, wx.Bitmap(image1))
        frame1.Show()

        frame2 = wx.Frame(None, -1, 'Разпределение на магнитудите')
        wx.StaticBitmap(frame2, -1, wx.Bitmap(image2))
        frame2.Show()

        frame4 = wx.Frame(None, -1, 'Карта на света със земетресения')
        wx.StaticBitmap(frame4, -1, wx.Bitmap(image4))
        frame4.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = SeismicAnalysisApp()
    app.MainLoop()
