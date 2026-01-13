import pytest
import os
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
from scripts.notifier import DownstreamNotifier

@pytest.fixture
def notifier():
    # Mocking Gemini client to avoid API calls during tests
    with patch('scripts.notifier.genai') as mock_genai:
        n = DownstreamNotifier(api_key="fake_key")
        n.client = MagicMock()
        return n

def test_git_check_availability(notifier):
    """Test the git availability check."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        assert notifier.check_git_available() is True
        
        mock_run.side_effect = FileNotFoundError
        assert notifier.check_git_available() is False

def test_read_providers(notifier, tmp_path):
    """Test reading providers from a mock JSON file."""
    import json
    registry_path = tmp_path / "test_providers.json"
    data = [
        {"id": "P001", "name": "Test Provider", "email": "test@example.com"}
    ]
    with open(registry_path, 'w') as f:
        json.dump(data, f)
    
    providers = notifier.read_providers(str(registry_path))
    assert len(providers) == 1
    assert providers[0]['id'] == 'P001'
    assert providers[0]['name'] == 'Test Provider'

def test_update_excel_mock(notifier, tmp_path):
    """Test Excel editing with mocked openpyxl."""
    with patch('openpyxl.load_workbook') as mock_load:
        mock_wb = MagicMock()
        mock_sheet = MagicMock()
        mock_load.return_value = mock_wb
        mock_wb.__getitem__.return_value = mock_sheet
        
        # Mock finding the row
        mock_cell = MagicMock()
        mock_cell.value = "Planned System Changes"
        mock_sheet.iter_rows.return_value = [[mock_cell]]
        
        success = notifier.update_article_13_excel("template.xlsx", "output.xlsx", "summary")
        assert success is True
        mock_wb.save.assert_called_once_with("output.xlsx")

def test_process_notification_flow(notifier, tmp_path):
    """Test the full notification flow with mocked components."""
    # Setup mock registry
    registry_path = tmp_path / "registry.json"
    with open(registry_path, 'w') as f:
        json.dump([{'id': 'P-001', 'name': 'User'}], f)
    
    template_path = tmp_path / "article_13.xlsx" # Doesn't need to exist if we mock update
    
    # Mock methods
    notifier.get_git_diff = MagicMock(return_value="fake diff")
    notifier.summarize_changes = MagicMock(return_value="Simulated summary")
    notifier.update_article_13_excel = MagicMock(return_value=True)
    notifier.run_md_to_pdf = MagicMock(return_value=True)
    
    with patch('pathlib.Path.mkdir'):
        with patch('pathlib.Path.write_text'):
            success = notifier.process_notification(
                registry_path=str(registry_path),
                template_path=template_path
            )
            assert success is True

if __name__ == "__main__":
    pytest.main([__file__])
