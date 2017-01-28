##################################################################################################################################################################
#Written by Brandon Ruggles (brandonrninefive@gmail.com) :)
##################################################################################################################################################################

import json
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

confFile = None
orders = []
debug = True

try:
	#We read our JSON data from a file called 'checkout.conf' for simplicity and readability.
	confFile = open("checkout.conf")
	orders = json.loads(confFile.read())["orders"]
except Exception as e:
	print "Error: either no checkout.conf was found, or it contains invalid JSON syntax!"
	if(debug):
		print 'Error Details: ' + str(e)
	
def login(username, password):
	if(username != '' and password != ''):
		driver.get('https://manager.linode.com/')
		formTbody = driver.find_element_by_xpath('/html/body/div[@id="page"]/form/fieldset/table/tbody')
		usernameBox = formTbody.find_element_by_xpath('./tr[1]/td[2]/input')
		passwordBox = formTbody.find_element_by_xpath('./tr[2]/td[2]/input')
		usernameBox.send_keys(username)
		passwordBox.send_keys(password)
		passwordBox.send_keys(Keys.ENTER)
		return True
	return False
	
def purchaseServer(server):
	linodesButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/a[1]')
	linodesButton.click()
	formTbody = driver.find_element_by_xpath('/html/body/div[@id="page"]/form/table/tbody')
	linodeRadioButton = formTbody.find_element_by_xpath('./tr[1]/td/table/tbody/tr/td/label[@for="linode' + server["plan"]  + '.5"]')
	linodeRadioButton.click()
	locationSelect = formTbody.find_element_by_xpath('./tr[3]/td/select')
	locationSelect.click()
	locationSelect.send_keys(server["location"])
	locationSelect.send_keys(Keys.ENTER)
	addButton = formTbody.find_element_by_xpath('./tr[4]/td/input[2]')
	addButton.click()

orderIndex = 1
startTime = time.time()
for order in orders:
	print 'Processing order number ' + str(orderIndex) + '...'
	print ''
	driver = webdriver.Chrome() #Non-headless webdriver
	#driver = webdriver.PhantomJS() #Headless webdriver
	
	logged_in = login(order['username'], order['password'])
	if(logged_in):
		for server in order['servers']:
			try:
				for i in range(server['quantity']):
					purchaseServer(server)
					print 'Successfully purchased a server!'
			except Exception as e:
				print "Error purchasing the server! Attempting to proceed anyway. Server JSON info: " + str(server)
				if(debug):
					print 'Error Details: ' + str(e)
	else:
		print 'No username and/or password provided. The order cannot be processed.'
	orderIndex+=1
print 'Total elapsed script time: ' + str(time.time() - startTime) + ' second(s).'
