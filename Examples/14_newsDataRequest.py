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

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):

        '''Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.'''

        
        self.logger.info(f'contractDetails: {contractDetails}')

    def openOrder(self, orderId: int, 
                        contract: Contract, 
                        order: Order,
                        orderState: OrderState):

        '''This function is called to feed in open orders.'''

        
        self.logger.info(f'orderId: {orderId} / contract: {contract} / order: {order} / orderState: {orderState}')

    def orderStatus(self, orderId: int, 
                          status: str, 
                          filled: float,
                          remaining: float, 
                          avgFillPrice: float, 
                          permId: int,
                          parentId: int, 
                          lastFillPrice: float, 
                          clientId: int,
                          whyHeld: str, 
                          mktCapPrice: float):

        '''This event is called whenever the status of an order changes. It is
        also fired after reconnecting to TWS if the client has any open orders.'''

        
        self.logger.info(f'orderId: {orderId} / status: {status} / filled: {filled} / remaining: {remaining} / avgFillPrice: {avgFillPrice} / clientId: {clientId}')

    def execDetails(self, reqId: int, 
                          contract: Contract, 
                          execution: Execution):

        '''This event is fired when the reqExecutions() functions is
        invoked, or when an order is filled.'''

        
        self.logger.info(f'contract: {contract} / execution: {execution}')

    def position(self, account: str, 
                       contract: Contract, 
                       position: float,
                       avgCost: float):

        '''This event returns real-time positions for all accounts in
        response to the reqPositions() method.'''

        
        self.logger.info(f'contract: {contract} / position: {position} / avgCost: {avgCost}')

    def accountSummary(self, reqId: int, 
                             account: str, 
                             tag: str, 
                             value: str,
                             currency: str):

        '''Returns the data from the TWS Account Window Summary tab in
        response to reqAccountSummary().'''

        
        self.logger.info(f'reqId: {reqId} / account: {account} / tag: {tag} / value: {value} / currency: {currency}')

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

    def createUSStockContract(self, symbol: str, primaryExchange: str):

        '''Create a US Stock contract placeholder.'''

        

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.primaryExchange = primaryExchange
        self.logger.info(f'Contract: {contract}')

        return contract

    def createFXPairContract(self, pair: str):

        '''Create a FX pair contract placeholder.
        Pair has to be an FX pair in the format EURUSD, GBPUSD...'''

        

        # Separate currency and symbol:
        assert len(pair) == 6
        symbol = pair[:3]
        currency = pair[3:]

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'CASH'
        contract.exchange = 'IDEALPRO'
        contract.currency = currency
        self.logger.info(f'Contract: {contract}')

        return contract

    def createMarketOrder(self, action: str, totalQuantity: int):

        '''Create a market order.'''

        

        order = Order()
        order.action = action
        order.orderType = 'MKT'
        order.totalQuantity = totalQuantity
        self.logger.info(f'Order: {order}')

        return order

    def createStopOrder(self, action: str, totalQuantity: int, stopPrice: float):

        '''Create a market order.'''

        

        order = Order()
        order.action = action
        order.orderType = 'STP'
        order.totalQuantity = totalQuantity
        order.auxPrice = stopPrice
        self.logger.info(f'Order: {order}')

        return order

if __name__ == "__main__":

    app = AlphaApp()
    app.connect('127.0.0.1', port=7497, clientId=123)
    app.run()