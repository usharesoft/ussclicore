__author__ = "UShareSoft"

import requests
from hurry.filesize import size
from progressbar import Bar, ETA, Percentage, ProgressBar
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import printer

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Download:
    def __init__(self, url, output_file_name, verify_ssl_certificate=True):
        self.url = url
        self.output_file_name = output_file_name
        self.verify = verify_ssl_certificate

    def read_chunk(self, response, output_file, chunk_size=8192, report_hook=False):
        total_size = int(response.headers['Content-Length'])
        current_chunk = 0

        printer.out("Ready to download " + size(total_size), printer.INFO)

        widgets = ['Status: ', Percentage(), ' ', Bar('>'), ' ', ETA()]
        progress_bar = ProgressBar(widgets=widgets, maxval=100).start()

        for chunk in response.iter_content(chunk_size):
            output_file.write(chunk)
            current_chunk += 1
            if report_hook:
                percent = int(current_chunk * chunk_size * 100 / total_size)
                progress_bar.update(percent)

        progress_bar.finish()

    def start(self):
        output_file = open(self.output_file_name, 'wb')
        try:
            response = requests.get(self.url, stream=True, verify=self.verify)
            response.raise_for_status()
            self.read_chunk(response, output_file, report_hook=True)
        except requests.exceptions.HTTPError as e:
            printer.out("Error getting URL: " + self.url, printer.ERROR)
            raise e
