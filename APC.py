"""
Created by Prasad DS
Updated on 27th December 2019
BeautifulSoup, Requests, Smtplib
"""



import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import time



def check_price(product_url,desired_price,receiver_id):
	"""Function to webscrape Amazon page regarding a specific and
	desired product and alert-mail the user in case of price drop"""

	browser_info={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"}

	product_website=requests.get(product_url,headers=browser_info)

	if product_website.status_code!=200:
		print("Bad Request!!!")
		print("Please Try Again Later!!!")
		return -100

	product_source=product_website.content 

	product_soup=BeautifulSoup(product_source,"lxml")

	product_title_tag=product_soup.find(id="productTitle")
	product_title=product_title_tag.text
	product_title=product_title.strip()

	product_price_tag=product_soup.find(id="priceblock_ourprice")
	product_price=product_price_tag.text
	product_price=product_price.strip()
	product_price=str_to_float(product_price)

	desired_price=float(desired_price)

	#Compare current product price and desired product price
	#If favourable price is there, send an automated mail
	if product_price <= desired_price:
		send_mail(product_url,product_price,receiver_id)



def str_to_float(str1):
	"""Function to remove unreadable price symbols
	remove comma[,] from str1 by split method and
	join method and finally convert it into float
	from string and return the vale"""
	price_str=str1
	price_str=price_str[2:]

	list1=price_str.split(",")
	price_str="".join(list1)

	price_float=float(price_str)

	return price_float



def send_mail(product_url,product_price,receiver_id):
	"""Function to send automated mail 
	regarding product price drop along with
	product title, its URL and its price"""

	with smtplib.SMTP("smtp.gmail.com",587) as connection1:
		connection1.ehlo()						#Identification of server connection
		connection1.starttls()					#Encryption of the connection traffic
		connection1.ehlo()						#Identification of encrypted server connection

		#Function to get login credentials from reading a file
		#Its recommended not to add sensitive information to script directly
		(sender_id,sender_password)=get_credentials()
		connection1.login(sender_id,sender_password)

		message=create_message(sender_id,receiver_id,product_url,product_price)
		connection1.send_message(message)


def get_credentials():
	"""Function to open and read a file to get 
	login credentials and return the information"""

	with open("Credentials.txt","r") as file1:
		list1=file1.readlines()
		sender_id_line=list1[1]
		garbage1,sender_id=sender_id_line.split(":")
		sender_id=sender_id.strip()

		sender_password_line=list1[2]
		garbage2,sender_password=sender_password_line.split(":")
		sender_password=sender_password.strip()

	return (sender_id,sender_password)



def create_message(sender_id,receiver_id,product_url,product_price):
	"""Function to create a proper and formatted message 
	containing an alert text regarding the price drop of
	the desired product in an email format"""

	message=EmailMessage()
	message["From"]=sender_id
	message["To"]=receiver_id
	message["Subject"]="PRICE DROP!!!"
	body_text="Hey!\nThere is a price-drop of the product in your wishlist.\n"
	body_text+="The effective price has dropped to Rupees {}.\n".format(product_price)
	body_text+="Checkout this link: {}".format(product_url)
	message.set_content(body_text)

	return message



#Taking input from users

product_url=input("Please enter the Amazon URL of the product you want to track:	")

desired_price=input("Please enter the desired price at which you want to buy the product:(Enter in numbers)	")

receiver_id=input("Please enter the email id you want to recieve notifications to:	")

check_time=input("How frequently you want to check the product:(Enter the number in hours)	")
check_time=int(check_time)
check_time=check_time*3600

while(True):													#Forever TRUE statement
	check_price(product_url,desired_price,receiver_id)			#Function calling to check product price frequently
	time.sleep(check_time)										#Pause the program for certain time
