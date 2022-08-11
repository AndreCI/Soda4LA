from unittest import TestCase

from Utils.filter_module import FilterModule


class TestFilterModule(TestCase):
    def setUp(self):
        self.module = FilterModule()
        self.range_value = "[3, 10]"
        self.multiple_value = "3;5;10"

    def test_evaluate(self):
        self.module.assign("3")
        self.assertEqual(self.module.evaluate(3), True)
        self.assertEqual(self.module.evaluate(6), False)

        self.module.assign(self.range_value)
        self.assertEqual(self.module.evaluate(4), True)
        self.assertEqual(self.module.evaluate(2), False)

        self.module.assign(self.multiple_value)
        self.assertEqual(self.module.evaluate(5), True)
        self.assertEqual(self.module.evaluate(6), False)

    def test_assign(self):
        self.assertEqual(self.module.assign("3"), True)
        self.assertEqual(self.module.mode, "Single")

        self.assertEqual(self.module.assign(self.range_value), True)
        self.assertEqual(self.module.mode, "Range")

        self.assertEqual(self.module.assign(self.multiple_value), True)
        self.assertEqual(self.module.mode, "Multiple")