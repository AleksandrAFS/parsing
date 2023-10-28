from fake_useragent import UserAgent
import requests, re

def main() -> None:
    ls = UserAgent()
    with (
        open(r"путь_к_файлу_с_прокси", 'rt') as ns,
        open(r"путь_к_файлу_куда_будет_запись_рабочих", 'a') as goto
    ):
        for prox in ns:
            if not (prox := re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', prox)):
                continue
            ip = prox.group()
            try:
                requests.get(url="http://httpbin.org/ip", proxies={
                    'http': f'http://{ip}',
                    'https': f'https://{ip}',
                }, headers={
                        'User-Agent': ls.random,                  
                        'Accept': 'text/html,application/xhtml+xml', 
                        'Connection': 'keep-alive'                  
                }, timeout=5)
            except Exception as e:
                print(f"Прокси: {ip} - не подходит, ошибка: {e.__class__.__name__}")
            else:
                print(f"Прокси {ip} - подходит")
                print(ip, file=goto)

if __name__ == '__main__':
    main()
