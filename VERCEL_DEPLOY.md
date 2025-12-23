# Vercel 部署说明

## 问题诊断

如果你的 Vercel 部署页面显示空白或没有数据，请按照以下步骤检查：

## 1. 配置环境变量

在 Vercel 项目设置中添加以下环境变量：

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择你的项目 `qingyun_digest`
3. 进入 **Settings** → **Environment Variables**
4. 添加以下变量：

```
FEISHU_APP_ID=cli_a9cc3ceff378dbc8
FEISHU_APP_SECRET=wB5PROmvIchqqTHmPfSyMd42UI6aeMBm
BASE_ID=Im3rwDEf1izTM4kR5U8ckOecnNe
TABLE_ID=tblM4pjgkvgmuihk
DEBUG=False
CACHE_TIMEOUT=300
```

**重要：** 确保这些环境变量应用到 **Production**、**Preview** 和 **Development** 环境。

## 2. 重新部署

配置环境变量后，需要重新部署：

1. 在 Vercel Dashboard 中，进入 **Deployments** 页面
2. 点击最新的部署
3. 点击右上角的 **Redeploy** 按钮
4. 选择 **Redeploy with existing Build Cache** 或 **Redeploy without Cache**

## 3. 检查部署日志

如果仍然有问题，检查部署日志：

1. 在 Vercel Dashboard 中，进入 **Deployments** 页面
2. 点击最新的部署
3. 查看 **Build Logs** 和 **Function Logs**
4. 查找任何错误信息

常见错误：
- `ModuleNotFoundError`: 检查 `requirements.txt` 是否包含所有依赖
- `401 Unauthorized`: 检查飞书 API 凭据是否正确
- `404 Not Found`: 检查 BASE_ID 和 TABLE_ID 是否正确

## 4. 测试飞书 API 连接

你可以访问以下 URL 来刷新缓存并测试 API 连接：

```
https://qingyun-digest.vercel.app/api/refresh
```

这应该返回类似以下的 JSON 响应：
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

## 5. 验证飞书多维表格字段

确保你的飞书多维表格包含以下字段：
- **标题** (必需)
- **金句输出** (可选)
- **黄叔点评** (可选)
- **概要内容输出** (可选)

## 6. 本地测试

在推送到 GitHub 之前，先在本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

访问 `http://localhost:5000` 查看是否能正常显示数据。

## 常见问题

### Q: 页面显示"暂无内容"
A: 
1. 检查环境变量是否正确配置
2. 检查飞书多维表格中是否有数据
3. 访问 `/api/refresh` 查看返回的 count 数量

### Q: 部署成功但页面报错
A: 
1. 查看 Vercel Function Logs
2. 确保 Python 版本兼容（Vercel 默认使用 Python 3.9）
3. 检查是否有缺失的依赖包

### Q: 静态文件（CSS/JS）无法加载
A: 
1. 检查 `vercel.json` 中的路由配置
2. 确保 `static` 文件夹已提交到 Git

## 快速修复步骤

1. **立即执行：** 在 Vercel 中配置环境变量
2. **重新部署：** 触发新的部署
3. **测试 API：** 访问 `/api/refresh` 端点
4. **查看日志：** 如果还有问题，查看 Function Logs

---

更新时间：2025-12-23
