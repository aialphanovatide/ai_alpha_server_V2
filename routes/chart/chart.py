import os
import requests
from http import HTTPStatus
from sqlalchemy import desc
from dotenv import load_dotenv
from functools import lru_cache
from sqlalchemy.exc import SQLAlchemyError
from cachetools import TTLCache
from cachetools.func import ttl_cache
from config import Chart, session, CoinBot, Session
from flask import jsonify, request, Blueprint, jsonify  

chart_bp = Blueprint('chart', __name__)


# Load environment variables
load_dotenv()

# Get WordPress API key from environment variables
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')


# # ----- ROUTE FOR THE DASHBOARD -------------------------------------------
# # Deletes the last support and resistance lines of a coin and adds new ones.
# @chart_bp.route('/save_chart', methods=['POST'])
# def save_chart():
#     try:
#         data = request.json
#         coin_bot_id = data.get('coin_bot_id')
#         pair = data.get('pair')
#         temporality = data.get('temporality')
#         token = data.get('token')


#         if not coin_bot_id or not pair or not temporality or not token:
#             return jsonify({'success': False, 'message': 'One or more fields are missing'}), 400

#         if token.casefold() == 'btc' and pair.casefold() == 'btc':
#             return jsonify({'success': False, 'message': 'Coin/pair not valid'}), 400
        
#         existing_chart = session.query(Chart).filter(Chart.coin_bot_id==coin_bot_id, 
#                                                      Chart.pair==pair.casefold(), 
#                                                      Chart.temporality==temporality.casefold(),
#                                                      Chart.token==token.casefold()).first()


#         if existing_chart:
#             # Update existing chart values
#             existing_chart.support_1 = data.get('support_1')
#             existing_chart.support_2 = data.get('support_2')
#             existing_chart.support_3 = data.get('support_3')
#             existing_chart.support_4 = data.get('support_4')
#             existing_chart.resistance_1 = data.get('resistance_1')
#             existing_chart.resistance_2 = data.get('resistance_2')
#             existing_chart.resistance_3 = data.get('resistance_3')
#             existing_chart.resistance_4 = data.get('resistance_4')

#             session.commit()

#             return jsonify({'success': True, 'message': 'Chart updated successfully'}), 200
#         else:
#             # Create a new chart
#             new_chart = Chart(
#                 support_1=data.get('support_1'),
#                 support_2=data.get('support_2'),
#                 support_3=data.get('support_3'),
#                 support_4=data.get('support_4'),
#                 resistance_1=data.get('resistance_1'),
#                 resistance_2=data.get('resistance_2'),
#                 resistance_3=data.get('resistance_3'),
#                 resistance_4=data.get('resistance_4'),
#                 token=token,
#                 pair=pair,
#                 temporality=data.get('temporality'),
#                 coin_bot_id=coin_bot_id
#             )

#             session.add(new_chart)
#             session.commit()

#             return jsonify({'success': True, 'message': 'Chart created successfully'}), 200

#     except Exception as e:
#         session.rollback()
#         return jsonify({'success': False, 'message': str(e)}), 500

    


# # ----- ROUTE FOR THE APP ---------------------------
# # Gets the support and resistance lines of a requested coin
# @chart_bp.route('/api/coin-support-resistance', methods=['GET'])
# def get_chart_values_by_coin_bot_id():

#     try:
#         coin_name = request.args.get('coin_name')
#         temporality = request.args.get('temporality')
#         pair = request.args.get('pair')
        
#         if not all([coin_name, temporality, pair]):
#             return jsonify({'success': False, 'message': 'Missing required parameters'})

#         coinbot = session.query(CoinBot).filter(CoinBot.bot_name == coin_name).first()
#         if not coinbot:
#             return jsonify({'success': False, 'message': 'CoinBot not found for the given coin name'})
        
#         chart = session.query(Chart).filter_by(coin_bot_id=coinbot.bot_id, temporality=temporality, pair=pair).first()
#         if chart:
#             chart_values = {
#                 'support_1': chart.support_1,
#                 'support_2': chart.support_2,
#                 'support_3': chart.support_3,
#                 'support_4': chart.support_4,
#                 'resistance_1': chart.resistance_1,
#                 'resistance_2': chart.resistance_2,
#                 'resistance_3': chart.resistance_3,
#                 'resistance_4': chart.resistance_4,
#                 'token': chart.token,
#                 'pair': chart.pair,
#                 'temporality': chart.temporality
#             }
#             return jsonify({'success': True, 'chart_values': chart_values})
#         else:
#             return jsonify({'success': False, 'message': 'Chart not found for the given parameters'})

#     except Exception as e:
#         session.rollback()
#         return jsonify({'success': False, 'message': str(e)})



# # ----- ROUTE FOR THE DASHBOARD ---------------------------
# # Gets the support and resistance lines of a requested coin
# # this route is duplicated with the previous one, just for convenience, as the dashboard is passing the ID of the coin.
# @chart_bp.route('/api/coin-support-resistance/dashboard', methods=['GET'])
# def get_s_and_r():

#     try:
#         coin_id=request.args.get('coin_id')
#         temporality=request.args.get('temporality')
#         pair=request.args.get('pair')

#         if coin_id is None or temporality is None or pair is None:
#             return jsonify({'success': False, 'message': 'One or more values are missing'}), 400

#         chart = session.query(Chart).filter(Chart.coin_bot_id==coin_id,Chart.pair==pair.casefold(),Chart.temporality==temporality.casefold()).first()

#         if chart:
#             chart_values = {
#                 'support_1': chart.support_1,
#                 'support_2': chart.support_2,
#                 'support_3': chart.support_3,
#                 'support_4': chart.support_4,
#                 'resistance_1': chart.resistance_1,
#                 'resistance_2': chart.resistance_2,
#                 'resistance_3': chart.resistance_3,
#                 'resistance_4': chart.resistance_4,
#                 'token': chart.token,
#                 'pair': chart.pair,
#                 'temporality': chart.temporality
#             }

#             return jsonify({'success': True, 'chart_values': chart_values}), 200
#         else:
#             return jsonify({'success': False, 'message': 'Chart not found for the given coin ID'}), 204

#     except Exception as e:
#         session.rollback()
#         return jsonify({'success': False, 'message': str(e)}), 500
    

# @chart_bp.route('/api/total_3_data', methods=['GET'])
# def get_total_3_data():
#     try:
#         url_btc = "https://pro-api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7&interval=daily"
#         url_eth = "https://pro-api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=7&interval=daily"
#         url_total = "https://pro-api.coingecko.com/api/v3/global/market_cap_chart?days=7"

#         headers = {"x-cg-pro-api-key": "CG-xXCJJaHa7QmvQNWyNheKmSfG"}

#         btc_response = requests.get(url_btc, headers=headers)
#         eth_response = requests.get(url_eth, headers=headers)
#         total_response = requests.get(url_total, headers=headers)

#         btc_response.raise_for_status()
#         eth_response.raise_for_status()
#         total_response.raise_for_status()

#         data_eth = eth_response.json()
#         data_total = total_response.json()
#         data_btc = btc_response.json()

#         btc_market_caps = [entry[1] for entry in data_btc["market_caps"]]
#         eth_market_caps = [entry[1] for entry in data_eth["market_caps"]]
#         total_market_caps = [entry[1] for entry in data_total["market_cap_chart"]["market_cap"]]

#         eth_btc_market_caps = [btc_market_caps[i] + eth_market_caps[i] for i in range(len(btc_market_caps))]
#         total_market_cap = total_market_caps

#         total3 = [total_market_cap[i] - eth_btc_market_caps[i] for i in range(len(total_market_cap))]

#         return jsonify({"data": total3})

#     except requests.exceptions.RequestException as e:
#         print("Error", str(e))
#         return jsonify({"error": "Error " + str(e)})
    

# ________________________ IMPROVED ENDPOINTS ________________________________________

@chart_bp.route('/save_chart', methods=['POST'])
def save_chart():
    """
    Adds a new support and resistance lines record for a coin.

    This endpoint creates a new chart entry for a specified coin, pair, and temporality,
    regardless of whether a previous entry exists.

    Args (JSON):
        coin_bot_id (int): The ID of the coin bot.
        pair (str): The trading pair.
        temporality (str): The time frame of the chart.
        token (str): The token symbol.
        support_1, support_2, support_3, support_4 (float): Support levels.
        resistance_1, resistance_2, resistance_3, resistance_4 (float): Resistance levels.

    Returns:
        dict: A JSON response indicating success or failure.
            Format: {"message": str or None, "error": str or None, "status": int}

    Raises:
        SQLAlchemyError: If there's a database-related error.
    """
    response = {
        "message": None,
        "error": None,
        "status": HTTPStatus.OK
    }

    session = Session()

    try:
        data = request.json
        required_fields = ['coin_bot_id', 'pair', 'temporality', 'token']
        
        if not all(field in data for field in required_fields):
            response["error"] = "One or more required fields are missing"
            response["status"] = HTTPStatus.BAD_REQUEST
            return jsonify(response), response["status"]

        coin_bot_id = data['coin_bot_id']
        pair = data['pair'].casefold()
        temporality = data['temporality'].casefold()
        token = data['token'].casefold()

        if token == 'btc' and pair == 'btc':
            response["error"] = "Invalid coin/pair combination"
            response["status"] = HTTPStatus.BAD_REQUEST
            return jsonify(response), response["status"]
        
        chart_data = {
            'support_1': data.get('support_1'),
            'support_2': data.get('support_2'),
            'support_3': data.get('support_3'),
            'support_4': data.get('support_4'),
            'resistance_1': data.get('resistance_1'),
            'resistance_2': data.get('resistance_2'),
            'resistance_3': data.get('resistance_3'),
            'resistance_4': data.get('resistance_4'),
            'token': token,
            'pair': pair,
            'temporality': temporality,
            'coin_bot_id': coin_bot_id
        }

        new_chart = Chart(**chart_data)
        session.add(new_chart)
        session.commit()

        response["message"] = "New chart record created successfully"
        response["status"] = HTTPStatus.CREATED

    except SQLAlchemyError as e:
        session.rollback()
        response["error"] = f"Database error: {str(e)}"
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        response["error"] = f"An unexpected error occurred: {str(e)}"
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        session.close()

    return jsonify(response), response["status"]


@chart_bp.route('/api/coin-support-resistance', methods=['GET'])
def get_chart_values():
    """
    Get the most recent support and resistance lines of a requested coin.

    This endpoint retrieves the most recent chart values including support and resistance levels
    for a specified coin (by name or ID), temporality, and trading pair.

    Args:
        coin_name (str, optional): The name of the coin.
        coin_id (int, optional): The ID of the coin.
        temporality (str): The time frame of the chart.
        pair (str): The trading pair.

    Returns:
        dict: A JSON response containing either the chart values or an error message.
            Format: {"message": dict or None, "error": str or None, "status": int}

    Raises:
        SQLAlchemyError: If there's a database-related error.
    """
    response = {
        "message": None,
        "error": None,
        "status": HTTPStatus.OK
    }

    session = Session()

    try:
        coin_name = request.args.get('coin_name')
        coin_id = request.args.get('coin_id')
        temporality = request.args.get('temporality')
        pair = request.args.get('pair')
        
        if not (coin_name or coin_id) or not temporality or not pair:
            response["error"] = "Missing required parameters"
            response["status"] = HTTPStatus.BAD_REQUEST
            return jsonify(response), response["status"]

        if coin_name:
            coinbot = session.query(CoinBot).filter(CoinBot.bot_name == coin_name).first()
            if not coinbot:
                response["error"] = f"CoinBot not found for the coin name: {coin_name}"
                response["status"] = HTTPStatus.NOT_FOUND
                return jsonify(response), response["status"]
            coin_id = coinbot.bot_id

        # Query for the most recent chart entry based on updated_at
        chart = session.query(Chart).filter_by(
            coin_bot_id=coin_id, 
            temporality=temporality.casefold(), 
            pair=pair.casefold()
        ).order_by(desc(Chart.updated_at)).first()

        if chart:
            chart_values = chart.as_dict()
            # Convert datetime objects to ISO format strings
            chart_values['created_at'] = chart_values['created_at'].isoformat() if chart_values['created_at'] else None
            chart_values['updated_at'] = chart_values['updated_at'].isoformat() if chart_values['updated_at'] else None
            response["message"] = chart_values
        else:
            response["error"] = "No chart found for the given parameters"
            response["status"] = HTTPStatus.NOT_FOUND

    except SQLAlchemyError as e:
        session.rollback()
        response["error"] = f"Database error: {str(e)}"
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        session.rollback()
        response["error"] = f"An unexpected error occurred: {str(e)}"
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        session.close()

    return jsonify(response), response["status"]


@chart_bp.route('/api/total_3_data', methods=['GET'])
def get_total_3_data():
    """
    Retrieve and calculate total market cap data for the top 3 cryptocurrencies.

    This endpoint fetches market cap data for Bitcoin, Ethereum, and the total market,
    then calculates the market cap for the third largest cryptocurrency by subtracting
    Bitcoin and Ethereum from the total.

    Returns:
        dict: A JSON response containing either the calculated data or an error message.
            Format: {"message": list or None, "error": str or None, "status": int}

    Raises:
        requests.exceptions.RequestException: If there's an error in the API requests.
        SQLAlchemyError: If there's a database-related error.
    """
    response = {
        "message": None,
        "error": None,
        "status": 200
    }

    try:
        total3 = calculate_total_3_data()
        response["message"] = total3
    except requests.exceptions.RequestException as e:
        response["error"] = f"API request failed: {str(e)}"
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
    except SQLAlchemyError as e:
        response["error"] = "Database error occurred"
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        response["error"] = f"An unexpected error occurred: {str(e)}"
        response["status"] = HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify(response), response["status"]

@ttl_cache(maxsize=1, ttl=3600)  # Cache for 1 hour
def calculate_total_3_data():
    """
    Calculate the market cap data for the third largest cryptocurrency.

    This function fetches data from the CoinGecko API for Bitcoin, Ethereum, and the total market,
    then calculates the difference to determine the market cap of the third largest cryptocurrency.

    Returns:
        list: A list of market cap values for the third largest cryptocurrency over 7 days.

    Raises:
        requests.exceptions.RequestException: If there's an error in the API requests.
    """
    base_url = "https://pro-api.coingecko.com/api/v3"
    endpoints = {
        "btc": f"{base_url}/coins/bitcoin/market_chart?vs_currency=usd&days=7&interval=daily",
        "eth": f"{base_url}/coins/ethereum/market_chart?vs_currency=usd&days=7&interval=daily",
        "total": f"{base_url}/global/market_cap_chart?days=7"
    }
    headers = {"x-cg-pro-api-key": COINGECKO_API_KEY}

    responses = {}
    for coin, url in endpoints.items():
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            responses[coin] = response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Error fetching {coin} data: {str(e)}")

    btc_market_caps = [entry[1] for entry in responses["btc"]["market_caps"]]
    eth_market_caps = [entry[1] for entry in responses["eth"]["market_caps"]]
    total_market_caps = [entry[1] for entry in responses["total"]["market_cap_chart"]["market_cap"]]

    eth_btc_market_caps = [btc + eth for btc, eth in zip(btc_market_caps, eth_market_caps)]
    total3 = [total - eth_btc for total, eth_btc in zip(total_market_caps, eth_btc_market_caps)]

    return total3
