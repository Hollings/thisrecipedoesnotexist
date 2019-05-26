from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import requests
import json
import twitter 
f = open("conf.json","r")
config = json.loads(f.read());

def wrap_text(text, width, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = text.split()
    font_size = font.getsize(text)

    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        w, h = font.getsize(' '.join(text_line))
        if w > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

    if len(text_line) > 0:
        text_lines.append(' '.join(text_line))

    return text_lines

r = requests.request(url="https://thisrecipedoesnotexist.com/api/recipe", method='get');
# print(r.text)
recipeData = json.loads(r.text)
titleText = recipeData['title']
ingredients = json.loads(recipeData['ingredients'])
directions = json.loads(recipeData['directions'])
inputText = ""
for line in ingredients:
	inputText += "\n" + line
inputText += "\n"	
for line in directions:
	inputText += "\n\n\t" + line



# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("font/arial.ttf", 14)
titleFont = ImageFont.truetype("font/journal.ttf", 40)
textLines = wrap_text(inputText, 450, ImageFont.truetype("font/arial.ttf", 14))
titleLines = wrap_text(titleText, 500, ImageFont.truetype("font/journal.ttf", 40))

finalText = "\n".join(textLines);
finalTitle = "\n".join(titleLines);

titleHeight = (len(titleLines) * 40)
height = (len(textLines) * 16) + titleHeight;

# print(finalText)
# print(font.getsize(finalText))
print(titleHeight)

img = Image.new("RGB", (600, height + 100), "#eee")
draw = ImageDraw.Draw(img)

draw.text((50, 20),finalTitle,(0,0,0),font=titleFont)
draw.text((75, 40 + titleHeight),finalText,(0,0,0),font=font)


img.save('sample-out.png', format='PNG', quality=100)


api = twitter.Api(config['consumer_key'],
                  config['consumer_secret'],
                  config['access_token_key'],
                  config['access_token_secret']
                  )

api.PostUpdate(titleText + " - thisrecipedoesnotexist.com/" + str(recipeData['id']), 'sample-out.png');