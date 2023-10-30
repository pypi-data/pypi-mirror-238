from axsqlalchemy.settings import Settings as DBSettings
from axdocsystem.utils.settings import (
    AuthRouteSettings as AuthSettings,
    LimitationSettings as LimitSettings,
    ConfigurationSettings,
)


class Settings(DBSettings, ConfigurationSettings, AuthSettings, LimitSettings):
    class Config:
        env_file = '.env'


