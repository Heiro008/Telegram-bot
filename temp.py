import time
def time_table():
	message = ''
	day = time.localtime().tm_wday
	classes=['probability -http://meet.google.com/xoc-vbtf-fbs ',
				'M&I -https://teams.microsoft.com/l/meetup-join/19%3a147121e710ba484f9ba5ede2ea51c000%40thread.tacv2/1609153145963?context=%7b%22Tid%22%3a%22858dc6a1-05e7-48c7-8a2b-4172a00a524a%22%2c%22Oid%22%3a%225fdaf900-6f9c-464b-b695-f1fa040f99e5%22%7d' ,
				'Digital electronics -https://meet.google.com/btv-jzsw-sfn ',
				'ISM -https://meet.google.com/fam-mmjr-ign?hs=224 ',
				'Control System -http://meet.google.com/rdp-pfgx-zff',
				'EPGS -https://meet.google.com/aux-byuh-ves ',
				'Indian consitution -https://meet.google.com/fyz-xvup-jpg?hs=224 ']
	map_classes = {0:[5,3,0,4],1:[2,1,6,0],2:[4,1,2,5],3:[5,3,4,2],4:[0,6,1,3],5:[]}
	session = ["9 :30 - 10:30","11:00 - 12:00","2 :00 - 3 :00","3 :30 - 4 :00"]
	for i,j in enumerate(map_classes[day]):
		message = message+session[i]+' '+classes[j]+'\n' 

	return message
	
print(time_table())
