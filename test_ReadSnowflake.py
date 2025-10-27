import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

from ReadSnowflake import ReadSnowflake

@patch('ReadSnowflake.get_secret')
@patch('ReadSnowflake.Session')
def test_pandas_to_sf_overwrite(mock_session_class, mock_get_secret):
    # Mock secret manager
    mock_get_secret.return_value = b"-----BEGIN PRIVATE KEY-----\n...".decode()

    # Create dummy DataFrame
    df = pd.DataFrame({
        'col1': [1, 2],
        'TIMESTAMP': ['2023-10-01', '2023-10-01']
    })

    # Setup mock session and write_pandas
    mock_session = MagicMock()
    mock_session.write_pandas.return_value = "mock_write_result"
    mock_session.close = MagicMock()

    mock_builder = MagicMock()
    mock_builder.configs.return_value.create.return_value = mock_session
    mock_session_class.builder = mock_builder

    reader = ReadSnowflake()
    result = reader.pandas_to_sf(df.copy(), "TEST_TABLE", overwrite=True)

    mock_session.write_pandas.assert_called_once()
    mock_session.close.assert_called_once()

@patch('ReadSnowflake.get_secret')
@patch('ReadSnowflake.Session')
def test_pandas_to_sf_check_exists(mock_session_class, mock_get_secret):
    # Mock secret manager
    mock_get_secret.return_value = b"-----BEGIN PRIVATE KEY-----\n...".decode()

    # Create dummy DataFrame
    df = pd.DataFrame({
        'col1': [1],
        'TIMESTAMP': ['2023-10-01']
    })

    # Setup mock session and query response
    mock_session = MagicMock()
    mock_session.sql.return_value.to_pandas.return_value = pd.DataFrame({'ValueExists': [1]})
    mock_session.write_pandas = MagicMock()
    mock_session.close = MagicMock()

    mock_builder = MagicMock()
    mock_builder.configs.return_value.create.return_value = mock_session
    mock_session_class.builder = mock_builder

    reader = ReadSnowflake()

    # Expect ValueError when data already exists
    with pytest.raises(ValueError) as excinfo:
        reader.pandas_to_sf(df.copy(), "TEST_TABLE", overwrite=False)

    assert "already contains column TIMESTAMP with value 2023-10-01" in str(excinfo.value)

