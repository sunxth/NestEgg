from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "sqlite:///./nestegg.db"
    secret_key: str = "your-secret-key-here"
    admin_password: str = "admin123"
    user_password: str = "user123"
    access_token_expire_minutes: int = 10080
    algorithm: str = "HS256"

    # Server酱推送配置
    serverchan_keys: str = ""  # 多个 key 用逗号分隔，如: "KEY1,KEY2"
    enable_weekly_report: bool = False  # 是否启用周报
    enable_monthly_report: bool = False  # 是否启用月报
    weekly_report_time: str = "09:00"  # 周报发送时间（每周一）
    monthly_report_time: str = "09:00"  # 月报发送时间（每月1号）

    # 邮箱推送配置
    smtp_server: str = ""  # SMTP 服务器地址
    smtp_port: int = 465  # SMTP 端口（QQ邮箱使用465）
    smtp_user: str = ""  # 发件邮箱地址
    smtp_password: str = ""  # SMTP 授权码（不是邮箱密码！）
    smtp_use_tls: bool = True  # 是否使用 TLS/SSL
    email_recipients: str = ""  # 收件人列表（多个邮箱用逗号分隔）
    enable_email_report: bool = False  # 是否启用邮件推送（周报/月报）
    enable_transaction_notification: bool = False  # 是否启用交易通知

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()