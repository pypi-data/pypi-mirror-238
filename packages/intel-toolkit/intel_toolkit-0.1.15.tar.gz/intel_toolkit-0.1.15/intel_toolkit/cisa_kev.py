import httpx
from functools import cache

class consult:
    def __init__(self):
        self.requests = httpx.Client(follow_redirects=True, default_encoding='utf-8')
        self.url_kev = 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json'
        self.get_kev_data()
        # print(self.kev.get('vulnerabilities'))

    def get_kev_data(self):
        try:
            self.kev = self.requests.get(url=self.url_kev).json()
        except:
            print('Error to get data CISA KEV')
            exit(1)
    
    @cache
    def get_info_cve(self, cveId):
        for cve in self.kev.get('vulnerabilities'):
            if cve.get('cveID') == cveId:
                return cve
        return None
    
    def is_Ransomware_Campaign_Use(self, cveId):
        cve = self.get_info_cve(cveId=cveId)
        if cve != None:
            if cve.get('knownRansomwareCampaignUse') == "Known":
                return True
            elif cve.get('knownRansomwareCampaignUse') == "Unknown":
                return False
        else:
            return False
    
if __name__ == "__main__":
    kev = consult()
    print(kev.get_info_cve('CVE-2023-36884'))
