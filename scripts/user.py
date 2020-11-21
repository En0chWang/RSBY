import sys
import json
import mysql.connector
import requests


def get_user_by_restaurant(user_id):
    cnx = mysql.connector.connect(
        user='root',
        password='wangyinuo696683',
        host='database-1.cjy5mlvqnx2k.us-west-1.rds.amazonaws.com',
        database='restaurant')
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
