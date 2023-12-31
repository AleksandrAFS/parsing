import requests, re, json
from bs4 import BeautifulSoup
from time import perf_counter

class parsing:
    r"""
        f_html - html файл, по ссылкам которого будет запрашиваться информация.  
        По умолчанию = C:\Users\User\www.html
        __head - защита от бана, во время запроса(лучше не изменять) 
        search - поиск ссылок в html файле по запросу (class_ = search). 
        По умолчанию = pep reference external
    """
       
    __head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0 (Edition Yx 05)"
              }
    
    def __init__(
                 self, f_html: str = r'C:\Users\User\www.htm', 
                 search: str ='pep reference external'
                 ) -> None:
        self.f_html = f_html
        self.search = search
        
    def __call__(
                 self, full: int = 10, 
                 request: str = 'python', js: str = r'C:\Users\User\infos_p.json'
                 ) -> str:
        
        r"""
           full - максимальное количество запросов по ссылкам из html кода, 
           который находиться в файле self.f_html. По умолчанию = 10
           request - ключевое слово для поиска информации. По умолчанию = 'python'
           js - путь к json файлу, в который будет записываться 
           информация. По умолчанию = C:\Users\User\infos_p.json
        """
        
        
        try:
            start = perf_counter()
            self.pars(full, request, js)
            print(f"Получение данных успешно завершилось!\
                    \nВы можете найти результат в файле: {js}")
            self.infos = js
                
        except Exception as e:
            print(f'Ошибка: {e.__class__.__name__}({e})')
        finally:
            print(f'Затрачено времени: {perf_counter() - start}')
            return js
            
    def pars(self, full: int, request: str, js: str) -> None:
        """метод для парсинга"""
        
        with (
              open(self.f_html, encoding='utf-8') as file,
              open(js, 'a', encoding='utf-8') as js_fil
               ):
                 now = file.read()
                 soup = BeautifulSoup(now, "lxml")
                 fiends = soup.find_all(class_=self.search)
                 islen = len(fiends)
                 for value in fiends:
                    if not full: break
   
                    url = value.get("href")
                    texts = requests.get(url, headers=self.__head).text
           
                    goto = BeautifulSoup(texts, "lxml")
                    info = goto.find("p", text=re.compile(request, flags=re.I))
                    if not info is None:
                        json.dump(info.text.split('\n'), js_fil, indent=4)
                    full -= 1
                    islen -= 1
                    print(f'Обработка...\nОсталось: {min([full, islen])}')
    
    def clear(self) -> None:
        with open(self.infos, 'w', encoding='utf-8'): 
            pass
        print("Файл очищен от информации")
