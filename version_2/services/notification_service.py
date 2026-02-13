import logging
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings
from domain.additional_models import TrendReliability

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        # Webhooks & API Keys
        self.discord_webhook_url = getattr(settings, 'DISCORD_WEBHOOK_URL', None)
        self.slack_webhook_url = getattr(settings, 'SLACK_WEBHOOK_URL', None)
        self.telegram_bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        self.telegram_chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
        
        # Email Settings
        self.email_smtp_server = getattr(settings, 'EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        self.email_smtp_port = getattr(settings, 'EMAIL_SMTP_PORT', 587)
        self.email_sender = getattr(settings, 'EMAIL_SENDER', None)
        self.email_password = getattr(settings, 'EMAIL_PASSWORD', None)
        self.email_recipients = getattr(settings, 'EMAIL_RECIPIENTS', []) # List of emails

    def send_trend_alert(self, reliability: TrendReliability):
        """
        신뢰도가 높은 트렌드가 감지되면 설정된 모든 채널로 알림을 보냅니다.
        """
        message_body = (
            f"🚨 **급상승 트렌드 감지!**\n\n"
            f"**키워드**: {reliability.keyword}\n"
            f"**신뢰도 점수**: {reliability.total_score:.1f}점\n"
            f"(Google: {reliability.google_score:.1f}, News: {reliability.news_score:.1f})"
        )
        
        # 1. Discord
        if self.discord_webhook_url:
            self.send_discord_alert(reliability)

        # 2. Slack
        if self.slack_webhook_url:
            self.send_slack_message(message_body)

        # 3. Telegram
        if self.telegram_bot_token and self.telegram_chat_id:
            self.send_telegram_message(message_body)

        # 4. Email (only for very high scores, e.g. > 80)
        if reliability.total_score >= 80 and self.email_sender:
            self.send_email(
                subject=f"[TrendTracker] 급상승 트렌드 발견: {reliability.keyword}",
                body=message_body
            )

    def send_discord_alert(self, reliability: TrendReliability):
        try:
            message = {
                "content": f"🚨 **급상승 트렌드 감지!**\n\n**키워드**: {reliability.keyword}\n**신뢰도 점수**: {reliability.total_score:.1f}점",
                "embeds": [
                    {
                        "title": "TrendTracker 분석 결과",
                        "description": "이 키워드는 여러 소스에서 동시에 포착되어 높은 신뢰도를 보이고 있습니다.",
                        "color": 15158332, # Red
                        "fields": [
                            {"name": "Google Trend Score", "value": f"{reliability.google_score:.1f}", "inline": True},
                            {"name": "News Coverage Score", "value": f"{reliability.news_score:.1f}", "inline": True}
                        ],
                        "footer": {"text": "TrendTracker AI"}
                    }
                ]
            }
            requests.post(self.discord_webhook_url, json=message, timeout=5)
            logger.info(f"Discord notification sent for {reliability.keyword}")
        except Exception as e:
            logger.error(f"Failed to send Discord notification: {e}")

    def send_slack_message(self, text: str):
        try:
            payload = {"text": text}
            requests.post(self.slack_webhook_url, json=payload, timeout=5)
            logger.info("Slack notification sent.")
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")

    def send_telegram_message(self, text: str):
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }
            requests.post(url, json=payload, timeout=5)
            logger.info("Telegram notification sent.")
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")

    def send_email(self, subject: str, body: str):
        if not self.email_sender or not self.email_recipients:
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = ", ".join(self.email_recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_smtp_server, self.email_smtp_port)
            server.starttls()
            server.login(self.email_sender, self.email_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent to {len(self.email_recipients)} recipients.")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
