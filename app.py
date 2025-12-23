from flask import Flask, render_template, jsonify
import requests
import time
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# 简单的内存缓存
cache = {
    'data': None,
    'timestamp': 0
}


class FeishuClient:
    """飞书API客户端"""
    
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = None
        self.token_expire_time = 0
    
    def get_tenant_access_token(self):
        """获取tenant_access_token"""
        # 如果token还未过期，直接返回
        if self.tenant_access_token and time.time() < self.token_expire_time:
            return self.tenant_access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            # 禁用代理，直接连接
            response = requests.post(url, json=data, headers=headers, proxies={"http": None, "https": None})
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') == 0:
                self.tenant_access_token = result.get('tenant_access_token')
                # 提前5分钟刷新token
                self.token_expire_time = time.time() + result.get('expire', 7200) - 300
                return self.tenant_access_token
            else:
                print(f"获取token失败: {result}")
                return None
        except Exception as e:
            print(f"获取token异常: {e}")
            return None
    
    def get_records(self, base_id, table_id):
        """获取多维表格记录"""
        token = self.get_tenant_access_token()
        if not token:
            return None
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{base_id}/tables/{table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        all_records = []
        page_token = None
        
        try:
            while True:
                params = {"page_size": 100}
                if page_token:
                    params["page_token"] = page_token
                
                response = requests.get(url, headers=headers, params=params, proxies={"http": None, "https": None})
                response.raise_for_status()
                result = response.json()
                
                if result.get('code') == 0:
                    data = result.get('data', {})
                    items = data.get('items', [])
                    all_records.extend(items)
                    
                    # 检查是否有下一页
                    if data.get('has_more'):
                        page_token = data.get('page_token')
                    else:
                        break
                else:
                    print(f"获取记录失败: {result}")
                    return None
            
            return all_records
        except Exception as e:
            print(f"获取记录异常: {e}")
            return None


# 初始化飞书客户端
feishu_client = FeishuClient(
    app_id=app.config['FEISHU_APP_ID'],
    app_secret=app.config['FEISHU_APP_SECRET']
)


def get_articles_from_feishu():
    """从飞书多维表格获取文章数据"""
    # 检查缓存
    current_time = time.time()
    if cache['data'] and (current_time - cache['timestamp']) < app.config['CACHE_TIMEOUT']:
        return cache['data']
    
    # 获取数据
    records = feishu_client.get_records(
        base_id=app.config['BASE_ID'],
        table_id=app.config['TABLE_ID']
    )
    
    if not records:
        return []
    
    # 解析数据
    articles = []
    for record in records:
        fields = record.get('fields', {})
        
        # 提取字段值 - 处理不同的数据格式
        def get_field_value(field_data):
            if isinstance(field_data, list) and len(field_data) > 0:
                # 数组格式
                return field_data[0].get('text', '') if isinstance(field_data[0], dict) else str(field_data[0])
            elif isinstance(field_data, str):
                # 字符串格式
                return field_data
            elif isinstance(field_data, dict):
                # 对象格式
                return field_data.get('text', '')
            else:
                return ''
        
        # 尝试从多个可能的字段中获取标题
        title = get_field_value(fields.get('文本', '')) or get_field_value(fields.get('标题', ''))
        quote = get_field_value(fields.get('金句输出', ''))
        comment = get_field_value(fields.get('黄叔点评', ''))
        content = get_field_value(fields.get('概要内容输出', ''))
        
        if title:  # 只添加有标题的记录
            articles.append({
                'id': record.get('record_id'),
                'title': title,
                'quote': quote,
                'comment': comment,
                'content': content,
                'preview': content[:100] + '...' if len(content) > 100 else content
            })
    
    # 更新缓存
    cache['data'] = articles
    cache['timestamp'] = current_time
    
    return articles


@app.route('/')
def index():
    """首页"""
    articles = get_articles_from_feishu()
    return render_template('index.html', articles=articles)


@app.route('/article/<article_id>')
def article_detail(article_id):
    """文章详情页"""
    articles = get_articles_from_feishu()
    article = next((a for a in articles if a['id'] == article_id), None)
    
    if not article:
        return "文章不存在", 404
    
    return render_template('detail.html', article=article)


@app.route('/api/refresh')
def refresh_cache():
    """刷新缓存API"""
    cache['data'] = None
    cache['timestamp'] = 0
    articles = get_articles_from_feishu()
    return jsonify({
        'success': True,
        'count': len(articles)
    })


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
