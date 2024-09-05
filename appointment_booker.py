import random
import requests
from bs4 import BeautifulSoup
from config import Config


class AppointmentBooker:
    def __init__(self, config: Config):
        self.config = config
        self.session = None

    def _initialize_session(self) -> (str, str, str, str, str, str):
        self.session = requests.Session()
        self.session.get("https://www.hikorea.go.kr/Main.pt")
        self.session.post("https://www.hikorea.go.kr/Main.pt", data={
            "locale": "en",
            "TRAN_TYPE": "ComSubmit"
        })
        self.session.post("https://www.hikorea.go.kr/resv/ResvIdntR.pt",
                          data={
                              "mem_gb": "NOMEM",
                              "TRAN_TYPE": "ComSubmit"
                          })
        captcha_num = random.randint(1000, 9999)
        res = self.session.post("https://www.hikorea.go.kr/resv/ResvIdntC.pt",
                                data={
                                    "inputNumFull": captcha_num,
                                    "confNum": captcha_num,
                                    "visaNo": self.config.visa_number,
                                    "visaNm": self.config.visa_name,
                                    "visaBirthYmd": self.config.visa_birth,
                                    "authType": 3,
                                    "TRAN_TYPE": "ComSubmit"
                                })
        val_11 = res.text.split('name="val11" value="')[1].split('" />')[0]
        val_21 = res.text.split('name="val21" value="')[1].split('" />')[0]
        val_31 = res.text.split('name="val31" value="')[1].split('" />')[0]
        val_41 = res.text.split('name="val41" value="')[1].split('" />')[0]
        val_51 = res.text.split('name="val51" value="')[1].split('" />')[0]
        val_61 = res.text.split('name="val61" value="')[1].split('" />')[0]
        return val_11, val_21, val_31, val_41, val_51, val_61

    def book_appointment(self, appointment) -> str:
        val_11, val_21, val_31, val_41, val_51, val_61 = self._initialize_session()
        res = self.session.post("https://www.hikorea.go.kr/resv/ResvC.pt", data={
            "userId": "hikorea_3",
            "operDeskCnt": appointment["oper_desk_cnt"],
            "targetSeq": appointment["target_seq"],
            "resvDt": appointment["date"],
            "selBusiTypeList": "F01,F08",
            "orgnCd": 1272332,
            "deskSeq": appointment["office_number"],
            "visiPurp": "AA",
            "resvTime1": "_".join(appointment['time']),
            "val11": val_11,
            "val21": val_21,
            "val31": val_31,
            "val41": val_41,
            "val51": val_51,
            "val61": val_61,
            "resvNm": self.config.visa_name,
            "selBusiType1_1": ["F01", "F08"],
            "telNo1": "",
            "telNo2": "",
            "telNo3": "",
            "mobileTelNo1": "",
            "mobileTelNo2": "",
            "mobileTelNo3": "",
            "resvPasswd": "0000",
            "resvYmd": f"{appointment['date']} {'~'.join(appointment['time'])}",
            "visiPurpTxt": "",
            "TRAN_TYPE": "ComSubmit"
        })
        if "msgId" in res.text:
            return res.text.split("msgId = '")[1].split("'")[0]
        return "Success"
