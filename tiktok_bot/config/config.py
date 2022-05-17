import argparse
import datetime
from pathlib import Path
from typing import Optional

import yaml
from loguru import logger
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
MEDIA_DIR = BASE_DIR / 'media'

LOG_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)


def load_yaml(file) -> dict:
    file = file if Path(file).suffix else f"{file}.yml"
    with open(Path(BASE_DIR, file), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_config():
    parser = argparse.ArgumentParser(description="config_file")
    parser.add_argument("-f", type=str)
    args = parser.parse_args()
    if args.f:
        logger.success(f"Выгрузка конфига из файла {args.f}")
    return args.f


class Bot(BaseModel):
    token: str
    admins: Optional[list[int]]
    chats: Optional[list[str]]


class Database(BaseModel):
    username: str
    password: str
    host: str
    port: int
    db_name: str


class Config(BaseModel):
    bot: Bot
    db: Database


I18N_DOMAIN = "tiktok_bot"
LOCALES_DIR = BASE_DIR / "tiktok_bot/apps/bot/locales"
TZ = datetime.timezone(datetime.timedelta(hours=3))
# config_file = parse_config()
config = Config(**load_yaml("config_dev.yml"))
