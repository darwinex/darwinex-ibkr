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

from dataclasses import dataclass, fields, astuple
import pandas as pd

import threading, logging, time
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s <> %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

#######################################

@dataclass
class BarDataNew:

    date: str = ''
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: int = 0
    average: float = 0.0
    barCount: int = 0

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

    def historicalData(self, reqId: int, 
                             bar: BarData):

        '''Returns the requested historical data bars.

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

        self.historicalDataContainer.append(BarDataNew(**bar.__dict__))

    def historicalDataEnd(self, reqId:int, 
                                start:str, 
                                end:str):

        '''Marks the ending of the historical bars reception.'''

        self.logger.info(f'reqId: {reqId} / start: {start} / end: {end}')

        # Print the data:
        df = self._convertDataToDataFrame(self.historicalDataContainer)
        self.logger.info(df)

        # Make some calculations:
        self.makeSomeCalculations(df)

    def _convertDataToDataFrame(self, data: list) -> pd.DataFrame:

        dataContainerList = data
        dataStructure = dataContainerList[0]

        df = pd.DataFrame.from_records(astuple(o) for o in dataContainerList)
        df.columns = [field.name for field in fields(dataStructure)]
        df = df.set_index('date', drop=True)

        return df

    def makeSomeCalculations(self, df: pd.DataFrame):

        # Calculate returns based on the close:
        df['Returns'] = df.close.pct_change()

        # Calculate some indicators:
        from ta.volatility import BollingerBands # pip install --upgrade ta

        # Initialize Bollinger Bands Indicator
        BBBands = BollingerBands(close=df.close, n=20, ndev=2)

        # Add Bollinger Bands features
        df['bb_bbm'] = BBBands.bollinger_mavg()
        df['bb_bbh'] = BBBands.bollinger_hband()
        df['bb_bbl'] = BBBands.bollinger_lband()

        self.logger.info(df)

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
        #eurodollarPair = self.createFXPairContract('EURUSD')
        self.historicalDataContainer = []
        self.reqHistoricalData(reqId=self.getNextValidId(), 
                               contract=nvidiaStock, # eurodollarPair
                               endDateTime='20200903 18:00:00',
                               durationStr='1 D', 
                               barSizeSetting='30 mins', 
                               whatToShow='BID',
                               useRTH=0, 
                               formatDate=1, 
                               keepUpToDate=False, 
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