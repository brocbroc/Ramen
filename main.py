"""Flask application"""
from stats import *
from flask import Flask, abort, render_template, request
import sqlite3
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main_homepage() -> str:
    """Loads main landing page"""
    return render_template('main.html')


@app.route('/location', methods=['GET'])
def get_best_brand() -> list[str]:
    """Finds the best brand for a specific location"""
    location = request.args.get('location')
    result = best_brand(location)

    if result == 'error':
        abort(404)

    return result


@app.route('/ramen', methods=['GET'])
def get_all_products() -> list:
    """Returns a list of all products for a specific location and/or brand"""
    location = request.args.get('location')
    brand = request.args.get('brand')
    result = all_products(location, brand)

    if result == 'error':
        abort(404)

    return result


@app.route('/ramen', methods=['POST'])
def insert_product() -> str:
    """Adds a new product to the ramen database"""
    con = sqlite3.connect("ramen.db")
    cursor = con.cursor()

    new_product = request.json
    id = int(cursor.execute("SELECT COUNT(*) FROM ramen_ratings").fetchone()[0]) + 1
    product_info = "INSERT INTO ramen_ratings VALUES('" + str(id) + "', '" + new_product['brand'] + "', '" + new_product['variety'] + "', '" + new_product['style'] + "', '" + new_product['country'] + "', '" + new_product['stars'] + "')"
    cursor.execute(product_info)

    con.commit()
    con.close()
    return "Product added"


@app.route('/ramen', methods=['DELETE'])
def delete_product() -> str:
    """Deletes a specific product by id from the ramen database"""
    con = sqlite3.connect("ramen.db")
    cursor = con.cursor()

    product = request.json
    id = product['number']
    command = "DELETE FROM ramen_ratings where number = " + str(id)
    cursor.execute(command)
    cursor.execute("UPDATE ramen_ratings SET number = number - 1 WHERE number > " + str(id))

    con.commit()
    con.close()
    return "Product deleted"


@app.errorhandler(404)
def page_not_found(error) -> tuple:
    """Handles errors"""
    return "The page cannot be found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
