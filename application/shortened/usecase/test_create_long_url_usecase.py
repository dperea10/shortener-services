import application.shortened.usecase.create_long_url_usecase
from unittest.mock import patch
from datetime import datetime
from application.shortened.usecase.delete_short_url_usecase import create_short_url_use, redis_adapter, long_url_adapter, short_url_adapter, user_adapter, settings
from infra.handlers.dtos import ShortenedUrlRequestDTO, ResponseDTO
from infra.adapters.redis.models.redis_model import DataShortenedUrlRedis
import unittest

class TestCreateShortUrlUse(unittest.TestCase):

    @patch('your_module.decode_token_base')
    def test_success(self, mock_decode_token_base):
        # Arrange
        mock_decode_token_base.return_value = 'token'
        mock_get_user_by_username = patch('your_module.user_adapter.get_user_by_username')
        mock_get_user_by_username.return_value = {'id': 123, 'username': 'user'}
        mock_get_redis = patch.object(redis_adapter, 'get_redis')
        mock_get_redis.return_value = None
        mock_register_long_url_adapter = patch.object(long_url_adapter, 'register_long_url_adapter')
        mock_register_long_url_adapter.return_value = {'id': 456, 'long_url': 'https://example.com'}
        mock_register_shortened_url_adapter = patch.object(short_url_adapter, 'register_shortened_url_adapter')
        mock_register_shortened_url_adapter.return_value = {'id': 789, 'hash_url': 'ABCD'}
        data_long_url = ShortenedUrlRequestDTO(long_url='https://example.com')
        
    # Act
    result = create_short_url_use(data_long_url=data_long_url, token=token)

    # Assert
    mock_decode_token_base.assert_called_once_with(token)
    if user_token is None:
        mock_response.assert_called_once_with(status="Error", message="Unauthorized")
    elif user_model is None:
        mock_response.assert_called_once_with(status="Error", message="UserNotfound")
    elif result_redis is not None:
        short_url_string = settings.base_url_service + result_redis.hash_url
        mock_response.assert_called_once_with(status="Ok", message="RegisterFound", data={"short_url": short_url_string, "hash_url": result_redis.hash_url})
    else:
        hash_url = str(uuid.uuid4())[:5].upper()
        mock_save_short_url_redis.assert_called_once_with(hash_url, data_long_url)
        mock_long_url_adapter.assert_called_once_with(long_url_document)
        mock_short_url_adapter.assert_called_once_with(short_url_document)
        short_url_string = settings.base_url_service + hash_url
        mock_response.assert_called_once_with(status="Ok", message="Success", data={"short_url": short_url_string, "hash_url": hash_url})
        mock_register_long_url_adapter.assert_called_once_with(long_url_document)
        mock_register_shortened_url_adapter.assert_called_once_with(short_url_document)

    @patch('your_module.decode_token_base')
    @patch('your_module.user_adapter.get_user_by_username')
    @patch('your_module.redis_adapter.get_redis')
    @patch('your_module.send_to_redis_cache')
    @patch('your_module.short_url_adapter.register_shortened_url_adapter')
    @patch('your_module.long_url_adapter.register_long_url_adapter')
    def test_success_register_found(self, mock_register_long_url_adapter, mock_register_shortened_url_adapter, mock_send_to_redis_cache, mock_get_redis, mock_get_user_by_username, mock_decode_token_base):
      # Arrange
      data_long_url = 'https://www.example.com/test'
      token = 'abc123'
      user_token = {'username': 'test'}
      user_model = UserModel(id=1, username='test', password_hash='password')
      data_long_url_struct = ShortenedUrlRequestDTO(short_url='', long_url=data_long_url, hash_url='')
      result_redis = ShortenedUrlModel(hash_url='ABC12', long_url_id=1)
      mock_decode_token_base.return_value = user_token
      mock_get_user_by_username.return_value = user_model
      mock_get_redis.return_value = result_redis
      mock_response = MagicMock()
      mock_response.return_value = ResponseDTO(status="Ok", message="RegisterFound", data={"short_url": settings.base_url_service + result_redis.hash_url, "hash_url": result_redis.hash_url})
      mock_save_short_url_redis = MagicMock()
      mock_long_url_adapter = MagicMock()
      mock_short_url_adapter = MagicMock()
      mock_register_shortened_url_adapter.return_value = ShortenedUrlModel(user_id=1, long_url_id=1, hash_url='ABC12')
      mock_register_long_url_adapter.return_value = LongUrlModel(id=1, user_id=1, long_url=data_long_url)
      
      # Act
      result = create_short_url_use(data_long_url=data_long_url, token=token)

      # Assert
      mock_decode_token_base.assert_called_once_with(token)
      mock_get_user_by_username.assert_called_once_with(user_token)
      mock_get_redis.assert_called_once_with(data_long_url_struct)
      short_url_string = settings.base_url_service + result_redis.hash_url
      mock_response.assert_called_once_with(status="Ok", message="RegisterFound", data={"short_url": short_url_string, "hash_url": result_redis.hash_url})

@patch('your_module.short_url_adapter.register_shortened_url_adapter')
@patch('your_module.long_url_adapter.register_long_url_adapter')
def test_register_shortened_url_adapter_error(self, mock_register_long_url_adapter, mock_register_shortened_url_adapter, mock_get_user_by_username, mock_get_redis):
    # Arrange
    mock_get_user_by_username.return_value = {'id': 123, 'username': 'testuser'}
    mock_get_redis.return_value = None
    mock_register_long_url_adapter.return_value = LongUrlModel(id=1, user_id=123, long_url="https://www.example.com")
    mock_register_shortened_url_adapter.return_value = None
    request_data = ShortenedUrlRequestDTO(long_url="https://www.example.com")
    token = 'valid_token'

    # Act
    response = create_short_url_use(request_data, token)

    # Assert
    mock_get_user_by_username.assert_called_once_with(token)
    mock_get_redis.assert_called_once_with(request_data)
    mock_register_long_url_adapter.assert_called_once()
    mock_register_shortened_url_adapter.assert_called_once()
    expected_response = ResponseDTO(status="Error", message="UnexpectedError")
    self.assertEqual(response, expected_response)

# Test case for unexpected error when registering long URL
@patch('your_module.short_url_adapter.register_shortened_url_adapter')
@patch('your_module.long_url_adapter.register_long_url_adapter')
def test_register_long_url_adapter_error(self, mock_register_long_url_adapter, mock_register_shortened_url_adapter, mock_get_user_by_username, mock_get_redis):
    # Arrange
    mock_get_user_by_username.return_value = {'id': 123, 'username': 'testuser'}
    mock_get_redis.return_value = None
    mock_register_long_url_adapter.return_value = None
    request_data = ShortenedUrlRequestDTO(long_url="https://www.example.com")
    token = 'valid_token'

    # Act
    response = create_short_url_use(request_data, token)

    # Assert
    mock_get_user_by_username.assert_called_once_with(token)
    mock_get_redis.assert_called_once_with(request_data)
    mock_register_long_url_adapter.assert_called_once()
    mock_register_shortened_url_adapter.assert_not_called()
    expected_response = ResponseDTO(status="Error", message="UnexpectedError")
    self.assertEqual(response, expected_response)

# Test case for when the short URL is not found in the database
@patch('your_module.short_url_adapter.get_short_url_by_long_url_id_adapter')
@patch('your_module.long_url_adapter.get_long_url_by_long_url_adapter')
# def test_short_url_not_found(self, mock_get_long_url_by_long_url_adapter, mock_get_short_url_by_long_url_id_adapter, mock_get_user_by_username, mock_get_redis):
#     # Arrange
#     mock_get_user_by_username.return_value = {'id': 123, 'username': 'testuser'}
#     mock_get_redis.return_value = None
#     mock_get_long_url_by_long_url_adapter.return_value = LongUrlModel(id=1, user_id=123, long_url="https://www.example.com")
#     mock_get_short_url_by_long_url_id_adapter.return_value = None
#     request_data = ShortenedUrlRequestDTO(long_url="https://www.example.com")
#     token = 'valid_token'

#     # Act
#     response = create_short_url_use(request_data, token)

#     # Assert
#     mock_get_user_by_username.assert_called_once_with(token)
#     mock_get_redis.assert_called_once_with(request_data)
#     mock_get_long_url_by_long_url_adapter.assert_called_once()
#     mock_get_short_url_by_long_url_id_adapter.assert_called_once()
#     expected_response = Response
