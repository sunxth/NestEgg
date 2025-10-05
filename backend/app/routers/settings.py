from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from ..auth import require_admin
from ..models import TokenData
from ..config import settings
import os
from pathlib import Path

router = APIRouter(prefix="/api/settings", tags=["settings"])


class NotificationSettings(BaseModel):
    # Server酱配置
    serverchan_keys: Optional[str] = None
    enable_weekly_report: bool = False
    enable_monthly_report: bool = False
    weekly_report_time: str = "09:00"
    monthly_report_time: str = "09:00"

    # 邮件配置
    smtp_server: Optional[str] = None
    smtp_port: int = 465
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: bool = True
    email_recipients: Optional[str] = None
    enable_email_report: bool = False
    enable_transaction_notification: bool = False


@router.get("/notifications", response_model=NotificationSettings)
async def get_notification_settings(
    current_user: TokenData = Depends(require_admin)
):
    """获取当前通知配置"""
    return NotificationSettings(
        serverchan_keys=settings.serverchan_keys,
        enable_weekly_report=settings.enable_weekly_report,
        enable_monthly_report=settings.enable_monthly_report,
        weekly_report_time=settings.weekly_report_time,
        monthly_report_time=settings.monthly_report_time,
        smtp_server=settings.smtp_server,
        smtp_port=settings.smtp_port,
        smtp_user=settings.smtp_user,
        smtp_password=settings.smtp_password if settings.smtp_password else None,
        smtp_use_tls=settings.smtp_use_tls,
        email_recipients=settings.email_recipients,
        enable_email_report=settings.enable_email_report,
        enable_transaction_notification=settings.enable_transaction_notification,
    )


@router.put("/notifications")
async def update_notification_settings(
    notification_settings: NotificationSettings,
    current_user: TokenData = Depends(require_admin)
):
    """更新通知配置并保存到 .env 文件"""
    try:
        # 读取当前 .env 文件
        env_path = Path(__file__).parent.parent.parent / ".env"

        if not env_path.exists():
            # 如果 .env 不存在，从 .env.example 复制
            example_path = env_path.parent / ".env.example"
            if example_path.exists():
                with open(example_path, 'r', encoding='utf-8') as f:
                    env_content = f.read()
            else:
                env_content = ""
        else:
            with open(env_path, 'r', encoding='utf-8') as f:
                env_content = f.read()

        # 更新配置项
        config_map = {
            'SERVERCHAN_KEYS': notification_settings.serverchan_keys or '',
            'ENABLE_WEEKLY_REPORT': str(notification_settings.enable_weekly_report).lower(),
            'ENABLE_MONTHLY_REPORT': str(notification_settings.enable_monthly_report).lower(),
            'WEEKLY_REPORT_TIME': notification_settings.weekly_report_time,
            'MONTHLY_REPORT_TIME': notification_settings.monthly_report_time,
            'SMTP_SERVER': notification_settings.smtp_server or '',
            'SMTP_PORT': str(notification_settings.smtp_port),
            'SMTP_USER': notification_settings.smtp_user or '',
            'SMTP_PASSWORD': notification_settings.smtp_password or '',
            'SMTP_USE_TLS': str(notification_settings.smtp_use_tls).lower(),
            'EMAIL_RECIPIENTS': notification_settings.email_recipients or '',
            'ENABLE_EMAIL_REPORT': str(notification_settings.enable_email_report).lower(),
            'ENABLE_TRANSACTION_NOTIFICATION': str(notification_settings.enable_transaction_notification).lower(),
        }

        # 解析现有内容
        lines = env_content.split('\n')
        updated_keys = set()

        for i, line in enumerate(lines):
            line_stripped = line.strip()
            # 跳过注释和空行
            if not line_stripped or line_stripped.startswith('#'):
                continue

            # 查找配置项
            if '=' in line:
                key = line.split('=')[0].strip()
                if key in config_map:
                    lines[i] = f"{key}={config_map[key]}"
                    updated_keys.add(key)

        # 添加缺失的配置项
        for key, value in config_map.items():
            if key not in updated_keys:
                lines.append(f"{key}={value}")

        # 写回文件
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        # 更新运行时配置（需要重启才能完全生效）
        settings.serverchan_keys = notification_settings.serverchan_keys or ''
        settings.enable_weekly_report = notification_settings.enable_weekly_report
        settings.enable_monthly_report = notification_settings.enable_monthly_report
        settings.weekly_report_time = notification_settings.weekly_report_time
        settings.monthly_report_time = notification_settings.monthly_report_time
        settings.smtp_server = notification_settings.smtp_server or ''
        settings.smtp_port = notification_settings.smtp_port
        settings.smtp_user = notification_settings.smtp_user or ''
        settings.smtp_password = notification_settings.smtp_password or ''
        settings.smtp_use_tls = notification_settings.smtp_use_tls
        settings.email_recipients = notification_settings.email_recipients or ''
        settings.enable_email_report = notification_settings.enable_email_report
        settings.enable_transaction_notification = notification_settings.enable_transaction_notification

        return {
            "message": "通知配置已更新。部分配置可能需要重启服务才能生效。",
            "requires_restart": True
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新配置失败: {str(e)}")
