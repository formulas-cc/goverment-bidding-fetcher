import requests
import json
from datetime import datetime, date

url = "http://zbcg-bjzc.zhongcy.com/gt-jy-toubiao/api/cggg/gonggao/queryZBGongGaoList.do"

# 指定采集日期（默认今日）
TARGET_DATE = date.today()
day_start = int(datetime(TARGET_DATE.year, TARGET_DATE.month, TARGET_DATE.day, 0, 0, 0).timestamp() * 1000)
day_end   = int(datetime(TARGET_DATE.year, TARGET_DATE.month, TARGET_DATE.day, 23, 59, 59).timestamp() * 1000)
print(f"采集日期: {TARGET_DATE}  时间戳范围: {day_start} ~ {day_end}")

# Session 自动管理 Cookie
session = requests.Session()
session.cookies.update({
    "YGCG_TBSESSION": "ba4d5bad-144a-4732-b5cb-cf2f85fad735",
    "JSESSIONID": "8A2E7F290DF882F672E206848FBB9BA7",
    "jcloud_alb_route": "600a4a10e7715683b0907d3450d289fc",
})
session.headers.update({
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Authorization": "Bearer 847f6d92-cce8-4f1a-a481-20bc93535219",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://zbcg-bjzc.zhongcy.com",
    "Pragma": "no-cache",
    "Referer": "http://zbcg-bjzc.zhongcy.com/bjczj-jy-toubiao/index.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "contentType": "formType",
})


def refresh_session_cookie():
    """清除重复的 YGCG_TBSESSION，保留最新值"""
    values = [c.value for c in session.cookies if c.name == "YGCG_TBSESSION"]
    if len(values) > 1:
        latest = values[-1]
        others = [c for c in session.cookies if c.name != "YGCG_TBSESSION"]
        session.cookies.clear()
        for c in others:
            session.cookies.set(c.name, c.value)
        session.cookies.set("YGCG_TBSESSION", latest)


def fetch_page(page, rows=100):
    data = {
        "ggName": "", "gcBH": "", "gcName": "",
        "bdBH": "", "bdName": "", "xmStatus": "",
        "page": str(page), "rows": str(rows),
    }
    response = session.post(url, data=data, timeout=10)
    refresh_session_cookie()
    return response.json()


# 逐页拉取，遇到超出今日范围的记录则停止
results = []
page = 1

while True:
    print(f"正在请求第 {page} 页...", end=" ")
    result = fetch_page(page)

    if not result.get("success") or not result.get("data", {}).get("rows"):
        print("无数据，停止")
        break

    rows = result["data"]["rows"]
    print(f"共 {len(rows)} 条")

    today_rows = []
    stop = False
    for row in rows:
        ts = row.get("ggStartTime")
        if ts is None:
            continue
        if ts < day_start:
            # 数据按时间倒序，一旦出现早于今日的记录即可停止翻页
            stop = True
            break
        if day_start <= ts <= day_end:
            today_rows.append(row)

    results.extend(today_rows)

    if stop or len(rows) < 100:
        break

    page += 1

print(f"\n今日（{TARGET_DATE}）共采集到 {len(results)} 条公告")
print(json.dumps(results, ensure_ascii=False, indent=2))
