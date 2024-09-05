import time
import requests
from bs4 import BeautifulSoup
from config import Config
from utils import get_today_ymd
import json


class AppointmentChecker:
    def __init__(self, config: Config):
        self.config = config

    def get_date_dict(self, desk_seq: str) -> (dict, int):
        res = requests.post("https://www.hikorea.go.kr/resv/ResvPopupR.pt", data={
            "deskSeq": desk_seq,
            "visiYmd": get_today_ymd(),
            "applCnt": 1,
            "TRAN_TYPE": "ComSubmit"
        })
        first_chunk = "var monthResvDataJSONList = JSON.parse('"
        last_chunk = "');"
        json_str = res.text.split(first_chunk)[1].split(last_chunk)[0]
        max_slots = res.text.split("if(value.totalResvNum >= ")[1].split(")")[0]
        return json.loads(json_str), int(max_slots)

    def get_desks(self, desk_seq: str, visi_ymd: int):
        res = requests.post("https://www.hikorea.go.kr/resv/ResvPopupR.pt", data={
            "deskSeq": desk_seq,
            "visiYmd": visi_ymd,
            "applCnt": 1,
            "TRAN_TYPE": "ComSubmit"
        })
        soup = BeautifulSoup(res.text, "html.parser")
        time_tags = soup.find_all("a", class_="time")
        for time_tag in time_tags:
            if not time_tag.has_attr("onclick"):
                continue
            desk_id = time_tag["id"]
            oper_desk_cnt = time_tag["onclick"].split("fncResvSet(this.id, '")[1].split("'")[0]
            target_seq = time_tag["onclick"].split("', '")[1].split("'")[0]
            slots = time_tag.text.split("(")[1].split(")")[0]
            total_slots, occupied_slots = slots.split("/")[0], slots.split("/")[1]
            yield {
                "desk_id": desk_id,
                "oper_desk_cnt": oper_desk_cnt,
                "target_seq": target_seq,
                "total_slots": total_slots,
                "occupied_slots": occupied_slots
            }

    def check_new_appointments(self):
        new_appointments = []
        for office_number in self.config.office_numbers:
            date_dict, max_slots = self.get_date_dict(office_number)
            for date_info in date_dict:
                visi_ymd = date_info["visiYmd"]
                if visi_ymd > self.config.max_inclusive_date:
                    continue
                total_resv_num = date_info["totalResvNum"]
                if total_resv_num >= int(max_slots):
                    continue
                for desk in self.get_desks(office_number, visi_ymd):
                    new_appointments.append({
                        "office_number": office_number,
                        "date": visi_ymd,
                        "time": desk["desk_id"].split("_"),
                        "oper_desk_cnt": desk["oper_desk_cnt"],
                        "target_seq": desk["target_seq"]
                    })
                time.sleep(3)

        return new_appointments
