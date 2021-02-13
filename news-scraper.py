from flask import Flask, render_template, redirect
from requests_html import HTMLSession
app = Flask(__name__)
#starts up session 
session = HTMLSession()
#gets google news home page and then renders html
r = session.get('https://news.google.com/topstories?hl=en-GB&gl=GB&ceid=GB:en')
r.html.render()
#searches html for article then img tags
articles = r.html.find("article")
images = r.html.find("img")
#creating empty lists for values to be stored later
initial_articles = []
initial_images = []
#route function for starting home page
@app.route("/", methods= ["get"])
def home():
  #iterates through each article tag found
  sub_title = "Top stories:"
  for item in articles:
    try:
      news_item = item.find('h3', first=True)
      news_title = news_item.text
      news_link = news_item.absolute_links
      article={
      #slices link to remove uneeded characters at front and back, so it..
      #can be used later
      "link":str(news_link)[2:-2],
      "title":news_title
      }
      #appends most recently created article to the article list
      initial_articles.append(article)
    except:
      #if article tag found is not h3, then it is ignored
      pass
  #iterates through all img tags found in the page's html
  for image in images:
    #checks if each image's src to see if it is a blank google image
    no = "https://lh3.googleusercontent.com/JDFOyo903E9WGstK0YhI2ZFOKR3h4qDxBngX5M8XJVBZFKzOBoxLmk3OVlgNw9SOE-HfkNgb"
    if no in image.attrs["src"]:
      pass
    else:
      #if not, the src is extracted into "image" under the "img" value
      news_img = image.attrs["src"]
      image={
        "img": news_img
      }
      #then appended to the image dictionary
      initial_images.append(image)
  #renders starting home page with breaking stories and their related articles with images
  return render_template("main_page.html", items=initial_articles, images = initial_images, sub_title = sub_title, length=5)

#route function for search terms - get method
@app.route("/<searcher>", methods=["GET"])
def search(searcher):
  sub_title = f"Top results for {searcher}:"
  #searches google news for the term the user enters then renders the html
  finds = session.get(f"https://news.google.com/search?q={searcher}&hl=en-GB&gl=GB&ceid=GB%3Aen")
  finds.html.render()
  #searches the html for article and img tags
  articles = finds.html.find("article")
  images = finds.html.find("img")
  #creates empty lists for the src's and articles to be added to later
  searched_articles = []
  searched_images = []
  for article in articles:
    try:
      article_item = article.find("h3", first=True)
      article_title = article_item.text
      article_link = article_item.absolute_links
      search_news = {
        'title': article_title,
        'link': str(article_link)[2:-2]
      }
      searched_articles.append(search_news)
    except:
      pass
  for image in images:
    no = "https://lh3.googleusercontent.com/JDFOyo903E9WGstK0YhI2ZFOKR3h4qDxBngX5M8XJVBZFKzOBoxLmk3OVlgNw9SOE-HfkNgb"
    if no in image.attrs["src"]:
      pass
    else:
      news_img = image.attrs["src"]
      image={
        "img": news_img
      }
      searched_images.append(image)

  return render_template("main_page.html", items=searched_articles, images = searched_images, sub_title = sub_title, length=5)
if __name__ == "__main__":
    app.run(debug=True)