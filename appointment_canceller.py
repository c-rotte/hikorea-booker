import random
import requests
from bs4 import BeautifulSoup
from config import Config


class AppointmentCanceller:
    def __init__(self, config: Config):
        self.config = config
        self.session = None

    def _initialize_session(self):
        self.session = requests.Session()
        self.session.get("https://www.hikorea.go.kr/Main.pt")
        self.session.post("https://www.hikorea.go.kr/Main.pt", data={
            "locale": "en",
            "TRAN_TYPE": "ComSubmit"
        })
        captcha_num = random.randint(1000, 9999)
        self.session.post("https://www.hikorea.go.kr/resv/ResvIdntC.pt", data={
            "inputNumFull": captcha_num,
            "confNum": captcha_num,
            "visaNo": self.config.visa_number,
            "visaNm": self.config.visa_name,
            "visaBirthYmd": self.config.visa_birth,
            "authType": 3,
            "pageGubun": "NonSearch",
            "TRAN_TYPE": "ComSubmit"
        })

    def get_current_appointments(self):
        self._initialize_session()
        app_l_info = ("QUFGQzR5TVpRWHpaY3Nua0tSVGx1VkFBWUQ0RytjWDhXS3hjcWpIZWl2akxOVXF0RFpZR3d0NFBYQ3"
                      "VDRVhjWXpwOVlYUms5YzlFR3g5aWZIYkZPYzRUK0NuWHVucUFaeDhudVNzVEtQNUhtQXc9PQ==")
        res = self.session.post("https://www.hikorea.go.kr/mypage/MypgNonResvPageR.pt", data={
            "applInfo": app_l_info,
            "authType": 3,
            "pageGubun": "NonSearch",
            "langCd": "en",
            "pageUserId": "hikorea_3",
            "TRAN_TYPE": "ComSubmit"
        })

        soup = BeautifulSoup(res.text, "html.parser")
        appointments = []
        for tr in soup.find_all("tr"):
            tds = tr.find_all("td", class_="tac")
            if len(tds) != 5:
                continue
            on_click = tds[0].find("a")["onclick"]
            reservation_id = on_click.split("fncDetailResv('")[1].split("'")[0]
            state = tds[3].text
            if state != "Reserved":
                continue
            date = tds[1].text.strip()
            appointments.append({"id": reservation_id, "date": date})
        return appointments

    def cancel_appointment(self, reservation_id):
        self.session.post("https://www.hikorea.go.kr/mypage/MypgNonResvDetailR.pt", data={
            "page": 1,
            "pageUserId": "hikorea_3",
            "applInfo": "QUFGQzR5TVpRWHpaY3Nua0tSVGx1VkFBWUQ0RytjWDhXS3hjcWpIZWl2akxOVXF0RFpZR3d0"
                        "NFBYQ3VDRVhjWXpwOVlYUms5YzlFR3g5aWZIYkZPYzRUK0NuWHVucUFaeDhudVNzVEtQNUhtQXc9PQ==",
            "searchStDt": 20240905,
            "searchEnDt": 20250305,
            "resvRecptNo": reservation_id
        })
        self.session.post("https://www.hikorea.go.kr/mypage/MypgResvD.pt", data={
            "TRAN_TYPE": "ComAjax",
            "resvRecptNo": reservation_id,
            "userId": "hikorea_3",
            "applNm": self.config.visa_name,
            "password": "XE0QiMRjnNHH2hLkoehFBo/A0MXx71ALd0fG4gB2ahzQC9/SWGQf61DQkx/DKMwCt9SisrkWyyHXzbWC4Hy3UA==",
            "suggest": "0000"
        })
