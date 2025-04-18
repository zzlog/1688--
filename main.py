"""
1688商品信息采集工具
环境要求：Python 3.6+ 
依赖库：requests, beautifulsoup4, pandas, pyinstaller(用于编译)
"""
import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.1688.com/'
    }
    
    try:
        # 发送请求（建议添加代理和延迟）
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 解析商品信息
        product = {
            '标题': soup.find('h1', class_='d-title').get_text(strip=True) if soup.find('h1', class_='d-title') else '',
            '价格': re.search(r'"offerPrice":(\d+\.\d+)', response.text).group(1) if re.search(r'"offerPrice":(\d+\.\d+)', response.text) else '',
            '销量': soup.find('span', class_='sale-num').get_text(strip=True) if soup.find('span', class_='sale-num') else '',
            '库存': re.search(r'"quantity":(\d+)', response.text).group(1) if re.search(r'"quantity":(\d+)', response.text) else '',
            '规格': [spec.get_text(strip=True) for spec in soup.select('.obj-spec li')],
            '主图': [img['src'] for img in soup.select('.vertical-img img')][0] if soup.select('.vertical-img img') else '',
            '详情页': url
        }
        return product
    except Exception as e:
        print(f'采集失败: {str(e)}')
        return None

def main():
    input_url = input("请输入1688商品链接：")
    
    # 获取商品数据
    product_data = get_product_info(input_url)
    
    if product_data:
        # 保存到Excel
        df = pd.DataFrame([product_data])
        df.to_excel(f'product_{int(time.time())}.xlsx', index=False)
        print("采集成功！数据已保存至当前目录")
    else:
        print("未能获取商品信息")

if __name__ == "__main__":
    main()
