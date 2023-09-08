from email.message import EmailMessage

import aiosmtplib
from loguru import logger as lo

EMAIL_MOCK_MODE = True


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
        await aiosmtplib.send(msg, hostname=host, port=port)

    lo.debug(f"Sending email from {from_} to {to} with subject {subject}")
    try:
        msg = compose()
        await send(msg)
    except Exception as e:
        lo.error(f"Failed to send email from {from_} to {to} with subject {subject} - error: {e}")
    else:
        lo.debug(f"Successfully sent email from {from_} to {to} with subject {subject}")