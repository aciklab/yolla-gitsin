#!/usr/bin/python3
import os,time,pwd,sys
import locale
from dialog import Dialog 
from subprocess import Popen,PIPE

class STATES:
	current_state = 0
	def __init__(self):
		#State : 0
		locale.setlocale(locale.LC_ALL, '')
		self.text_port = "2222"
		self.text_host = "pardus@10.150.17.180"
		self.text_pass = "1"
		self.text_host_dir="pardus@10.150.17.180:/home/pardus/Masaüstü/."
		self.path = "/home/" + pwd.getpwuid(os.getuid())[0] +"/Masaüstü/"
		self.d = Dialog(dialog="dialog")
		self.d.set_background_title("Yolla Gitsin Moruq")
		self.current_state += 1
		
	def state_01(self):
		#State : 1
		self.d.msgbox("Hoş Geldiniz!\n\nLütfen dosyaların taşınmasını istediğiniz bilgisayarda openssh-server uygulamasının kurulu olduğundan emin olun.",width=40,height=12)
		self.current_state += 1
	
	def state_02(self):
		#State : 2
		code = self.d.yesno("SSH Key üretilsin mi?")
		if(code == self.d.OK):
			self.current_state += 1
		#7. State'e dallan
		else:
			self.current_state = 7 
	def state_03(self):
		#SSH-KEYGEN
		os.popen("rm -rf ~/.ssh")
		output = Popen(['ssh-keygen', '-t', 'rsa'], stdout=PIPE, stdin=PIPE)
		output.stdin.write("\n\n\n".encode())
		output.stdin.close()
		output.wait()
		self.d.infobox("SSH KEY'ler oluşturuldu.", width=0, height=0, title="Başarılı")
		time.sleep(2)
		self.current_state += 1
	
	def state_04(self):
		#ALERT : SSH-KEY Karşı Bilgisayar Kopyalanıcak
		self.d.infobox("Public KEY karşı pc'ye kopyalanıcak")
		time.sleep(1)	
		self.current_state += 1
	def state_05(self):
		#Bağlanılacak PC için Bilgiler
		isDone, tag, text = self.d.inputmenu("Bağlanılacak bilgisayarın bilgilerini giriniz",height=18, menu_height=16, choices=[("Port",self.text_port),("Host",self.text_host),("Host_Direction",self.text_host_dir),("Password",self.text_pass)])
		if(isDone == 'renamed'):
			if(tag == 'Port'):
				self.text_port = text
			elif tag == "Password":
				self.text_pass = text
			elif tag == "Host":
				self.text_host = text
			elif tag == "Host_Direction":
				self.text_host_dir = text 
		elif(isDone == 'accepted'):
			self.current_state += 1
		else:
			self.current_state -= 1
	def state_06(self):
		#SSH-COPY-ID
		output2 = Popen(['sshpass -p "{}" ssh-copy-id -o StrictHostKeyChecking=no -p {} {} '.format(self.text_pass, self.text_port, self.text_host)], stdout=PIPE, stdin=PIPE,shell=True)
		output2.stdin.close()
		output2.wait()	
		self.d.infobox("SSH KEY'ler aktarıldı.", width=0, height=0, title="Başarılı")
		time.sleep(1)
		self.current_state += 2
	def state_07(self):
		#SSH-KEYGEN ÜRETİLMEDEN çalıştırma   
		self.d.infobox("SSH KEY üretilmeden devam ediliyor.",width=40,height=3)
		time.sleep(2)
		self.current_state += 1
	def state_08(self):
		isDone, self.path = self.d.dselect(self.path)
		if isDone == 'ok':
			self.current_state += 1
		else:
			self.current_state = 0
	def state_09(self):
		onlyfiles = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path,f))]
		onlyfiles_len = len(onlyfiles)
		info4files = []
		
		for i in range(onlyfiles_len):
			info4files.append((onlyfiles[i],"",False))
		
		code,send_files = self.d.checklist("Gönderilecek dosyaları seç", height=20, choices=info4files)
		if code == 'cancel':
			self.current_state -= 1
		elif code == 'ok':
			send_files_len = len(send_files)
			if(send_files_len == 0):
				self.d.infobox("Dosya Seçilmedi")
				time.sleep(2)
			else:
				for i in range(send_files_len):
					output3= Popen(['sshpass -p "{}" scp -P {} {} {}'.format(self.text_pass, self.text_port,os.path.join(self.path,send_files[i]),self.text_host_dir)],stdin=PIPE,stdout=PIPE,shell=True)
					output3.stdin.close()
					out = output3.stdout.read().decode("utf-8")
					self.d.infobox(text = out)
					output3.wait()
			self.current_state += 1
		#State : 10
	def state_repeat(self):
		code = self.d.yesno("Dosya Yollamaya devam etmek ister misiniz?",yes_label = "Yes Baba",no_label="No Baba")
		if(code == 'ok'):
			self.current_state = 8
		else:
			self.current_state += 1
			
	def state_final(self):
		self.d.infobox("Çıkıyor Moruq")
		time.sleep(2)

def Yolla_Gitsin_begin():
	states = STATES()
	while True:
		if(states.current_state == 0):
			states.__init__()
		if(states.current_state == 1):
			states.state_01()
		if(states.current_state == 2):
			states.state_02()
		if(states.current_state == 3):
			states.state_03()
		if(states.current_state == 4):
			states.state_04()
		if(states.current_state == 5):
			states.state_05()
		if(states.current_state == 6):
			states.state_06()
		if(states.current_state == 7):
			states.state_07()
		if(states.current_state == 8):
			states.state_08()
		if(states.current_state == 9):
			states.state_09()	
		if(states.current_state == 10):
			states.state_repeat()
		if(states.current_state == 11):
			states.state_final()		
			exit()
			#states.state_final()
