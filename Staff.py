import tkinter as tk
from tkinter import ttk
import sys

from PublicClass import *

class Staff(ttk.Frame):
	header_list = ["待ち番号",	 "会員番号",	"お名前",	"内容",	"予約",		"担当",	"来店時刻", "状態"]
	col_width = [ 	2,			2,     			5,			7,		2,		2,		2,			4]
	row_max = 7 #表示可能な人数

	def __init__(self,root:tk.Tk,row_start=1):
		super().__init__(root,width=WINDOW_WIDTH,height=WINDOW_HEIGHT)
		self.row_start:int = row_start #表示している最初の待ち番号

		self.reception_reload:function

		self.reload(row_start=self.row_start)
	
	def reload(self,row_start=1): #最新情報を読み込んで表示更新
		ChildDelete(self)
		self.add_header()

		client_list = ClientInfo.query_all()
		clients_num = len(client_list)
		if row_start == 0 : row_start = 1 #更新ボタン押下時にrow_start=0で実行の可能性あり
		self.row_start = clients_num if row_start>clients_num else row_start #開始行が実際のデータ数より多い時はデータがある部分まで戻す
		
		put(ttk.Button(self,text="更新",command=lambda: self.reload(row_start=self.row_start)),xy=(sum(Staff.col_width)+1,4),w=2,h=2) #更新ボタン
		if row_start > 1: put(ttk.Button(self,text="▲",command=lambda: self.reload(row_start=self.row_start-1)),xy=(sum(Staff.col_width)+1,1),w=2,h=2) #上ボタン
		if row_start+Staff.row_max <= clients_num: put(ttk.Button(self,text="▼",command=lambda: self.reload(row_start=self.row_start+1)),xy=(sum(Staff.col_width)+1,7),w=2,h=2) #下ボタン

		for row_count in range(Staff.row_max):
			try:
				self.add_row(client=client_list[row_count+self.row_start-1],row=row_count+2)
			except IndexError:
				break
	
	def reload_from_reception(self):
		self.reload(row_start=self.row_start)
	
	def add_header(self):
		col = 0
		for index in range(len(Staff.col_width)):
			put(ttk.Label(self,text=Staff.header_list[index],font=("Arial",11),background="gray",anchor=tk.CENTER),xy=(col,1),w=Staff.col_width[index])
			col += Staff.col_width[index]
	
	def add_row(self,client:ClientInfo,row:int):
		member_num_str = "一般" if client.member_num==-1 else "番号不明" if client.member_num==0 else str(client.member_num)
		data = [client.waiting_num,member_num_str,client.name+" 様",client.subject,"あり"if client.reservation else "なし","あり"if client.staff else "なし",client.timestamp]
		col = 0
		for index in range(len(data)):
			if client.status == "対応済み": font_color = "green"
			elif client.status == "キャンセル": font_color = "gray"
			elif client.member_num >= 0: font_color = "blue"
			else: font_color = "black"
			put(ttk.Label(self,text=data[index],font=("Arial",12),foreground=font_color,anchor=tk.CENTER),xy=(col,row),w=Staff.col_width[index])
			col += Staff.col_width[index]
		status_box = ttk.Combobox(self,values=ClientInfo.status_list,state="readonly")
		status_box.set(client.status)
		status_box.bind('<<ComboboxSelected>>',lambda _:self.status_changed(client,status_box))
		put(status_box,xy=(col,row),w=Staff.col_width[-1])
	
	def status_changed(self,client:ClientInfo,statusbox:ttk.Combobox):
		client.status_update(statusbox.get())
		self.reception_reload()
		self.reload(row_start=self.row_start)
	
	#override
	def close_check(self):
		ChildDelete(self)
		put(ttk.Label(self,text="本当に終了しますか?",font=("Arial",30),anchor=tk.CENTER),xy=(0,0),w=30,h=4)
		put(ttk.Button(self,text="OK",command=sys.exit),xy=(5,5),w=5,h=3)
		put(ttk.Button(self,text="Cancel",command=partial(self.reload,self.row_start)),xy=(20,5),w=5,h=3)

CELL_WIDTH = STAFF_WIDTH//30
CELL_HEIGHT = STAFF_HEIGHT//10
def put(widget:ttk.Widget,xy:tuple[int,int],w=1,h=1):
	widget.place(x=(xy[0]+w/2)*CELL_WIDTH,y=(xy[1]+h/2)*CELL_HEIGHT,width=w*CELL_WIDTH,height=h*CELL_HEIGHT,anchor=tk.CENTER)