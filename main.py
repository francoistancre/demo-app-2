from functions import get_all_category
from functions import get_book_url_by_categories
from functions import get_book_data
from functions import get_image
from functions import get_csv
import os

##### URL DU SITE #####
url = "http://books.toscrape.com/"

data_categories = get_all_category(url)
#print(data_categories)

dict_fieldname = {"product_page_url" : "", "universal_product_code" : "", "price_excluding_tax" : "", "price_including_tax" : "", "number_available" : "", "review_rating" : "", "product_description" : "", "category" : "", "title" : "", "image_url" : ""}
#"universal_product_code" : "", "price_excluding_tax" : "", "price_including_tax" : "", "number_available" : "", "review_rating" : "", "product_description" : "", "category" : "", "title" : "", "image_url" : ""

#newWriter = get_csv(dict_fieldname)

if not os.path.exists("CSV"):
    # if the demo_folder directory is not present 
    # then create it.
    os.makedirs("CSV")

if not os.path.exists("images"):
    # if the demo_folder directory is not present 
    # then create it.
    os.makedirs("images")

for category_url in data_categories:
    #le but de la boucle : pour chaque categories execute ci-dessous
    books = []
    ###### URL DE LA CATEGORIE ###### 
    url_cat = category_url.get("link") # Donne l'URL de la catégorie présent dans le dictionnaire lui-même présent à la première place de la liste de dictionnaire de catégories
    #print(url_cat)

    book_url_categories = get_book_url_by_categories(url_cat)
    #print(book_url_categories)

    for book_url_category in book_url_categories:

        ###### URL DU LIVRE ######
        url_book = book_url_category.get("link")
        #print(url_book)

        book = get_book_data(url_book)
        books.append(book)
        #print(book_list)
        ###### URL DE L'IMAGE DU LIVRE ######
        url_imgage = book["image_url"]
        img = get_image(url_imgage)
    
    get_csv(category_url.get("name"), dict_fieldname, books)        
        

