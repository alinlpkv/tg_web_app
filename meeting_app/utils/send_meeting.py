import datetime
import os

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import smtplib


class SmtpSend:
    """
    Класс для работы с SMTP почтового сервера, для отправки писем
    """

    def __init__(self):
        self.server = None

    def get_connection(self, login: str, password: str, smtp_server: str, smtp_port: int):
        self.server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        self.server.login(login, password)

    def close_connection(self):
        self.server.close()

    def send_msg(self, sender: str, recipient: str, subject: str, message: str):
        """
        Отправка письма через SMTP

        :param sender: EMAIL адрес с которого будет происходить отправка
        :param recipient: EMAIL адрес получателя письма
        :param subject: Тема письма
        :param message: Текст письма
        """
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))
        mail = msg.as_string()
        self.server.sendmail(sender, recipient, mail)

    def send_meeting(self, user_email: str, data: dict):
        CRLF = "\r\n"
        DATE_FORMAT = '%Y%m%dT%H%M%S%Z'

        bot_name = 'ai-helper'
        organizer = f"ORGANIZER;CN=AI-помощник банкира:mailto:{bot_name}{CRLF} @mail.ru"
        email_from = "ai-helper <ai-helper@mail.ru>"

        cur_date = datetime.datetime.now()
        dt_stamp = cur_date.strftime(DATE_FORMAT)

        # data from user
        email_to = user_email
        # email_to = "m2211968@edu.misis.ru"
        meeting_start = data.get('date_start')
        meeting_end = data.get('date_end')

        user_timezone = data.get('timezone')
        meeting_start += datetime.timedelta(hours=user_timezone)
        meeting_end += datetime.timedelta(hours=user_timezone)

        meeting_start_frmt = meeting_start.strftime(DATE_FORMAT)
        meeting_end_frmt = meeting_end.strftime(DATE_FORMAT)

        meeting_theme = data.get('theme')
        meeting_description = data.get("description")

        email_to_frmt = (f"ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"
                         f"{CRLF} ;CN={email_to};X-NUM-GUESTS=0:{CRLF} mailto:{email_to}{CRLF}")

        ical = (
            f"BEGIN:VCALENDAR{CRLF}PRODID:pyICSParser{CRLF}VERSION:2.0{CRLF}CALSCALE:GREGORIAN{CRLF}"
            f"METHOD:REQUEST{CRLF}BEGIN:VEVENT{CRLF}DTSTART:{meeting_start_frmt}{CRLF}DTEND:{meeting_end_frmt}{CRLF}"
            f"DTSTAMP:{dt_stamp}{CRLF}{organizer}{CRLF}"
            f"UID:FIXMEUID{dt_stamp}{CRLF}"
            f"{email_to_frmt}CREATED:{dt_stamp}{CRLF}DESCRIPTION: {meeting_description}{CRLF}LAST-MODIFIED:{dt_stamp}{CRLF}LOCATION:{CRLF}"
            f"SEQUENCE:0{CRLF}STATUS:CONFIRMED{CRLF}"
            f"SUMMARY:{meeting_theme}{CRLF}TRANSP:OPAQUE{CRLF}END:VEVENT{CRLF}END:VCALENDAR{CRLF}"
        )

        eml_body = meeting_description
        msg = MIMEMultipart('mixed')
        msg['Date'] = formatdate(localtime=True)
        msg['Reply-To'] = email_from
        msg['Subject'] = meeting_theme
        msg['From'] = email_from
        msg['To'] = email_to

        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        ical_atch = MIMEBase('application/ics', ' ;name="%s"' % ("invite.ics"))
        ical_atch.set_payload(ical)
        encoders.encode_base64(ical_atch)
        ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"' % ("invite.ics"))
        eml_atch = MIMEText('', 'plain')
        encoders.encode_base64(eml_atch)
        eml_atch.add_header('Content-Transfer-Encoding', "")

        part_email = MIMEText(eml_body, "html")
        msgAlternative.attach(part_email)
        msgAlternative.attach(MIMEText(ical, 'calendar;method=REQUEST'))

        mailServer = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        mailServer.login(os.getenv('MAIL_RU_LOGIN'), os.getenv('MAIL_RU_PASSWORD'))
        mailServer.sendmail(email_from, email_to, msg.as_string())
        mailServer.close()
