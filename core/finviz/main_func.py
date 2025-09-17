from datetime import datetime

from lxml import etree

from .helper_functions.request_functions import http_request_get
from .helper_functions.scraper_functions import get_table

STOCK_URL = "https://finviz.com/quote.ashx"
NEWS_URL = "https://finviz.com/news.ashx"
CRYPTO_URL = "https://finviz.com/crypto_performance.ashx"
STOCK_PAGE = {}


def get_page(ticker):
    global STOCK_PAGE

    if ticker not in STOCK_PAGE:
        STOCK_PAGE[ticker], _ = http_request_get(
            url=STOCK_URL, payload={"t": ticker}, parse=True
        )


def get_stock(ticker):
    """
    Returns a dictionary containing stock data.

    :param ticker: stock symbol
    :type ticker: str
    :return dict
    """

    get_page(ticker)
    page_parsed = STOCK_PAGE[ticker]

    # 获取基本信息 - 使用新的页面结构
    data = {}
    
    # 获取股票代码
    ticker_element = page_parsed.cssselect('.quote-header_ticker-wrapper_ticker')
    if ticker_element:
        data["Ticker"] = ticker_element[0].text.strip()
    
    # 获取公司名称
    company_element = page_parsed.cssselect('.quote-header_ticker-wrapper_company a')
    if company_element:
        data["Company"] = company_element[0].text.strip()
        company_link = company_element[0].get("href")
        data["Website"] = company_link if company_link and company_link.startswith("http") else None
    
    # 获取行业信息 - 从标签链接中提取
    tab_links = page_parsed.cssselect('.tab-link')
    for link in tab_links:
        href = link.get("href", "")
        if "sec_" in href:
            data["Sector"] = link.text.strip()
        elif "ind_" in href:
            data["Industry"] = link.text.strip()
        elif "geo_" in href:
            data["Country"] = link.text.strip()

    # 获取股票数据表格
    all_rows = [
        row.xpath("td//text()")
        for row in page_parsed.cssselect('tr[class="table-dark-row"]')
    ]

    for row in all_rows:
        for column in range(0, len(row) - 1, 2):
            if column + 1 < len(row):
                key = row[column].strip()
                value = row[column + 1].strip()
                
                # 处理特殊情况
                if key == "EPS next Y" and "EPS next Y" in data.keys():
                    data["EPS growth next Y"] = value
                    continue
                elif key == "Volatility":
                    vols = value.split()
                    if len(vols) >= 2:
                        data["Volatility (Week)"] = vols[0]
                        data["Volatility (Month)"] = vols[1]
                    continue
                
                data[key] = value

    return data


def get_insider(ticker):
    """
    Returns a list of dictionaries containing all recent insider transactions.

    :param ticker: stock symbol
    :return: list
    """

    get_page(ticker)
    page_parsed = STOCK_PAGE[ticker]
    outer_table = page_parsed.cssselect('table[class="body-table insider-trading-table"]')

    if len(outer_table) == 0:
        return []

    table = outer_table[0]
    headers = table[0].xpath("td//text()")

    data = [dict(zip(
        headers,
        [etree.tostring(elem, method="text", encoding="unicode") for elem in row]
    )) for row in table[1:]]

    return data


def get_news(ticker):
    """
    Returns a list of sets containing news headline and url

    :param ticker: stock symbol
    :return: list
    """

    get_page(ticker)
    page_parsed = STOCK_PAGE[ticker]
    news_table = page_parsed.cssselect('table[id="news-table"]')

    if len(news_table) == 0:
        return []

    rows = news_table[0].xpath("./tr[not(@id)]")

    results = []
    current_date = None
    
    for row in rows:
        tds = row.xpath("./td")
        if len(tds) < 2:
            continue
            
        # 获取时间文本并清理
        time_text = tds[0].xpath("text()")[0] if tds[0].xpath("text()") else ""
        raw_timestamp = time_text.strip()
        
        # 解析时间格式
        try:
            if "Today" in raw_timestamp:
                # 处理 "Today 06:00AM" 格式
                time_part = raw_timestamp.replace("Today", "").strip()
                parsed_timestamp = datetime.strptime(time_part, "%I:%M%p").replace(
                    year=datetime.now().year,
                    month=datetime.now().month,
                    day=datetime.now().day
                )
                current_date = parsed_timestamp.date()
            elif len(raw_timestamp) > 8 and "-" in raw_timestamp:
                # 处理 "Dec-15-24 06:00AM" 格式
                parsed_timestamp = datetime.strptime(raw_timestamp, "%b-%d-%y %I:%M%p")
                current_date = parsed_timestamp.date()
            else:
                # 处理 "06:00AM" 格式（使用当前日期）
                if current_date is None:
                    current_date = datetime.now().date()
                parsed_timestamp = datetime.strptime(raw_timestamp, "%I:%M%p").replace(
                    year=current_date.year,
                    month=current_date.month,
                    day=current_date.day
                )
        except ValueError:
            # 如果时间解析失败，跳过这条新闻
            continue
        
        # 获取新闻信息
        news_link = tds[1].cssselect('a[class="tab-link-news"]')
        if not news_link:
            continue
            
        title = news_link[0].xpath("text()")[0] if news_link[0].xpath("text()") else ""
        url = news_link[0].get("href", "")
        
        # 获取来源信息
        source_span = tds[1].cssselect('div[class="news-link-right"] span')
        source = source_span[0].xpath("text()")[0][1:] if source_span and source_span[0].xpath("text()") else ""

        results.append((
            parsed_timestamp.strftime("%Y-%m-%d %H:%M"),
            title,
            url,
            source
        ))

    return results


def get_all_news():
    """
    Returns a list of sets containing time, headline and url
    :return: list
    """

    page_parsed, _ = http_request_get(url=NEWS_URL, parse=True)
    all_dates = [
        row.text_content() for row in page_parsed.cssselect('td[class="nn-date"]')
    ]
    all_headlines = [
        row.text_content() for row in page_parsed.cssselect('a[class="nn-tab-link"]')
    ]
    all_links = [
        row.get("href") for row in page_parsed.cssselect('a[class="nn-tab-link"]')
    ]

    return list(zip(all_dates, all_headlines, all_links))


def get_crypto(pair):
    """

    :param pair: crypto pair
    :return: dictionary
    """

    page_parsed, _ = http_request_get(url=CRYPTO_URL, parse=True)
    page_html, _ = http_request_get(url=CRYPTO_URL, parse=False)
    crypto_headers = page_parsed.cssselect('tr[valign="middle"]')[0].xpath("td//text()")
    crypto_table_data = get_table(page_html, crypto_headers)

    return crypto_table_data[pair]


def get_analyst_price_targets(ticker, last_ratings=5):
    """
    Returns a list of dictionaries containing all analyst ratings and Price targets
     - if any of 'price_from' or 'price_to' are not available in the DATA, then those values are set to default 0
    :param ticker: stock symbol
    :param last_ratings: most recent ratings to pull
    :return: list
    """

    analyst_price_targets = []

    try:
        get_page(ticker)
        page_parsed = STOCK_PAGE[ticker]
        table = page_parsed.cssselect(
            'table[class="js-table-ratings fullview-ratings-outer"]'
        )[0]

        for row in table:
            rating = row.xpath("td//text()")
            rating = [val.replace("→", "->").replace("$", "") for val in rating if val != "\n"]
            rating[0] = datetime.strptime(rating[0], "%b-%d-%y").strftime("%Y-%m-%d")

            data = {
                "date": rating[0],
                "category": rating[1],
                "analyst": rating[2],
                "rating": rating[3],
            }
            if len(rating) == 5:
                if "->" in rating[4]:
                    rating.extend(rating[4].replace(" ", "").split("->"))
                    del rating[4]
                    data["target_from"] = float(rating[4])
                    data["target_to"] = float(rating[5])
                else:
                    data["target"] = float(rating[4])

            analyst_price_targets.append(data)
    except Exception as e:
        pass

    return analyst_price_targets[:last_ratings]
