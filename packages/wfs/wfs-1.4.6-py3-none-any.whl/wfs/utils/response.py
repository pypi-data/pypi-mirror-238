import cdxg
import traceback, json
import urllib3
urllib3.disable_warnings()


class apicall(cdxg.TestCase):

    def apicall(self, header, method, url):
        try:
            if method == 'GET':
                callapis = self.get(url=url, verify=False, headers=header)
                status_code = callapis.status_code
                getalljson = json.loads(callapis.content)
                return getalljson, url
        except Exception as e:
            traceback.print_exc()
