from email.message import EmailMessage

from aiosmtplib import SMTP
from config import EMAIL_MOCK_MODE
from loguru import logger as lo


async def send_smtp_email(host, port, from_, to, subject, content, additional_headers=None):
    def compose():
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_
        msg['To'] = to
        if additional_headers:
            for k, v in additional_headers.items():
                msg[k] = v
        msg.set_content(content)
        return msg

    async def send(msg):
        if EMAIL_MOCK_MODE:
            lo.debug(f"Email mock mode is on, email will not be sent. Email content: \n{msg}")
            return
        smtp_client = SMTP(hostname=host, port=port, validate_certs=False)
        async with smtp_client:
            await smtp_client.send_message(msg)

    lo.debug(f"Sending email from {from_} to {to} with subject {subject}")
    try:
        msg = compose()
        await send(msg)
    except Exception as e:
        lo.error(f"Failed to send email from {from_} to {to} with subject {subject} - error: {e}")
    else:
        lo.debug(f"Successfully sent email from {from_} to {to} with subject {subject}")