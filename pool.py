import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def parse_resource(s):
	s = s.strip();
	end = s.rfind(" ")
	limit = None
	if end > 0:
		limit = s[end+1:]
		s = s[:end]
		limit = limit.replace(".", "")
		if s.find(",") > 0:
			limit = limit.replace(",", ".")
			limit = float(limit)
		else:
			limit = int(limit)
	return s, limit

def parse_number(s):
	s = s.strip();
	end = s.find(" ")
	unit = None
	if end > 0:
		unit = s[end+1:]
		s = s[:end]
	s = s.replace(".", "");
	if s.find(",") > 0:
		s = s.replace(",", ".");
		return float(s), unit
	return int(s), unit

def fetch(username, password):
	result = {}

	driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
	driver.implicitly_wait(10)

	driver.get("https://rechnung.t-mobile.at/index.cfm")

	form_username = driver.find_element_by_name("account")
	form_password = driver.find_element_by_name("password")

	form_username.send_keys(username)
	form_password.send_keys(password)
	form_password.send_keys(Keys.RETURN)

	link = driver.find_element_by_link_text("Business Complete");
	link.click()

	table = driver.find_element_by_class_name("main_table")
	table_rows = table.find_elements_by_tag_name("tr")

	for row in table_rows[1:]:
		cell = row.find_elements_by_tag_name("td")
		resource = parse_resource(cell[2].text)
		used = parse_number(cell[3].text)
		free = parse_number(cell[5].text)
		result[resource[0]] = {"used": used[0], "limit": used[0] + free[0], "unit": used[1]}

	driver.close()
	return result

