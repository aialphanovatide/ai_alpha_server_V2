import os
import json
from flask import Flask
from flask_cors import CORS
from routes.chart.chart import chart_bp
from routes.chart.chart_olhc import chart_graphs_bp
from routes.news_bot.index import scrapper_bp
from routes.telegram.index import telegram_bp
from routes.analysis.analysis import analysis_bp 
from routes.tradingview.index import tradingview_bp
from routes.slack.slack_actions import slack_events_bp
from routes.fundamentals.introduction import introduction
from routes.fundamentals.competitors import competitor_bp
from routes.dashboard_access.access import dashboard_access_bp
from routes.fundamentals.hacks import hacks_bp
from routes.fundamentals.tokenomics import tokenomics
from routes.fundamentals.upgrades import upgrades_bp
from routes.telegram.email_invitation_link.invitation_link import send_email_bp
from routes.fundamentals.revenue_model import revenue_model_bp
from routes.fundamentals.dapps import dapps_bp
from routes.news_bot.used_keywords import news_bots_features_bp
from routes.news_bot.index import scrapper_bp
from routes.narrative_trading.narrative_trading import narrative_trading_bp
from routes.user.user import user_bp
from routes.api_keys.api_keys import api_keys_bp
from routes.category.category import category_bp
from routes.external_apis.profit import profit_bp
from routes.external_apis.coindar import coindar_bp
from routes.external_apis.revenuecat import revenuecat_bp
from routes.external_apis.capitalcom import capitalcom_bp
from routes.external_apis.coinalyze import coinalyze_bp
from routes.external_apis.twelvedata import twelvedata_bp
from routes.external_apis.binance import binance_bp
from routes.coin_bot.coinbot import coin_bot_bp
from flasgger import Swagger
from decorators.api_key import check_api_key
from ws.socket import init_socketio

app = Flask(__name__)
app.name = 'AI Alpha API'
swagger_template_path = os.path.join(app.root_path, 'static', 'swagger.json')

# Check API key for all requests
@app.before_request
def before_request():
    result = check_api_key()
    if result is not None:
        return result

# Initialize SocketIO
socketio = init_socketio(app)

app.static_folder = 'static'
app.secret_key = os.urandom(24)

# Swagger configuration
with open(swagger_template_path, 'r') as f:
    swagger_template = json.load(f)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'swagger',
            "route": '/swagger.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",
    "title": "AI Alpha API",
    "description": "API for AI Alpha",
    "logo": {
        "url": "static/logo.png",
        "backgroundColor": "#FFFFFF",
        "altText": "AI Alpha Logo"
    },
    "swagger_ui_config": {
        "docExpansion": "none",
        "tagsSorter": "alpha"
    }
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)
CORS(app, origins='*', supports_credentials=True)


# Register blueprints -  routes
app.register_blueprint(scrapper_bp)
app.register_blueprint(news_bots_features_bp)
app.register_blueprint(chart_bp)
app.register_blueprint(chart_graphs_bp)
app.register_blueprint(dashboard_access_bp)
app.register_blueprint(telegram_bp)
app.register_blueprint(api_keys_bp)
app.register_blueprint(send_email_bp)
app.register_blueprint(competitor_bp)
app.register_blueprint(tradingview_bp)
app.register_blueprint(slack_events_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(hacks_bp)
app.register_blueprint(revenue_model_bp)
app.register_blueprint(introduction)
app.register_blueprint(upgrades_bp)
app.register_blueprint(category_bp)
app.register_blueprint(dapps_bp)
app.register_blueprint(tokenomics)
app.register_blueprint(narrative_trading_bp)
app.register_blueprint(user_bp)
app.register_blueprint(profit_bp)
app.register_blueprint(coindar_bp)
app.register_blueprint(revenuecat_bp)
app.register_blueprint(capitalcom_bp)
app.register_blueprint(coinalyze_bp)
app.register_blueprint(twelvedata_bp)
app.register_blueprint(binance_bp)
app.register_blueprint(coin_bot_bp)



if __name__ == '__main__':
    try:
        with app.app_context():
            print('---AI Alpha API is running---') 
            app.run(port=9000, debug=False, use_reloader=False, threaded=True, host='0.0.0.0') 
    except Exception as e:
        print(f"Failed to start the AI Alpha server: {e}")
    finally:
        # send_INFO_message_to_slack_channel( channel_id="C06FTS38JRX",
        #                                     title_message="*CRITICAL ERROR*", 
        #                                     sub_title="AI Alpha server has stopped running",
        #                                     message="@David P. - Check this error on the Mac mini immediately")
        print('---AI Alpha server was stopped---')



