from requests import post
import sys
from json import loads
import time
import threading
from rich import print
from config import cookie, time_, typelist
# ————————————————————————
url = 'https://www.venuseye.com.cn/ve/ip/ioc'
nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
t_t_T = time.mktime(time.strptime(time_, "%Y-%m-%d %H:%M:%S"))
# t_t_T ge nowtime
# ————————————————————————
def get_data(SearchIp):
    data = {"target": SearchIp}
    res = post(url, data=data,cookies=cookie)
    return loads(res.text)


def search(SearchIp):
    print('[+] Searching: '+SearchIp)
    resdata = get_data(SearchIp)
    if resdata['status_code'] == 409:
        while(resdata == {'status_code': 409}):
            print(
                '[blue][-]', SearchIp, 'researching...[/] 查询过于频繁 请登录https://www.venuseye.com.cn 或通过验证码来解除')
            time.sleep(5)
            resdata = get_data(SearchIp)
    if resdata['status_code'] == 404:
        if debug:
            print('[yellow][-]',url,'[yellow]None data&404')
        return
    if debug:
        print('[yellow][*] Debug: status_code:',resdata['status_code'])
    for i in range(len(resdata['data']['ioc'])):
        if resdata['data']['ioc'][i]['update_time'] > t_t_T:
            for type_ in resdata['data']['ioc'][i]['categories']:
                if type_ in typelist:
                    print('[red][+] Found: [/]'+resdata['data']['ip'])
                    out.write(resdata['data']['ip']+'\n')
                    return

def main():
    global usrin, out, debug
    if 'debug' in sys.argv:
        debug = True
        sys.argv.remove('debug')
    if len(sys.argv) < 2:
        print(f'usage: python {sys.argv[0]} <input.txt> \[output.txt] \[debug]')
        return
    usrin = sys.argv[1:]
    if len(usrin) < 2:
        usrin.append('output.txt')
    ips = open(usrin[0], 'r').read().splitlines()
    out = open(usrin[1], 'a+')

    threadlist:list[threading.Thread] = []
    for i in ips:
        t = threading.Thread(target=search, args=(i,), daemon=True)
        t.start()
        threadlist.append(t)
    for t in threadlist:
        t.join()
    out.close()

if __name__ == '__main__':
    main()