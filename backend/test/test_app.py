from unittest.mock import MagicMock, patch
import pytest
from app import app, ensure_users_table

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.get_db_connection')
def test_get_users(mock_get_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'Alice'}]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db.return_value = mock_conn

    response = client.get('/api/users')
    assert response.status_code == 200
    assert response.json == [{'id': 1, 'name': 'Alice'}]

@patch('app.get_db_connection')
def test_ensure_users_table_exists(mock_get_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db.return_value = mock_conn

    ensure_users_table()

    assert any(
        call_args[0][0].startswith('CREATE TABLE IF NOT EXISTS users')
        for call_args in mock_cursor.execute.call_args_list
    )
