# Traceroute
Вы вызываете файл **traceroute.py** через командную строку или через любые другие методы которые вы знаете <br /> __вводите доменное имя или IP-адрес.__ 
![Traceroute](https://user-images.githubusercontent.com/46073895/232246401-084fcae7-3dd1-4e36-b8b7-623cf706867c.jpg)
Вам пишут ожидайте **(к сожелению это может занять несколько минут)** <br />
Причина длительности в том что сайт **"https://www.nic.ru/whois/?searchWord="** при многократном обращении не выдаёт информацию об IP-адресе и таблица заполняется ничем
и я сделал time.sleep(30) <br />
**Вот пример вывода того же кода но без time.sleep(30)**
![Traceroute2](https://user-images.githubusercontent.com/46073895/232248269-a71d5ecd-7f35-46a6-a650-189c3207e42c.jpg)
Функция **traceroute** (является главной функцией)
```
def traceroute(data):
    print("Ожидайте")
    data_table = []
    number = 0
    tracert = get_IP_from_tracert(data)
    print(tracert)
    columns = len(th)
    table = PrettyTable(th)
    for ip in tracert:
        number += 1
        data_table.append(number)
        data_table.extend(get_info_from_IP(ip))
        table.add_row(data_table[:columns])
        data_table = data_table[columns:]
        time.sleep(30)
    return table
```
Далее вступает функция **get_IP_from_tracert** которая вызывает команду OC **tracert** <br /> Записывает IP-адреса в массив и выводит на экран
```
def get_IP_from_tracert(name: str):
    cmd = f"tracert {name}"
    founds_IP = IP.findall(os.popen(cmd).read())
    return founds_IP
``` 
Затем с мы идём циклом по списку и с помощью функции **get_info_from_IP** <br /> Используя сайт **"https://www.nic.ru/whois/?searchWord="** и регулярные выражения мы узнаём онформацию об **IP-адресе**
```
def get_info_from_IP(ip):
    if is_grey_IP(ip):
        return ip, 'grey', 'grey', 'grey'
    else:
        with urlopen(f'https://www.nic.ru/whois/?searchWord={ip}') as site:
            info = site.read().decode('utf-8')
            return ip, parser(info, AS), parser(info, country), parser(info, provider)
```
И записываем в функции **traceroute** эти данные в таблицу <br />
А в конце как видно на фотографии выводим на экран
