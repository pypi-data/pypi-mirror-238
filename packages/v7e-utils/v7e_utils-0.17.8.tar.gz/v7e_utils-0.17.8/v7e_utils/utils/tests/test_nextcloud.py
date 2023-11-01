from v7e_utils.utils.nextclould import Nextcloud
from v7e_utils.utils.config import NextCloudItem
from django.test import TestCase


class UtilsNextcloudTestCase(TestCase):
    def test_mkdir(self):
        parameters = NextCloudItem()
        print(parameters)
        next = Nextcloud(
            config_parameters=parameters
        )
        result = next.mkdir(path="Reports/PDFs/expedientes/88888888")

        self.assertTrue(result)
        
    
    def test_download_file(self):
        parameters = NextCloudItem()
        print(parameters)
        next = Nextcloud(
            config_parameters=parameters
        )
        # example route with path = "Reports/PDFs/contrato/test_pdf.pdf"
        result = next.download_file(path="Nextcloud Manual.pdf")
        self.assertTrue(result != None)
