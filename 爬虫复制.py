from bs4 import BeautifulSoup
html_sample = ' \
<html> \
<body> \
<h1 id="title">Hello World</h1> \
<a href="#" class="link">This is link1</a> \
<a href="# link2" class="link" id="10">This is link2</a> \
</body> \
</html>'

soup = BeautifulSoup(html_sample,"html.parser")
soup1 = BeautifulSoup(html_sample,"html.parser")
b = soup.findAll("a",attrs ={"id":"10"})
print(soup.text)
for price in b:
    print(price.string)