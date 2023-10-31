import os
import smtplib
from collections.abc import Sequence
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self, user_id, user_password):
        """
        :param user_id:메일 전송을 위한 계정 ID
        :param user_password:메일 전송을 위한 계정 비밀번호
        """
        self.user_id = user_id
        self.user_password = user_password
        self.smtp_server = "smtp.worksmobile.com"
        self.smtp_port = 465

    def send_email(self, subject: str, body: str, recipient_emails: Sequence, *, from_name: str = None,
                   cc: Sequence = (),
                   bcc: Sequence = (),
                   attachments: Sequence = ()):
        """
         Parameters
         ----------
            :param subject: 메일 제목
            :param body: 본문
            :param recipient_emails:수신자 이메일 목록
            :param from_name: 발신자 이름
            :param cc: 참조 목록
            :param bcc: 숨은 참조 목록
            :param attachments: 첨부파일 경로 목록. 파일명만 나열 또는 (파일명, 파일타입) 튜플로 나열. 파일 타입은 'image' 또는 'file'로 지정.
        """

        if len(attachments) > 0:
            message = MIMEMultipart("alternative")
        else:
            message = MIMEMultipart("mixed")

        message["Subject"] = subject
        if from_name is None:
            message["From"] = f"{self.user_id}"
        else:
            message["From"] = f"{Header(from_name, 'utf-8').encode()}<{self.user_id}>"
        message["To"] = ",".join(recipient_emails)
        message["Cc"] = ",".join(cc)

        all_recipient_emails = tuple(recipient_emails) + tuple(cc) + tuple(bcc)

        message.attach(MIMEText(body, 'html'))

        for attachment in attachments:
            if isinstance(attachment, tuple):
                attachment_path, type = attachment
                if type == 'image':
                    file_data = MIMEBase('image', attachment_path.split('.')[-1].lower())
                elif type == 'file':
                    file_data = MIMEBase('application', 'octect-stream')
                else:
                    raise ValueError('Invalid attachment type')
                attachment = attachment_path
            else:
                file_data = MIMEBase('application', 'octect-stream')

            with open(attachment, 'rb') as fp:
                file_data.set_payload(fp.read())

            encoders.encode_base64(file_data)

            filename = os.path.basename(attachment)
            file_data.add_header('Content-Disposition', 'attachment; filename="' + filename + '"')
            message.attach(file_data)

        smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        smtp.login(self.user_id, self.user_password)

        smtp.sendmail(self.user_id,
                      all_recipient_emails,
                      message.as_string())
        smtp.close()
