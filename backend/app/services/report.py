"""
报表生成和推送服务
"""
import httpx
from datetime import datetime, timedelta
from sqlmodel import Session, select, func
from app.models import Transaction, TransactionType
from app.database import engine
from app.config import settings


async def generate_weekly_report() -> dict:
    """生成周报数据"""
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # 本周一
    week_end = today

    with Session(engine) as session:
        # 查询本周交易
        statement = select(Transaction).where(
            Transaction.date >= week_start,
            Transaction.date <= week_end
        )
        transactions = session.exec(statement).all()

        # 统计数据
        total_income = sum(float(t.amount) for t in transactions if t.type == TransactionType.INCOME)
        total_expense = sum(float(t.amount) for t in transactions if t.type == TransactionType.EXPENSE)
        net = total_income - total_expense

        # 按分类统计支出
        expense_by_category = {}
        for t in transactions:
            if t.type == TransactionType.EXPENSE:
                category = t.category
                expense_by_category[category] = expense_by_category.get(category, 0) + float(t.amount)

        # 排序分类支出
        top_categories = sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "period": f"{week_start.strftime('%m月%d日')} - {week_end.strftime('%m月%d日')}",
            "income": total_income,
            "expense": total_expense,
            "net": net,
            "transaction_count": len(transactions),
            "top_categories": top_categories
        }


async def generate_monthly_report() -> dict:
    """生成月报数据"""
    today = datetime.now().date()
    month_start = today.replace(day=1)

    with Session(engine) as session:
        # 查询本月交易
        statement = select(Transaction).where(
            Transaction.date >= month_start,
            Transaction.date <= today
        )
        transactions = session.exec(statement).all()

        # 统计数据
        total_income = sum(float(t.amount) for t in transactions if t.type == TransactionType.INCOME)
        total_expense = sum(float(t.amount) for t in transactions if t.type == TransactionType.EXPENSE)
        net = total_income - total_expense

        # 按分类统计支出
        expense_by_category = {}
        for t in transactions:
            if t.type == TransactionType.EXPENSE:
                category = t.category
                expense_by_category[category] = expense_by_category.get(category, 0) + float(t.amount)

        # 排序分类支出
        top_categories = sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)[:5]

        # 日均支出
        days_passed = (today - month_start).days + 1
        daily_avg = total_expense / days_passed if days_passed > 0 else 0

        return {
            "period": f"{today.year}年{today.month}月",
            "income": total_income,
            "expense": total_expense,
            "net": net,
            "transaction_count": len(transactions),
            "daily_avg": daily_avg,
            "top_categories": top_categories
        }


def format_report_markdown(data: dict, report_type: str = "weekly") -> str:
    """格式化报表为 Markdown"""
    category_labels = {
        "food": "餐饮",
        "transport": "交通",
        "shopping": "购物",
        "utilities": "水电",
        "entertainment": "娱乐",
        "medical": "医疗",
        "education": "教育",
        "salary": "工资",
        "bonus": "奖金",
        "other": "其他"
    }

    title = f"📊 {'周报' if report_type == 'weekly' else '月报'} - {data['period']}"

    content = f"""## {title}

### 💰 收支概览
- **收入**：¥{data['income']:.2f}
- **支出**：¥{data['expense']:.2f}
- **结余**：{'🟢' if data['net'] >= 0 else '🔴'} ¥{data['net']:.2f}
- **交易笔数**：{data['transaction_count']}笔
"""

    if report_type == "monthly" and "daily_avg" in data:
        content += f"- **日均支出**：¥{data['daily_avg']:.2f}\n"

    if data['top_categories']:
        content += "\n### 📈 支出分类 TOP5\n"
        for i, (category, amount) in enumerate(data['top_categories'], 1):
            category_name = category_labels.get(category, category)
            content += f"{i}. {category_name}：¥{amount:.2f}\n"

    content += f"\n---\n🤖 NestEgg 自动生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    return content


async def send_to_serverchan(title: str, content: str, send_key: str) -> bool:
    """
    通过 Server酱 发送消息

    Args:
        title: 消息标题
        content: 消息内容（支持 Markdown）
        send_key: Server酱 SendKey

    Returns:
        是否发送成功
    """
    url = f"https://sctapi.ftqq.com/{send_key}.send"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                data={
                    "title": title,
                    "desp": content
                },
                timeout=10.0
            )

            result = response.json()
            if result.get("code") == 0:
                print(f"✅ 消息发送成功: {title}")
                return True
            else:
                print(f"❌ 消息发送失败: {result.get('message')}")
                return False

        except Exception as e:
            print(f"❌ 发送异常: {e}")
            return False


async def send_weekly_report_to_wechat(send_keys: list[str]) -> bool:
    """
    生成并发送周报到微信

    Args:
        send_keys: Server酱 SendKey 列表（支持发送给多人）

    Returns:
        是否全部发送成功
    """
    # 生成报表
    data = await generate_weekly_report()
    content = format_report_markdown(data, "weekly")
    title = f"📊 NestEgg 周报 - {data['period']}"

    # 发送给所有接收者
    success_count = 0
    for send_key in send_keys:
        if await send_to_serverchan(title, content, send_key):
            success_count += 1

    return success_count == len(send_keys)


async def send_monthly_report_to_wechat(send_keys: list[str]) -> bool:
    """
    生成并发送月报到微信

    Args:
        send_keys: Server酱 SendKey 列表（支持发送给多人）

    Returns:
        是否全部发送成功
    """
    # 生成报表
    data = await generate_monthly_report()
    content = format_report_markdown(data, "monthly")
    title = f"📊 NestEgg 月报 - {data['period']}"

    # 发送给所有接收者
    success_count = 0
    for send_key in send_keys:
        if await send_to_serverchan(title, content, send_key):
            success_count += 1

    return success_count == len(send_keys)
