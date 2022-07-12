from unittest import TestCase

from Models.time_settings_model import TimeSettings


class TestTimeSettings(TestCase):
    def setUp(self):
        self.settings = TimeSettings()


    def test_get_temporal_position(self):
        self.settings.set_type(self.settings.possible_types[0])
        self.assertEqual(self.settings.get_temporal_position(0, 1, 0), 0)
        self.assertEqual(self.settings.get_temporal_position(0, 1, 1), 1)
        self.assertEqual(self.settings.get_temporal_position(0, 50, 50), 1)
        self.assertEqual(self.settings.get_temporal_position(0, 100, 50), 0.5)
        self.assertEqual(self.settings.get_temporal_position(50, 150, 150), 1)
        self.assertEqual(self.settings.get_temporal_position(100, 200, 150), 0.5)
        self.assertEqual(self.settings.get_temporal_position(0, 200, 150), 0.75)
