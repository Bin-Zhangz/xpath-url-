import requests  
from lxml import etree  
from concurrent.futures import ThreadPoolExecutor  
  
def fetch_and_extract_url(url):  
    try:  
        response = requests.get(url)  
        response.raise_for_status()  
        wb_data = response.text  
        html = etree.HTML(wb_data)  
        # 假设这里是我们想要提取的XPath  
        td_text = html.xpath('//*[@id="tblBody1"]/tbody/tr[29]/td[2]/text()')  
        if td_text:  
            return td_text[0].strip()  
    except (requests.RequestException, etree.XPathError) as e:  
        print(f"Error fetching or parsing URL {url}: {e}")  
    return None  
  
def main():  
    result_urls = []  
      
    # 假设urls_file_path是包含URL列表的文件路径  
    urls_file_path = 'D:/test.txt'  
      
    # 读取文件中的所有URL  
    with open(urls_file_path, 'r', encoding='utf-8') as file:  
        urls = [line.strip() for line in file.readlines()]  
      
    # 使用线程池并发处理URL  
    with ThreadPoolExecutor(max_workers=10) as executor:  
        futures = [executor.submit(fetch_and_extract_url, url) for url in urls]  
        for future in futures:  
            result_url = future.result()  
            if result_url:  
                result_urls.append(result_url)  
      
    # 将提取的URL写入文件  
    result_urls_file_path = 'D:/result_urls.txt'  
    with open(result_urls_file_path, 'w', encoding='utf-8') as file:  
        for url in result_urls:  
            file.write(url + '\n')  
      
    print("URLs have been saved to result_urls.txt")  
  
if __name__ == "__main__":  
    main()


