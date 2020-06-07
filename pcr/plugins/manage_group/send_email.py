import smtplib
import config
from email.mime.text import MIMEText
from email.utils import formataddr


def email(sender_name, bug_info):
    # 将bug信息发送给作者
    ret = True
    msg = f"收到来自指挥官{sender_name}的反馈喵：{bug_info}"
    title = f"收到了新的反馈喵~"
    try:
        mail = MIMEText(msg, 'plain', 'utf-8')
        mail['From'] = formataddr([config.MY_NAME, config.SENDER_ADDRESS])
        mail['To'] = formataddr(['DDavid', config.RECEIVE_ADDRESS])
        mail['Subject'] = title
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(config.SENDER_ADDRESS, config.SENDER_PWD)
        server.sendmail(config.SENDER_ADDRESS, config.RECEIVE_ADDRESS, mail.as_string())
    except smtplib.SMTPException as e:
        print(e)
        ret = False
    finally:
        pass
        # server.quit()

    return ret







