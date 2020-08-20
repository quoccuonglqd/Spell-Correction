from flask import Flask, request, jsonify, make_response

from process import *
import time

app = Flask(__name__)

@app.route("/post_processing_religion", methods=["POST"])
def religion():

    if request.is_json and request.get_json().get('name') is not None:

        req = request.get_json()
        tmp = req.get('name')
        st = time.time()
        ans = religion_correction(tmp)
        fn = time.time()
        total = fn-st
        print('Input: {}'.format(tmp))
        print('Output: {}'.format(ans))
        print("Runtime: {} s".format(total))
        response_body = {
                'religion' : ans
        }

        res = make_response(jsonify(response_body), 200)

        return res

    else:

        return make_response(jsonify({"message": "Request body must be JSON. Example: {'name': 'Nao Vei'} "}), 400)

@app.route("/post_processing_province", methods=["POST"])
def province():

    if request.is_json and request.get_json().get('name') is not None:

        req = request.get_json()
        tmp = req.get('name')
        st = time.time()
        ans = province_correction(tmp)
        fn = time.time()
        total = fn-st
        print('Input: {}'.format(tmp))
        print('Output: {}'.format(ans))
        print("Runtime: {} s".format(total))
        response_body = {
                'province' : ans
        }

        res = make_response(jsonify(response_body), 200)

        return res

    else:

        return make_response(jsonify({"message": "Request body must be JSON. Example: {'name': 'Thài Bính'} "}), 400)


@app.route("/post_processing_folk", methods=["POST"])
def folk():

    if request.is_json and request.get_json().get('name') is not None:

        req = request.get_json()
        tmp = req.get('name')
        st = time.time()
        ans = folk_correction(tmp)
        fn = time.time()
        total = fn-st
        print('Input: {}'.format(tmp))
        print('Output: {}'.format(ans))
        print("Runtime: {} s".format(total))
        response_body = {
                'religion' : ans
        }

        res = make_response(jsonify(response_body), 200)

        return res

    else:

        return make_response(jsonify({"message": "Request body must be JSON. Example: {'name': 'cu to'} "}), 400)

@app.route("/post_processing_address", methods=["POST"])
def address():

    if request.is_json and request.get_json().get('name') is not None:

        req = request.get_json()
        tmp = req.get('name')
        st = time.time()
        ans = address_correction(tmp)
        fn = time.time()
        total = fn-st
        print('Input: {}'.format(tmp))
        print('Output: {}'.format(ans))
        print("Runtime: {} s".format(total))
        response_body = {
                'address' : ans
        }

        res = make_response(jsonify(response_body), 200)

        return res

    else:

        return make_response(jsonify({"message": "Request body must be JSON. Example: {'name': 'Ltr Td HCMA'} "}), 400)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8062, debug=True)
