from dataclasses import dataclass


@dataclass
class Config:
    visa_name: str
    visa_number: str
    visa_birth: int
    office_numbers: list[str]
    max_inclusive_date: str
    check_interval: int
