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
from ibapi.common import BarData, TickAttribLast, TickAttrib
from ibapi.ticktype import TickType

import threading, logging, inspect, time
logging.basicConfig(level=logging.INFO)

#######################################

class AlphaApp(EWrapper, EClient):

    def __init__(self):

        self.logger = logging.getLogger(__name__)
        EClient.__init__(self, wrapper=self)

    ###########################################################

    def error(self, reqId: int, errorCode: int, errorString: str):

        '''This event is called when there is an error with the
        communication or when TWS wants to send a message to the client.'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.error(f'{funcName} <> reqId: {reqId} / Code: {errorCode} / Error String: {errorString}')

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):

        '''Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> contractDetails: {contractDetails}')

    def openOrder(self, orderId: int, 
                        contract: Contract, 
                        order: Order,
                        orderState: OrderState):

        '''This function is called to feed in open orders.'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> orderId: {orderId} / contract: {contract} / order: {order} / orderState: {orderState}')

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

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> orderId: {orderId} / status: {status} / filled: {filled} / remaining: {remaining} / avgFillPrice: {avgFillPrice} / clientId: {clientId}')

    def execDetails(self, reqId: int, 
                          contract: Contract, 
                          execution: Execution):

        '''This event is fired when the reqExecutions() functions is
        invoked, or when an order is filled.'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> contract: {contract} / execution: {execution}')

    def position(self, account: str, 
                       contract: Contract, 
                       position: float,
                       avgCost: float):

        '''This event returns real-time positions for all accounts in
        response to the reqPositions() method.'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> contract: {contract} / position: {position} / avgCost: {avgCost}')

    def accountSummary(self, reqId: int, 
                             account: str, 
                             tag: str, 
                             value: str,
                             currency: str):

        '''Returns the data from the TWS Account Window Summary tab in
        response to reqAccountSummary().'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> reqId: {reqId} / account: {account} / tag: {tag} / value: {value} / currency: {currency}')

    ###########################################################

    def tickPrice(self, reqId: int, 
                        tickType: TickType, 
                        price: float,
                        attrib: TickAttrib):

        '''Market data tick price callback. Handles all price related ticks.'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> reqId: {reqId} / tickType: {tickType} / price: {price} / attrib: {attrib}')

    def tickSize(self, reqId: int, 
                       tickType: TickType, 
                       size: int):

        '''Market data tick size callback. Handles all size-related ticks.'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> reqId: {reqId} / tickType: {tickType} / size: {size}')

    def tickByTickAllLast(self, reqId: int, 
                                tickType: int, 
                                time: int, 
                                price: float,
                                size: int, 
                                tickAtrribLast: TickAttribLast, 
                                exchange: str,
                                specialConditions: str):

        '''Here you will received data from reqTickByTickData request.'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> reqId: {reqId} / tickType: {tickType} / time: {time} / price: {price} / size: {size} / tickAtrribLast: {tickAtrribLast} / exchange: {exchange} / specialConditions: {specialConditions}')

    def updateMktDepth(self, reqId: int, 
                             position: int, 
                             operation: int,
                             side: int, 
                             price: float, 
                             size: int):

        '''Here you will received data from reqMktDepth request.

            tickerId -  the request's identifier
            position -  the order book's row being updated
            operation - how to refresh the row:
                0 = insert (insert this new order into the row identified by 'position')
                1 = update (update the existing order in the row identified by 'position')
                2 = delete (delete the existing order at the row identified by 'position').
            side -  0 for ask, 1 for bid
            price - the order's price
            size -  the order's size'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> reqId: {reqId} / position: {position} / operation: {operation} / side: {side} / price: {price} / size: {size}')

    def updateMktDepthL2(self, reqId: int, 
                               position: int, 
                               marketMaker: str,
                               operation: int, 
                               side: int, 
                               price: float, 
                               size: int, 
                               isSmartDepth: bool):

        '''Here you will received data from reqMktDepth request.

            tickerId -  the request's identifier
            position -  the order book's row being updated
            marketMaker - the exchange holding the order
            operation - how to refresh the row:
                0 = insert (insert this new order into the row identified by 'position')
                1 = update (update the existing order in the row identified by 'position')
                2 = delete (delete the existing order at the row identified by 'position').
            side -  0 for ask, 1 for bid
            price - the order's price
            size -  the order's size
            isSmartDepth - is SMART Depth request'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> reqId: {reqId} / position: {position} / marketMaker: {marketMaker} / operation: {operation} / side: {side} / price: {price} / size: {size} / isSmartDepth: {isSmartDepth}')

    def realtimeBar(self, reqId: int,
                          time: int, 
                          open_: float, 
                          high: float, 
                          low: float, 
                          close: float,
                          volume: int, 
                          wap: float, 
                          count: int):

        '''Here you will received data from reqRealTimeBars request.'''

        funcName = inspect.currentframe().f_code.co_name
        self.logger.info(f'{funcName} <> reqId: {reqId} / time: {time} / open: {open_} / high: {high} / low: {low} / close: {close} / volume: {volume} / wap: {wap} / count: {count}')

    ###########################################################

    def nextValidId(self, orderId: int):

        '''Receives next valid order id from TWS.'''

        funcName = inspect.currentframe().f_code.co_name
        self._nextValidOrderId = orderId

        self.logger.info(f'{funcName} <> ¡Connected!')
        self.logger.info(f'{funcName} <> NextValidOrderId: {orderId}')
        
        a = threading.active_count()
        self.logger.info(f'{funcName} <> Thread count for reference: {a}')

        # Call client method:
        self.reqCurrentTime()

        # Get real-time data:
        # Request contract data:
        nvidiaStock = self.createUSStockContract('NVDA', primaryExchange='NASDAQ')
        eurodollarPair = self.createFXPairContract('EURUSD')

        # "Real-time" watchlist data:
        #self.createMktDataRequest(eurodollarPair)

        # Real-time tick-by-tick data:
        #self.createTickByTickDataRequest(eurodollarPair)

        # Real-time market depth data:
        #self.createMktDepthDataRequest(nvidiaStock)

        # Real-time 5s bar data:
        self.createRealTimeBarsRequest(eurodollarPair)

    def getNextValidId(self) -> int:

        '''Get new request ID by incrementing previous one.'''

        funcName = inspect.currentframe().f_code.co_name
        newId = self._nextValidOrderId
        self._nextValidOrderId += 1
        self.logger.info(f'{funcName} <> NextValidOrderId: {newId}')
        return newId

    ###########################################################

    def createMktDataRequest(self, contract: Contract):

        self.reqMktData(self.getNextValidId(), 
                        contract=contract,
                        genericTickList='', 
                        snapshot=False,
                        regulatorySnapshot=False,
                        mktDataOptions=[])

    def createTickByTickDataRequest(self, contract: Contract):

        self.reqTickByTickData(self.getNextValidId(), 
                               contract=contract,
                               tickType='Last',
                               numberOfTicks=0, 
                               ignoreSize=True)

    def createMktDepthDataRequest(self, contract: Contract):

        self.reqMktDepth(self.getNextValidId(), 
                         contract=contract,
                         numRows=5, 
                         isSmartDepth=False, 
                         mktDepthOptions=[])

    def createRealTimeBarsRequest(self, contract: Contract):

        self.reqRealTimeBars(self.getNextValidId(), 
                             contract=contract,
                             barSize=5,
                             whatToShow='BID', 
                             useRTH=0,
                             realTimeBarsOptions=[])

    def createUSStockContract(self, symbol: str, primaryExchange: str):

        '''Create a US Stock contract placeholder.'''

        funcName = inspect.currentframe().f_code.co_name

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.primaryExchange = primaryExchange
        self.logger.info(f'{funcName} <> Contract: {contract}')

        return contract

    def createFXPairContract(self, pair: str):

        '''Create a FX pair contract placeholder.
        Pair has to be an FX pair in the format EURUSD, GBPUSD...'''

        funcName = inspect.currentframe().f_code.co_name

        # Separate currency and symbol:
        assert len(pair) == 6
        symbol = pair[:3]
        currency = pair[3:]

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'CASH'
        contract.exchange = 'IDEALPRO'
        contract.currency = currency
        self.logger.info(f'{funcName} <> Contract: {contract}')

        return contract

    def createMarketOrder(self, action: str, totalQuantity: int):

        '''Create a market order.'''

        funcName = inspect.currentframe().f_code.co_name

        order = Order()
        order.action = action
        order.orderType = 'MKT'
        order.totalQuantity = totalQuantity
        self.logger.info(f'{funcName} <> Order: {order}')

        return order

    def createStopOrder(self, action: str, totalQuantity: int, stopPrice: float):

        '''Create a market order.'''

        funcName = inspect.currentframe().f_code.co_name

        order = Order()
        order.action = action
        order.orderType = 'STP'
        order.totalQuantity = totalQuantity
        order.auxPrice = stopPrice
        self.logger.info(f'{funcName} <> Order: {order}')

        return order

if __name__ == "__main__":

    app = AlphaApp()
    app.connect('127.0.0.1', port=7497, clientId=123)
    app.run()