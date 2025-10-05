"""
测试微信推送功能
使用方法：
1. 替换 YOUR_SENDKEY 为你的 Server酱 SendKey
2. 运行：python test_wechat_push.py
"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.services.report import (
    generate_weekly_report,
    generate_monthly_report,
    format_report_markdown,
    send_to_serverchan
)


async def test_weekly_report():
    """测试周报生成和推送"""
    print("=" * 50)
    print("📊 测试周报生成")
    print("=" * 50)

    # 生成周报数据
    data = await generate_weekly_report()
    print("\n周报数据：")
    print(f"  时间段：{data['period']}")
    print(f"  收入：¥{data['income']:.2f}")
    print(f"  支出：¥{data['expense']:.2f}")
    print(f"  结余：¥{data['net']:.2f}")
    print(f"  交易笔数：{data['transaction_count']}笔")

    # 格式化为 Markdown
    content = format_report_markdown(data, "weekly")
    print("\n" + "=" * 50)
    print("📄 周报 Markdown 预览")
    print("=" * 50)
    print(content)

    # 推送测试
    send_key = input("\n请输入你的 Server酱 SendKey (直接回车跳过推送测试)：").strip()
    if send_key:
        print("\n正在发送...")
        success = await send_to_serverchan(
            title=f"📊 NestEgg 周报 - {data['period']}",
            content=content,
            send_key=send_key
        )
        if success:
            print("✅ 推送成功！请查看微信消息")
        else:
            print("❌ 推送失败，请检查 SendKey 是否正确")


async def test_monthly_report():
    """测试月报生成和推送"""
    print("\n\n" + "=" * 50)
    print("📊 测试月报生成")
    print("=" * 50)

    # 生成月报数据
    data = await generate_monthly_report()
    print("\n月报数据：")
    print(f"  时间段：{data['period']}")
    print(f"  收入：¥{data['income']:.2f}")
    print(f"  支出：¥{data['expense']:.2f}")
    print(f"  结余：¥{data['net']:.2f}")
    print(f"  交易笔数：{data['transaction_count']}笔")
    print(f"  日均支出：¥{data['daily_avg']:.2f}")

    # 格式化为 Markdown
    content = format_report_markdown(data, "monthly")
    print("\n" + "=" * 50)
    print("📄 月报 Markdown 预览")
    print("=" * 50)
    print(content)

    # 推送测试
    send_key = input("\n请输入你的 Server酱 SendKey (直接回车跳过推送测试)：").strip()
    if send_key:
        print("\n正在发送...")
        success = await send_to_serverchan(
            title=f"📊 NestEgg 月报 - {data['period']}",
            content=content,
            send_key=send_key
        )
        if success:
            print("✅ 推送成功！请查看微信消息")
        else:
            print("❌ 推送失败，请检查 SendKey 是否正确")


async def main():
    print("\n🎯 NestEgg 微信推送功能测试\n")

    # 测试周报
    await test_weekly_report()

    # 测试月报
    await test_monthly_report()

    print("\n" + "=" * 50)
    print("✅ 测试完成！")
    print("=" * 50)
    print("\n下一步：")
    print("1. 访问 https://sct.ftqq.com/ 获取 SendKey")
    print("2. 在 backend/.env 中配置 SERVERCHAN_KEYS")
    print("3. 设置 ENABLE_WEEKLY_REPORT=true 启用周报")
    print("4. 设置 ENABLE_MONTHLY_REPORT=true 启用月报")
    print("5. 重启后端服务即可自动推送\n")


if __name__ == "__main__":
    asyncio.run(main())
