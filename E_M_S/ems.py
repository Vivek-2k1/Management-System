#Importing Libraries

from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import geocoder
from requests import *
from datetime import *
import os
import pandas as pd
import matplotlib.pyplot as plt


#Functions

def f1():
	main_Menu.withdraw()
	create_emp.deiconify()
def f2():
	create_emp.withdraw()
	main_Menu.deiconify()
def f3():
	main_Menu.withdraw()
	emp_list.deiconify()
	emp_list_st_data.delete(1.0,END)

	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "select * from emp_data"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "ID : " + str(d[0]) + "        " + "Name : " + str(d[1]) + "        " + "Address : " + str(d[2]) + "        " + "Job_T : " + str(d[3]) + "        " + "Salary : " + str(d[4]) + "\n"
		emp_list_st_data.insert(INSERT, info)
	except Exception as e:
		showerror("Issue ", e)
	finally:
		if con is not None:
			con.close()

def f4():
	emp_list.withdraw()
	main_Menu.deiconify()
def f5():
	main_Menu.withdraw()
	update_emp.deiconify()
def f6():
	update_emp.withdraw()
	main_Menu.deiconify()
def f7():
	main_Menu.withdraw()
	delete_emp.deiconify()
def f8():
	delete_emp.withdraw()
	main_Menu.deiconify()
def f9():
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "insert into emp_data values('%d','%s','%s','%s','%d')"
		if create_emp_ent_id.get().isdigit() and create_emp_ent_salary.get().isdigit():
			id = int(create_emp_ent_id.get())
			name = create_emp_ent_name.get()
			address = create_emp_ent_address.get()
			job_title = create_emp_ent_jobT.get()
			salary = int(create_emp_ent_salary.get())
			cursor.execute(sql%(id,name,address,job_title,salary))
			con.commit()
			showinfo("Info", "Record Added Successfully !!")
		else:
			showinfo("Info", "ID and Salary Should be in Numbers !!")

	except Exception as e:
		showerror("Issue : ", e)
	finally:
		create_emp_ent_id.delete(0,END)
		create_emp_ent_name.delete(0,END)
		create_emp_ent_address.delete(0,END)
		create_emp_ent_jobT.delete(0,END)
		create_emp_ent_salary.delete(0,END)
		create_emp_ent_id.focus()
		if con is not None:
			con.close()

def f10():
	con = None
	try:
		con = connect("ems.db")
		sql = "update emp_data set name='%s',address='%s', jobTitle = '%s', salary='%d' where id = '%d' "
		cursor = con.cursor() 
		if update_emp_ent_id.get().isdigit() and update_emp_ent_salary.get().isdigit():
			id = int(update_emp_ent_id.get())
			name = update_emp_ent_name.get()
			address = update_emp_ent_address.get()
			job_title = update_emp_ent_jobT.get()
			salary = int(update_emp_ent_salary.get())
			cursor.execute(sql%(name,address,job_title,salary,id))
			if cursor.rowcount == 1:
				con.commit()
				print('record updated')
				showinfo("Info", "Record Updated Successfully !!")
			else:
				print(id, 'does not exists ')
				showinfo("Info", "Entered ID Does Not Exists !!" )
		else:
			showinfo("Info", "ID and Salary Should be in Numbers !!")

		
	except Exception as e:
		con.rollback()
		print('issue', e)
	finally:
		update_emp_ent_id.delete(0,END)
		update_emp_ent_name.delete(0,END)
		update_emp_ent_address.delete(0,END)
		update_emp_ent_jobT.delete(0,END)
		update_emp_ent_salary.delete(0,END)
		update_emp_ent_id.focus()
		if con is not None:
			con.close()
			print('connection closed ')

def f11():
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "delete from emp_data where id = '%d'"
		if delete_emp_ent_id.get().isdigit():
			id = int(delete_emp_ent_id.get())
			cursor.execute(sql%(id))
			if cursor.rowcount == 1:
				con.commit()
				print('record deleted')
				showinfo("Info", "Record Deleted Successfully !!")
			else:
				print(id, 'does not exists ')
				showinfo("Info", "Entered ID Does Not Exists !!" )
		else:
			showinfo("Info", "ID Should be in Numbers !!")

	except Exception as e:
		con.rollback()
		print('issue', e)
	finally:
		delete_emp_ent_id.delete(0,END)
		delete_emp_ent_id.focus()
		if con is not None:
			con.close()
			print('connection closed ')

def f12():
	con = None
	try:
		con = connect("ems.db")
		sql = "select name, salary from emp_data order by salary desc limit 5;"	
		data = pd.read_sql(sql, con)
		
		plt.bar(data.name, data.salary)
		plt.title("Highest Earning Employee")
		plt.show()
	
	except Exception as e:
		#showerror("Issue ", e)
		print('issue', e)
	finally:
		if con is not None:
			con.close()
			print('connection closed ')


def f13():
	dt_c = datetime.now()

	if dt_c.hour < 12:
		state = str('Good Morning !')
	elif dt_c.hour < 16:
		state = str('Good Afternoon !')
	else:
		state = str('Good Evening !')
	
	return(state)

def confirmExit():
	if askyesno('Quit', 'Do you really want to quit?'):
		main_Menu.destroy()

	

g = geocoder.ip('me')
lat = str(g.lat)
lng = str(g.lng)
try:
	a1 = "https://api.openweathermap.org/data/2.5/weather"
	a2 = "?lat=" + lat 
	a3 = "&lon=" + lng
	a4 = "&appid=" + "c6e315d09197cec231495138183954bd"
	a5 = "&units=" + "metric"
	wa = a1 + a2+ a3 + a4 + a5
	res = get(wa)
	#print(res)
	data = res.json()
	#print(data)
	temp = data["main"]["temp"]
	city = data["name"]
	#print("temp =", temp)
	#print("city =", city)
except Exception as e:
	print("issue", e)


f = ("Georgia", 30, "bold")	# font
g = ("Georgia", 20, "bold")
h = ("Georgia", 15, "bold")
y = 20				#for padding

# Main menu GUI

main_Menu = Tk()
main_Menu.title("Employee Manager")
main_Menu.geometry("1000x600+50+50")
main_Menu.configure(bg="Black")


main_Menu_btn_add = Button(main_Menu, text="Create Employee", bg ="Yellow", font = f, width = 15, command = f1)
main_Menu_btn_view = Button(main_Menu, text="Employee List", bg ="Yellow", font = f, width = 15, command = f3)
main_Menu_btn_update = Button(main_Menu, text="Update Employee", bg ="Yellow", font = f, width = 15, command = f5)
main_Menu_btn_delete = Button(main_Menu, text="Delete Employee", bg ="Yellow", font = f, width = 15, command = f7)
main_Menu_btn_chart = Button(main_Menu, text="Chart", bg ="Yellow", font = f, width = 15, command = f12)

main_Menu_btn_add.place(relx = 0.05, rely = 0.25, width = 400, height = 55)
main_Menu_btn_view.place(relx = 0.54, rely = 0.25, width = 400, height = 55)
main_Menu_btn_update.place(relx = 0.05, rely = 0.45, width = 400, height = 55)
main_Menu_btn_delete.place(relx = 0.54, rely = 0.45, width = 400, height = 55)
main_Menu_btn_chart.place(relx = 0.3, rely = 0.65, width = 400, height = 55)

#Main Menu Info Labels

main_Menu_lab_wish = Label(main_Menu, text = f13(), bg = "Black", font = g, foreground = "Yellow")
main_Menu_lab_date = Label(main_Menu, text = "Date : " + str(datetime.now().date()), bg = "Black", font = g, foreground = "Yellow")
main_Menu_lab_loc  = Label(main_Menu, text = "City : " + city, bg = "Black", font = g, foreground = "Yellow")
main_Menu_lab_temp = Label(main_Menu, text = "Temperature : " + str(temp) + " C", bg = "Black", font = g, foreground = "Yellow")

main_Menu_lab_wish.place(relx = 0.05, rely = 0.07)
main_Menu_lab_date.place(relx = 0.6, rely = 0.07)
main_Menu_lab_loc.place(relx = 0.05, rely = 0.87)
main_Menu_lab_temp.place(relx = 0.65, rely = 0.87)

# Create employee GUI

create_emp = Toplevel(main_Menu)
create_emp.title("Create Employee")
create_emp.geometry("1000x700+50+50")
create_emp.configure(bg="Black")

create_emp_lab_id = Label(create_emp,    text=" Employee ID : ", bg ="Yellow", font = f)
create_emp_lab_name = Label(create_emp,    text=" Name : ", bg ="Yellow", font = f)
create_emp_lab_address = Label(create_emp, text=" Address : ", bg ="Yellow", font = f)
create_emp_lab_jobT = Label(create_emp,    text=" Job Title : ", bg ="Yellow", font = f)
create_emp_lab_salary = Label(create_emp,  text=" Salary : ", bg ="Yellow", font = f)
create_emp_ent_id = Entry(create_emp, font = f)
create_emp_ent_name = Entry(create_emp, font = f)
create_emp_ent_address = Entry(create_emp, font = f)
create_emp_ent_jobT = Entry(create_emp, font = f)
create_emp_ent_salary = Entry(create_emp, font = f)

create_emp_lab_id.place(relx = 0.025, rely = 0.10, width = 300, height = 50)
create_emp_ent_id.place(relx = 0.35, rely = 0.10, width = 600, height = 45)
create_emp_lab_name.place(relx = 0.05, rely = 0.25, width = 250, height = 50)
create_emp_ent_name.place(relx = 0.35, rely = 0.25, width = 600, height = 45)
create_emp_lab_address.place(relx = 0.05, rely = 0.40, width = 250, height = 50)
create_emp_ent_address.place(relx = 0.35, rely = 0.40, width = 600, height = 45)
create_emp_lab_jobT.place(relx = 0.05, rely = 0.55, width = 250, height = 50)
create_emp_ent_jobT.place(relx = 0.35, rely = 0.55, width = 600, height = 45)
create_emp_lab_salary.place(relx = 0.05, rely = 0.70, width = 250, height = 50)
create_emp_ent_salary.place(relx = 0.35, rely = 0.70, width = 600, height = 45)

create_emp_btn_save = Button(create_emp, text="Save", bg ="Yellow", font=f, width=15, command = f9)
create_emp_btn_back = Button(create_emp, text="Back", bg ="Yellow", font=f, width=15, command = f2)

create_emp_btn_save.place(relx = 0.20, rely = 0.85, width = 150, height = 60)
create_emp_btn_back.place(relx = 0.65, rely = 0.85, width = 150, height = 60)

create_emp.withdraw()

# View Employee Info GUI

emp_list = Toplevel(main_Menu)
emp_list.title("Employee List")
emp_list.geometry("1200x600+50+50")
emp_list.configure(bg="Black")

emp_list_st_data = ScrolledText(emp_list, width = 20, height = 10, font = h, bg = "Yellow")
emp_list_btn_back = Button(emp_list, text="Back", font = f, bg = "Yellow", command = f4)
emp_list_st_data.place(relx = 0.065, rely = 0.10, width = 1000, height = 400)
emp_list_btn_back.place(relx = 0.4, rely = 0.850, width = 150, height = 60)

emp_list.withdraw()

# Update Employee Info GUI

update_emp = Toplevel(main_Menu)
update_emp.title("Update Employee Information")
update_emp.geometry("1000x700+50+50")
update_emp.configure(bg="Black")

update_emp_lab_id = Label(update_emp, text="Employee ID", font = f, bg ="Yellow")
update_emp_lab_name = Label(update_emp, text="Name", font = f, bg ="Yellow")
update_emp_lab_address = Label(update_emp, text="Address", font = f, bg ="Yellow")
update_emp_lab_jobT = Label(update_emp, text="Job Title", font = f, bg ="Yellow")
update_emp_lab_salary = Label(update_emp, text="Salary", font = f, bg ="Yellow")
update_emp_ent_id = Entry(update_emp, font = f)
update_emp_ent_name = Entry(update_emp, font = f)
update_emp_ent_address = Entry(update_emp, font = f)
update_emp_ent_jobT = Entry(update_emp, font = f)
update_emp_ent_salary = Entry(update_emp, font = f)

update_emp_lab_id.place(relx = 0.05, rely = 0.10, width = 275, height = 50)
update_emp_ent_id.place(relx = 0.35, rely = 0.10, width = 600, height = 45)
update_emp_lab_name.place(relx = 0.05, rely = 0.25, width = 275, height = 50)
update_emp_ent_name.place(relx = 0.35, rely = 0.25, width = 600, height = 45)
update_emp_lab_address.place(relx = 0.05, rely = 0.40, width = 275, height = 50)
update_emp_ent_address.place(relx = 0.35, rely = 0.40, width = 600, height = 45)
update_emp_lab_jobT.place(relx = 0.05, rely = 0.55, width = 275, height = 50)
update_emp_ent_jobT.place(relx = 0.35, rely = 0.55, width = 600, height = 45)
update_emp_lab_salary.place(relx = 0.05, rely = 0.70, width = 275, height = 50)
update_emp_ent_salary.place(relx = 0.35, rely = 0.70, width = 600, height = 45)

update_emp_btn_update = Button(update_emp, text="Update", bg = "Yellow", font=f, width=15, command = f10)
update_emp_btn_back = Button(update_emp, text="Back", bg = "Yellow", font=f, width=15, command = f6)

update_emp_btn_update.place(relx = 0.20, rely = 0.85, width = 175, height = 60)
update_emp_btn_back.place(relx = 0.65, rely = 0.85, width = 150, height = 60)

update_emp.withdraw()

# Delete Employee Info GUI

delete_emp = Toplevel(main_Menu)
delete_emp.title("Delete Employee Information")
delete_emp.geometry("1000x250+50+50")
delete_emp.configure(bg = "Black")

delete_emp_lab_id = Label(delete_emp, text="Employee ID", bg = "Yellow", font = f)
delete_emp_ent_id = Entry(delete_emp, font = f)
delete_emp_lab_id.place(relx = 0.05, rely = 0.15, width = 275, height = 50)
delete_emp_ent_id.place(relx = 0.35, rely = 0.15, width = 600, height = 45)

delete_emp_btn_delete = Button(delete_emp, text="Delete", bg = "Yellow", font=f, width=15, command = f11)
delete_emp_btn_back = Button(delete_emp, text="Back", bg = "Yellow", font=f, width=15, command = f8)

delete_emp_btn_delete.place(relx = 0.20, rely = 0.6, width = 175, height = 60)
delete_emp_btn_back.place(relx = 0.65, rely = 0.6, width = 175, height = 60)

delete_emp.withdraw()

main_Menu.protocol('WM_DELETE_WINDOW',confirmExit)

main_Menu.mainloop()