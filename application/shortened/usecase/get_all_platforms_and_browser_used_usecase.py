from infra.adapters.shortened.access_count_adapter import AccessCountAdapter
from infra.handlers.dtos.response import ResponseDTO
from infra.adapters.shortened.user_adapter import UserAdapter
from infra.utils.functions import decode_token_base

access_count_adapter = AccessCountAdapter()
user_adapter = UserAdapter()

def get_all_platforms_and_browser_used_use(token: str) -> ResponseDTO:
    user_token = decode_token_base(token)
    if user_token is None:
       response = ResponseDTO(status="Error", message="Unauthorized")       
       return response

    user_model = user_adapter.get_user_by_username(user_token)
    if user_model is None:
       response = ResponseDTO(status="Error", message="UserNotfound")       
       return response

    access_urls = access_count_adapter.get_all_platform_and_browsers_adapter()

    if access_urls is not None:
      response = ResponseDTO(status="Ok", message="Success", data={"access_urls":access_urls})
      return response

    response = ResponseDTO(status="Ok", message="NotFound")
    return response
