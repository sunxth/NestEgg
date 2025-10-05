"""
快速发送测试邮件
"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.services.email_service import send_email, send_weekly_report_email


async def main():
    # 配置
    from app.config import settings
    settings.smtp_server = "smtp.qq.com"
    settings.smtp_port = 465
    settings.smtp_user = "429316335@qq.com"
    settings.smtp_password = "raadejyreifvcaef"
    settings.smtp_use_tls = True

    print("📧 正在发送测试邮件到 3407028118@qq.com...")
    print()

    # 发送基本测试邮件
    html_content = """
    <h2>📧 NestEgg 邮件推送测试</h2>
    <p>你好！这是一封来自 NestEgg 家庭记账系统的测试邮件。</p>

    <h3>💡 功能说明</h3>
    <ul style="line-height: 1.8;">
        <li>✅ 自动生成周报/月报</li>
        <li>📊 详细收支统计分析</li>
        <li>📈 支出分类排名</li>
        <li>🔔 定时推送到邮箱</li>
    </ul>

    <h3>📮 推送设置</h3>
    <p>如果你收到这封邮件，说明邮箱配置已成功！</p>
    <p>系统将在以下时间自动推送：</p>
    <ul style="line-height: 1.8;">
        <li>📅 每周一 09:00 - 周报</li>
        <li>📅 每月1号 09:00 - 月报</li>
    </ul>

    <hr style="margin: 20px 0; border: none; border-top: 1px solid #e5e7eb;">
    <p style="color: #666; font-size: 0.9em; text-align: center;">
        🤖 此邮件由 NestEgg 自动发送，请勿回复<br>
        生成时间: 2025-10-05
    </p>
    """

    success1 = await send_email(
        to_emails=["3407028118@qq.com"],
        subject="📧 NestEgg 邮件推送测试",
        content=html_content,
        content_type="html"
    )

    if success1:
        print("✅ 测试邮件发送成功！")
    else:
        print("❌ 测试邮件发送失败")

    # 等待2秒
    await asyncio.sleep(2)

    # 发送周报
    print("\n📊 正在发送周报邮件...")
    success2 = await send_weekly_report_email(["3407028118@qq.com"])

    if success2:
        print("✅ 周报邮件发送成功！")
    else:
        print("❌ 周报邮件发送失败")

    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 所有邮件发送成功！请查收 3407028118@qq.com 邮箱")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
