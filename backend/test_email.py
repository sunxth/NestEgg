"""
测试邮件推送功能
"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.services.email_service import send_email, send_weekly_report_email, markdown_to_html
from app.services.report import generate_weekly_report, format_report_markdown


async def test_basic_email():
    """测试基本邮件发送"""
    print("=" * 50)
    print("📧 测试基本邮件发送")
    print("=" * 50)

    # 测试邮件内容
    html_content = """
    <h2>📧 NestEgg 邮件测试</h2>
    <p>这是一封来自 NestEgg 的测试邮件。</p>
    <ul>
        <li>✅ 如果你收到这封邮件，说明配置成功</li>
        <li>📊 周报和月报将自动发送到此邮箱</li>
        <li>🔔 支持多个收件人</li>
    </ul>
    <hr>
    <p style="color: #666; font-size: 0.9em;">
        🤖 NestEgg 自动生成
    </p>
    """

    success = await send_email(
        to_emails=["429316335@qq.com"],
        subject="📧 NestEgg 邮件推送测试",
        content=html_content,
        content_type="html"
    )

    if success:
        print("✅ 测试邮件发送成功！请查收邮箱")
    else:
        print("❌ 测试邮件发送失败")

    return success


async def test_weekly_report_email():
    """测试周报邮件发送"""
    print("\n" + "=" * 50)
    print("📊 测试周报邮件发送")
    print("=" * 50)

    # 生成周报
    data = await generate_weekly_report()
    print(f"\n周报数据：")
    print(f"  时间段：{data['period']}")
    print(f"  收入：¥{data['income']:.2f}")
    print(f"  支出：¥{data['expense']:.2f}")
    print(f"  结余：¥{data['net']:.2f}")

    # 发送周报邮件
    print("\n正在发送周报邮件...")
    success = await send_weekly_report_email(["429316335@qq.com"])

    if success:
        print("✅ 周报邮件发送成功！请查收邮箱")
    else:
        print("❌ 周报邮件发送失败")

    return success


async def main():
    print("\n🎯 NestEgg 邮件推送功能测试\n")
    print("配置信息：")
    print(f"  SMTP 服务器：smtp.qq.com")
    print(f"  SMTP 端口：465")
    print(f"  发件人：429316335@qq.com")
    print(f"  收件人：429316335@qq.com")
    print()

    # 测试基本邮件发送
    await test_basic_email()

    # 等待2秒
    await asyncio.sleep(2)

    # 测试周报邮件发送
    await test_weekly_report_email()

    print("\n" + "=" * 50)
    print("✅ 测试完成！")
    print("=" * 50)
    print("\n下一步：")
    print("1. 在 backend/.env 中配置邮箱信息")
    print("2. 设置 ENABLE_EMAIL_REPORT=true 启用邮件推送")
    print("3. 重启后端服务即可自动推送\n")


if __name__ == "__main__":
    # 临时设置配置
    from app.config import settings
    settings.smtp_server = "smtp.qq.com"
    settings.smtp_port = 465
    settings.smtp_user = "429316335@qq.com"
    settings.smtp_password = "raadejyreifvcaef"
    settings.smtp_use_tls = True

    asyncio.run(main())
