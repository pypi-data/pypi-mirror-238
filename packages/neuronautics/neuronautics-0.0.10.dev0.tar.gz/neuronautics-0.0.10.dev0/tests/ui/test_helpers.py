import unittest
from unittest.mock import  MagicMock
from neuronautics.ui.helpers import clear_layout


class TestHelpers(unittest.TestCase):

    def test_clear_layout(self):
        # Create a mock QLayout and its associated widget
        layout_mock = MagicMock()
        widget_mock = MagicMock()
        layout_mock.__mock=[MagicMock(widget=widget_mock), MagicMock(widget=widget_mock)]
        layout_mock.count.side_effect = lambda: len(layout_mock.__mock)
        layout_mock.takeAt.side_effect = lambda i: layout_mock.__mock.pop(i)

        # Call the function with the mock layout
        clear_layout(layout_mock)

        # Verify that methods were called as expected
        layout_mock.takeAt.assert_called_with(0)
        for w in layout_mock.__mock:
            w.deleteLater.assert_called()


if __name__ == '__main__':
    unittest.main()
