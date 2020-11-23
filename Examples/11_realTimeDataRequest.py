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

    ###########################################################

    def tickPrice(self, reqId: int, 
                        tickType: TickType, 
                        price: float,
                        attrib: TickAttrib):

        '''Market data tick price callback. Handles all price related ticks.'''

        self.logger.info(f'reqId: {reqId} / tickType: {tickType} / price: {price} / attrib: {attrib}')

    def tickSize(self, reqId: int, 
                       tickType: TickType, 
                       size: int):

        '''Market data tick size callback. Handles all size-related ticks.'''

        self.logger.info(f'reqId: {reqId} / tickType: {tickType} / size: {size}')

    def tickByTickAllLast(self, reqId: int, 
                                tickType: int, 
                                time: int, 
                                price: float,
                                size: int, 
                                tickAtrribLast: TickAttribLast, 
                                exchange: str,
                                specialConditions: str):

        '''Here you will received data from reqTickByTickData request.'''

        self.logger.info(f'reqId: {reqId} / tickType: {tickType} / time: {time} / price: {price} / size: {size} / tickAtrribLast: {tickAtrribLast} / exchange: {exchange} / specialConditions: {specialConditions}')

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

        self.logger.info(f'reqId: {reqId} / position: {position} / operation: {operation} / side: {side} / price: {price} / size: {size}')

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

        self.logger.info(f'reqId: {reqId} / position: {position} / marketMaker: {marketMaker} / operation: {operation} / side: {side} / price: {price} / size: {size} / isSmartDepth: {isSmartDepth}')

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

        self.logger.info(f'reqId: {reqId} / time: {time} / open: {open_} / high: {high} / low: {low} / close: {close} / volume: {volume} / wap: {wap} / count: {count}')

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

        # Get real-time data:
        # Request contract data:
        nvidiaStock = self.createUSStockContract('NVDA', primaryExchange='NASDAQ')

        # "Real-time" watchlist data:
        #self.createMktDataRequest(nvidiaStock)

        # Real-time tick-by-tick data:
        #self.createTickByTickDataRequest(nvidiaStock)

        # Real-time market depth data:
        #self.createMktDepthDataRequest(nvidiaStock)

        # Real-time 5s bar data:
        self.createRealTimeBarsRequest(nvidiaStock)

    def getNextValidId(self) -> int:

        '''Get new request ID by incrementing previous one.'''

        newId = self._nextValidOrderId
        self._nextValidOrderId += 1
        self.logger.info(f'NextValidOrderId: {newId}')
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

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.primaryExchange = primaryExchange
        self.logger.info(f'Contract: {contract}')

        return contract

if __name__ == "__main__":

    app = AlphaApp()
    app.connect('127.0.0.1', port=7497, clientId=123)
    app.run()