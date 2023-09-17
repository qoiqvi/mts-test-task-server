from time import sleep

from bs4 import BeautifulSoup
import json
import requests
import re

headers = {
    'Accept': '*/*',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

req = requests.get(url='https://moskva.mts.ru/personal/mobilnaya-svyaz/tarifi/vse-tarifi/mobile', headers=headers)



soup = BeautifulSoup(req.text, 'lxml')


def get_all_tariffs_json():
    scripts = soup.find_all('script')

    target_script = None
    for script in scripts:
        if 'window.globalSettings.tariffs' in script.text:
            target_script = script.text
            break

    if target_script:
        pattern = r'window\.globalSettings\.tariffs\s*=\s*({.*?});'
        match = re.search(pattern, target_script)
        json_data = match.group(1)
        data = json.loads(json_data)

        tariffs_list = []

        for tariff_data in data['actualTariffs']:
            new_tariff = {
                'id': tariff_data.get('marketingId', None),
                'type': tariff_data.get('tariffType', None),
                'label': tariff_data.get('productLabels', None),
                'productCharacteristics': tariff_data.get('productCharacteristics', None),
                'parametrizedTariffSettings': tariff_data.get('parametrizedTariffSettings', None),
                'productFeatures': tariff_data.get('productFeatures', None),
                'benefitsDescription': tariff_data.get('benefitsDescription', None),
                'title': tariff_data.get('title', None),
                'description': tariff_data.get('description', None),
                'cardImageUrl': tariff_data.get('cardImageUrl', None),
                'subscriptionFee': tariff_data.get('subscriptionFee', None),
                # "isActionButtonHidden": tariff_data.get('isActionButtonHidden'),
                # "isDetailsButtonHidden": tariff_data.get('isActionButtonHidden'),
            }
            tariffs_list.append(new_tariff)
        with open("tariffs.json", 'w', encoding="utf-8") as file:
            json.dump(tariffs_list, file, indent=4, ensure_ascii=False)

        print('DATA REFETCH COMPLETED')
    else:
        print("Значение переменной не найдено.")


get_all_tariffs_json()
