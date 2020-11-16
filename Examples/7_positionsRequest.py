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
        self.reqPositions()

    def getNextValidId(self) -> int:

        '''Get new request ID by incrementing previous one.'''

        funcName = inspect.currentframe().f_code.co_name
        newId = self._nextValidOrderId
        self._nextValidOrderId += 1
        self.logger.info(f'{funcName} <> NextValidOrderId: {newId}')
        return newId

    ###########################################################

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