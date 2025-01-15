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
                self.stdout.write(self.style.ERROR(f"Unsupported website: {website.name}"))
                continue

            login = crawler.login() 

            if login:
                job_search_success = crawler.search_jobs()
                if job_search_success:
                    list_of_jobs = crawler.jobs_list()
                    if list_of_jobs:
                        for job_url in list_of_jobs:
                            job_processed = crawler.open_job_link([job_url])
                            if job_processed:
                                print(f"Successfully applied or messaged for job: {job_url}")
                            else:
                                print(f"Skipping job: {job_url}")

                print("===================================================================")
                # Close the driver after all jobs are processed
                crawler.close_driver()
                self.stdout.write(self.style.SUCCESS(f"Applied for jobs on {website.name}"))
            else:
                print("Login failed. Unable to proceed.")

      