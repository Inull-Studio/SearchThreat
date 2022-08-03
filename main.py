from requests import post
import sys
from json import loads
import time
import threading
from rich import print

# ____Test____
url = 'https://www.venuseye.com.cn/ve/ip/ioc'

nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
time_ = '2021-1-1 00:00:00'
t_t_T = time.mktime(time.strptime(time_, "%Y-%m-%d %H:%M:%S"))
# t_t_T ge nowtime

typelist = ['主机扫描', '爆破攻击', 'Web漏洞攻击', '恶意软件']

# _____________


def get_data(SearchIp):
    data = {"target": SearchIp}
    res = post(url, data=data)
    return loads(res.text)


def search(SearchIp):

    # data={
    #     "target":SearchIp
    # }
    print('[+] Searching: '+SearchIp)
    resdata = get_data(SearchIp)
    if resdata['status_code'] == 409:
        while(resdata == {'status_code': 409}):
            print(
                '[blue][-]', SearchIp, 'researching...[/] 查询过于频繁 请登录https://www.venuseye.com.cn 或通过验证码来解除')
            time.sleep(5)
            resdata = get_data(SearchIp)
    if resdata['status_code'] == 404:
        print('[red][-]',url,'[red]404 Not Found')
        return
    for i in range(len(resdata['data']['ioc'])):
        if resdata['data']['ioc'][i]['update_time'] > t_t_T:
            # print('[*] dbug:Time True')
            for type_ in resdata['data']['ioc'][i]['categories']:
                if type_ in typelist:
                    print('[red][+] Found: [/]'+resdata['data']['ip'])
                    out.write(resdata['data']['ip']+'\n')
                    return


if __name__ == '__main__':
    usrin = sys.argv[1:]
    ips = open(usrin[0], 'r').read().splitlines()
    out = open('output.txt', 'a+')

    for i in ips:
        t = threading.Thread(target=search, args=(i,))
        t.setDaemon(True)
        t.start()
        t.join()
    out.close()
