# Installing (source activate ENVIRONMENT):
# Cd to: cd ~/Desktop/Darwinex/darwinex-ibkr/TWS_API/twsapi_macunix.976.01/IBJts/source/pythonclient/
# Do: python3 setup.py bdist_wheel
# Do: python3 -m pip install --user --upgrade dist/ibapi-9.76.1-py3-none-any.whl

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, ContractDetails
from ibapi.order import Order
from ibapi.order_state import OrderState
import threading, logging
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
        self.reqPositions()

        # Request contract data:
        nvidiaStock = self.createUSStockContract('NVDA', primaryExchange='NASDAQ')
        self.reqContractDetails(self.getNextValidId(), nvidiaStock)

        time.sleep(5)

        # Create orders:
        mktOrder = self.createMarketOrder('BUY', totalQuantity=100)
        stpOrder = self.createStopOrder('SELL', totalQuantity=100, stopPrice=200.25)

        # Place them:
        self.placeOrder(self.getNextValidId(), nvidiaStock, mktOrder)
        self.placeOrder(self.getNextValidId(), nvidiaStock, stpOrder)

        time.sleep(5)

        # Request openOrders and get the result back:
        self.reqOpenOrders()

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