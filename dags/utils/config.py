from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    airflow_uid :int
    airflow_gid :int
    is_prod: bool

    model_config = SettingsConfigDict(env_file=('.env.dev','.env'), env_file_encoding='utf-8')

settings = Settings()