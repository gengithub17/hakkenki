import tkinter as tk

from PublicClass import *
from Reception import Reception
from Staff import Staff

class StaffWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
		self.title("スタッフ管理画面")
		self.protocol("WM_DELETE_WINDOW",self.confirm_close)
		self.staff = Staff(self)
		self.staff.pack()
	
	def confirm_close(self):
		self.staff.close_check() #消えてくれない...

class ReceptionWindow(tk.Toplevel):
	def __init__(self):
		super().__init__()
		self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
		self.title("タッチで操作してください")
		self.protocol("WM_DELETE_WINDOW",lambda :None) #受付管理画面でのxボタンは無視
		self.reception = Reception(self)
		self.reception.pack()

def exchange_functions(staff:Staff,reception:Reception):
	staff.reception_reload = reception.reload_from_staff
	reception.staff_reload = staff.reload_from_reception

test_client = ClientInfo(member_num=-1,name="ハマダ",subject="操作説明，ご相談")
test2_client = ClientInfo(member_num=16002222,name="ニシノ",subject="定期点検(プレミアムメンバー様限定)")

if __name__ == "__main__":
	try:
		create_table()
		staffwindow = StaffWindow()
		receptionwindow = ReceptionWindow()

		exchange_functions(staffwindow.staff,receptionwindow.reception)

		for _ in range(0):
			test_client.registration()
			test2_client.registration()

		staffwindow.mainloop()
	finally:
		remove_table()