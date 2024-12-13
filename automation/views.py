from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from automation.selenium_crawler.linkedin import LinkedIn

from .models import Website


class JobApplicationAutomationView(APIView):

    def post(self, request, *args, **kwargs):
        websites = Website.objects.all()
        result = []

        for website in websites:
            if website.name.lower() == "linkedin":
                crawler = LinkedIn(website)
            elif website.name.lower() == "indeed":
                crawler = IndeedCrawler(website)
            elif website.name.lower() == "monster":
                crawler = MonsterCrawler(website)
            else:
                result.append(
                    {
                        "website": website.name,
                        "status": "error",
                        "message": "Unsupported website",
                    }
                )
                continue

            login = crawler.login()

            if login:
                crawler.search_jobs()
                result.append(
                    {
                        "website": website.name,
                        "status": "success",
                        "message": "Applied for jobs",
                    }
                )
            else:
                result.append(
                    {
                        "website": website.name,
                        "status": "error",
                        "message": "Login failed",
                    }
                )

            crawler.close_driver()

        return Response(result, status=status.HTTP_200_OK)
