"""
Example code showing use of UIGridLayout.
"""
import arcade
from arcade.gui import UIFlatButton 

from UIGridLayout import UIGridLayout


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 700, "Example", resizable=True)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        top_right_button = UIFlatButton(text="Test 1", width=100, height=50)
        top_middle_button = UIFlatButton(text="Test 2", width=75, height=35)
        top_left_button = UIFlatButton(text="Test 3", width=150, height=25)

        center_right_button = UIFlatButton(text="Test 4", width=150)
        center_middle_button= UIFlatButton(text="Test 5", height=120)
        center_left_button = UIFlatButton(text="Test 6", width=50)

        bottom_right_button = UIFlatButton(text="Test 7", height=150)
        bottom_middle_button = UIFlatButton(text="Test 8", height=150)
        bottom_left_button = UIFlatButton(text="Test 9", height=200)

        self.g_box = UIGridLayout(column_count=3, row_count=3, align_vertical="c", align_horizontal="c", horizontal_spacing=20, vertical_spacing=20)

        self.g_box.add_widget(top_right_button, 0, 0)
        self.g_box.add_widget(top_middle_button, 1, 0)
        self.g_box.add_widget(top_left_button, 2, 0)

        self.g_box.add_widget(center_right_button, 0, 1)
        self.g_box.add_widget(center_middle_button, 1, 1)
        self.g_box.add_widget(center_left_button, 2, 1)

        self.g_box.add_widget(bottom_right_button, 0, 2)
        self.g_box.add_widget(bottom_middle_button, 1, 2)
        self.g_box.add_widget(bottom_left_button, 1, 2)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=300,
                align_y=100,
                child=self.g_box)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()


if __name__ == '__main__':
    window = MyWindow()
    arcade.run()
