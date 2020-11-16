# Installing (source activate ENVIRONMENT):
# Cd to: cd ~/Desktop/Darwinex/darwinex-ibkr/TWS_API/twsapi_macunix.976.01/IBJts/source/pythonclient/
# Do: python3 setup.py bdist_wheel
# Do: python3 -m pip install --user --upgrade dist/ibapi-9.76.1-py3-none-any.whl

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import threading

class AlphaWrapper(EWrapper):

    pass

class AlphaClient(EClient):

    def __init__(self, wrapper):

        EClient.__init__(self, wrapper)

#######################################

class AlphaApp(AlphaWrapper, AlphaClient):

    def __init__(self):

        AlphaWrapper.__init__(self)
        AlphaClient.__init__(self, wrapper=self)

    def nextValidId(self, orderId:int):

        """ Receives next valid order id."""

        print('Connected!')
        print(f'OrderID: {orderId}')
        
        a = threading.active_count()
        print(f'Thread count: {a}')

        # Make another call to do calcs for example:
        self.doCalculation()

    def doCalculation(self):

        print('Doing calculation...')

app = AlphaApp()
app.connect('127.0.0.1', port=7497, clientId=123)
app.run()