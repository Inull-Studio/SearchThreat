# SearchThreat
基于 www.venuseye.com.cn 的批量威胁IP收集

# Use:
  python main.py ip.txt output.txt(留空则默认为output.txt)
 
    #ip.txt:
 
    127.0.0.1
  
    192.168.1.1
    
    192.168.0.1
  
    ...
  
#Config:

  time_:在此日期之后的所有ip将会被记录
  
  typelist:攻击类型 -> list ,当查询的ip记录中存在该攻击 则记录此ip
  
  cookie:你的cookie,请自行使用调试模式获取你的cookie
