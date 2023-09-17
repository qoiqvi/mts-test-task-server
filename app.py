from time import sleep
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from main import get_all_tariffs_json

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('tariffs.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tariffs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marketingId INTEGER NOT NULL,
        type TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        label TEXT,
        productCharacteristics TEXT,
        parametrizedTariffSettings TEXT,
        productFeatures TEXT,
        benefitsDescription TEXT,
        cardImageUrl TEXT,
        subscriptionFee TEXT
    )''')
conn.close()

# Функцию отвечает за добавление данных в таблицу
def get_tariffs_data():
    with open('tariffs.json', 'r', encoding='utf-8') as file:
        tariffs = json.load(file)
    conn = sqlite3.connect('tariffs.db')
    cursor = conn.cursor()

    for tariff in tariffs:
        cursor.execute('''
        INSERT INTO tariffs (
            marketingId,
            type,
            title,
            description,
            label, 
            productCharacteristics, 
            parametrizedTariffSettings, 
            productFeatures, 
            benefitsDescription, 
            cardImageUrl, 
            subscriptionFee
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
            tariff['id'],
            tariff['type'],
            tariff['title'],
            tariff['description'],
            json.dumps(tariff['label']),
            json.dumps(tariff["productCharacteristics"]),
            json.dumps(tariff['parametrizedTariffSettings']),
            json.dumps(tariff['productFeatures']),
            json.dumps(tariff['benefitsDescription']),
            tariff['cardImageUrl'],
            json.dumps(tariff['subscriptionFee'])
    ))
    conn.commit()
    conn.close()


@app.route('/refetch', methods=['GET'])
def refetch_tarrifs_data():
    try:
        conn = sqlite3.connect('tariffs.db')
        conn.execute('DELETE FROM tariffs;')
        conn.commit()
        get_all_tariffs_json()
        sleep(5)
        get_tariffs_data()
        conn.commit()
        return 'Data refetched', 200
    except Exception as e:
        return f"Произошла ошибка: {e}"
    finally:
        conn.close()


@app.route('/tariffs', methods=['GET'])
def get_tariffs():
    conn = sqlite3.connect('tariffs.db')
    cursor = conn.cursor()
    query_type = request.args.get('type')
    if query_type:
        try:
            cursor.execute("SELECT * FROM tariffs WHERE type=?", (query_type,))
            tariffs_data = cursor.fetchall()
            data = []
            for tariff in tariffs_data:
                data.append({
                    'id': tariff[0],
                    'marketingId': tariff[1],
                    'title': tariff[2],
                    'description': tariff[3],
                    'type': tariff[4],
                    'label': json.loads(tariff[5]) if tariff[5] else None,
                    'productCharacteristics': json.loads(tariff[6]) if tariff[6] else None,
                    'parametrizedTariffSettings': json.loads(tariff[7]) if tariff[7] else None,
                    'productFeatures': json.loads(tariff[8]) if tariff[8] else None,
                    'benefitsDescription': json.loads(tariff[9]) if tariff[9] else None,
                    'cardImageUrl': tariff[10],
                    'subscriptionFee': json.loads(tariff[11]) if tariff[11] else None,
                })
            return data, 200
        except Exception as e:
            return f"Произошла ошибка: {e}"
        finally:
            conn.close()
    else:
        try:
            cursor.execute('SELECT * FROM tariffs')
            tariffs_data = cursor.fetchall()
            data = []
            for tariff in tariffs_data:
                data.append({
                    'id': tariff[0],
                    'marketingId': tariff[1],
                    'title': tariff[2],
                    'description': tariff[3],
                    'type': tariff[4],
                    'label': json.loads(tariff[5]) if tariff[5] else None,
                    'productCharacteristics': json.loads(tariff[6]) if tariff[6] else None,
                    'parametrizedTariffSettings': json.loads(tariff[7]) if tariff[7] else None,
                    'productFeatures': json.loads(tariff[8]) if tariff[8] else None,
                    'benefitsDescription': json.loads(tariff[9]) if tariff[9] else None,
                    'cardImageUrl': tariff[10],
                    'subscriptionFee': json.loads(tariff[11]) if tariff[11] else None,
                })
            return jsonify(data), 200
        except Exception as e:
            return f"Произошла ошибка: {e}"
        finally:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)