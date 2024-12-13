import time

from django.core.management.base import BaseCommand

from automation.models import Website
from automation.selenium_crawler.linkedin import LinkedIn


class Command(BaseCommand):
    help = "Automates job applications on various job portals"

    def handle(self, *args, **kwargs):
        websites = Website.objects.all()

        for website in websites:
            if website.name.lower() == "linkedin":
                crawler = LinkedIn(website)
            elif website.name.lower() == "indeed":
                crawler = IndeedCrawler(website)
            elif website.name.lower() == "monster":
                crawler = MonsterCrawler(website)
            else:
                self.stdout.write(
                    self.style.ERROR(f"Unsupported website: {website.name}")
                )
                continue

            login = crawler.login()

            if login:
                job = crawler.search_jobs()
                if job:
                    crawler.paste_and_send_message()

            print("===================================================================")
            crawler.close_driver()
            self.stdout.write(self.style.SUCCESS(f"Applied for jobs on {website.name}"))
