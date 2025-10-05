"""
报表推送 API
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth import require_admin
from app.services.report import (
    generate_weekly_report,
    generate_monthly_report,
    send_weekly_report_to_wechat,
    send_monthly_report_to_wechat,
    format_report_markdown
)
from app.config import get_settings


router = APIRouter(prefix="/api/reports", tags=["reports"])
settings = get_settings()


class TestPushRequest(BaseModel):
    send_keys: list[str]
    report_type: str  # "weekly" 或 "monthly"


@router.get("/weekly")
async def get_weekly_report(current_user: dict = Depends(require_admin)):
    """获取周报数据（管理员）"""
    data = await generate_weekly_report()
    return data


@router.get("/monthly")
async def get_monthly_report(current_user: dict = Depends(require_admin)):
    """获取月报数据（管理员）"""
    data = await generate_monthly_report()
    return data


@router.post("/test-push")
async def test_push_report(
    request: TestPushRequest,
    current_user: dict = Depends(require_admin)
):
    """
    测试推送报表到微信（管理员）

    Args:
        send_keys: Server酱 SendKey 列表
        report_type: 报表类型 ("weekly" 或 "monthly")
    """
    if not request.send_keys:
        raise HTTPException(status_code=400, detail="请提供至少一个 SendKey")

    if request.report_type == "weekly":
        success = await send_weekly_report_to_wechat(request.send_keys)
        return {
            "success": success,
            "message": "周报推送成功" if success else "部分推送失败"
        }
    elif request.report_type == "monthly":
        success = await send_monthly_report_to_wechat(request.send_keys)
        return {
            "success": success,
            "message": "月报推送成功" if success else "部分推送失败"
        }
    else:
        raise HTTPException(status_code=400, detail="无效的报表类型")


@router.get("/preview/{report_type}")
async def preview_report(
    report_type: str,
    current_user: dict = Depends(require_admin)
):
    """
    预览报表内容（管理员）

    Args:
        report_type: 报表类型 ("weekly" 或 "monthly")
    """
    if report_type == "weekly":
        data = await generate_weekly_report()
        content = format_report_markdown(data, "weekly")
    elif report_type == "monthly":
        data = await generate_monthly_report()
        content = format_report_markdown(data, "monthly")
    else:
        raise HTTPException(status_code=400, detail="无效的报表类型")

    return {
        "data": data,
        "markdown": content
    }
