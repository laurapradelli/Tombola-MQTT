from random import *
import paho.mqtt.client as mqtt
import time

class Tombola:

	def __init__(self, nome):
		self.nome=nome
		self.tabella=[['','','','','','','','',''], ['','','','','','','','',''], ['','','','','','','','','']]
		for i in range(0,3):
			for j in range(0,5):
				while True:
					riga=i
					colonna=randint(0,8)
					if self.tabella[riga][colonna]=='':
						break

				if riga==0:
					self.tabella[riga][colonna]=randint((colonna*10)+1, (colonna*10)+8)

				if riga==1:
					if self.tabella[0][colonna]!='':
						self.tabella[riga][colonna]=randint(self.tabella[0][colonna]+1, ((colonna+1)*10)-1)
					else:
						self.tabella[riga][colonna]=randint((colonna*10)+2, (colonna*10)+9)

				if riga==2:
					if self.tabella[0][colonna]!='' and self.tabella[1][colonna]!='':
						self.tabella[riga][colonna]=randint(self.tabella[1][colonna]+1, (colonna+1)*10)
					elif self.tabella[0][colonna]!='':
						self.tabella[riga][colonna]=randint(self.tabella[0][colonna]+2, (colonna+1)*10)
					elif self.tabella[1][colonna]!='':
						self.tabella[riga][colonna]=randint(self.tabella[1][colonna]+1, (colonna+1)*10)
					else:
						self.tabella[riga][colonna]=randint((colonna*10)+3, (colonna*10)+10)

	def __repr__(self):
		s=''
		for riga in self.tabella:
			for numero in riga:
				if numero != '':
					s+=str(numero)
				else:
					s+="  "
				s+=", "
			s+="\n"
		return s


if __name__=='__main__':

	while True:
		a=0
		while a==0:

			lista_giocatori=[]

			def giocatore(nome):
				g=Tombola(nome)
				lista_giocatori.append(g)

			print('Benvenut* nella tombola MQTT!')
			while True:
				print('Vuoi aggiungere un giocatore? s / n')
				r=input()
				if r=='s' or r=='S':
					print('Inserisci il nome del giocatore')
					name=input()
					giocatore(name)
				else:
					break

			vittorie={}
			contatori={}
			vincitori={}

			for giocatore in lista_giocatori:
				vittorie[giocatore.nome]=[[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
				contatori[giocatore.nome]=[0,0,0]

			vinto=0
			tot=0
			combinazione=''
			parziale='tombola/'
			flag=0

			broker = 'test.mosquitto.org'
			topic = 'tombola/numbers'

			def on_connect(client, userdata, flags, rc):
				print(f'{mqtt.connack_string(rc)}')
				client.subscribe(topic)

			def on_subscribe(client, userdata, mid, granted_qos):
				print(f'subscribed {topic} with qos {granted_qos[0]}\n')

			def on_message(client, userdata, msg):
				print(f'numero estratto: {msg.payload.decode()}')
				numero=msg.payload.decode()
				global vinto
				global tot
				global flag
				global a

				for giocatore in lista_giocatori:
					for riga in range(0,3):
						for cella in giocatore.tabella[riga]:
							if cella!='':
								if int(cella)==int(numero):
									vittorie[giocatore.nome][riga][contatori[giocatore.nome][riga]]=1
									if contatori[giocatore.nome][riga]==4:
										contatori[giocatore.nome][riga]=0
									else:
										contatori[giocatore.nome][riga]+=1

					combinazioni={15:'tombola', 5:'cinquina', 4:'quaterna', 3:'terna', 2:'ambo'}

					for vittoria in vittorie:
						for riga in vittorie[vittoria]:
							vinto=riga.count(1)
							tot=int(vinto)+tot
							if tot==15 and flag==4:
								flag+=1
								client.publish(parziale+combinazioni[tot], vittoria)
								vincitori[combinazioni[tot]]=vittoria
								client.disconnect()
								client.loop_stop()
								a=1
							if (vinto==5 and flag==3) or (vinto==4 and flag==2) or (vinto==3 and flag==1) or (vinto==2 and flag==0):
								flag+=1
								client.publish(parziale+combinazioni[vinto], vittoria)
								vincitori[combinazioni[vinto]]=vittoria
						tot=0		

			def main():
				client = mqtt.Client()

				client.on_connect = on_connect
				client.on_subscribe = on_subscribe
				client.on_message = on_message

				print('MQTT client connection....')
				client.connect(broker)
				try:
					client.loop_forever()
				except KeyboardInterrupt:
					print('MQTT client disconnection...')
				finally:
					client.disconnect()
					client.loop_stop()

			main()

		
		print('Il gioco è terminato, di seguito i vari vincitori per categoria')
		for categoria in vincitori:
			print(f'{categoria}: {vincitori[categoria]}')