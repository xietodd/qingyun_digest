# 使用 Vercel CLI 自动同步环境变量

## 方法一：使用 Vercel CLI（推荐）

### 1. 安装 Vercel CLI

```bash
npm install -g vercel
```

### 2. 登录 Vercel

```bash
vercel login
```

### 3. 链接项目

在项目目录中运行：

```bash
vercel link
```

按照提示选择：
- 选择你的团队/账户
- 选择现有项目 `qingyun_digest`

### 4. 从本地 .env 文件同步环境变量到 Vercel

```bash
vercel env pull .env.production
```

这会从 Vercel 拉取现有的环境变量。

### 5. 推送本地环境变量到 Vercel

```bash
# 将 .env 文件中的变量推送到 Vercel 的 production 环境
vercel env add FEISHU_APP_ID production < .env
```

或者使用交互式方式添加：

```bash
vercel env add FEISHU_APP_ID
# 然后输入值：cli_a9cc3ceff378dbc8
# 选择环境：Production, Preview, Development (全选)
```

重复以上步骤添加其他变量：
- `FEISHU_APP_SECRET`
- `BASE_ID`
- `TABLE_ID`

### 6. 验证环境变量

```bash
vercel env ls
```

### 7. 重新部署

```bash
vercel --prod
```

---

## 方法二：使用脚本批量导入（更简单）

我已经为你创建了一个自动化脚本 `sync_env_to_vercel.ps1`，运行它可以自动将 .env 文件中的所有变量同步到 Vercel。

### 使用方法：

1. 确保已安装 Vercel CLI 并登录
2. 确保已链接项目（`vercel link`）
3. 运行脚本：

```powershell
.\sync_env_to_vercel.ps1
```

---

## 方法三：手动在 Vercel Dashboard 配置（最简单但需要手动操作）

如果你不想使用 CLI，可以：

1. 访问 https://vercel.com/dashboard
2. 选择项目 `qingyun_digest`
3. Settings → Environment Variables
4. 手动添加每个变量

---

## 注意事项

⚠️ **永远不要将 .env 文件提交到 Git**

- `.env` 已经在 `.gitignore` 中
- `.vercelignore` 也会阻止它被上传到 Vercel
- 只有 `.env.example` 应该被提交（不包含真实密钥）

✅ **正确的工作流程**

1. 本地开发时使用 `.env` 文件
2. 使用 Vercel CLI 或 Dashboard 配置生产环境变量
3. 只将代码和 `.env.example` 提交到 GitHub
4. Vercel 从其自己的环境变量系统读取配置

---

## 为什么这样做？

1. **安全性**：密钥不会暴露在 GitHub 上
2. **灵活性**：不同环境可以使用不同的配置
3. **团队协作**：团队成员可以有自己的本地配置
4. **最佳实践**：符合 12-Factor App 原则
