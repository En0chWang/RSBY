import sys
import json
import mysql.connector
import requests


def dot_product(x, category_binary_vector):
    x = map(int, x.split(','))
    return sum(i[0] * i[1] for i in zip(x, category_binary_vector))


def main(category_binary_vector, price, rating, city, state):
    cnx = mysql.connector.connect(
        user='root',
        password='wangyinuo696683',
        host='database-1.cjy5mlvqnx2k.us-west-1.rds.amazonaws.com',
        database='restaurant')
    cursor = cnx.cursor()
    query = "select * from restaurant_basic_info left join restaurant_vector on restaurant_basic_info.business_id = restaurant_vector.business_id where stars >= '%s' and price >= '%s' and city = '%s' and state = '%s';" % (
        rating, price, city, state)
    cursor.execute(query)

    sub_li = []
    for name in cursor:
        temp_list = list(name)
        temp_list[-1] = dot_product(temp_list[-1], category_binary_vector)
        sub_li.append(temp_list)
    cursor.close()
    sub_li.sort(key=lambda i: i[-1], reverse=True)

    res_list = []
    for i in range(min(10, len(sub_li))):
        res_list.append(sub_li[i])
    response_list = []
    for each in res_list:
        url = "https://api.yelp.com/v3/businesses/%s" % (each[0])

        payload = {}
        headers = {
            'Authorization': 'Bearer Rd1MPDe-jclgH88GgLpwIXviyb5ujN8uRr_8E0YBhrELRUrHIQLTSrEE935jUfEVaDHutQvSOqxlUsKRYngDgf5XwE6rZSp972Q9JVeU8PlsucB0ydeiYBejvoBUXHYx'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        response_list.append({
            'business_id': each[0],
            'name': each[1],
            'address': each[2],
            'city': each[3],
            'state': each[4],
            'categories': each[5],
            'is_open': each[6],
            'stars': each[8],
            'price': each[9],
            'review_count': each[10],
            'photo': response['image_url']
        })
    print(json.dumps(response_list))


if __name__ == "__main__":
    category = sys.argv[1].lower()
    price = sys.argv[2]
    if price == '$':
        price = 1
    elif price == '$$':
        price = 2
    elif price == '$$$':
        price = 3
    else:
        price = 4
    rating = sys.argv[3]
    city = sys.argv[4]
    state = sys.argv[5]

    restaurant_list = ['butcher', 'dumplings', 'fondue', 'laotian', 'cambodian', 'pan asian', 'indian', 'german', 'signature cuisine', 'basque', 'polynesian', 'shaved snow', 'juice bars & smoothies', 'persian/iranian', 'canadian (new)', 'sugar shacks', 'indonesian', 'cheesesteaks', 'donairs', 'brazilian', 'swiss food', 'catalan', 'bakeries', 'kombucha', 'specialty food', 'taiwanese', 'coffee & tea', 'soul food', 'eastern european', 'hungarian', 'buffets', 'cideries', 'delis', 'gluten-free', 'american (new)', 'russian', 'comfort food', 'african', 'hawaiian', 'international grocery', 'sri lankan', 'milkshake bars', 'syrian', 'sushi bars', 'supper clubs', 'ice cream & frozen yogurt', 'czech/slovakian', 'backshop', 'vegan', 'food court', 'thai', 'cafes', 'food delivery services', 'nicaraguan', 'pretzels', 'bubble tea', 'kebab', 'modern european', 'scottish', 'tapas/small plates', 'acai bowls', 'coffee & tea supplies', 'fish & chips', 'middle eastern', 'csa', 'peruvian', 'internet cafes', 'poutineries', 'austrian', 'bagels', 'sandwiches', 'hong kong style cafe', 'tex-mex', 'waffles', 'donuts', 'breakfast & brunch', 'do-it-yourself food', 'british', 'polish', 'honey', 'eritrean', 'salad', 'game meat', 'desserts', 'belgian', 'pizza', 'beverage store', 'armenian', 'ethiopian', 'pakistani', 'chicken wings', 'seafood', 'street vendors', 'cafeteria',
                       'honduran', 'southern', 'smokehouse', 'barbeque', 'himalayan/nepalese', 'uzbek', 'water stores', 'imported food', 'beer hall', 'american (traditional)', 'cupcakes', 'latin american', 'ukrainian', 'shaved ice', 'creperies', 'chicken shop', 'international', 'burmese', 'delicatessen', 'rotisserie chicken', 'kosher', 'vietnamese', 'bulgarian', 'diners', 'bistros', 'japanese', 'caribbean', 'convenience stores', 'malaysian', 'mediterranean', 'arabian', 'turkish', 'halal', 'farmers market', 'mexican', 'new mexican cuisine', 'chinese', 'korean', 'greek', 'steakhouses', 'kiosk', 'slovakian', 'grocery', 'organic stores', 'moroccan', 'island pub', 'churros', 'noodles', 'coffee roasteries', 'guamanian', 'custom cakes', 'patisserie/cake shop', 'brasseries', 'food trucks', 'empanadas', 'beer garden', 'cuban', 'australian', 'soup', 'irish', 'burgers', 'tapas bars', 'chimney cakes', 'spanish', 'bangladeshi', 'poke', 'cajun/creole', 'czech', 'gastropubs', 'fast food', 'japanese sweets', 'wineries', 'hot dogs', 'hot pot', 'pita', 'scandinavian', 'argentine', 'distilleries', 'portuguese', 'live/raw food', 'mongolian', 'pub food', 'asian fusion', 'gelato', 'french', 'breweries', 'wraps', 'filipino', 'singaporean', 'pop-up restaurants', 'food stands', 'ethical grocery', 'meaderies', 'dinner theater', 'vegetarian', 'italian', 'afghan', 'tea rooms', 'iberian']

    category_set = set(category.split(" "))
    category_binary_vector = list(
        map(lambda x: 1 if len(set(x.split(' ')).intersection(category_set)) > 0 else 0, restaurant_list))
    main(category_binary_vector, price, rating, city, state)
