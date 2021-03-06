# ~*~ coding: utf-8 ~*~

from hostinfo.models import Host,Monitor
from hostinfo.views import ssh
import threading

def   job(id):  ##计划任务
		
		i = Host.objects.filter(id=id).first()
		cpu1 = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password, cmd=" top -bn 1 -i -c | grep Cpu   ")
		cpu = float(cpu1['data'][8:14])
		total = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password, cmd=" free | grep  Mem:  ")
		list = total['data'].split(" ")
		while '' in list:
			list.remove('')
		mem = float('%.2f' % (int(list[2]) / int(list[1])))*100
		Monitor.objects.create(server_id=i.id,cpu_use=cpu,mem_use=mem,)
		

def  monitor_job():
	object =  Host.objects.all()
	i_list=[]
	for i in object:
		i_list.append(i.id)
		
	print(i_list)
	
	t_list=[]
	for i in i_list:  ##循环调用
		t = threading.Thread(target=job, args=[i, ])
		t.start()
		t_list.append(t)
	for i in t_list:
		i.join()
	
	print("结束了")

