---
name: govb-fetcher
description: 地方政府采购商机自动抓取工具（非军队采购）。从北京中建云智等地方政府采购平台抓取招标公告，按关键词过滤，补全采购人、代理机构、预算、时间节点等详情，生成 Excel 报表。当用户说"政府采购商机"、"地方政府采购"、"地方招标"、"北京政府采购"、"政府商机"时触发。与 milb-fetcher（军队采购）互补，milb-fetcher 负责军工/军队渠道，本工具负责地方政府渠道。
metadata: {"openclaw":{"emoji":"🏛️","requires":{govb-fetcher},"install":"uv pip install -e {baseDir}"}}
---

## govb-fetcher 使用说明

### 快速开始

```bash
# 首次使用：写入登录凭证
govb-fetcher --set-cookie --bearer "Bearer xxx" --session "YGCG_TBSESSION=xxx; JSESSIONID=xxx; jcloud_alb_route=xxx"

# 抓取今日数据
govb-fetcher --today

# 快速预览（跳过详情补全）
govb-fetcher --today --no-detail
```

---

### 日期选项

```bash
govb-fetcher                        # 默认抓取今日
govb-fetcher --today                # 抓取今日
govb-fetcher --yesterday            # 抓取昨日
govb-fetcher --date 2026-03-30      # 抓取指定日期
```

---

### 过滤参数

```bash
--keywords "关键词1,关键词2"              # 覆盖默认核心关键词
--exclude-keywords "排除词1,排除词2"     # 覆盖默认排除关键词
--high-value-keywords "高价值词1,词2"    # 覆盖高价值关键词（影响推荐等级）
```

---

### 输出控制

```bash
--output /path/to/output.xlsx       # 指定输出路径
--no-detail                         # 跳过详情 API，仅保存列表字段（更快）
```

---

### 凭证管理

登录凭证（Cookie / Bearer token）存储在 `.env` 文件中，有两种更新方式：

**方式一：命令行更新**
```bash
govb-fetcher --set-cookie \
  --bearer "Bearer 847f6d92-cce8-4f1a-a481-20bc93535219" \
  --session "YGCG_TBSESSION=ba4d5bad-xxx; JSESSIONID=8A2E7F...; jcloud_alb_route=600a4a10..."
```

**方式二：手动编辑 `.env`**
复制 `.env.example` 为 `.env` 后修改：
```
FETCHER_BEARER_TOKEN=your-token
FETCHER_YGCG_TBSESSION=your-session-id
FETCHER_JSESSIONID=your-jsessionid
```

> 运行期间服务器下发的新 `YGCG_TBSESSION` 会自动写回 `.env`，无需手动更新。

---

### 配置文件

| 环境变量 | 用途 | 默认值 |
|---------|------|--------|
| `FETCHER_BEARER_TOKEN` | Bearer 认证 token | 无（必填）|
| `FETCHER_YGCG_TBSESSION` | 会话 Cookie | 无（必填）|
| `FETCHER_JSESSIONID` | Java Session ID | 无（必填）|
| `FETCHER_JCT_ALB_ROUTE` | 负载均衡路由 | 固定值 |
| `FETCHER_KEYWORDS` | 核心关键词 | 体系,模型,仿真,数据... |
| `FETCHER_EXCLUDE_KEYWORDS` | 排除关键词 | 医疗,药品,工程... |
| `FETCHER_HIGH_VALUE_KEYWORDS` | 高价值关键词（影响推荐等级）| 模型,AI,软件... |
| `FETCHER_OUTPUT_DIR` | Excel 输出目录 | `~/.openclaw/workspace/govb-fetcher` |

配置文件搜索顺序（高优先级在前）：
1. 当前目录 `.env`
2. `~/.config/govb-fetcher/.env`

---

### Excel 字段说明

| 列 | 说明 |
|----|------|
| 项目名称 | 公告标题 |
| 标段名称 | 分包/标段名称 |
| 招标方式 | 公开招标 / 竞争性磋商等 |
| 预算金额 | 项目预算 |
| 文件获取开始/截止时间 | 招标文件领取时间窗口 |
| 开标时间 | 开标/截止投标时间 |
| 采购人 / 电话 | 甲方信息 |
| 代理机构 / 电话 | 招标代理机构信息 |
| 项目概况 | 项目简述（前100字）|
| 详情链接 | 直接跳转到平台详情页 |
| 推荐等级 | 高 / 中 / 空，基于关键词评级 |
| 备注 | 自动生成的跟进建议 |

推荐等级规则：
- **高**：含高价值关键词（模型/仿真/数据/AI/软件等）或"意向"
- **中**：含"系统"关键词
- **空**：其他匹配项
