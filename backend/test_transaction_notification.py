"""
测试交易通知功能
"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.services.notification import notify_transaction_created


async def main():
    # 临时配置
    from app.config import settings
    settings.smtp_server = "smtp.qq.com"
    settings.smtp_port = 465
    settings.smtp_user = "429316335@qq.com"
    settings.smtp_password = "raadejyreifvcaef"
    settings.smtp_use_tls = True
    settings.email_recipients = "429316335@qq.com,3407028118@qq.com"
    settings.serverchan_keys = "SCT235597TTHluFJ9SPSgy1ekeJZzKjDwj"
    settings.enable_transaction_notification = True

    print("🎯 测试交易通知功能\n")
    print("=" * 50)

    # 测试支出通知
    print("📤 测试1：支出通知")
    print("=" * 50)
    expense_data = {
        'id': 1,
        'date': '2025-10-05',
        'amount': '128.50',
        'type': 'expense',
        'category': 'food',
        'description': '午餐 - 海底捞火锅'
    }

    print(f"\n交易信息：")
    print(f"  类型：支出")
    print(f"  金额：¥{expense_data['amount']}")
    print(f"  分类：餐饮")
    print(f"  备注：{expense_data['description']}")
    print(f"\n正在发送通知...")

    await notify_transaction_created(expense_data)
    print("✅ 支出通知已发送！\n")

    # 等待2秒
    await asyncio.sleep(2)

    # 测试收入通知
    print("\n" + "=" * 50)
    print("📥 测试2：收入通知")
    print("=" * 50)
    income_data = {
        'id': 2,
        'date': '2025-10-05',
        'amount': '5000.00',
        'type': 'income',
        'category': 'salary',
        'description': '10月工资'
    }

    print(f"\n交易信息：")
    print(f"  类型：收入")
    print(f"  金额：¥{income_data['amount']}")
    print(f"  分类：工资")
    print(f"  备注：{income_data['description']}")
    print(f"\n正在发送通知...")

    await notify_transaction_created(income_data)
    print("✅ 收入通知已发送！\n")

    print("=" * 50)
    print("🎉 测试完成！")
    print("=" * 50)
    print("\n请查收：")
    print("  📧 邮箱：429316335@qq.com, 3407028118@qq.com")
    print("  📱 微信：Server酱推送")
    print("\n共发送：4封邮件 + 2条微信消息\n")


if __name__ == "__main__":
    asyncio.run(main())
