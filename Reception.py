from PublicClass import *

import tkinter as tk
from tkinter import ttk

class Reception(ttk.Frame):
	def __init__(self,root:tk.Toplevel):
		super().__init__(root,width=WINDOW_WIDTH,height=WINDOW_HEIGHT)
		
		self.client = ClientInfo()
		self.reservation_var = tk.BooleanVar()
		self.mem_bool_var = tk.BooleanVar()
		self.mem_num_var = tk.StringVar()
		self.name_var = tk.StringVar()
		self.subject_var = tk.StringVar()
		self.staff_var = tk.BooleanVar()

		self.using:bool #最初の画面ならFalse #Staffから勝手に更新していいのかを判断
		self.staff_reload:function
		self.waiting_num_var = tk.IntVar()

		self.client_reset()
		self.reception_start()
	
	def client_reset(self): #顧客情報初期化
		self.client.clear()
		self.reservation_var.set(False)
		self.mem_bool_var.set(False)
		self.mem_num_var.set("")
		self.name_var.set("")
		self.subject_var.set("")
		self.staff_var.set(False)
	
	###画面1 : 受付開始###
	def reception_start(self):
		self.using = False
		self.reservation_var.set(False)
		put(ttk.Label(self,text="受付はこちらから",anchor=tk.CENTER,font=("Arial",40)),xy=(2,0),w=4,h=2)
		#put(ttk.Label(self,text=f"現在,{count_waiting()}組のお客様にお待ちいただいております。\nまた予約いただいたお客様や月額会員様の優先受付など\nにより受付の順番が前後する場合がございます。",font=("Arial",20)),xy=(0.5,3),w=4)
		put(ttk.Label(self,text=f"現在,{count_waiting()}組のお客様にお待ちいただいております。",font=("Arial",30,"bold")),xy=(0.5,2),w=6)
		put(ttk.Label(self,text="また予約いただいたお客様や月額会員様の優先受付など\nにより受付の順番が前後する場合がございます。",font=("Arial",20)),xy=(0.5,3),w=4)
		put(SwitchButton(self,function=self.reservation_check,text="受付開始",color="yellow"),xy=(6,3),w=2,h=2)
	
	def reload_from_staff(self):
		if self.using: return
		self.reception_start()
	
	###画面2 : 予約確認
	def reservation_check(self):
		self.using = True
		self.reservation_var.set(False)
		put(ttk.Label(self,text="本日のご来店に際しまして，事前にお時間のご予約はございますか?",anchor=tk.CENTER,font=("Arial",30)),xy=(0,0),w=8,h=2)
		put(SwitchButton(parent=self,function=self.reception_start,text="戻る"),xy=(0,3),w=2,h=2)
		put(SwitchButton(parent=self,function=self.reservation_set,text="はい",color="yellow"),xy=(3,3),w=2,h=2)
		put(SwitchButton(parent=self,function=self.member_check,text="いいえ",color="yellow"),xy=(6,3),w=2,h=2)
	
	##予約ありボタン押下時実行##
	def reservation_set(self):
		self.reservation_var.set(True)
		self.member_check()
	
	###画面3 : メンバー確認###
	def member_check(self):
		self.mem_bool_var.set(False)
		put(widget=ttk.Label(self,text="PCデポのメンバー様ですか?(優先受付いたします)",anchor=tk.CENTER,font=("Arial",30)),xy=(0,0),w=8)
		put(widget=ttk.Label(self,text="※月額のメンバーシップ制のことです。\n※ケーズデンキの安心パスポートとは異なります。",anchor=tk.CENTER,font=("Arial",30)),xy=(0,1),w=8)
		put(widget=SwitchButton(parent=self,function=self.reservation_check,text="戻る"),xy=(0,3),w=2,h=2)
		put(widget=SwitchButton(parent=self,function=self.fill_number,text="メンバー",color="blue"),xy=(3,3),w=2,h=2)
		#put(widget=SwitchButton(parent=self,function=self.check_member,text="わからない"),xy=(3,3),w=2,h=2)
		put(widget=SwitchButton(parent=self,function=self.fill_name,text="メンバーでない",color="yellow"),xy=(6,3),w=2,h=2)
	
	##メンバー番号入力##
	def fill_number(self):
		self.mem_bool_var.set(True)
		put(ttk.Label(self,text="メンバー番号を入力してください(不明な場合は空白で結構です)",anchor=tk.CENTER,font=("Arial",30)),xy=(0,0),w=8)
		put(ttk.Label(self,textvariable=self.mem_num_var,font=("Arial",30),background="white"),xy=(2,1),w=4)
		put(SwitchButton(parent=self,function=self.staff_check,text="決定",color="yellow"),xy=(5,1))
		put(SwitchButton(parent=self,function=self.member_check,text="戻る"),xy=(6,1))
		put(NumberKey(parent=self,strvar=self.mem_num_var,maxlen=8),xy=(2,2),w=5,h=3)
	
	##担当スタッフの有無##
	def staff_check(self):
		self.staff_var.set(False)
		put(ttk.Label(self,text="当店で担当のスタッフはいらっしゃいますか?",anchor=tk.CENTER,font=("Arial",30)),xy=(0,0),w=8)
		put(SwitchButton(parent=self,function=self.fill_number,text="戻る"),xy=(0,3),w=2,h=2)
		put(SwitchButton(parent=self,function=self.staff_selected,text="はい",color="yellow"),xy=(3,3),w=2,h=2)
		put(SwitchButton(parent=self,function=self.fill_name,text="いいえ",color="yellow"),xy=(6,3),w=2,h=2)
	
	##担当スタッフがいる場合##
	def staff_selected(self):
		self.staff_var.set(True)
		self.fill_name()
	
	###画面4 : 名前入力###
	def fill_name(self,color="black"): #未入力時は赤字で入力促す
		put(ttk.Label(self,text="お客様のお名前を入力してください",anchor=tk.CENTER,font=("Arial",30),foreground=color),xy=(0,0),w=8)
		put(ttk.Label(self,textvariable=self.name_var,font=("Arial",30),background="white"),xy=(2,1),w=2)
		put(ttk.Label(self,text="様",font=("Arial",30)),xy=(4,1))
		put(SwitchButton(parent=self,function=self.name_check,text="決定",color="yellow"),xy=(6,1))
		put(SwitchButton(parent=self,function=self.member_check,text="戻る"),xy=(7,1))
		put(Keyboard(parent=self,var=self.name_var),xy=(0,2),w=8,h=3)
	
	##名前入力確認##
	def name_check(self):
		if self.name_var.get() : self.select_subject_ver2()
		else : self.fill_name(color="red")

	###画面5 : 用件確認###
	def select_subject(self):
		put(ttk.Label(self,text="本日はいかがなさいましたか?\n(以下から選択)",anchor=tk.CENTER,font=("Arial",30)),xy=(2,0),w=4,h=2)
		put(ttk.Combobox(self,textvariable=self.subject_var,values=ClientInfo.subject_list,state="readonly",font=("Arial",20)),xy=(2,3),w=4)
		put(SwitchButton(self,function=self.fill_name,text="戻る"),xy=(0,2),w=2,h=2)
		put(SwitchButton(self,function=self.data_confirmation,text="決定",color="yellow"),xy=(6,2),w=2,h=2)
	
	def select_subject_ver2(self):
		style = ttk.Style()
		style.theme_use("default")
		style.configure('TRadiobutton',font=("Arial",20))
		put(ttk.Label(self,text="本日はいかがなさいましたか?(以下から選択)",anchor=tk.CENTER,font=("Arial",30)),xy=(0,0),w=8)
		# put(ttk.Radiobutton(self,text=ClientInfo.subject_list[0],value=ClientInfo.subject_list[0],variable=self.subject_var),xy=(0,1.5),w=4,h=0.5)
		# put(ttk.Radiobutton(self,text=ClientInfo.subject_list[1],value=ClientInfo.subject_list[1],variable=self.subject_var),xy=(4,1.5),w=4,h=0.5)
		# put(ttk.Radiobutton(self,text=ClientInfo.subject_list[2],value=ClientInfo.subject_list[2],variable=self.subject_var),xy=(0,2),w=4,h=0.5)
		for i in range(7):
			put(ttk.Radiobutton(self,text=ClientInfo.subject_list[i],value=ClientInfo.subject_list[i],variable=self.subject_var),xy=(4*(i%2),((i//2)+2)/2),w=4,h=0.5)
		put(SwitchButton(self,function=self.fill_name,text="戻る"),xy=(0,3),w=2,h=2)
		put(SwitchButton(self,function=self.data_confirmation,text="決定",color="yellow"),xy=(6,3),w=2,h=2)
	
	###画面6 : 入力情報確認###
	def data_confirmation(self):
		put(ttk.Label(self,text="入力内容をご確認ください",anchor=tk.CENTER,font=("Arial",30)),xy=(0,0),w=8)
		label_text = ""
		label_text += "お名前　  : " + self.name_var.get() + "様\n"
		label_text += "ご予約　  : " + ("あり" if self.reservation_var.get() else "なし") + "\n"
		label_text += "会員番号  : " + (self.mem_num_var.get() if self.mem_bool_var.get() else "--------") + "\n"
		label_text += "内容　　  : " + self.subject_var.get() + "\n"
		if self.mem_bool_var.get(): label_text += "担当スタッフ : " + ("いる" if self.staff_var.get() else "いない") + "\n"
		put(ttk.Label(self,text=label_text,font=("Arial",30)),xy=(2,1),w=6,h=3)
		put(SwitchButton(parent=self,function=self.select_subject_ver2,text="戻る"),xy=(0,3),w=2,h=2)
		put(SwitchButton(parent=self,function=self.data_conversion,text="決定",color="yellow"),xy=(6,3),w=2,h=2)
	
	##入力内容をClientInfo型に変換
	def data_conversion(self):
		client = ClientInfo()
		client.reservation = self.reservation_var.get()
		client.member_num = -1 if not(self.mem_bool_var.get()) else 0 if self.mem_num_var.get()=="" else self.mem_num_var.get()
		client.name = self.name_var.get()
		client.subject = self.subject_var.get()
		client.staff = self.staff_var.get()

		client.registration()
		self.finish_reception(client.waiting_num)

	###画面7 : 受付完了画面###
	def finish_reception(self,waiting_num:int):
		put(ttk.Label(self,text="受付が完了しました。",font=("Arial",30),anchor=tk.CENTER),xy=(2,0),w=4)
		put(ttk.Label(self,text="順番にご案内いたしますのでしばらくお待ちください。",font=("Arial",20),anchor=tk.W),xy=(2,1),w=5)
		put(ttk.Label(self,text=f"お客様の受付番号は{waiting_num}番です。\n現在{count_waiting()}組のお客様にお待ちいただいております。",font=("Arial",25),anchor=tk.W),xy=(2,2),w=6)
		put(ttk.Label(self,text="メンバー様優先受付やご用件になど応じてご案内\nの順番が前後する場合がございます。\nあらかじめご了承ください。",font=("Arial",20),anchor=tk.W),xy=(2,3),w=4)

		self.staff_reload()
		self.client_reset()
		put(SwitchButton(parent=self,function=self.reception_start,text="受付画面へ",color="yellow"),xy=(6,3),w=2,h=2)


class SwitchButton(ttk.Button): #画面遷移を行うボタン
	def __init__(self,parent:Reception,function,text:str,color="#ddd"): #フレームと実行関数を渡す
		self.parent = parent
		self.function = function
		style = ttk.Style()
		style.theme_use("default") #なぜかbackground変更に必要
		style.configure(f'switch{color}.TButton',font=("Arial",25),background=color) #色ごとにstyle名分ける
		super().__init__(parent,text=text,command=self.pushed,style=f'switch{color}.TButton')
	
	def pushed(self):
		ChildDelete(self.parent)
		self.function()
		del self
	
	#override
	def destroy(self):
		super().destroy()
		del self

CELL_WIDTH = WINDOW_WIDTH//8
CELL_HEIGHT = WINDOW_HEIGHT//5
def put(widget:ttk.Widget,xy:tuple[int,int],w=1,h=1):
	widget.place(x=(xy[0]+w/2)*CELL_WIDTH,y=(xy[1]+h/2)*CELL_HEIGHT,width=w*CELL_WIDTH,height=h*CELL_HEIGHT,anchor=tk.CENTER)