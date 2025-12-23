# 青云精选 - TED Talks 精华摘要网站

这是一个基于 Flask 的内容展示网站，数据来源于飞书多维表格。采用现代设计风格，提供简洁优雅的阅读体验。

🌐 **在线访问**: [https://qingyun-digest.vercel.app](https://qingyun-digest.vercel.app)

## ✨ 功能特点

### 首页展示
- 文章标题
- 精选金句（高亮显示）
- 青云点评
- 文章预览（前100字）
- 新标签页打开文章详情

### 文章详情页
- 完整标题
- 精选金句
- 点评内容
- 完整文章内容

## 🛠 技术栈

- **后端**: Python Flask 3.0.0
- **前端**: 原生 HTML/CSS/JavaScript
- **数据源**: 飞书多维表格 API
- **部署**: Vercel

## 📋 飞书配置要求

### 1. 创建飞书应用
- 访问 [飞书开放平台](https://open.feishu.cn/)
- 创建企业自建应用
- 获取应用凭证（App ID 和 App Secret）
- 开启多维表格权限：`bitable:record:read`

### 2. 创建多维表格
创建包含以下字段的表格：
- **标题** (必需)
- **金句输出** (可选)
- **黄叔点评** (可选)
- **概要内容输出** (可选)

## 🚀 快速开始

### 本地开发

1. **克隆项目**
```bash
git clone https://github.com/xietodd/qingyun_digest.git
cd qingyun_digest
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**

复制 `.env.example` 为 `.env` 并填入你的飞书应用信息：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
# 飞书应用配置
FEISHU_APP_ID=你的应用ID
FEISHU_APP_SECRET=你的应用密钥

# 多维表格配置
BASE_ID=你的多维表格ID
TABLE_ID=你的数据表ID

# Flask配置
SECRET_KEY=your-secret-key-here
DEBUG=True

# 缓存配置（秒）
CACHE_TIMEOUT=300
```

4. **运行应用**
```bash
python app.py
```

5. **访问网站**
打开浏览器访问 http://localhost:5000

## 🌐 部署到 Vercel

### 方法一：通过 GitHub 自动部署（推荐）

1. **推送代码到 GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin master
```

2. **在 Vercel 中导入项目**
   - 访问 [Vercel Dashboard](https://vercel.com/dashboard)
   - 点击 "Add New Project"
   - 选择你的 GitHub 仓库
   - 点击 "Import"

3. **配置环境变量** ⚠️ **重要步骤**
   
   在 Vercel 项目设置中添加环境变量：
   - 进入 **Settings** → **Environment Variables**
   - 添加以下变量（应用到 Production, Preview, Development）：
     ```
     FEISHU_APP_ID=你的应用ID
     FEISHU_APP_SECRET=你的应用密钥
     BASE_ID=你的多维表格ID
     TABLE_ID=你的数据表ID
     DEBUG=False
     CACHE_TIMEOUT=300
     ```

4. **重新部署**
   - 进入 **Deployments** 页面
   - 点击最新部署的 **Redeploy** 按钮

### 方法二：使用 Vercel CLI 自动同步环境变量

如果你已经有本地的 `.env` 文件，可以使用自动化脚本同步到 Vercel：

1. **安装 Vercel CLI**
```bash
npm install -g vercel
```

2. **登录并链接项目**
```bash
vercel login
vercel link
```

3. **使用自动同步脚本**

**Python 版本**（推荐）：
```bash
python sync_env_to_vercel.py
```

**PowerShell 版本**（Windows）：
```powershell
.\sync_env_to_vercel.ps1
```

4. **重新部署**
```bash
vercel --prod
```

详细说明请查看 [setup_vercel.md](setup_vercel.md) 和 [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md)

## 🔍 故障排查

### 页面显示"暂无内容"

1. **检查环境变量**
   - 确保在 Vercel 中正确配置了所有环境变量
   - 变量名要完全一致（区分大小写）

2. **测试 API 连接**
   访问 `/api/refresh` 端点：
   ```
   https://你的域名.vercel.app/api/refresh
   ```
   
   正常响应示例：
   ```json
   {
     "success": true,
     "count": 5
   }
   ```
   
   如果 `count` 为 0，说明：
   - 飞书 API 凭据可能不正确
   - 多维表格中可能没有数据
   - 字段名称可能不匹配

3. **查看部署日志**
   - 在 Vercel Dashboard 中查看 Function Logs
   - 查找错误信息

### 常见错误

- **401 Unauthorized**: 检查 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`
- **404 Not Found**: 检查 `BASE_ID` 和 `TABLE_ID`
- **空数据**: 确保多维表格中有数据且字段名匹配

## 📁 项目结构

```
qingyun_digest/
├── .env                    # 环境变量（不提交到 Git）
├── .env.example           # 环境变量示例
├── .gitignore             # Git 忽略文件
├── .vercelignore          # Vercel 忽略文件
├── app.py                 # Flask 主应用
├── config.py              # 配置文件
├── wsgi.py                # WSGI 入口
├── vercel.json            # Vercel 配置
├── requirements.txt       # Python 依赖
├── README.md              # 项目说明
├── VERCEL_DEPLOY.md       # Vercel 部署详细说明
├── setup_vercel.md        # Vercel CLI 使用指南
├── sync_env_to_vercel.py  # 环境变量同步脚本（Python）
├── sync_env_to_vercel.ps1 # 环境变量同步脚本（PowerShell）
├── static/                # 静态文件
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/             # HTML 模板
    ├── base.html
    ├── index.html
    └── detail.html
```

## 🔒 安全注意事项

1. **永远不要将 `.env` 文件提交到 Git**
   - `.env` 已在 `.gitignore` 中
   - 只提交 `.env.example` 作为模板

2. **使用环境变量管理敏感信息**
   - 本地开发使用 `.env` 文件
   - Vercel 部署使用环境变量配置
   - 不要在代码中硬编码密钥

3. **定期更新密钥**
   - 定期轮换飞书应用密钥
   - 更新后同步到 Vercel

## 🎯 API 端点

- `GET /` - 首页，显示文章列表
- `GET /article/<article_id>` - 文章详情页
- `GET /api/refresh` - 刷新缓存并返回文章数量

## 📝 开发建议

1. **本地开发**
   - 使用 Flask 调试模式（`DEBUG=True`）
   - 修改代码后自动重载

2. **数据管理**
   - 在飞书多维表格中编辑内容
   - 缓存 5 分钟后自动刷新
   - 可手动访问 `/api/refresh` 立即刷新

3. **性能优化**
   - 已实现内存缓存机制
   - 可调整 `CACHE_TIMEOUT` 控制缓存时间

## 🚧 后续优化方向

- [ ] 添加文章分类功能
- [ ] 实现搜索功能
- [ ] 添加分页功能
- [ ] 优化移动端体验
- [ ] 添加 RSS 订阅
- [ ] 支持 Markdown 渲染

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**更新时间**: 2025-12-23
