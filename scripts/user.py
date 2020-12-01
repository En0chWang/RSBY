import sys
import json
import mysql.connector
import requests
import keys


def get_user_by_restaurant(user_id):
    cnx = mysql.connector.connect(
        user=keys.MYSQL_USER,
        password=keys.MYSQL_PASSWORD,
        host=keys.MYSQL_HOST,
        database=keys.MYSQL_DATABASE)
    cursor = cnx.cursor()
    query = "select * from user_basic_info where user_id = '%s';" % (user_id)
    cursor.execute(query)
    res = []
    for each in cursor:
        res.append({'user_id': each[0], 'name': each[1], 'average_stars': each[2],
                    'yelping_since': each[3], 'fans': each[4], 'user_website': 'https://www.yelp.com/user_details?userid=' + each[0]})
    cursor.close()
    return res[0]


def get_review_by_restaurant(business_id):

    url = "http://3.21.133.7/api/businessId?businessId=%s" % (business_id)

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'charset': 'UTF-8'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    return response


if __name__ == "__main__":
    users = sys.argv[1].split(',')

    user_list = []
    for user_id in users:
        user_list.append(get_user_by_restaurant(user_id))
    print(json.dumps(user_list))
