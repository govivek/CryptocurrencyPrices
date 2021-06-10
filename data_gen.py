import csv, requests, json
import concurrent.futures

time_unit = 0

fieldnames = ["TIME", "BTC_USD_KRAKEN", "BTC_USD_BITSTAMP"]
# Public API from exchanges that do not require API Key for authentication
URL_TO_FIELD_DIC = {
    'https://api.kraken.com/0/public/Ticker?pair=xbtusd' : 'BTC_USD_KRAKEN',
    'https://www.bitstamp.net/api/ticker/' : 'BTC_USD_BITSTAMP'
}

row_dic = {key: None for key in URL_TO_FIELD_DIC.values()}
# Create CSV file with set of headers
with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()


def get_price(url):
    try:
        r = requests.get(url)
        priceFloat = extract_price(URL_TO_FIELD_DIC[url], r)
        return priceFloat
    except requests.ConnectionError:
        # handle error status code
        print ("Error querying exchange API")


def extract_price(exchange, r):
    if exchange == 'BTC_USD_KRAKEN':
        return float(json.loads(r.text)['result']['XXBTZUSD']['a'][0])
    else:
        return float(json.loads(r.text)['last'])

# Write data to CSV file in append mode by invoking public end-point APIs.
while True:
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(get_price, url): url for url in URL_TO_FIELD_DIC.keys()}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    row_dic[URL_TO_FIELD_DIC[url]] = data
                    #print(f"url is :{url} with data : {data}")
                except Exception as exc:
                    print(f'%r generated an exception: %s' % (url, exc))


        print("BTC_USD_KRAKEN :" + str(row_dic['BTC_USD_KRAKEN']))
        print("BTC_USD_BITSTAMP :" + str(row_dic['BTC_USD_BITSTAMP']))

        info = {
            "TIME": time_unit,
            "BTC_USD_KRAKEN": row_dic['BTC_USD_KRAKEN'],
            "BTC_USD_BITSTAMP": row_dic['BTC_USD_BITSTAMP']
        }

        csv_writer.writerow(info)
        time_unit += 1

    # Server-side Rate-Limiting required if/any
    #time.sleep(1)