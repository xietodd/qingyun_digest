#!/usr/bin/env python3
"""
Vercel 环境变量同步工具
读取 .env 文件并同步到 Vercel
"""

import os
import subprocess
import sys
from pathlib import Path

def check_vercel_cli():
    """检查 Vercel CLI 是否安装"""
    try:
        subprocess.run(['vercel', '--version'], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def read_env_file(env_path='.env'):
    """读取 .env 文件"""
    env_vars = {}
    
    if not os.path.exists(env_path):
        return None
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            
            # 解析 KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars

def sync_to_vercel(key, value, environments=['production', 'preview', 'development']):
    """同步单个环境变量到 Vercel"""
    success = True
    
    for env in environments:
        try:
            # 使用 echo 和管道传递值
            process = subprocess.Popen(
                ['vercel', 'env', 'add', key, env],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 发送值并关闭输入
            stdout, stderr = process.communicate(input=value)
            
            if process.returncode != 0:
                # 如果变量已存在，尝试更新
                if 'already exists' in stderr.lower():
                    print(f"  ⚠️  {key} 在 {env} 环境已存在，跳过")
                else:
                    print(f"  ❌ {key} 同步到 {env} 失败: {stderr}")
                    success = False
            else:
                print(f"  ✅ {key} → {env}")
                
        except Exception as e:
            print(f"  ❌ {key} 同步到 {env} 出错: {e}")
            success = False
    
    return success

def main():
    print("=" * 50)
    print("Vercel 环境变量同步工具")
    print("=" * 50)
    print()
    
    # 检查 Vercel CLI
    print("🔍 检查 Vercel CLI...")
    if not check_vercel_cli():
        print("❌ 未检测到 Vercel CLI")
        print()
        print("请先安装 Vercel CLI:")
        print("  npm install -g vercel")
        print()
        print("然后登录并链接项目:")
        print("  vercel login")
        print("  vercel link")
        print()
        sys.exit(1)
    
    print("✅ Vercel CLI 已安装")
    print()
    
    # 读取 .env 文件
    print("📖 读取 .env 文件...")
    env_vars = read_env_file('.env')
    
    if env_vars is None:
        print("❌ 未找到 .env 文件")
        print("请确保 .env 文件存在于当前目录")
        sys.exit(1)
    
    if not env_vars:
        print("⚠️  .env 文件为空")
        sys.exit(0)
    
    print(f"✅ 找到 {len(env_vars)} 个环境变量")
    print()
    
    # 显示将要同步的变量
    print("📋 将要同步的变量:")
    for key in env_vars.keys():
        masked_value = '*' * 20
        print(f"  • {key} = {masked_value}")
    print()
    
    # 确认
    confirm = input("是否继续同步到 Vercel? (y/n): ")
    if confirm.lower() not in ['y', 'yes']:
        print("已取消")
        sys.exit(0)
    
    print()
    print("🚀 开始同步...")
    print()
    
    # 同步每个变量
    success_count = 0
    fail_count = 0
    
    for key, value in env_vars.items():
        print(f"📤 同步 {key}...")
        if sync_to_vercel(key, value):
            success_count += 1
        else:
            fail_count += 1
        print()
    
    # 总结
    print("=" * 50)
    print("同步完成!")
    print("=" * 50)
    print(f"✅ 成功: {success_count}")
    print(f"❌ 失败: {fail_count}")
    print()
    
    if success_count > 0:
        print("📝 下一步:")
        print("1. 运行 'vercel env ls' 查看所有环境变量")
        print("2. 运行 'vercel --prod' 重新部署到生产环境")
        print()

if __name__ == '__main__':
    main()
