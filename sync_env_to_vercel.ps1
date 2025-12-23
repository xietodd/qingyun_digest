# Vercel 环境变量同步脚本
# 此脚本会读取 .env 文件并将变量同步到 Vercel

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Vercel 环境变量同步工具" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否安装了 Vercel CLI
Write-Host "检查 Vercel CLI..." -ForegroundColor Yellow
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue

if (-not $vercelInstalled) {
    Write-Host "❌ 未检测到 Vercel CLI" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装 Vercel CLI:" -ForegroundColor Yellow
    Write-Host "  npm install -g vercel" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ Vercel CLI 已安装" -ForegroundColor Green
Write-Host ""

# 检查 .env 文件是否存在
if (-not (Test-Path ".env")) {
    Write-Host "❌ 未找到 .env 文件" -ForegroundColor Red
    Write-Host "请确保 .env 文件存在于当前目录" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ 找到 .env 文件" -ForegroundColor Green
Write-Host ""

# 读取 .env 文件
Write-Host "读取环境变量..." -ForegroundColor Yellow
$envVars = @{}
Get-Content ".env" | ForEach-Object {
    $line = $_.Trim()
    # 跳过空行和注释
    if ($line -and -not $line.StartsWith("#")) {
        $parts = $line -split "=", 2
        if ($parts.Length -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            $envVars[$key] = $value
        }
    }
}

Write-Host "找到 $($envVars.Count) 个环境变量" -ForegroundColor Green
Write-Host ""

# 显示将要同步的变量（隐藏值）
Write-Host "将要同步的变量:" -ForegroundColor Cyan
foreach ($key in $envVars.Keys) {
    $maskedValue = "*" * 20
    Write-Host "  - $key = $maskedValue" -ForegroundColor White
}
Write-Host ""

# 确认
$confirm = Read-Host "是否继续同步到 Vercel? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "已取消" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "开始同步..." -ForegroundColor Yellow
Write-Host ""

# 同步每个变量
$successCount = 0
$failCount = 0

foreach ($key in $envVars.Keys) {
    $value = $envVars[$key]
    
    Write-Host "同步 $key..." -ForegroundColor Cyan
    
    # 使用 echo 和管道将值传递给 vercel env add
    # 为 production, preview, development 环境都添加
    try {
        # 创建临时文件存储值
        $tempFile = [System.IO.Path]::GetTempFileName()
        $value | Out-File -FilePath $tempFile -Encoding utf8 -NoNewline
        
        # 添加到 production
        $result = Get-Content $tempFile | vercel env add $key production 2>&1
        
        # 添加到 preview
        $result = Get-Content $tempFile | vercel env add $key preview 2>&1
        
        # 添加到 development
        $result = Get-Content $tempFile | vercel env add $key development 2>&1
        
        # 删除临时文件
        Remove-Item $tempFile -Force
        
        Write-Host "  ✅ $key 同步成功" -ForegroundColor Green
        $successCount++
    }
    catch {
        Write-Host "  ❌ $key 同步失败: $_" -ForegroundColor Red
        $failCount++
    }
    
    Write-Host ""
}

# 总结
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "同步完成!" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "成功: $successCount" -ForegroundColor Green
Write-Host "失败: $failCount" -ForegroundColor Red
Write-Host ""

if ($successCount -gt 0) {
    Write-Host "下一步:" -ForegroundColor Yellow
    Write-Host "1. 运行 'vercel env ls' 查看所有环境变量" -ForegroundColor White
    Write-Host "2. 运行 'vercel --prod' 重新部署到生产环境" -ForegroundColor White
    Write-Host ""
}
