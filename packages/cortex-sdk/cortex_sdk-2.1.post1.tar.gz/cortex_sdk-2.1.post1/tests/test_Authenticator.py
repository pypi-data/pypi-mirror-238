from cortex_sdk import Authenticator as auth
from cortex_sdk.types.CortexConfig import CortexConfig


default_test_dir = 'tests/fixtures'

nh_token = 'nhp_***'
nh_api_url = 'https://api.nearlyhuman.ai'
profile_name = 'default'
config = CortexConfig(default_user_path=default_test_dir)


def test_login():
    auth.Login(nh_token, nh_api_url, profile_name, cortex_config_loader=config)
    auth_url = auth.Get_Auth_URL(cortex_config_loader=config)
    token = auth.Get_Auth_Token(cortex_config_loader=config)

    assert auth.NH_API_URL(cortex_config_loader=config) == auth_url
    assert auth.NH_API_HEADERS(cortex_config_loader=config) == {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
        }

    assert auth.Check_Login_Status() == True


def test_fixtures_clean_up():
    config.delete_config()














