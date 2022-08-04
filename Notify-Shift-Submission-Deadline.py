from email import message
import sys,os,logging,psycopg2,json
from datetime import datetime, date, timedelta,timezone
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
from linebot.exceptions import LineBotApiError

LINE_CHANNEL_ACCESS_TOKEN   = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET         = os.environ['LINE_CHANNEL_SECRET']
LINE_BOT_API = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
LINE_HANDLER = WebhookHandler(LINE_CHANNEL_SECRET)

host = os.environ['HOST']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
dbname = os.environ['DB_NAME']
port = os.environ['PORT']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

try:
    conn = psycopg2.connect(f"dbname={dbname} user={username} password={password} host={host} port={port}")

except psycopg2.OperationalError as e:
    logging.error('ERROR: Unexpected error: Could not connect to PostgreSQL instance.')
    logging.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to heroku PostgreSQL succeeded")
def handler(event, context):
    logger.info(event)

    with conn.cursor() as cur:
        
        #LINE登録しているユーザーを取得
        SQL_LINE_Registered_Users = 'SELECT line_user_id FROM "ShiftManagementApp_line_user_id"'
        cur.execute(SQL_LINE_Registered_Users)
        LINE_Registered_Users = cur.fetchall() #list型、中身はtuple
        logger.info((LINE_Registered_Users))
        
    conn.commit()

    for LINE_Registered_User in LINE_Registered_Users:
        push_message = 'お疲れ様です。\nシフト提出期限は明日23:59までです。\n\nよろしくお願いします。'
        
        try:
            LINE_BOT_API.push_message(LINE_Registered_User[0], TextSendMessage(text=push_message))
            logger.info(f'[SUCCESS]:Message Sending Completed.line_user_id:{LINE_Registered_User[0]},push_message:{push_message}')
        except LineBotApiError as e:
            logger.error(f'[ERROR]:Message Sending failed.line_user_id:{LINE_Registered_User[0]},push_message:{push_message},reason:{e}')
            
    """
    LINE_HANDLER.handle(body, signature)
    """
    return 0