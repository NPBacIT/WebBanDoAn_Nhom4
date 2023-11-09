from fdmgmt.utils import utils
from fdmgmt.common import conf as cfg 
import json
from flask import Flask, request, jsonify

CONF = cfg.CONF

app = Flask(__name__)
db_utils = utils.DatabaseUtils()

@app.route('/v1/items', methods=['GET'])
def get_all_items():
    table_name = request.args.get('table_name')
    try:
        items = db_utils.get_all_items(table_name)
        return jsonify(items)
    except Exception as e:
        warning = {
            'error': str(e),
            'example': {
                'table_name': 'MonAn'
            }
        }
        return jsonify(warning), 400

@app.route('/v1/filter', methods=['GET'])
def filter():
    table_name = request.args.get('table_name')
    table_key = request.args.get('table_key')
    value = request.args.get('value')
    try:
        items = db_utils.filter_items(table_name, table_key, value) 
        return jsonify(items)
    except Exception as e:
        warning = {
            'error': str(e),
            'example': {
                'table_name': 'MonAn',
                'table_key': 'MaMA',
                'value': '1'
            }
        }
        return jsonify(warning), 400

@app.route('/v1/item', methods=['GET'])
def get_item():
    table_name = request.args.get('table_name')
    table_key = request.args.get('table_key')
    value = request.args.get('value')
    try:
        item = db_utils.get_item(table_name, table_key, value)
        print(item)
        if not item:
            return jsonify({'error': 'key has to be the uniq object such as ID'}), 400
        return jsonify(item)
    except Exception as e:
        warning = {
            'error': str(e),
            'example': {
                'table_name': 'MonAn',
                'table_key': 'MaMA',
                'value': '1'
            }
        }
        return jsonify(warning), 400

@app.route('/v1/add_mon_an', methods=['POST'])
def add_mon_an():
    try:
        TenMA = request.args.get('TenMA')
        ChiTietMA = request.args.get('ChiTietMA')
        Gia = request.args.get('Gia')
        AnhMA = request.args.get('AnhMA')
        SoLuongMA = request.args.get('SoLuongMA')
        MaLoaiMA = request.args.get('MaLoaiMA')

        success = db_utils._mon_an_model_add(TenMA, ChiTietMA, Gia, 
                                            AnhMA, SoLuongMA, MaLoaiMA)
        if success:
            return jsonify({'message': 'Item added successfully'})
        else:
            return jsonify({'message': 'Item already exists'})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/v1/update_mon_an', methods=['PATCH'])
def update_mon_an():
    try:
        MaMA = request.args.get('MaMA')
        Gia = request.args.get('Gia')
        SoLuongMA = request.args.get('SoLuongMA')

        success = db_utils._mon_an_model_udapte(MaMA, Gia, SoLuongMA)
        if success:
            return jsonify(success)
        else:
            return None
    except Exception as e:
        warning = {
            'error': str(e),
            'example': {
                'MaMA': '1',
                'Gia': '12',
                'SoLuong': '20'
            }
        }
        return jsonify(warning), 400

@app.route('/v1/delete_mon_an', methods=['DELETE'])
def delete_item():
    try:
        MaMA = request.args.get('MaMA')
        ok = db_utils._mon_an_model_delete(MaMA) 
        if ok:
            return jsonify({'OK': 'Delete item success'}), 200
        else:
            return jsonify({'error': 'Delete item Failed'}), 400
    except Exception as e:
        warning = {
            'error': str(e),
            'example': {
                'MaMA': '1',
            }
        }
        return jsonify(warning), 400

if __name__ == '__main__':
    app.run(debug=True, host=CONF['DEFAULT']['hostname'], port=CONF['DEFAULT']['hostport'])