##################################################################################################################################################################
#Written by Brandon Ruggles (brandonrninefive@gmail.com) :)
##################################################################################################################################################################

import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

confFile = None
orders = []
ipList = []
nameList = []
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
	try:
		formTbody = driver.find_element_by_xpath('/html/body/div[@id="page"]/form/table/tbody')
		linodeRadioButton = formTbody.find_element_by_xpath('./tr[1]/td/table/tbody/tr/td/label[@for="linode' + server["plan"]  + '.5"]')
		linodeRadioButton.click()
		locationSelect = formTbody.find_element_by_xpath('./tr[3]/td/select')
		locationSelect.click()
		locationSelect.send_keys(server["location"])
		locationSelect.send_keys(Keys.ENTER)
		addButton = formTbody.find_element_by_xpath('./tr[4]/td/input[2]')
		addButton.click()
		print 'Successfully purchased a new server!'
	except Exception as e:
		print "Couldn't find the linode buttons...attempting to click the 'Add a Linode' button instead..."
		if(debug):
			print 'Error details: ' + str(e)
		addButton = driver.find_element_by_xpath('/html/body/div[@id="page"]/table/tfoot/tr/td/a[3]')
		addButton.click()
		formTbody = driver.find_element_by_xpath('/html/body/div[@id="page"]/form/table/tbody')
		linodeRadioButton = formTbody.find_element_by_xpath('./tr[1]/td/table/tbody/tr/td/label[@for="linode' + server["plan"]  + '.5"]')
		linodeRadioButton.click()
		locationSelect = formTbody.find_element_by_xpath('./tr[3]/td/select')
		locationSelect.click()
		locationSelect.send_keys(server["location"])
		locationSelect.send_keys(Keys.ENTER)
		addButton = formTbody.find_element_by_xpath('./tr[4]/td/input[2]')
		addButton.click()
		print 'Successfully purchased a new server!'

def configureServer(server):
	print 'Attempting to configure the server...'
	tableTbody = driver.find_element_by_xpath('/html/body/div[@id="page"]/table/tbody')
	linodes = tableTbody.find_elements_by_xpath('./tr')
	for linode in linodes:
		name = linode.find_element_by_xpath('./td[1]')
		status = linode.find_element_by_xpath('./td[2]')
		ip = linode.find_element_by_xpath('./td[4]')
		dashboardButton = linode.find_element_by_xpath('./td[7]/a[1]')
		if(name.text not in nameList and (status.text == 'Brand New' or status.text == 'Being Created')):
			nameList.append(name.text)
			ipList.append(ip.text)
			dashboardButton.click()
			imageButton = driver.find_element_by_xpath('/html/body/div[@id="page"]/table/tbody/tr/td/div[@id="dashboard_configs"]/form/table/tbody/tr[3]/td[2]/a[2]')
			imageButton.click()
			formTbody = driver.find_element_by_xpath('/html/body/div[@id="page"]/form/table/tbody')
			if(server["image"] != ""):
				imageSelect = formTbody.find_element_by_xpath('./tr[2]/td[2]/select')
				imageSelect.click()
				imageSelect.send_keys(server["image"])
				imageSelect.send_keys(Keys.ENTER)
			if(server["disk_size"] != ""):
				diskBox = formTbody.find_element_by_xpath('./tr[3]/td[2]/input')
				diskBox.send_keys(server["disk_size"])
			if(server["swap_disk"] != ""):
				swapSelect = formTbody.find_element_by_xpath('./tr[4]/td[2]/select')
				swapSelect.send_keys(server["swap_disk"])
				swapSelect.send_keys(Keys.ENTER)
			passBox = formTbody.find_element_by_xpath('./tr[5]/td[2]/input')
			passBox.send_keys(server["root_pass"])
			passBox.send_keys(Keys.ENTER)
			bootButton = driver.find_element_by_xpath('/html/body/div[@id="page"]/table/tbody/tr/td[1]/div[@id="dashboard_configs"]/form/table/tbody/tr[4]/td[1]/input')
			bootButton.click()
			alert = driver.switch_to_alert()
			alert.accept()
			linodesButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/a[1]')
			linodesButton.click()
			break
				
def outputPurchaseInfo():
	print 'Outputting info on the purchased servers... The following messages will also be written to the local file "servers.txt".'
	print ''
	outputFile = open('servers.txt','a')
	outputFile.write(str(datetime.datetime.now()) + '\n')
	outputFile.write('--------------------\n')
	print 'Purchased the following Linodes:'
	outputFile.write('Purchased the following Linodes:\n')
	for i in range(len(nameList)):
		print nameList[i] + ' - ' + ipList[i]
		outputFile.write(nameList[i] + ' - ' + ipList[i] + '\n')
	print ''
	print 'Note: The Linodes may take a few minutes to start running.'
	outputFile.write('Note: The Linodes may take a few minutes to start running.\n')
	outputFile.write('\n')
	outputFile.close()

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
					configureServer(server)
			except Exception as e:
				print "Error purchasing the server! Attempting to proceed anyway. Server JSON info: " + str(server)
				if(debug):
					print 'Error Details: ' + str(e)
	else:
		print 'No username and/or password provided. The order cannot be processed.'
	orderIndex+=1
outputPurchaseInfo()
print ''
print 'Total elapsed script time: ' + str(time.time() - startTime) + ' second(s).'
