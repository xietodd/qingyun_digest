import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """应用配置类"""
    
    # 飞书应用配置
    FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', 'cli_a9cc3ceff378dbc8')
    FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', 'wB5PROmvIchqqTHmPfSyMd42UI6aeMBm')
    
    # 多维表格配置
    BASE_ID = os.getenv('BASE_ID', 'Im3rwDEf1izTM4kR5U8ckOecnNe')
    TABLE_ID = os.getenv('TABLE_ID', 'tblM4pjgkvgmuihk')
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # 缓存配置（秒）
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '300'))
