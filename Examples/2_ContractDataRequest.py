# Installing (source activate ENVIRONMENT):
# Cd to: cd ~/Desktop/Darwinex/darwinex-ibkr/TWS_API/twsapi_macunix.976.01/IBJts/source/pythonclient/
# Do: python3 setup.py bdist_wheel
# Do: python3 -m pip install --user --upgrade dist/ibapi-9.76.1-py3-none-any.whl

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, ContractDetails
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

        self.logger.error(f'ERROR <> reqId: {reqId} / Code: {errorCode} / Error String: {errorString}')

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):

        '''Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.'''

        self.logger.info(f'CONTRACT_DETAILS <> contractDetails: {contractDetails}')

    def contractDetailsEnd(self, reqId: int):

        '''This function is called once all contract details for a given
        request are received. This helps to define the end of an option
        chain.'''

        self.logger.info(f'CONTRACT_DETAILS <> contractDetails: {reqId}')

    ###########################################################

    def nextValidId(self, orderId: int):

        '''Receives next valid order id from TWS.'''

        self._nextValidOrderId = orderId

        self.logger.info('NEXT_VALID_ID <> ¡Connected!')
        self.logger.info(f'NEXT_VALID_ID <> NextValidOrderId: {orderId}')
        
        a = threading.active_count()
        self.logger.info(f'NEXT_VALID_ID <> Thread count for reference: {a}')

        # Call client method:
        self.reqCurrentTime()
        self.reqPositions()

        # Request contract data:
        nvidiaStock = self.createUSStockContract('NVDA', primaryExchange='NASDAQ')
        self.reqContractDetails(self.getNextValidId(), nvidiaStock)

    def getNextValidId(self) -> int:

        '''Get new request ID by incrementing previous one.'''

        newId = self._nextValidOrderId
        self._nextValidOrderId += 1
        self.logger.info(f'GET_NEXT_VALID_ID <> NextValidOrderId: {newId}')
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
        self.logger.info(f'US_STOCK_CONTRACT <> Contract: {contract}')

        return contract

if __name__ == "__main__":

    app = AlphaApp()
    app.connect('127.0.0.1', port=7497, clientId=123)
    app.run()