import ghasedak
from ...envs.common import SMS_SETTINGS

sms = ghasedak.Ghasedak(SMS_SETTINGS['API_KEY'])


def send_single_sms(message, receptor):
    sms.send(
        {
            "message": message,
            "receptor": receptor,
            "linenumber": "10008566"
        }
    )
