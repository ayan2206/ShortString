from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests
from xml.dom.minidom import parse
import xml.dom.minidom


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/shortString/missingShortStrings/": {"origins": "127.0.0.1:5000"}})


# define query
query_part_one = 'SELECT ?item ?itemLabel \
WHERE \
{\
  ?item wdt:P31 wd:'

query_part_two = '. SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }\
}\
LIMIT 10'


# query1 = 'SELECT ?item ?itemLabel \
# WHERE \
# {\
#   ?item wdt:P31 wd:{}.\
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }\
# }\
# LIMIT 10'


# custom struct
class Item:
    def __init__(self, item_label, item_url):
        self.item_label = item_label
        self.item_url = item_url

    def serialize(self):
        return {"itemLabel": self.item_label,
                "itemUrl": self.item_url}


@app.route('/shortString/missingShortStrings/', methods=['GET'])
def get_tasks():

    # extract query param

    type = ''
    if 'categoryType' in request.args:
        type = request.args['categoryType']
        print(type)
    else:
        return "Error: No categoryType provided. Please select a valid categoryType."

    # construct query
    query = query_part_one + type + query_part_two


    # request to execute query

    # headers = {
    #     'accept': 'application/json',
    #     'Content-Type': 'application/json'
    # }
    url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query="+query
    response = requests.get(url)

    # response = requests.get(url, headers)

    file = open('queryResponse.xml', 'w')
    file.write(response.text)
    file.close()

    file = open('queryResponse.xml', 'r')

    # XML parsing
    dom_tree = xml.dom.minidom.parse(open('queryResponse.xml', 'r'))
    allResults = dom_tree.getElementsByTagName('result')

    # return this result
    final_result = []

    for result in allResults:

        url = result.getElementsByTagName('uri')[0].childNodes[0].data
        label = result.getElementsByTagName('literal')[0].childNodes[0].data

        item = Item(label, url)
        final_result.append(item.serialize())


    response = jsonify(final_result)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    app.run(debug=True)

