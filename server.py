import os
from flask import Flask
from flask_cors import CORS
from websocket.socket import socketio
from routes.dashboard.bots import bots_route
from routes.news_bot.index import scrapper_bp
from routes.telegram.index import telegram_bp 
from routes.tradingview.index import tradingview_bp
from routes.dashboard.bot_status import bots_status
from routes.analysis.google_docs import analysis_bp
from routes.dashboard.all_coin_bots import coin_bots
from routes.dashboard.erase_keyword import delete_kw
from routes.dashboard_access.register import sign_up 
from routes.analysis.get_a import get_analysis_by_id
from routes.chart.last_chart_update import last_chart
from routes.slack.slack_actions import slack_events_bp
from routes.dashboard.all_keywords import all_keywords
from routes.dashboard.get_total_bots import total_bots
from routes.chart.get_s_r_chart import get_chart_values
from routes.dashboard.new_chart_s_r import save_new_chart
from routes.dashboard_access.sign_in_session import sign_in
from routes.dashboard.create_new_keyword import new_keyword
from routes.dashboard.activate_all_bots import bots_activator
from routes.trendspider.index import trendspider_notification_bp
from routes.dashboard.deactivate_all_bots import bots_deactivator
from routes.telegram.email_invitation_link.invitation_link import send_email_bp
from routes.slack.templates.news_message import send_INFO_message_to_slack_channel

app = Flask(__name__)
app.name = 'AI Alpha'

CORS(app, origins='*')

# Init of Socket
socketio.init_app(app)

app.static_folder = 'static'
app.secret_key = os.urandom(24)

# Register blueprints -  routes
app.register_blueprint(sign_up)
app.register_blueprint(sign_in)
app.register_blueprint(coin_bots)
app.register_blueprint(delete_kw)
app.register_blueprint(bots_route)
app.register_blueprint(last_chart)
app.register_blueprint(total_bots)
app.register_blueprint(scrapper_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(bots_status)
app.register_blueprint(telegram_bp)
app.register_blueprint(new_keyword)
app.register_blueprint(all_keywords)
app.register_blueprint(send_email_bp)
app.register_blueprint(save_new_chart)
app.register_blueprint(bots_activator)
app.register_blueprint(tradingview_bp)
app.register_blueprint(slack_events_bp)
app.register_blueprint(bots_deactivator)
app.register_blueprint(get_chart_values)
app.register_blueprint(get_analysis_by_id)
app.register_blueprint(trendspider_notification_bp)



if __name__ == '__main__':
    try:
        print('---AI Alpha server is running---') 
        socketio.run(app, port=9000, debug=False, use_reloader=False) 
    except Exception as e:
        print(f"Failed to start the AI Alpha server: {e}")
    finally:
        # send_INFO_message_to_slack_channel( channel_id="C06FTS38JRX",
        #                                     title_message="*CRITICAL ERROR*", 
        #                                     sub_title="AI Alpha server has stop running",
        #                                     message="@David P. - Check this error on the Mac mini immediately")
        print('---AI Alpha server was stopped---')




