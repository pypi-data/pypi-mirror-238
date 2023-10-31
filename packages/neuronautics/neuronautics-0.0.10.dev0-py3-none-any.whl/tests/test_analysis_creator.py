import unittest
from unittest.mock import mock_open, patch
from neuronautics.analysis.analysis_creator import AnalysisCreator


class TestAnalysisCreator(unittest.TestCase):
    def test_create(self):
        # Define test input data
        name = "Test Analysis"
        type = "graph"

        # Mock the behavior of open() to return a predefined template
        with (patch("builtins.open", mock_open(read_data="template content")) as mock_file_open,
              patch("neuronautics.analysis.analysis_creator.AnalysisCreator.save") as spy_save,
              patch("neuronautics.analysis.analysis_creator.file_path") as spy_file_path
              ):
            spy_file_path.side_effect = lambda x: f'/home/mock/{x}'
            # Call the create method
            result = AnalysisCreator.create(name, type)

        # Assert that the file was written with the correct content
        mock_file_open.assert_called_with("/home/mock/analysis/custom/scripts/graph/test_analysis.py", "w")
        mock_file_open.return_value.write.assert_called_once_with("template content")

        spy_save.assert_called_once()
        # Assert that the result is the expected path
        self.assertEqual(result, "/home/mock/analysis/custom/scripts/graph/test_analysis.py")

    def test_save(self):
        # Define test input data
        name = "Test Analysis"
        path = "path/to/your/generated/analysis/graph_test_analysis.py"
        module = "graph_test_analysis"
        class_name = "GraphTestAnalysis"

        # Mock the Loader.save method to ensure it's called with the correct arguments
        with patch("neuronautics.analysis.analysis_creator.Loader.save") as mock_loader_save:
            AnalysisCreator.save(name, path, module, class_name)

        # Assert that Loader.save was called with the correct arguments
        mock_loader_save.assert_called_once_with({
            'name': name,
            'module': module,
            'path': path,
            'class': class_name
        })


if __name__ == '__main__':
    unittest.main()
