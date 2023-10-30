import os
from snqueue.boto3_clients import SesClient
from snqueue.boto3_clients.kms_client import KmsClient
from snqueue.boto3_clients.s3_client import S3Client
from snqueue.utils.email import Email, send_ses_email, get_s3_email

profile_name = 'terminus'

'''
# Sending email
email = Email(
  From='嘉敏 <zhaojiamin@muguobio.com>',
  To=['Jiamin <jiamin@gmail.com>', 'jiamin@yeeyan.com'],
  Cc='赵嘉敏 <jiamin@dongxi.net>',
  Subject='测试邮件发送',
  Body='这是一封测试邮件。\n\nCongrats!',
  Attachments=[os.path.join(os.path.dirname(__file__), 'mediq_template.xlsx')]
)

with SesClient(profile_name) as ses:
  res = send_ses_email(ses, email)
  print(res)
'''

# Getting email from S3
bucket_name = 'incoming-mail-littledumb'
#object_key = '6gmu0p32jlfa0et6t1fsvc9hvcdaqp6tnthv3jo1'
object_key = '3n5usjpr3jmkjnliipcq3j21cq3j2qov9lbsbuo1'

with S3Client(profile_name) as s3:
  with KmsClient(profile_name) as kms:
    with get_s3_email(s3, kms, bucket_name, object_key) as email:
      print(email)
      if len(email.Attachments) > 0:
        print(os.stat(email.Attachments[0]))

