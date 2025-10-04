# 🚀 Vercel部署指南

替代Netlify，使用Vercel部署前端（更适合个人项目）

---

## 为什么选择Vercel？

- ✅ **免费层更慷慨** - 100GB带宽/月（Netlify只有100GB）
- ✅ **更好的性能** - 全球边缘网络
- ✅ **零配置** - 自动检测项目类型
- ✅ **GitHub集成** - 自动部署
- ✅ **自定义域名** - 免费HTTPS

---

## 📦 方法1: Vercel Dashboard部署（最简单）

### 步骤1: 推送代码到GitHub
```bash
# 已完成！代码在 https://github.com/duel512/cv-agent.git
```

### 步骤2: 连接Vercel
1. 访问 https://vercel.com
2. 点击 "Add New" → "Project"
3. 连接GitHub账号
4. 选择 `cv-agent` 仓库
5. 配置：
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`（点击Edit，选择frontend目录）
   - **Build Command**: 留空
   - **Output Directory**: `.`（当前目录）
6. 点击 "Deploy"

### 步骤3: 获取URL
- 部署完成后，Vercel会给你一个URL
- 例如: `https://cv-agent-duel512.vercel.app`

---

## 📦 方法2: Vercel CLI部署（更快）

### 安装Vercel CLI
```bash
npm i -g vercel
```

### 登录Vercel
```bash
vercel login
```

### 部署
```bash
cd /Users/ruomushao/Documents/Projects_Py/CV_agent

# 部署到生产环境
vercel --prod --cwd frontend
```

### 配置
CLI会问你几个问题：
```
? Set up and deploy "~/cv-agent/frontend"? [Y/n] y
? Which scope? Your Username
? Link to existing project? [y/N] n
? What's your project's name? cv-agent
? In which directory is your code located? ./
? Want to override the settings? [y/N] n
```

完成后会得到部署URL！

---

## 🔧 方法3: 使用vercel.json配置（推荐）

我已经创建了 `vercel.json` 配置文件，它会：
- ✅ 自动设置输出目录为 `frontend`
- ✅ 配置SPA路由（所有路径指向index.html）
- ✅ 添加安全头
- ✅ 优化性能

### 使用配置文件部署
```bash
# 在项目根目录
vercel --prod
```

Vercel会自动读取 `vercel.json` 并正确配置！

---

## ⚙️ 重要：更新Railway后端URL

部署后端到Railway后，更新 `frontend/app.js`：

```javascript
// 将这行：
: 'https://your-railway-app.up.railway.app';

// 改为你的实际Railway URL：
: 'https://cv-agent-production-xxxx.up.railway.app';
```

然后重新部署：
```bash
git add .
git commit -m "Update Railway backend URL"
git push origin main
# Vercel会自动重新部署
```

---

## 🌐 自定义域名（可选）

### 在Vercel添加自定义域名

1. 在Vercel项目设置中，点击 "Domains"
2. 添加你的域名（例如：`ruomushao.com`）
3. 按照指示配置DNS：
   ```
   Type: CNAME
   Name: @
   Value: cname.vercel-dns.com
   ```

### 推荐域名注册商
- **Namecheap** - $8-12/年
- **Cloudflare** - 成本价（最便宜）
- **GoDaddy** - 常有优惠

---

## 🔄 自动部署工作流

配置后，每次push到GitHub，Vercel会：
1. ✅ 自动检测更改
2. ✅ 构建并部署
3. ✅ 运行健康检查
4. ✅ 更新生产URL

**零手动操作！**

---

## 📊 对比：Vercel vs Netlify

| 特性 | Vercel | Netlify |
|------|--------|---------|
| **免费带宽** | 100GB/月 | 100GB/月 |
| **构建时间** | 6000分钟/月 | 300分钟/月 |
| **部署速度** | 非常快 | 快 |
| **GitHub集成** | ✅ | ✅ |
| **边缘网络** | ✅ 全球 | ✅ 全球 |
| **自定义域名** | ✅ 免费HTTPS | ✅ 免费HTTPS |
| **商业用途** | ✅ 允许 | ✅ 允许 |
| **Serverless函数** | ✅ | ✅ |
| **分析** | ✅ 付费 | ✅ 付费 |

**结论**: 都很好，Vercel在构建时间上更慷慨

---

## 🐛 常见问题

### 问题1: 部署后显示404
**解决**:
- 检查 `vercel.json` 中的 `outputDirectory` 是否为 `frontend`
- 或在Vercel Dashboard设置中指定Root Directory为 `frontend`

### 问题2: API调用失败（CORS错误）
**解决**:
```bash
# 在Railway中确保CORS设置正确
railway variables set CORS_ORIGINS=*
# 或设置为具体的Vercel URL
railway variables set CORS_ORIGINS=https://your-app.vercel.app
```

### 问题3: 更新代码后没有生效
**解决**:
```bash
# 强制重新部署
vercel --prod --force
```

---

## ✅ 部署清单

部署前检查：
- [ ] 代码已push到GitHub
- [ ] Railway后端已部署并获得URL
- [ ] 更新了 `frontend/app.js` 中的后端URL
- [ ] Vercel账号已创建
- [ ] 已连接GitHub到Vercel

部署后检查：
- [ ] 前端能正常加载
- [ ] 能与后端通信
- [ ] 聊天功能正常
- [ ] 移动端显示正常
- [ ] 无CORS错误

---

## 📝 快速部署命令

```bash
# 1. 部署Railway后端
cd /Users/ruomushao/Documents/Projects_Py/CV_agent
railway login
railway init
railway up
railway domain  # 获取后端URL

# 2. 更新前端API URL
# 编辑 frontend/app.js，替换Railway URL

# 3. 提交更改
git add .
git commit -m "Update backend URL"
git push origin main

# 4. 部署Vercel前端
vercel login
vercel --prod

# 完成！🎉
```

---

## 🔗 有用的链接

- Vercel Dashboard: https://vercel.com/dashboard
- Vercel文档: https://vercel.com/docs
- Railway Dashboard: https://railway.app/dashboard
- 你的GitHub仓库: https://github.com/duel512/cv-agent

---

## 🎉 完成后

你会得到：
- ✅ **前端URL**: `https://cv-agent-xxx.vercel.app`
- ✅ **后端URL**: `https://cv-agent-xxx.up.railway.app`
- ✅ **GitHub仓库**: `https://github.com/duel512/cv-agent`

把前端URL添加到简历上：
```
🤖 AI Assistant: https://cv-agent-xxx.vercel.app
与我的AI助手聊天，了解我的背景和技能！
```

搞定！🚀
