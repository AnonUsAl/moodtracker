"""MoodTracker — 手机端 Kivy 原生界面

打包 APK:
    cd mobile
    buildozer init   (已提供 buildozer.spec，跳过)
    buildozer android debug deploy run
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from datetime import datetime

from storage import load_records, add_record

MOOD_DATA = [
    (1, "😢", "很低", "#f87171"),
    (2, "😕", "低",   "#fb923c"),
    (3, "😐", "一般", "#facc15"),
    (4, "🙂", "好",   "#4ade80"),
    (5, "😄", "很好", "#22d3ee"),
]
MOOD_MAP = {m[0]: m for m in MOOD_DATA}


class LogScreen(Screen):
    """录入页面。"""

    selected_mood = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(16))

        # 标题
        title = Label(
            text="记录心情",
            font_size=dp(24),
            size_hint_y=None,
            height=dp(50),
            color=(1, 1, 1, 1),
        )
        layout.add_widget(title)

        # 情绪按钮网格
        grid = GridLayout(cols=5, spacing=dp(8), size_hint_y=None, height=dp(100))
        for mood_val, emoji, label, color in MOOD_DATA:
            btn = Button(
                text=f"{emoji}\n{label}",
                font_size=dp(14),
                markup=True,
            )
            btn.mood_val = mood_val
            btn.color_hex = color
            btn.background_normal = ""
            btn.background_color = self._hex_to_rgba(color, 0.15)
            btn.bind(on_release=self.on_mood_select)
            grid.add_widget(btn)
        layout.add_widget(grid)

        # 备注
        self.note_input = TextInput(
            hint_text="备注（可选）",
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16),
            multiline=False,
        )
        layout.add_widget(self.note_input)

        # 保存按钮
        self.submit_btn = Button(
            text="保存记录",
            font_size=dp(18),
            size_hint_y=None,
            height=dp(55),
            disabled=True,
            background_normal="",
            background_color=(0.42, 0.55, 0.91, 1),
        )
        self.submit_btn.bind(on_release=self.on_submit)
        layout.add_widget(self.submit_btn)

        # 状态提示
        self.status_label = Label(
            text="",
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30),
            color=(0.29, 0.87, 0.5, 1),
        )
        layout.add_widget(self.status_label)

        # 底部导航
        nav = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        btn_hist = Button(text="📊 历史", font_size=dp(14), background_normal="", background_color=(0.15, 0.17, 0.21, 1))
        btn_hist.bind(on_release=lambda x: setattr(self.manager, "current", "history"))
        btn_stats = Button(text="📈 统计", font_size=dp(14), background_normal="", background_color=(0.15, 0.17, 0.21, 1))
        btn_stats.bind(on_release=lambda x: setattr(self.manager, "current", "stats"))
        nav.add_widget(btn_hist)
        nav.add_widget(btn_stats)
        layout.add_widget(nav)

        self.add_widget(layout)

    def on_mood_select(self, btn):
        self.selected_mood = btn.mood_val
        self.submit_btn.disabled = False
        # 高亮选中
        for child in btn.parent.children:
            m = child.mood_val
            color = child.color_hex
            if m == self.selected_mood:
                child.background_color = self._hex_to_rgba(color, 0.5)
            else:
                child.background_color = self._hex_to_rgba(color, 0.15)
        self.status_label.text = ""

    def on_submit(self, btn):
        if not self.selected_mood:
            return
        note = self.note_input.text.strip()
        add_record(self.selected_mood, note)
        self.status_label.text = "✅ 已保存!"
        self.note_input.text = ""
        self.selected_mood = 0
        self.submit_btn.disabled = True
        # 重置按钮颜色
        grid = self.children[0].children[3]  # grid widget
        for child in grid.children:
            child.background_color = self._hex_to_rgba(child.color_hex, 0.15)

    @staticmethod
    def _hex_to_rgba(hex_color, alpha=1.0):
        h = hex_color.lstrip("#")
        r = int(h[0:2], 16) / 255.0
        g = int(h[2:4], 16) / 255.0
        b = int(h[4:6], 16) / 255.0
        return (r, g, b, alpha)


class HistoryScreen(Screen):
    """历史记录页面。"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))

        title = Label(text="历史记录", font_size=dp(24), size_hint_y=None, height=dp(50), color=(1, 1, 1, 1))
        layout.add_widget(title)

        scroll = ScrollView(size_hint_y=1)
        self.list_container = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(8))
        self.list_container.bind(minimum_height=self.list_container.setter("height"))
        scroll.add_widget(self.list_container)
        layout.add_widget(scroll)

        nav = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        btn_log = Button(text="📝 记录", font_size=dp(14), background_normal="", background_color=(0.15, 0.17, 0.21, 1))
        btn_log.bind(on_release=lambda x: setattr(self.manager, "current", "log"))
        btn_stats = Button(text="📈 统计", font_size=dp(14), background_normal="", background_color=(0.15, 0.17, 0.21, 1))
        btn_stats.bind(on_release=lambda x: setattr(self.manager, "current", "stats"))
        nav.add_widget(btn_log)
        nav.add_widget(btn_stats)
        layout.add_widget(nav)

        self.add_widget(layout)

    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.list_container.clear_widgets()
        records = load_records()
        if not records:
            self.list_container.add_widget(
                Label(text="还没有记录\n先记录一下今天的心情吧", font_size=dp(16), color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=dp(80))
            )
            return

        for r in reversed(records):
            mood_val = r["mood"]
            _, emoji, label, color_hex = MOOD_MAP.get(mood_val, (0, "❓", "?", "#888888"))
            bar = "█" * mood_val + "░" * (5 - mood_val)

            item = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(60), spacing=dp(10))

            # 左侧颜色条
            color_label = Label(
                text="",
                size_hint_x=None,
                width=dp(6),
            )
            color_label.canvas.before.clear()
            with color_label.canvas.before:
                Color(*self._hex_to_rgba(color_hex))
                color_label.rect = Rectangle(pos=color_label.pos, size=(dp(6), dp(60)))
            color_label.bind(pos=lambda inst, val, r=color_label.rect: setattr(r, "pos", val))
            color_label.bind(size=lambda inst, val, r=color_label.rect: setattr(r, "size", (dp(6), val[1])))
            item.add_widget(color_label)

            info = BoxLayout(orientation="vertical", spacing=dp(2))
            info.add_widget(Label(
                text=f"{r['date']} {r['time']}  {emoji} {mood_val}/5",
                font_size=dp(14),
                color=(0.85, 0.85, 0.85, 1),
                size_hint_y=None,
                height=dp(24),
                halign="left",
                valign="middle",
            ))
            info.add_widget(Label(
                text=r.get("note", "") or "（无备注）",
                font_size=dp(12),
                color=(0.55, 0.55, 0.55, 1),
                size_hint_y=None,
                height=dp(20),
                halign="left",
                valign="middle",
                text_size=(None, None),
            ))
            item.add_widget(info)
            self.list_container.add_widget(item)

    @staticmethod
    def _hex_to_rgba(hex_color, alpha=1.0):
        h = hex_color.lstrip("#")
        r = int(h[0:2], 16) / 255.0
        g = int(h[2:4], 16) / 255.0
        b = int(h[4:6], 16) / 255.0
        return (r, g, b, alpha)


class StatsScreen(Screen):
    """统计页面。"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(16))
        self.add_widget(self.layout)

    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.layout.clear_widgets()
        records = load_records()
        if not records:
            self.layout.add_widget(Label(text="还没有记录，无法统计", font_size=dp(16), color=(0.5, 0.5, 0.5, 1)))
        else:
            moods = [r["mood"] for r in records]
            avg = sum(moods) / len(moods)
            title = Label(text="统计概览", font_size=dp(24), size_hint_y=None, height=dp(50), color=(1, 1, 1, 1))
            self.layout.add_widget(title)

            grid = GridLayout(cols=2, spacing=dp(12), size_hint_y=None, height=dp(160))
            grid.add_widget(self._stat_card("平均情绪", f"{avg:.1f}", "#6c8ce8"))
            grid.add_widget(self._stat_card("总记录数", str(len(records)), "#6c8ce8"))
            grid.add_widget(self._stat_card("最高", f"{max(moods)}/5", "#4ade80"))
            grid.add_widget(self._stat_card("最低", f"{min(moods)}/5", "#f87171"))
            self.layout.add_widget(grid)

            # 分布
            dist_title = Label(text="分布", font_size=dp(18), size_hint_y=None, height=dp(40), color=(1, 1, 1, 1))
            self.layout.add_widget(dist_title)

            for score in range(5, 0, -1):
                count = moods.count(score)
                _, emoji, label, color_hex = MOOD_MAP[score]
                bar = "█" * count + "░" * (max(count, 1))
                row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(36), spacing=dp(10))
                row.add_widget(Label(
                    text=f"{emoji} {score}/5",
                    font_size=dp(14),
                    size_hint_x=None,
                    width=dp(80),
                    color=(0.85, 0.85, 0.85, 1),
                ))
                row.add_widget(Label(
                    text=bar,
                    font_name="",
                    font_size=dp(14),
                    color=self._hex_to_rgba(color_hex),
                ))
                row.add_widget(Label(
                    text=str(count),
                    font_size=dp(14),
                    size_hint_x=None,
                    width=dp(40),
                    color=(0.55, 0.55, 0.55, 1),
                ))
                self.layout.add_widget(row)

        # 底部导航
        nav = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        btn_log = Button(text="📝 记录", font_size=dp(14), background_normal="", background_color=(0.15, 0.17, 0.21, 1))
        btn_log.bind(on_release=lambda x: setattr(self.manager, "current", "log"))
        btn_hist = Button(text="📊 历史", font_size=dp(14), background_normal="", background_color=(0.15, 0.17, 0.21, 1))
        btn_hist.bind(on_release=lambda x: setattr(self.manager, "current", "history"))
        nav.add_widget(btn_log)
        nav.add_widget(btn_hist)
        self.layout.add_widget(nav)

    def _stat_card(self, label_text, value_text, color_hex):
        card = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(4))
        with card.canvas.before:
            Color(*self._hex_to_rgba(color_hex, 0.15))
            card.bg = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=lambda inst, val: setattr(card.bg, "pos", val))
        card.bind(size=lambda inst, val: setattr(card.bg, "size", val))
        card.add_widget(Label(text=value_text, font_size=dp(28), color=(1, 1, 1, 1), size_hint_y=None, height=dp(40)))
        card.add_widget(Label(text=label_text, font_size=dp(13), color=(0.55, 0.55, 0.55, 1), size_hint_y=None, height=dp(24)))
        return card

    @staticmethod
    def _hex_to_rgba(hex_color, alpha=1.0):
        h = hex_color.lstrip("#")
        r = int(h[0:2], 16) / 255.0
        g = int(h[2:4], 16) / 255.0
        b = int(h[4:6], 16) / 255.0
        return (r, g, b, alpha)


class MoodTrackerApp(App):
    """MoodTracker 主应用。"""

    def build(self):
        self.title = "MoodTracker"
        sm = ScreenManager()
        sm.add_widget(LogScreen(name="log"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.add_widget(StatsScreen(name="stats"))
        return sm


if __name__ == "__main__":
    MoodTrackerApp().run()
