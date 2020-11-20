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
from ibapi.common import BarData

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

    def historicalData(self, reqId: int, 
                             bar: BarData):

        '''Returns the requested historical data bars

            reqId - the request's identifier
            date  - the bar's date and time (either as a yyyymmss hh:mm:ssformatted
                string or as system time according to the request)
            open  - the bar's open point
            high  - the bar's high point
            low   - the bar's low point
            close - the bar's closing point
            volume - the bar's traded volume if available
            count - the number of trades during the bar's timespan (only available
                for TRADES).
            WAP -   the bar's Weighted Average Price
            hasGaps  -indicates if the data has gaps or not.'''

        self.logger.info(f'reqId: {reqId} / bar: {bar}')

    def historicalDataEnd(self, reqId:int, 
                                start:str, 
                                end:str):

        '''Marks the ending of the historical bars reception.'''

        self.logger.info(f'reqId: {reqId} / start: {start} / end: {end}')

    def historicalDataUpdate(self, reqId: int, 
                                   bar: BarData):

        '''Returns updates in real time when keepUpToDate is set to True.'''

        self.logger.info(f'reqId: {reqId} / bar: {bar}')

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

        # Get historical data:
        # Request contract data:
        nvidiaStock = self.createUSStockContract('NVDA', primaryExchange='NASDAQ')
        self.reqHistoricalData(reqId=self.getNextValidId(), 
                               contract=eurodollarPair, 
                               endDateTime='20200903 18:00:00',
                               durationStr='5 D', 
                               barSizeSetting='30 mins', 
                               whatToShow='BID',
                               useRTH=0, 
                               formatDate=1, 
                               keepUpToDate=False, # True > historicalUpdate
                               chartOptions=[])

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

if __name__ == "__main__":

    app = AlphaApp()
    app.connect('127.0.0.1', port=7497, clientId=123)
    app.run()