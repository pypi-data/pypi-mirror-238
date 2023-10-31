"""
░░░░░░░███████╗██╗░░██╗░█████╗░██╗░░██╗░█████╗░███╗░░██╗░██████╗░███████╗░░░░░░░█████╗░██████╗░██╗░░░░░░░
░░░░░░░██╔════╝╚██╗██╔╝██╔══██╗██║░░██║██╔══██╗████╗░██║██╔════╝░██╔════╝░░░░░░██╔══██╗██╔══██╗██║░░░░░░░
░░░░░░░█████╗░░░╚███╔╝░██║░░╚═╝███████║███████║██╔██╗██║██║░░██╗░█████╗░░█████╗███████║██████╔╝██║░░░░░░░
░░░░░░░██╔══╝░░░██╔██╗░██║░░██╗██╔══██║██╔══██║██║╚████║██║░░╚██╗██╔══╝░░╚════╝██╔══██║██╔═══╝░██║░░░░░░░
░░░░░░░███████╗██╔╝╚██╗╚█████╔╝██║░░██║██║░░██║██║░╚███║╚██████╔╝███████╗░░░░░░██║░░██║██║░░░░░██║░░░░░░░
░░░░░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░╚══════╝░░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░░░

 [*]Descr:     INTERACT & EXECUTE TASKS/TRADES ON AN EXCHANGE USING CCXT API WITH AUTHENTICATED ACCOUNT, 
               OPEN/CLOSE/CANCEL ORDERS, CHECK BALANCES, VIEW INFO & MAKE WITHDRAWALS USING EXCHANGE API.
 [*]Email:     wuddz_devs@protonmail.com                                                                 
 [*]Github:    https://github.com/wuddz-devs                                                             
 [*]Donation:                                                                                            
    BTC   ->   bc1qa7ssx0e4l6lytqawrnceu6hf5990x4r2uwuead                                                
    ERC20 ->   0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1                                                
    LTC   ->   LdbcFiQVUMTfc9eJdc5Gw2nZgyo6WjKCj7                                                        
    TRON  ->   TY6e3dWGpqyn2wUgnA5q63c88PJzfDmQAD                                                        
    DOGE  ->   DFwLwtcam7n2JreSpq1r2rtkA48Vos5Hgm                                                        

 [*]Menu:                                                                                                
    ab    =>   Account Balances                                                                          
    lb    =>   Limit Buy Order                                                                           
    ls    =>   Limit Sell Order                                                                          
    mb    =>   Market Buy Order                                                                          
    ms    =>   Market Sell Order                                                                         
    cbl   =>   Limit Close Buy Order                                                                     
    csl   =>   Limit Close Sell Order                                                                    
    cbm   =>   Market Close Buy Order                                                                    
    csm   =>   Market Close Sell Order                                                                   
    sl    =>   Stop_Loss                                                                                 
    oc    =>   Cancel All Orders                                                                         
    oi    =>   View & Cancel Order_ID                                                                    
    vo    =>   View Open Orders                                                                          
    vp    =>   View Positions                                                                            
    vw    =>   View Withdrawals                                                                          
    vt    =>   View Symbol Market/Trade Info                                                             
    wt    =>   Withdraw Tokens From Exchange                                                             
    a     =>   Authenticate To Exchange                                                                  
    s     =>   Set Symbol/Trade Pair                                                                     
    v     =>   Set Leverage                                                                              
    b     =>   Back To Previous Screen                                                                   
    f     =>   Set Output As File [`trade_output.txt` In Wuddz-Dapp Output Directory]                    
    p     =>   Set Output As Print [Print Results On Screen]                                             
    e     =>   Exit Program                                                                              
"""

import ccxt, logging, json, dapp, docs
from datetime import datetime
from getpass import getpass
from logging.handlers import RotatingFileHandler
from os import system
system('')


class Exchange:
    def __init__(self):
        """Interact & Execute Tasks On An Exchange Using Api Authenticated Account."""
        self.out='Screen'
        self.exc=None
        self.lev=None
        self.sym=None
        self.flst=None
        self.slst=None
        self.wlst=None
        self.exchange=None
        self.so='\n\033[1;34;40mAuthentication: {} | Output: {} | Symbol: {} | Leverage: {}' 
        self.wd=dapp.Dapp()
        self.sd={
                 'ab': 'Account Balances',
                 'lb': 'Limit Buy Order',
                 'ls': 'Limit Sell Order',
                 'mb': 'Market Buy Order',
                 'ms': 'Market Sell Order',
                 'cbl': 'Limit Close Buy Order',
                 'csl': 'Limit Close Sell Order',
                 'cbm': 'Market Close Buy Order',
                 'csm': 'Market Close Sell Order',
                 'sl': 'Stop_Loss',
                 'oc': 'Cancel All Orders',
                 'oi': 'View & Cancel Order_ID',
                 'vo': 'View Open Orders',
                 'vp': 'View Positions',
                 'vw': 'View Withdrawals',
                 'vt': 'View Symbol Market/Trade Info',
                 'wt': 'Withdraw Tokens From Exchange'
                }
        fh=RotatingFileHandler(
            filename=self.wd.lf,
            mode='a',
            maxBytes=5*1024*1024,
            backupCount=2,
            encoding='utf-8',
            delay=False
            )
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-15s %(levelname)-8s %(message)s",
            datefmt="%y-%m-%d %H:%M:%S",
            handlers=[fh]
            )
    
    def _authentication(self):
        """Loads Menu To Specify & Authenticate To An Exchange With Required Credentials."""
        exd={
            'enableRateLimit': True,
            'options': {'adjustForTimeDifference': True}
            }
        while True:
            try:
                ta=None
                self.wd.clear_screen()
                es=self.so.format(self.exc,self.out,self.sym,self.lev)
                exc=input(f'\033[1;32;40m{docs.exs}{es}\033[0m\n\nInput Exchange=> ').lower()
                if exc=='b':break
                if exc=='e':self.wd.pexit()
                elif len(exc)>1:
                    if exc[-2:]==' t':
                        ta='testnet'
                        exc=exc[:-2]
                    ex=getattr(ccxt,exc)
                    exd=self.auth_dict(ex.requiredCredentials,exc,exd)
                    self._exchange(exc,exd,tn=ta)
                    break
            except Exception as e:
                self.wd.get_menu(f'\033[1;31;40m{e}!!')
    
    def _balance(self) -> dict:
        """Returns Current Balance(s) Result Dictionary."""
        return self.exchange.fetch_balance()
    
    def _exchange(self, en: str, ad: dict, tn: str=None):
        """
        Returns Authenticated Ccxt Exchange Instance.
        :param en: Name Of Exchange To Authenticate To e.g `bybit`
        :param ad: Dictionary Containing Exchange Required Credentials For Authentication
        :param tn: String To Specify Testnet Defaults To None e.g `t`
        """
        exchange=eval(f'ccxt.{en}(ad)')
        if exchange.check_required_credentials():
            self.exc=en
            if tn:
                exchange.set_sandbox_mode(True)
                self.exc=f'{en} {tn}'
            exchange.load_markets()
            self.flst=exchange.has
            self.slst=exchange.symbols
            self.wlst=list(exchange.currencies.keys())
            self.exchange=exchange
    
    def _leverage(self, l: str, s: str=None) -> dict:
        """
        Sets Leverage For A Market (Margin Trading).
        :param l: Leverage To Set e.g `10`
        :param s: Symbol/Trade Pair To Set Leverage For Defaults To None e.g `btc/usd:btc`
        """
        return self.exchange.set_leverage(float(l), symbol=s.upper())
    
    def _output(self, d, t: str, o: str):
        """
        Writes Or Prints Executed Task Output To File (`trade_output.txt`) Or Screen.
        :param d: Output To Write To File Or Print On Screen
        :param t: Executed Menu Task To Get Output
        :param o: Output Type e.g `String | File`
        """
        if type(d) is dict:d=json.dumps(d, indent=4, default=str)
        if type(d) is list:
            a=''
            for i in d:
                if type(i) is dict:a+=json.dumps(i, indent=4, default=str)+'\n\n'
            if a:d=a
        if o=='Screen':self.wd.get_menu(f'\033[1;34;40m{t} Result:\n{d}')
        else:
            ts=datetime.now().strftime("%d-%m-%Y@%H:%M:%S")
            self.wd._fwrite(self.wd.to, f'{t} Result On {ts}:\n{d}\n\n')
            self.wd.get_menu(f'\033[1;34;40m{t} Results Saved To {self.wd.to} Successfully')
    
    def _withdraw(self, fc: str) -> dict:
        """
        Loads Menu To Set Arguments, Executes & Returns Token Withdrawal Result Dictionary.
        :param fc: Specified Main Menu Option
        """
        wd={}
        if self.flst.get('withdraw'):
            od=self.order_vars(fc, w='w')
            if type(od) is dict:
                for key in ['Chain','Memo']:
                    if od.get(key):wd[key.lower()]=od[key]
                return self.token_withdraw(od,wd)
    
    def auth_dict(self, ad: dict, exc: str, exd: dict) -> dict:
        """
        Loads Menu To Set Exchange API Authentication & Returns As Dictionary.
        :param ad:  Dictionary Containing Required Credentials For Exchange Authentication
        :param exc: Specified Exchange As String e.g `bybit t | binance`
        :param exd: Dictionary Containing Credentials & Parameters To Authenticate With
        """
        self.wd.clear_screen()
        print(f'\033[1;32;40m{docs.exa.format(exc.upper())}\033[0m')
        lst=[x for x in ad.keys() if ad.get(x)]
        if exc=='kucoin' and lst.count('password')==0:lst.append('password')
        for l in lst:
            exd[l]=getpass(f'Input {l}=> ')
        return exd
    
    def cancel_orders(self, fc: str) -> dict:
        """
        Returns Cancel Order By ID Or Cancel All Orders Result Dictionary.
        :param fc: Specified Main Menu Option
        """
        if fc=='oc':return self.order_cancel(self.sym)
        elif fc=='oi':
            olst=self.get_orders(self.sym)
            if olst:
                oid=input(f'\033[1;34;40m{olst}\n\033[0mInput Order_ID Or Skip=> ') or None
                if oid:return self.order_cancel_id(oid,self.sym)
    
    def get_orders(self, sym: str) -> str:
        """
        Returns List Of Currently Open Orders' Result Dictionaries.
        :param sym: Symbol Of Trading Pair To Execute Function For e.g `btc/usdt`
        """
        olst=''
        if self.flst.get('fetchOpenOrders'):
            since=self.exchange.milliseconds()-86400000
            while since < self.exchange.milliseconds():
                limit=10
                orders=self.exchange.fetch_open_orders(sym.upper(),since,limit)
                if len(orders):
                    since=orders[len(orders)-1]['timestamp']+1
                    olst+=json.dumps(orders, indent=4, default=str)
                else:break
        return olst
    
    def order_cancel_id(self, i: str, s: str) -> dict:
        """
        Returns Cancelled OrderId Result Dictionary.
        :param i: Order Id e.g `a7396446-b6a3-4350-93c2-f3fee8154a1b`
        :param s: Symbol Of Trading Pair To Cancel Order Id For e.g `BTC/USD:BTC`
        """
        return self.exchange.cancel_order(i,s.upper())
    
    def order_cancel(self, s: str) -> dict:
        """
        Returns Cancel All Orders Result Dictionary.
        :param s: Symbol Of Trading Pair To Cancel All Orders For e.g `BTC/USD:BTC`
        """
        return self.exchange.cancel_all_orders(s.upper())
    
    def order_create(self, od: dict, op: dict={}) -> dict:
        """
        Returns Executed Limit Buy Order Result Dictionary.
        :param od: Order Arguments Dictionary e.g Required Keys -> `Symbol,Type,Side,Amount,Price`
        :param op: Order Parameters Dictionary Defaults To Empty Dictionary e.g `{'timeInForce': 'GTC'}`
        """
        return self.exchange.create_order(
            od['Symbol'],
            od['Type'],
            od['Side'],
            od['Amount'],
            od['Price'],
            params=op
        )
    
    def order_open(self, fc: str) -> dict:
        """
        Returns Executed Open/Close Limit/Market Order Result Dictionary.
        :param fc: Specified Main Menu Option
        """
        r=''
        od=self.order_vars(fc)
        if type(od) is dict:
            if fc in ['mb','ms','csm','cbm']:
                od['Type']='market'
                params={"timeInForce": "FOK"}
            else:
                od['Type']='limit'
                params={"timeInForce": "GTC"}
            if fc[0]=='c':params['reduceOnly']=True
            if fc in ['mb','lb','csl','csm']:od['Side']='buy'
            if fc in ['ms','ls','cbl','cbm']:od['Side']='sell'
            r=self.order_create(od,params)
        return r
    
    def order_position(self, s: str) -> dict:
        """
        Returns Current Position(s) Result Dictionary.
        :param s: Symbol To Fetch Current Positions Result Dictionary e.g `BTC/USD:BTC`
        """
        return self.exchange.fetch_positions(s.upper())
    
    def order_stop(self, od: dict, op: dict={}):
        """
        Returns Executed Stoploss Order Result Dictionary.
        :param od: Stop Order Arguments Dictionary e.g Required Keys -> `Symbol,Type,Side,Amount,Price,StopPrice`
        :param op: Stop Order Parameters Dictionary Defaults To Empty Dictionary e.g `{'reduceOnly': True}`
        """
        return self.exchange.create_stop_order(
                od['Symbol'],
                od['Type'],
                od['Side'],
                od['Amount'],
                od['Price'],
                od['StopPrice'],
                params=op
            )
    
    def order_vars(self, et: str, w: str=None) -> dict:
        """
        Loads Menu To Set & Return Order Arguments & Values As Dictionary.
        :param w: Optional String To Specify Menu Banner & Arguments Defaults To None
        """
        os=docs.exos
        od={'Amount': '', 'Price': ''}
        if w=='w':
            od={'Amount': '', 'Address': '', 'Tag': None, 'Chain': '', 'Memo': ''}
            os=docs.exws
        elif w=='s':
            od={'Amount': '', 'Price': '', 'StopPrice': '', 'Side': '', 'Type': ''}
            os=docs.exos+docs.exns
        vd=dict(od)
        hd={f'{i+1} ': list(od.keys())[i] for i in range(len(od))}
        while True:
            self.wd.clear_screen()
            ds='\033[1;32;40m{}\n{}\n\033[1;32;40m\n{} Parameters:\n\033[1;34;40m{}\n\n\033[0mInput Choice=> '
            cp=self.so.format(self.exc,self.out,self.sym,self.lev)
            ov=input(ds.format(docs.exov.format(os),cp,self.sd[et],json.dumps(od, indent=2))) or 'a'
            if ov=='b':return
            if ov=='d':od.update(vd)
            elif ov=='x':break
            elif ov=='p':self.wd.get_menu(self.token_info())
            elif ov=='e':self.wd.pexit()
            elif ov=='s':
                if w=='w':self.set_symbol('w')
                else:self.set_symbol()
            elif len(ov)>=3:
                k=ov[:2]
                v=ov[2:]
                if hd.get(k):od[hd[k]]=v
        if not od.get('Price'):od['Price']=self.token_info(self.sym)['last']
        od['Symbol']=self.sym
        return od
    
    def set_leverage(self):
        """Loads Menu To Set Leverage (Margin Trading If Available)."""
        cp=self.so.format(self.exc,self.out,self.sym,self.lev)
        lv=input(f'\033[1;32;40m{docs.slv}\n{cp}\n\n\033[0mInput Leverage=> ') or None
        if lv.isdigit() and int(lv)<=100:
            r=self._leverage(float(lv), self.sym)['retMsg']
            if r=='OK':self.lev=lv
    
    def set_stoploss(self, fc: str) -> dict:
        """
        Loads Menu To Set & Execute Stop Loss Argument Values And Return Result Dictionary.
        :param fc: Specified Main Menu Option
        """
        od=self.order_vars(fc, w='s')
        if type(od) is dict:
            return self.order_stop(od,op={'reduceOnly': True})
    
    def set_symbol(self, w: str=None):
        """
        Loads Menu To Search & Set Symbol.
        :param w: String To Specify Symbol List To Iterate Defaults To None e.g `w`
        """
        while True:
            self.wd.clear_screen()
            slst=self.slst
            if w:slst=self.wlst
            so=self.so.format(self.exc, self.out, self.sym, self.lev)
            sbc=input(f'\n\033[1;32;40m{docs.exgs}{so}\n\n\033[0mInput Format=> ')
            if sbc=='b':break
            elif sbc=='e':self.wd.pexit()
            elif len(sbc)>1:
                k,v='',sbc.upper()
                if v[:2]=='S ':k,v=v[:2],v[2:]
                nl=[s for s in slst if v in s]
                if nl:
                    if k:self.sym=v
                    else:self.wd.get_menu('\033[1;34;40m'+'\n'.join(nl))
    
    def token_info(self, s: str) -> dict:
        """
        Returns Symbol Info Result Dictionary.
        :param s: Symbol To Fetch Info Result Dictionary e.g `BTC/USD:BTC`
        """
        return self.exchange.fetch_ticker(s.upper())
    
    def token_withdrawals(self) -> dict:
        """Returns Executed Withdrawals Result Dictionary."""
        return self.exchange.fetch_withdrawals()
    
    def token_withdraw(self, od: dict, op: dict={}) -> dict:
        """
        Returns Executed Withdraw Result Dictionary.
        :param od: Withdraw Arguments Dictionary e.g Required Keys -> `Symbol,Amount,Address,Tag`
        :param op: Withdraw Parameters Dictionary Defaults To Empty Dictionary e.g `{'Chain': 'BEP20'}`
        """
        return self.exchange.withdraw(
                   od['Symbol'],
                   od['Amount'],
                   od['Address'],
                   od['Tag'],
                   params=op
               )
    
    def main(self):
        """Loads Wuddz-Dapp Exchange-API Main Menu."""
        while True:
            try:
                r=''
                self.wd.clear_screen()
                ms=self.so.format(self.exc, self.out, self.sym, self.lev)
                self.wd.slow_print(__doc__)
                fc=(input(f'\033[1;32;40m{ms}\n\033[0m\nInput Choice=> ') or 'x').lower()
                self.wd.clear_screen()
                if fc=='ab':r=self._balance()
                elif fc[0] in ['l','m','c']:r=self.order_open(fc)
                elif fc in ['oc','oi']:r=self.cancel_orders(fc)
                elif fc=='vo':r=self.get_orders(self.sym)
                elif fc=='sl':r=self.set_stoploss(fc)
                elif fc=='vp':r=self.order_position(self.sym)
                elif fc=='vw':r=self.token_withdrawals()
                elif fc=='vt':r=self.token_info(self.sym)
                elif fc=='wt':r=self._withdraw(fc)
                elif fc=='a':self._authentication()
                elif fc=='b':break
                elif fc=='f':self.out='File'
                elif fc=='p':self.out='Print'
                elif fc=='v':self.set_leverage()
                elif fc=='s':self.set_symbol()
                elif fc=='e':self.wd.pexit()
                elif fc:self.wd.get_menu(f'\033[1;31;40m{fc} Not In List!!')
                if r:self._output(r, self.sd[fc], self.out)
            except Exception as e:
                self.wd.get_menu(f'\033[1;31;40m{e}!!')
        self.wd.clear_screen()

def cli_main():
    """Wuddz-Dapp Exchange_API Entry Point Launches Exchange-API Main Menu."""
    Exchange().main()
