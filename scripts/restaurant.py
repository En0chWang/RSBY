import sys
import json
import mysql.connector
import heapq


def dot_product(x, category_binary_vector):
    x = map(int, x.split(','))
    return sum(i[0] * i[1] for i in zip(x, category_binary_vector))


def main(category_binary_vector, price, rating):
    cnx = mysql.connector.connect(
        user='root',
        password='wangyinuo696683',
        host='database-1.cjy5mlvqnx2k.us-west-1.rds.amazonaws.com',
        database='restaurant')
    cursor = cnx.cursor()
    query = "select * from restaurant_basic_info left join restaurant_vector on restaurant_basic_info.business_id = restaurant_vector.business_id where stars >= '%s' and price >= '%s';" % (
        rating, price)
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
            'review_count': each[10]
        })
    print(json.dumps(response_list))


if __name__ == "__main__":
    category = sys.argv[1]
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

    restaurant_list = ['Butcher', 'Dumplings', 'Fondue', 'Laotian', 'Cambodian', 'Pan Asian', 'Indian', 'German', 'Signature Cuisine', 'Basque', 'Polynesian', 'Shaved Snow', 'Juice Bars & Smoothies', 'Persian/Iranian', 'Canadian (New)', 'Sugar Shacks', 'Indonesian', 'Cheesesteaks', 'Donairs', 'Brazilian', 'Swiss Food', 'Catalan', 'Bakeries', 'Kombucha', 'Specialty Food', 'Taiwanese', 'Coffee & Tea', 'Soul Food', 'Eastern European', 'Hungarian', 'Buffets', 'Cideries', 'Delis', 'Gluten-Free', 'American (New)', 'Russian', 'Comfort Food', 'African', 'Hawaiian', 'International Grocery', 'Sri Lankan', 'Milkshake Bars', 'Syrian', 'Sushi Bars', 'Supper Clubs', 'Ice Cream & Frozen Yogurt', 'Czech/Slovakian', 'Backshop', 'Vegan', 'Food Court', 'Thai', 'Cafes', 'Food Delivery Services', 'Nicaraguan', 'Pretzels', 'Bubble Tea', 'Kebab', 'Modern European', 'Scottish', 'Tapas/Small Plates', 'Acai Bowls', 'Coffee & Tea Supplies', 'Fish & Chips', 'Middle Eastern', 'CSA', 'Peruvian', 'Internet Cafes', 'Poutineries', 'Austrian', 'Bagels', 'Sandwiches', 'Hong Kong Style Cafe', 'Tex-Mex', 'Waffles', 'Donuts', 'Breakfast & Brunch', 'Do-It-Yourself Food', 'British', 'Polish', 'Honey', 'Eritrean', 'Salad', 'Game Meat', 'Desserts', 'Belgian', 'Pizza', 'Beverage Store', 'Armenian', 'Ethiopian', 'Pakistani', 'Chicken Wings', 'Seafood', 'Street Vendors', 'Cafeteria',
                       'Honduran', 'Southern', 'Smokehouse', 'Barbeque', 'Himalayan/Nepalese', 'Uzbek', 'Water Stores', 'Imported Food', 'Beer Hall', 'American (Traditional)', 'Cupcakes', 'Latin American', 'Ukrainian', 'Shaved Ice', 'Creperies', 'Chicken Shop', 'International', 'Burmese', 'Delicatessen', 'Rotisserie Chicken', 'Kosher', 'Vietnamese', 'Bulgarian', 'Diners', 'Bistros', 'Japanese', 'Caribbean', 'Convenience Stores', 'Malaysian', 'Mediterranean', 'Arabian', 'Turkish', 'Halal', 'Farmers Market', 'Mexican', 'New Mexican Cuisine', 'Chinese', 'Korean', 'Greek', 'Steakhouses', 'Kiosk', 'Slovakian', 'Grocery', 'Organic Stores', 'Moroccan', 'Island Pub', 'Churros', 'Noodles', 'Coffee Roasteries', 'Guamanian', 'Custom Cakes', 'Patisserie/Cake Shop', 'Brasseries', 'Food Trucks', 'Empanadas', 'Beer Garden', 'Cuban', 'Australian', 'Soup', 'Irish', 'Burgers', 'Tapas Bars', 'Chimney Cakes', 'Spanish', 'Bangladeshi', 'Poke', 'Cajun/Creole', 'Czech', 'Gastropubs', 'Fast Food', 'Japanese Sweets', 'Wineries', 'Hot Dogs', 'Hot Pot', 'Pita', 'Scandinavian', 'Argentine', 'Distilleries', 'Portuguese', 'Live/Raw Food', 'Mongolian', 'Pub Food', 'Asian Fusion', 'Gelato', 'French', 'Breweries', 'Wraps', 'Filipino', 'Singaporean', 'Pop-Up Restaurants', 'Food Stands', 'Ethical Grocery', 'Meaderies', 'Dinner Theater', 'Vegetarian', 'Italian', 'Afghan', 'Tea Rooms', 'Iberian']
    category_set = set(category.split(" "))
    category_binary_vector = list(
        map(lambda x: 1 if x in category_set else 0, restaurant_list))
    main(category_binary_vector, price, rating)
