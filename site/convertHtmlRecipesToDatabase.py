#!/usr/bin/python3

import pymysql
import os
from bs4 import BeautifulSoup
import json
def getRecipeData(file):
	f = open(file,"r")
	contents = f.read()

	soup = BeautifulSoup(contents, 'html.parser')


	if soup.h1 and len(soup.h1.text) < 254:
		print(soup.h1.text)
		title = soup.h1.text
	else:
		return False


	ing = soup.find_all("div", class_="ing")
	if len(ing) > 0:
		ingredients = ing[0].text.split("- ")[1:]
	else:
		return False

	dir = soup.find_all("div", class_="dir")
	if len(dir) > 0:
		directions = dir[0].text.split("- ")[1:]
	else:
		return False

	return [title, json.dumps(ingredients), json.dumps(directions)]




def addRecipe(recipeData):
	# Open database connection
	

	# Prepare SQL query to INSERT a record into the database.
	# sql = "INSERT INTO recipes(title, ingredients, directions) VALUES ('%s', '%s', '%s')" % (recipeData[0], recipeData[1], recipeData[2])
	cursor.execute("INSERT INTO recipes(title, ingredients, directions) VALUES (%s, %s, %s)", [recipeData[0], recipeData[1], recipeData[2]])
	# print("about to execute(%s)" % sql)

	# Commit your changes in the database
	db.commit()



path = 'C:\\Winginx\\home\\recipehtml'
db = pymysql.connect("localhost","root","","recipe" )
# prepare a cursor object using cursor() method
cursor = db.cursor()

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.html' in file:
            files.append(os.path.join(r, file))

for f in files:
	recipeData = getRecipeData(f)
	if recipeData:
		addRecipe(recipeData)


# disconnect from server
db.close()


