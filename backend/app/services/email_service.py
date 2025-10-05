"""
邮件推送服务
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
from app.config import settings


async def send_email(
    to_emails: list[str],
    subject: str,
    content: str,
    content_type: str = "html"
) -> bool:
    """
    发送邮件

    Args:
        to_emails: 收件人列表
        subject: 邮件主题
        content: 邮件内容（支持 HTML 或纯文本）
        content_type: 内容类型 ("html" 或 "plain")

    Returns:
        是否发送成功
    """
    if not settings.smtp_server or not settings.smtp_user:
        print("❌ 未配置邮箱 SMTP 信息")
        return False

    try:
        # 创建邮件
        message = MIMEMultipart('alternative')
        message['From'] = Header(f"NestEgg <{settings.smtp_user}>")
        message['To'] = ", ".join(to_emails)
        message['Subject'] = Header(subject, 'utf-8')
        message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

        # 添加邮件内容
        if content_type == "html":
            html_part = MIMEText(content, 'html', 'utf-8')
            message.attach(html_part)
        else:
            text_part = MIMEText(content, 'plain', 'utf-8')
            message.attach(text_part)

        # 发送邮件
        async with aiosmtplib.SMTP(
            hostname=settings.smtp_server,
            port=settings.smtp_port,
            use_tls=settings.smtp_use_tls
        ) as smtp:
            await smtp.login(settings.smtp_user, settings.smtp_password)
            await smtp.send_message(message)

        print(f"✅ 邮件发送成功: {subject} -> {', '.join(to_emails)}")
        return True

    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False


def markdown_to_html(markdown_content: str) -> str:
    """
    将 Markdown 格式的报表转换为 HTML 邮件
    简单实现，支持基本 Markdown 语法
    """
    # 替换标题
    html = markdown_content
    html = html.replace('## ', '<h2>').replace('\n### ', '</h2>\n<h3>').replace('\n---', '</h3>\n<hr>')

    # 处理列表
    lines = html.split('\n')
    result = []
    in_list = False

    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul style="list-style-type: none; padding: 0;">')
                in_list = True
            # 提取内容
            content = line.strip()[2:]
            result.append(f'<li style="padding: 8px 0;">{content}</li>')
        elif line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            if not in_list:
                result.append('<ol style="padding-left: 20px;">')
                in_list = True
            # 提取内容
            content = line.strip().split('. ', 1)[1] if '. ' in line else line.strip()
            result.append(f'<li style="padding: 4px 0;">{content}</li>')
        else:
            if in_list:
                result.append('</ul>' if '- ' in '\n'.join(result[-3:]) else '</ol>')
                in_list = False
            result.append(line)

    if in_list:
        result.append('</ul>')

    html = '\n'.join(result)

    # 替换加粗
    import re
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

    # 替换表情符号样式
    html = html.replace('🟢', '<span style="color: #10b981;">🟢</span>')
    html = html.replace('🔴', '<span style="color: #ef4444;">🔴</span>')
    html = html.replace('📊', '<span style="font-size: 1.2em;">📊</span>')
    html = html.replace('💰', '<span style="font-size: 1.1em;">💰</span>')
    html = html.replace('📈', '<span style="font-size: 1.1em;">📈</span>')

    # 包装在 HTML 模板中
    html_template = f"""
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
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h2 {{
            color: #1f2937;
            border-bottom: 2px solid #6366f1;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h3 {{
            color: #4b5563;
            margin-top: 20px;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e5e7eb;
            margin: 20px 0;
        }}
        .amount {{
            font-family: 'SF Pro Display', -apple-system, monospace;
            font-variant-numeric: tabular-nums;
        }}
        .footer {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            color: #6b7280;
            font-size: 0.875rem;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html}
        <div class="footer">
            此邮件由 NestEgg 自动发送，请勿回复
        </div>
    </div>
</body>
</html>
"""
    return html_template


async def send_weekly_report_email(to_emails: list[str]) -> bool:
    """
    发送周报到邮箱

    Args:
        to_emails: 收件人邮箱列表

    Returns:
        是否全部发送成功
    """
    from app.services.report import generate_weekly_report, format_report_markdown

    # 生成报表
    data = await generate_weekly_report()
    markdown_content = format_report_markdown(data, "weekly")

    # 转换为 HTML
    html_content = markdown_to_html(markdown_content)

    # 发送邮件
    subject = f"📊 NestEgg 周报 - {data['period']}"
    return await send_email(to_emails, subject, html_content, "html")


async def send_monthly_report_email(to_emails: list[str]) -> bool:
    """
    发送月报到邮箱

    Args:
        to_emails: 收件人邮箱列表

    Returns:
        是否全部发送成功
    """
    from app.services.report import generate_monthly_report, format_report_markdown

    # 生成报表
    data = await generate_monthly_report()
    markdown_content = format_report_markdown(data, "monthly")

    # 转换为 HTML
    html_content = markdown_to_html(markdown_content)

    # 发送邮件
    subject = f"📊 NestEgg 月报 - {data['period']}"
    return await send_email(to_emails, subject, html_content, "html")
