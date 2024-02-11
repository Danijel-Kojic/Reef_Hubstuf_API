from datetime import date, timedelta

from src.api_client import HubstuffApiClient
from src.data_parser import HubstuffDataParser
from src.html_generator import HtmlGenerator
from src.email_sender import EmailSender
from src.logger import get_root_logger


logger = get_root_logger(__name__)


def main():
    try:
        api_client = HubstuffApiClient()
        data_parser = HubstuffDataParser(api_client=api_client)
        today = date.today()
        # yesterday = today - timedelta(days=1)
        yesterday = today
        activities_by_day = data_parser.get_activities_by_day(yesterday)
        html_generator = HtmlGenerator()
        table_html = html_generator.dump_work_time_table(activities_by_day)
        table_html_str = str(table_html.decode('utf-8'))
        print(table_html_str)
        # with open('table.html', 'wb') as f:
        #     f.write(table_html)
        try:
            email_sender = EmailSender()
            subject = f"Work stats on {yesterday.strftime('%Y-%m-%d')}"
            email_sender.send_email(subject=subject, content=table_html_str)
        except Exception as e:
            logger.error(f'Failed to send email {e}')

    except Exception as e:
        logger.error(e)
        return False
    return True


if __name__ == '__main__':
    main()