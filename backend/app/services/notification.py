"""
交易通知服务
"""
from datetime import datetime
from app.services.email_service import send_email
from app.services.report import send_to_serverchan
from app.config import settings


def format_transaction_html(transaction_data: dict) -> str:
    """
    格式化交易记录为 HTML 邮件

    Args:
        transaction_data: 交易数据字典

    Returns:
        HTML 格式的邮件内容
    """
    # 交易类型和颜色
    is_income = transaction_data['type'] == 'income'
    type_text = '收入' if is_income else '支出'
    type_color = '#10b981' if is_income else '#ef4444'
    type_emoji = '💰' if is_income else '💸'
    amount_prefix = '+' if is_income else '-'

    # 分类标签
    category_labels = {
        'food': '餐饮',
        'transport': '交通',
        'shopping': '购物',
        'utilities': '水电',
        'entertainment': '娱乐',
        'medical': '医疗',
        'education': '教育',
        'salary': '工资',
        'bonus': '奖金',
        'other': '其他'
    }
    category_text = category_labels.get(transaction_data.get('category', 'other'), '其他')

    # 格式化金额
    amount = float(transaction_data['amount'])
    amount_text = f"{amount_prefix}¥{amount:,.2f}"

    # 格式化日期
    date = transaction_data.get('date', datetime.now().strftime('%Y-%m-%d'))
    if 'T' in date:
        date = date.split('T')[0]

    # 备注
    description = transaction_data.get('description', '无')

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e5e7eb;
        }}
        .header h2 {{
            color: #1f2937;
            margin: 0;
            font-size: 24px;
        }}
        .amount-card {{
            background: linear-gradient(135deg, {type_color}15 0%, {type_color}05 100%);
            border-left: 4px solid {type_color};
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .amount {{
            font-size: 32px;
            font-weight: bold;
            color: {type_color};
            font-family: 'SF Pro Display', -apple-system, monospace;
            font-variant-numeric: tabular-nums;
            margin: 10px 0;
        }}
        .type-badge {{
            display: inline-block;
            background-color: {type_color};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
        }}
        .details {{
            margin-top: 20px;
        }}
        .detail-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #f3f4f6;
        }}
        .detail-row:last-child {{
            border-bottom: none;
        }}
        .detail-label {{
            color: #6b7280;
            font-weight: 500;
        }}
        .detail-value {{
            color: #1f2937;
            font-weight: 600;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
            font-size: 14px;
        }}
        .icon {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">{type_emoji}</div>
            <h2>新增{type_text}记录</h2>
        </div>

        <div class="amount-card">
            <div style="text-align: center;">
                <span class="type-badge">{type_text}</span>
                <div class="amount">{amount_text}</div>
            </div>
        </div>

        <div class="details">
            <div class="detail-row">
                <span class="detail-label">📅 日期</span>
                <span class="detail-value">{date}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">🏷️ 分类</span>
                <span class="detail-value">{category_text}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">📝 备注</span>
                <span class="detail-value">{description}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">⏰ 记录时间</span>
                <span class="detail-value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
        </div>

        <div class="footer">
            🤖 此邮件由 NestEgg 自动发送，请勿回复
        </div>
    </div>
</body>
</html>
"""
    return html_content


def format_transaction_markdown(transaction_data: dict) -> str:
    """
    格式化交易记录为 Markdown（用于微信推送）

    Args:
        transaction_data: 交易数据字典

    Returns:
        Markdown 格式的内容
    """
    # 交易类型
    is_income = transaction_data['type'] == 'income'
    type_text = '收入' if is_income else '支出'
    type_emoji = '💰' if is_income else '💸'
    amount_prefix = '+' if is_income else '-'

    # 分类标签
    category_labels = {
        'food': '餐饮',
        'transport': '交通',
        'shopping': '购物',
        'utilities': '水电',
        'entertainment': '娱乐',
        'medical': '医疗',
        'education': '教育',
        'salary': '工资',
        'bonus': '奖金',
        'other': '其他'
    }
    category_text = category_labels.get(transaction_data.get('category', 'other'), '其他')

    # 格式化金额
    amount = float(transaction_data['amount'])
    amount_text = f"{amount_prefix}¥{amount:,.2f}"

    # 格式化日期
    date = transaction_data.get('date', datetime.now().strftime('%Y-%m-%d'))
    if 'T' in date:
        date = date.split('T')[0]

    # 备注
    description = transaction_data.get('description', '无')

    content = f"""## {type_emoji} 新增{type_text}记录

### 金额
**{amount_text}**

### 详细信息
- 📅 **日期**：{date}
- 🏷️ **分类**：{category_text}
- 📝 **备注**：{description}
- ⏰ **记录时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
🤖 NestEgg 自动通知"""

    return content


async def notify_transaction_created(transaction_data: dict):
    """
    新增交易记录时发送通知

    Args:
        transaction_data: 交易数据字典
    """
    # 检查是否启用交易通知
    if not settings.enable_transaction_notification:
        return

    is_income = transaction_data['type'] == 'income'
    type_text = '收入' if is_income else '支出'
    amount = float(transaction_data['amount'])

    # 邮件标题
    email_subject = f"{'💰' if is_income else '💸'} 新增{type_text}：¥{amount:,.2f}"

    # 发送邮件通知
    if settings.email_recipients:
        email_list = [email.strip() for email in settings.email_recipients.split(",") if email.strip()]
        if email_list:
            html_content = format_transaction_html(transaction_data)
            await send_email(
                to_emails=email_list,
                subject=email_subject,
                content=html_content,
                content_type="html"
            )

    # 发送微信通知
    if settings.serverchan_keys:
        keys = [k.strip() for k in settings.serverchan_keys.split(",") if k.strip()]
        markdown_content = format_transaction_markdown(transaction_data)
        for key in keys:
            await send_to_serverchan(
                title=email_subject,
                content=markdown_content,
                send_key=key
            )
