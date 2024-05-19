from pydantic_settings import BaseSettings


class AdminConf(BaseSettings):
    superuser: int
    bot_token: str

    class Config:
        env_file = '.env'


admin_conf = AdminConf()
