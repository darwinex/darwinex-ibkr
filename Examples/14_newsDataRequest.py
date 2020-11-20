# Installing (source activate ENVIRONMENT):
# Cd to: cd ~/Desktop/Darwinex/darwinex-ibkr/TWS_API/twsapi_macunix.976.01/IBJts/source/pythonclient/
# Do: python3 setup.py bdist_wheel
# Do: python3 -m pip install --user --upgrade dist/ibapi-9.76.1-py3-none-any.whl

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, ContractDetails
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.execution import Execution, ExecutionFilter
from ibapi.common import BarData, ListOfNewsProviders

import threading, logging, time
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s <> %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

#######################################

class AlphaApp(EWrapper, EClient):

    def __init__(self):

        self.logger = logging.getLogger(__name__)
        EClient.__init__(self, wrapper=self)

    ###########################################################

    def error(self, reqId: int, errorCode: int, errorString: str):

        '''This event is called when there is an error with the
        communication or when TWS wants to send a message to the client.'''

        self.logger.error(f'reqId: {reqId} / Code: {errorCode} / Error String: {errorString}')

    def newsProviders(self, newsProviders: ListOfNewsProviders):

        '''Returns available, subscribed API news providers'''

        self.logger.info(f'newsProviders: {newsProviders}')

    def newsArticle(self, requestId: int, 
                          articleType: int, 
                          articleText: str):

        '''Returns body of news article'''

        self.logger.info(f'reqId: {requestId} / articleType: {articleType} / articleText: {articleText}')

    def historicalNews(self, requestId: int, 
                             time: str, 
                             providerCode: str, 
                             articleId: str, 
                             headline: str):

        '''Returns historical news headlines'''

        self.logger.info(f'reqId: {requestId} / time: {time} / providerCode: {providerCode} / articleId: {articleId} / headline: {headline}')

    def updateNewsBulletin(self, msgId: int, 
                                 msgType:int, 
                                 newsMessage: str,
                                 originExch: str):

        '''Provides IB's bulletins
            msgId - the bulletin's identifier
            msgType - one of: 1 - Regular news bulletin 2 - Exchange no longer
                available for trading 3 - Exchange is available for trading
            message - the message
            origExchange -    the exchange where the message comes from.'''

        self.logger.info(f'msgId: {msgId} / msgType: {msgType} / newsMessage: {newsMessage} / originExch: {originExch}')

    ###########################################################

    def nextValidId(self, orderId: int):

        '''Receives next valid order id from TWS.'''

        self._nextValidOrderId = orderId

        self.logger.info(f'¡Connected!')
        self.logger.info(f'NextValidOrderId: {orderId}')
        
        a = threading.active_count()
        self.logger.info(f'Thread count for reference: {a}')

        # Call client method:
        self.reqCurrentTime()

        # Make news data requests:
        self.reqNewsProviders()

        self.reqNewsArticle(reqId=self.getNextValidId(), 
                            providerCode='BRFG', 
                            articleId='BRFG$09cb908d', 
                            newsArticleOptions=[])

        self.reqHistoricalNews(reqId=self.getNextValidId(), 
                               conId=8314, 
                               providerCodes='BRFG',
                               startDateTime='', 
                               endDateTime='', 
                               totalResults=10, 
                               historicalNewsOptions=[])

        self.reqNewsBulletins(allMsgs=True)

    def getNextValidId(self) -> int:

        '''Get new request ID by incrementing previous one.'''

        
        newId = self._nextValidOrderId
        self._nextValidOrderId += 1
        self.logger.info(f'NextValidOrderId: {newId}')
        return newId

    ###########################################################

if __name__ == "__main__":

    app = AlphaApp()
    app.connect('127.0.0.1', port=7497, clientId=123)
    app.run()