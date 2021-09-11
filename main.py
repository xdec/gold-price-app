import requests
from flask import Flask
from flask_restful import Resource, Api, reqparse

# Start Flask API
app = Flask(__name__)
api = Api(app)

# Create endpoints
class Prices(Resource):
    def get(self):
        # Parser
        parser = reqparse.RequestParser()
        parser.add_argument('currency', required=True)
        args = parser.parse_args()

        currency = {'currency': args['currency']}
        print(currency)
        currency = currency['currency']

        # FETCH Data
        try:
            r = requests.get("https://fsapi.gold.org/api/v11/charts/spotprice")
        except Exception as e:
            print(e)
            return "CRITICAL ERROR - DATA CAN'T BE FETCHED!"

        # Create JSON
        data = r.json()
        print("JSON CREATED!")

        try:
            # Get Data
            price = data['chartData'][f'{currency.lower()}']['ask']['price'].replace(",","")
            print("PRICE FETCHED!")
        except KeyError as e:
            print(f'''
                {"CRITICAL ERROR".center(50,"-")}
                ERROR:      {Exception}
                TYPE:       KeyError
                MESSAGE:    {e} DOES NOT EXIST
            ''')
            return "PLEASE SELECT A VALID CURRENCY!", 500

        # Result
        print(f'''
            {"GOLD PRICE".center(50, "-")}
            Status:       {r.status_code}
            Currency:     {currency}
            Price:        {price}
        ''')

        return {
            'currency': currency,
            'price': price
            }, 200

api.add_resource(Prices, '/prices')

if __name__ == '__main__':
    app.run()