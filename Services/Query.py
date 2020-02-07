# from flask import Flask, jsonify, request, abort, make_response
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests
from xml.dom.minidom import parse
import xml.dom.minidom


app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/shortString/missingShortStrings/": {"origins": "127.0.0.1:5000"}})

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

query1 = 'SELECT ?item ?itemLabel \
WHERE \
{\
  ?item wdt:P31 wd:Q146.\
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }\
}\
LIMIT 10'

query_part_one = 'SELECT ?item ?itemLabel \
WHERE \
{\
  ?item wdt:P31 wd:'

query_part_two = '. SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }\
}\
LIMIT 10'


test_url = 'http://www.reddit.com/user/spilcm/about/.json'
# test_url = 'http://dummy.restapiexample.com/api/v1/employees'


class Item:
    def __init__(self, item_label, item_url):
        self.item_label = item_label
        self.item_url = item_url

    # def getInfo(self):
    #     return jsonify(label=self.item_label,
    #                    url=self.item_url)

    def serialize(self):
        return {"itemLabel": self.item_label,
                "itemUrl": self.item_url}


@app.route('/shortString/missingShortStrings/', methods=['GET'])
def get_tasks():

    print("entering here")

    type = ''
    if 'categoryType' in request.args:
        type = request.args['categoryType']
        print(type)
    else:
        return "Error: No categoryType provided. Please select a valid categoryType."

    print("creating query--------")
    print("one", query_part_one)
    print("two", query_part_two)
    # query = 'SELECT ?item ?itemLabel \
    #         WHERE \
    #         {\
    #           ?item wdt:P31 wd:{}.\
    #           SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }\
    #         }\
    #         LIMIT 10'.format(type)

    query = query_part_one + type + query_part_two

    print(query)

    # response = requests.get("https://query.wikidata.org/#"+query)

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query="+query
    print('url', url)
    response = requests.get(url, headers)
    # requests.headers['Content-Type'] = 'application/json'

    # print(response.text)

    print(response.headers['Content-Type'])
    print(response.headers.get('content-type'))

    print('--------------- writing start')
    file = open('queryResponse.xml', 'w')
    file.write(response.text)
    file.close()
    print('--------------- writing end ------')

    # response = requests.get(test_url)

    print('=------------reading file')
    file = open('queryResponse.xml', 'r')
    saved_text = file.read()
    file.close()
    # print(saved_text)
    print('-------------- reading complete')

    # response.text
    # print(response.text)

    dom_tree = xml.dom.minidom.parse(open('queryResponse.xml', 'r'))

    allResults = dom_tree.getElementsByTagName('result')

    final_result = []

    for result in allResults:
        url = result.getElementsByTagName('uri')[0].childNodes[0].data
        label = result.getElementsByTagName('literal')[0].childNodes[0].data

        # print('Item Label ---- ', label)
        # print('Item url ---- ', url)

        item = Item(label, url)
        print('Item Label ---- ', item.item_label)
        print('Item url ---- ', item.item_url)

        final_result.append(item.serialize())


    # print(final_result)
    # print("---------------------------------", len(final_result))


    # return jsonify(label=obj.item_label, url=obj.item_url) for obj in final_result

    # r = jsonify(final_result)
    # print(r)

    print("-------------- end -------------------")

    response = jsonify(final_result)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


    # return jsonify({'finalResult': final_result})



# @app.route('/')
# def index():
#     return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)





# @app.route('/todo/api/v1.0/tasks/', methods=['GET'])
# def get_onetask():
#     if 'id' in request.args:
#         id = int(request.args["id"])
#     else:
#         return "Error: No id field provided. Please specify an id."
#
#     result = []
#
#     for task in tasks:
#         if task['id'] == id:
#             result.append(task)
#             break
#
#     return jsonify({'task': result})






# @app.route('/todo/api/v1.0/tasks/alternate', methods=['POST'])
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#
#     tasks.append(task)
#     return jsonify({'tasks': tasks}), 201


# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)


# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#
#     return jsonify({'task': task[0]})



