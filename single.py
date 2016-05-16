import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def parse_resource(s):
	return s.strip()

def parse_number(s):
	s = s.strip()
	s = s.replace(".", "")
	if s.find(",") > 0:
		s = s.replace(",", ".");
		return float(s), unit
	return int(s)

def fetch(username, password):
	result = []

	driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
	driver.implicitly_wait(10)

	driver.get("https://mein.t-mobile.at/myTNT/invoice.page")

	form_username = driver.find_element_by_name("j_username")
	form_password = driver.find_element_by_name("j_password")

	form_username.send_keys(username)
	form_password.send_keys(password)
	form_password.send_keys(Keys.RETURN)

	container = driver.find_element_by_class_name("graph-box").find_element_by_class_name("c12")
	rows = container.find_elements_by_class_name("row")

	for row in rows[:-1]:
		resource = parse_resource(row.find_element_by_class_name("title").text)
		used = parse_number(row.find_element_by_class_name("used").text)
		limit = parse_number(row.find_element_by_class_name("total").text)
		result.append((resource, used, limit))

	driver.close()
	return result

