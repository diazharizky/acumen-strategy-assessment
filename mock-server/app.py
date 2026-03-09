import json
import logging

from flask import Blueprint, Flask, jsonify, request

MOCK_DATA_PATH = 'data/customers.json'

logger = logging.getLogger('mock_server')


def prepare_in_mem_data():
    logger.info('Loading data into memory...')
    data = []
    indexed_data = {}
    try:
        with open(MOCK_DATA_PATH, 'r') as f:
            data = json.load(f)
            for customer in data:
                indexed_data[customer['customer_id']] = customer
        logger.info('Data loaded successfully')
    except Exception as e:
        logger.error(f'Error loading data: {e}')
    finally:
        return data, indexed_data


api_group = Blueprint('api', __name__)


@api_group.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})


in_mem_data, in_mem_data_indexed = prepare_in_mem_data()
customers_group = Blueprint('customers', __name__)


@customers_group.route('/', methods=['GET'])
def get_customers():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    start = (page - 1) * limit
    end = start + limit

    return jsonify({
        "data": in_mem_data[start:end],
        "total": len(in_mem_data),
        "page": page,
        "limit": limit,
    })


@customers_group.route('/<string:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    if customer_id in in_mem_data_indexed:
        return jsonify({"data": in_mem_data_indexed[customer_id]})
    else:
        return jsonify({"message": "Customer not found"}), 404


api_group.register_blueprint(customers_group, url_prefix='/customers')

app = Flask(__name__)
app.register_blueprint(api_group, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
