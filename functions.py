""" Fonctions """
import csv
import urllib.request
import os
import requests
from bs4 import BeautifulSoup

TIMEOUT_VALUE = 5 # en secondes

# Fonction qui retourne une liste de dictionnaires de categories [Name, Link]
def get_all_category(url):
    ##### URL DU SITE #####
    #url = "http://books.toscrape.com/"

    response = requests.get(url, timeout=TIMEOUT_VALUE)

    #Liste de dictionnaires de categories et son lien
    data_categories = []

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        #Récupérer le div dont l'attribut class est side_categories
        div_side_categories = soup.find('div', {'class':'side_categories'})

        #Récuperer tout les éléments avec comme attribut a
        categories = div_side_categories.findAll('a')

        #Créer un dictionnaire pour chaque categorie sauf le premier attribut a
        #et le mettre dans la liste de dictionnaires 
        for category in categories[1:]:
            dict_categories = {}
            #recuperation de text avec .get_text
            # .strip() pour enlever les espaces
            category_name = category.get_text().strip()
            #print(category_name)
            
            #recuperation de l'attribut
            link = 'https://books.toscrape.com/'
            category_link = link + category['href']
            #print(category_link)

            #Ajout dans un dictionnaire pour une categorie
            dict_categories["name"] = category_name
            dict_categories["link"] = category_link

            data_categories.append(dict_categories)
    
    return data_categories

# Fonction qui retourne une liste de dictionnaires de livres [Name, Link]
def get_book_url_by_categories(url_cat):

    ###### URL DE LA CATEGORIE ######
    #url_cat = data_categories[3].get("link") # Donne l'URL de la catégorie présent dans le dictionnaire lui-même présent à la première place de la liste de dictionnaire de catégories
    #print(url_cat)

    # --------------------------------------------------------------------------
    # Récupérer le nombre de livres
    # --------------------------------------------------------------------------

    response = requests.get(url_cat, timeout=TIMEOUT_VALUE)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
    #nouvelle request + nouveau soup
    form_qty = soup.find('form', {'class':'form-horizontal'})
    strong_text = form_qty.find('strong').get_text()
    print(strong_text)

    # Conversion d'un string en int
    book_qty = int(strong_text)

    # On détermine s'il y a plusieurs pages de 20 livres
    page_qty = (book_qty // 20) + 1 # modulo quantity
    print("moodulo :" + str(page_qty))
    if page_qty > 1:
        print("il y a plusieurs pages")


    # Liste contenant des dictionnaires correspondant à chaque livre
    book_list = []

    # Début de l'url pour chaque livre
    url_book_begin = "https://books.toscrape.com/catalogue"
    
    if page_qty > 1:
        page_nbr = 1
        while page_nbr <= page_qty:
            print("page_nbr a pour valeur", page_nbr)
            page_nbr_string = str(page_nbr)
            if page_nbr == 1:
                url_cat = url_cat.replace('index.html','page-' + page_nbr_string + '.html')

                response = requests.get(url_cat, timeout=TIMEOUT_VALUE)
                if response.ok:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    div_product_pod = soup.findAll('article', {'class':'product_pod'})
                    #print(div_product_pod)

                    for book in div_product_pod:
                        # Un dictionnaire contenant noms de livre + lien
                        dict_book = {}
                        #print("+"*50)
                        book_name = book.find('h3').get_text().strip()
                        dict_book["name"] = book_name
                        print(dict_book["name"])
                        book_link = book.find('a').get('href').replace('../../..',url_book_begin)
                        dict_book["link"] = book_link
                        print(dict_book["link"])
                        book_list.append(dict_book)
            else:
                page_nbr_actuel = str(page_nbr - 1)
                url_cat = url_cat.replace('page-' + page_nbr_actuel + '.html','page-' + page_nbr_string + '.html')

                response = requests.get(url_cat, timeout=TIMEOUT_VALUE)
                if response.ok:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    div_product_pod = soup.findAll('article', {'class':'product_pod'})
                    #print(div_product_pod)

                    for book in div_product_pod:
                        # Un dictionnaire contenant noms de livre + lien
                        dict_book = {}
                        #print("+"*50)
                        book_name = book.find('h3').get_text().strip()
                        dict_book["name"] = book_name
                        print(dict_book["name"])
                        book_link = book.find('a').get('href').replace('../../..',url_book_begin)
                        dict_book["link"] = book_link
                        print(dict_book["link"])
                        book_list.append(dict_book)

            print(url_cat)
            page_nbr = page_nbr + 1
    else:
        response = requests.get(url_cat, timeout=TIMEOUT_VALUE)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')

            div_product_pod = soup.findAll('article', {'class':'product_pod'})
            #print(div_product_pod)

            for book in div_product_pod:
                # Un dictionnaire contenant noms de livre + lien
                dict_book = {}
                #print("+"*50)
                book_name = book.find('h3').get_text().strip()
                dict_book["name"] = book_name
                print(dict_book["name"])
                book_link = book.find('a').get('href').replace('../../..',url_book_begin)
                dict_book["link"] = book_link
                print(dict_book["link"])
                book_list.append(dict_book)


    return book_list

# Fonction qui retourne un dictionnaires contenant les informations d'un livre
def get_book_data(url_book):

    ###### URL DU LIVRE ######
    #url_book = book_list[0].get("link")
    #print(url_book)

    ##### URL DU SITE #####
    url = "http://books.toscrape.com/"

    # --------------------------------------------------------------------------
    # Récupérer des informations sur le livre et les mettre dans un dictionnaire
    # --------------------------------------------------------------------------
    response = requests.get(url_book, timeout=TIMEOUT_VALUE)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

    book_infos = {} #Création du dictionnaire
    book_infos["product_page_url"] = url_book #Ajout au dictionnaire
    
    # Récupérer des infos contenues dans une table
    table_book_infos = soup.find('table', {'class':'table table-striped'})
    row_list = table_book_infos.findAll('tr')

    for row in row_list:
        row_header = row.th.get_text()
        row_cell = row.td.get_text()

        if row_header == "UPC":
            row_header = "universal_product_code" 
        if row_header == "Product Type":
            continue
        if row_header == "Price (excl. tax)":
            row_header = "price_excluding_tax" 
        if row_header == "Price (incl. tax)":
            row_header = "price_including_tax" 
        if row_header == "Tax":
            continue
        if row_header == "Availability":
            row_header = "number_available"         
        if row_header == "Number of reviews":
            row_header = "review_rating"      

        row_cell = row_cell.replace('In stock (','')     
        row_cell = row_cell.replace(' available)','') 
        row_cell = row_cell.replace('Â£','£')    
        
        book_infos[row_header] = row_cell #Ajout au dictionnaire

    # Recupération de la description du livre
    book_desc = soup.find('article', {'class':'product_page'})
    if book_desc.find('p', {'class':''}):
        p_text = book_desc.find('p', {'class':''}).get_text()
    else:
        p_text = ''

    #p_text = p_text.replace('â','\"')
    book_infos["product_description"] = p_text #Ajout au dictionnaire

    # Recupération de la category du livre et du titre
    book_infos_in_list = soup.find('ul', {'class':'breadcrumb'})
    li_book = book_infos_in_list.findAll('li')

    book_cat_text = li_book[2].find('a').get_text()
    book_title = li_book[3].get_text()

    book_infos["category"] = book_cat_text #Ajout au dictionnaire
    book_infos["title"] = book_title #Ajout au dictionnaire

    # Récupérer l'URL de l'image du livre 
    div_image = soup.find('div', {'class':'item active'})
    img_link = div_image.find('img').get('src').replace('../../',url)

    book_infos["image_url"] = img_link #Ajout au dictionnaire

    # Récupérer l'image du livre et la stocker dans le dossier images
    urllib.request.urlretrieve(img_link, "images/Image.jpg")

    return book_infos 

# Fonction qui retourne un dictionnaires contenant les informations d'un livre
def get_image(url_img):
    filename = os.path.basename(url_img) #recupere le nom du fichier
    urllib.request.urlretrieve(url_img, "images/" + filename)

# Fonction qui crée un fichier CSV
def get_csv(book_cat, book_field, books):
    
    with open(f'CSV/{book_cat}.csv', 'w', newline='') as csvfile:
        fieldnames = []
        for key in book_field:
            fieldnames.append(key)
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print(fieldnames)
        writer.writeheader()
        for book_data in books:
            writer.writerow(book_data)
    

