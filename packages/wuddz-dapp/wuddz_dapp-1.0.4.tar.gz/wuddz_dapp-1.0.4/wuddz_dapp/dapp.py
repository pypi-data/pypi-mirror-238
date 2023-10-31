"""
░░░░░░░░░░░██╗░░░░░░░██╗██╗░░░██╗██████╗░██████╗░███████╗░░░░░░██████╗░░█████╗░██████╗░██████╗░░░░░░░░░░░░
░░░░░░░░░░░██║░░██╗░░██║██║░░░██║██╔══██╗██╔══██╗╚════██║░░░░░░██╔══██╗██╔══██╗██╔══██╗██╔══██╗░░░░░░░░░░░
░░░░░░░░░░░╚██╗████╗██╔╝██║░░░██║██║░░██║██║░░██║░░███╔═╝█████╗██║░░██║███████║██████╔╝██████╔╝░░░░░░░░░░░
░░░░░░░░░░░░████╔═████║░██║░░░██║██║░░██║██║░░██║██╔══╝░░╚════╝██║░░██║██╔══██║██╔═══╝░██╔═══╝░░░░░░░░░░░░
░░░░░░░░░░░░╚██╔╝░╚██╔╝░╚██████╔╝██████╔╝██████╔╝███████╗░░░░░░██████╔╝██║░░██║██║░░░░░██║░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░╚═╝░░░╚═╝░░░╚═════╝░╚═════╝░╚═════╝░╚══════╝░░░░░░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░░░░░░░░░░░░

 [*]Descr:     ERC20 DAPP, CREATE ACCOUNTS, GET ALL TOKEN BALANCES & USD VALUE FOR AN ACCOUNT/WALLET,     
               MAKE TRANSACTIONS, INTERACT SMART CONTRACTS, SWAP ERC20 TOKENS, GET CURRENT CRYPTO PRICES, 
               AUTHENTICATE TO EXCHANGE ACCOUNT VIA API, CONVERT CRYPTO TO CRYPTO VALUE AND BASE64 DECODER
 [*]Coder:     Wuddz_Devs                                                                                 
 [*]Email:     wuddz_devs@protonmail.com                                                                  
 [*]Github:    https://github.com/wuddz-devs                                                              
 [*]Reddit:    https://reddit.com/users/wuddz-devs                                                        
 [*]Twitter:   https://twitter.com/wuddz_devs                                                             
 [*]Telegram:  https://t.me/wuddz_devs                                                                    
 [*]Videos:    https://mega.nz/folder/IWVAXTqS#FoZAje2NukIcIrEXXKTo0w                                     
 [*]Youtube:   https://youtube.com/@wuddz-devs                                                            
 [*]Donation:                                                                                             
    BTC   ->   bc1qa7ssx0e4l6lytqawrnceu6hf5990x4r2uwuead                                                 
    ERC20 ->   0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1                                                 
    LTC   ->   LdbcFiQVUMTfc9eJdc5Gw2nZgyo6WjKCj7                                                         
    TRON  ->   TY6e3dWGpqyn2wUgnA5q63c88PJzfDmQAD                                                         
    DOGE  ->   DFwLwtcam7n2JreSpq1r2rtkA48Vos5Hgm                                                         

 [*]Menu:                                                                                                 
    1     =>   Create A New Ethereum Account                                                              
    2     =>   Check Account Balance(s)                                                                   
    3     =>   Send/Deposit To An Account                                                                 
    4     =>   Get Account Address & Balance(s) From Private Key Or Mnemonic Seed                         
    5     =>   Get Transaction Hash Attributes                                                            
    6     =>   Compile & Deploy Smart Contract To Blockchain                                              
    7     =>   Interact, Read & Execute Smart Contract Functions                                          
    8     =>   Verify Deployed Smart Contract On Etherscan/Polygonscan                                    
    9     =>   Swap/Purchase ERC20 Tokens Using 0x Api                                                    
    x     =>   Interact With Exchange Account (Authentication ApiKey, ApiSecret, ApiPassword etc...)      
    d     =>   Decode Base64 String                                                                       
    p     =>   Crypto Price & Conversion                                                                  
    n     =>   Choose Blockchain Network                                                                  
    e     =>   Exit Program                                                                               
"""

import docs, re, sys, json, base64, requests, warnings
from secrets import choice
from platform import system as _ps
from importlib.machinery import SourceFileLoader
from shutil import copy as Cp
from pycoingecko import CoinGeckoAPI
from time import sleep
from pathlib import Path
from web3 import Web3, EthereumTesterProvider
from subprocess import call
from os import system, _exit
warnings.simplefilter(action='ignore', category=FutureWarning)
system('')


class Dapp:
    def __init__(self):
        """Connect & Interact With Various Ethereum Blockchains Using Specified Testnet/Mainnet Networks."""
        self.da=''
        self.pk=''
        self.nw=None
        self.node_url=''
        self.name=_ps()
        self.cg=CoinGeckoAPI()
        self.bt={
                'celo': 'CELO', 'starknet': 'STRK',
                'aurora': 'AURORA', 'near': 'NEAR', 
                'avalanche': 'AVAX', 'palm': 'PALM', 
                'arbitrum': 'ARB', 'optimism': 'OP', 
                'polygon': 'MATIC', 'bsc': 'BNB'
                }
        self.ss='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.sw='https://{}api.0x.org/swap/v1/quote?buyToken={}&sellToken={}&{}Amount={}&slippagePercentage={}&takerAddress={}'
        self.hs='\n\033[1;34;40m{}\nTx_Hash: {}\033[0m'
        self.ns='\n\033[1;34;40m    current network: {} | connected: {}\n'
        self.nh='\n\033[1;34;40mTransaction Completed Successfully\nTx_Hash: {}\033[0m'
        self.at='\n\033[1;32;40mDo You Approve Transaction?\nInput y or n=> '
        pkg=str(Path.home().expanduser().joinpath('Desktop','DAPP'))
        if not Path(pkg).exists:Path(pkg).mkdir(parents=True, exist_ok=True)
        self.dp=Path(pkg).joinpath('config.py')
        self.cf=Path(pkg).joinpath('contract_info.txt')
        self.kf=Path(pkg).joinpath('key_file.txt')
        self.kd=Path(pkg).joinpath('key_data.txt')
        self.tr=Path(pkg).joinpath('tx_receipts.txt')
        self.lf=Path(pkg).joinpath('trade-log.txt')
        self.to=Path(pkg).joinpath('trade_output.txt')
        self.dc=(Path(__file__).absolute().parent).joinpath('dapp_config.py')
        if not Path(self.dp).exists():Cp(self.dc, self.dp)
        self.dcfg=self.config_import()
        self.web3=Web3(EthereumTesterProvider)
        self.web3.eth.account.enable_unaudited_hdwallet_features()
    
    def _fwrite(self, fn: str, data):
        """
        Writes Data To Specified File.
        :param fn: File To Write Data To
        :param data: Data To Write To File
        """
        with open(fn, 'a', encoding='utf-8') as fw:
            fw.write(data)
    
    def _fread(self, fn: str):
        """
        Returns Data Read From Specified File.
        :param fn: File To Read Data From
        """
        with open(fn, 'r', encoding='utf-8') as fr:
            return fr.read()
    
    def nw_status(self) -> bool:
        """Returns Web3 Connection Status True Or False."""
        try:
            return self.web3.is_connected()
        except:return False
    
    def config_import(self):
        """Returns `config.py` Module Imported From Wuddz-Dapp Output Folder."""
        mn='config'
        sp=SourceFileLoader(mn, str(self.dp))
        cm=sp.load_module()
        return cm
    
    def pexit(self):
        """Clear CLI Screen & Exit Program."""
        self.clear_screen()
        _exit(0)
    
    def get_menu(self, m: str='', c: bool=True):
        """
        Print Output To Screen & Wait For User Input.
        :param m: Optional String To Print To Screen, If String Is `e` Prints `*Error Occurred*`
        :param c: Optional Bool To Clear CLI Screen Or Not Defaults To True
        """
        if c:self.clear_screen()
        if m:
            a='\033[1;32;40m[*]OUTPUT:\n\n'
            if m=='e':m='\033[1;31;40m*Error Occurred*'
            m=a+m
        input(m+'\n\n\033[1;32;40m...Hit Enter|Return Key To Continue....\033[0m\n')
    
    def slow_print(self, doc: str, sp: float=0.0005):
        """
        Print String By Speed In Seconds Less Is Faster.
        :param doc: String To Be Printed
        :param sp:  Speed To Print String `e.g 0.0001 or 0.0005 used`
        """
        for d in doc:
            sys.stdout.write(f"\033[1;32;40m{d}")
            sleep(sp)
    
    def clear_screen(self):
        """Clear Command Line Screen."""
        if self.name=='Linux':system('clear')
        elif self.name=='Windows':system('cls')
        elif self.name=='Darwin':system("printf '\\33c\\e[3J'")
    
    def decode_bsf(self, s: str):
        """
        Prints Decoded Base64 String To Screen.
        :param s: Encoded Base64 String e.g `3R1ZGVudCBub2l=`
        """
        self.get_menu('\033[1;34;40m'+str(base64.b64decode(s).decode('utf-8')))
    
    def func_menu(self, c: str, i: str, n: str=None, f: str=None):
        """
        Loads Menu To Return Input.
        :param c: Menu Banner Type Docstring
        :param i: String Specifying Menu Input
        :param n: String To Specify Network Choice In Menu Defaults To None
        :param f: String Specifying Method To Execute Defaults To None
        """
        while True:
            try:
                self.clear_screen()
                d=f'\033[1;32;40m{c}\n\033[0mInput {i}=> '
                if n:d=f'\033[1;32;40m{c}{self.ns.format(self.nw,self.nw_status())}\n\033[0mInput {i}=> '
                a=input(d) or None
                if a=='b':break
                elif a=='e':self.pexit()
                elif n and a=='n':self.block_network()
                elif a and f:eval(f'self.{f}(a)')
                elif a:return a
            except Exception as e:self.get_menu(f'\033[1;31;40m{e}')
    
    def get_price(self, i: str='ethereum'):
        """
        Return Price Of Token In Usd Using CoinGecko API Token ID.
        :param i: Coingecko Token Id To Get Usd Value Defaults To BTC e.g `ethereum`
        """
        return self.cg.get_price(i,'usd')[i]['usd']
    
    def js_resp(self, u: str, h: dict={}):
        """
        Returns Url Request Response
        :param u: Url To Call
        :param h: Headers As Type Dictionary
        """
        return requests.get(u, headers=h, verify=None)
    
    def account_auth(self):
        """Loads Menu To Return Eth Account Object & Private Key From Input, Mnemonic String Or File."""
        try:
            pp=self.func_menu(docs.aa, 'Authentication', 'n')
            if not pp:return 'b',None
            if len(pp) in [64,66] or ' ' in pp:pk=pp
            elif len(pp)==44:pk=self.pkey_file(pp)
            da=self.account_key(pk, x='d')
            return da, pk
        except:pass
    
    def account_key(self, s: str, x: str=None):
        """
        Returns Address Or Prints Address Balance To Screen.
        :param s: Mnemonic String Or Private Key
        :param x: String To Specify Print Balance To Screen If Specified
        """
        if ' ' in s:acct=self.mnemonic_str(s)
        else:acct=self.pkey_str(s)
        if x:return acct
        bal=self.bal_main(acct.address)
    
    def mnemonic_str(self, m: str):
        """
        Returns Web3 Eth Account Object From Mnemonic String.
        :param m: Mnemonic String Of Account
        """
        return self.web3.eth.account.from_mnemonic(m)
    
    def pkey_str(self, k: str):
        """
        Returns Web3 Eth Account Object From Private Key.
        :param k: Private Key Of Account
        """
        return self.web3.eth.account.from_key(k)
    
    def account_create(self):
        """Creates A Web3 Eth Account, Writes Encrypted Data & Base64 Encoded Info To Output Files & Prints Address To Screen."""
        psd=''.join(choice(self.ss) for i in range(32))
        pd=base64.urlsafe_b64encode(bytes(psd, 'utf-8'))
        acct, mnemonic=self.eth_wallet()
        encrypted=self.web3.eth.account.encrypt(acct.key, psd)
        pk=base64.urlsafe_b64encode(bytes(self.web3.to_hex(acct.key), 'utf-8'))
        mn=base64.urlsafe_b64encode(bytes(mnemonic, 'utf-8'))
        self._fwrite(self.kf, f'{pd[:14]} {json.dumps(encrypted)}\n')
        self._fwrite(self.kd, f'Account: {acct.address}\nPrivate_Key: {pk}\nPrivate_Key_Password: {pd}\nMnemonic: {mn}\n\n')
        self.get_menu(f'\033[1;34;40mAccount_Created=> {acct.address}')
    
    def pkey_file(self, p: str):
        """
        Returns Private Key From File Containing Encrypted Account Data Using Password.
        :param p: Password To Decrypt Account Data
        """
        psd=str(base64.b64decode(p).decode('utf-8'))
        line=re.search("b'"+p[:14]+"' (.*)",self._fread(self.kf)).group(1)
        return self.web3.to_hex(self.web3.eth.account.decrypt(line, psd))
    
    def crypto_price(self):
        """Loads Menu To Get Crypto Price & Conversion Using CoinGecko API."""
        while True:
            try:
                self.clear_screen()
                cc=self.func_menu(docs.cp, 'Choice')
                if not cc:break
                ccl=cc.split()
                cd=self.cg.get_coin_by_id(ccl[1])
                cpa=self.cg.get_price(cd['id'],'usd')[str(cd['id'])]['usd']
                crp="${:,.2f}".format(float(ccl[0])*float(cpa))
                syma=cd['symbol'].upper()
                if len(ccl)==2:self.get_menu(f"\033[1;34;40m{cc.replace(ccl[1],syma)} => {crp} USD")
                elif len(cc.split())==3:
                    cb=self.cg.get_coin_by_id(ccl[2])
                    symb=cb['symbol'].upper()
                    cpb=self.cg.get_price(ccl[2],'usd')[str(ccl[2])]['usd']
                    cvv=float(ccl[0])*(float(cpa)/float(cpb))
                    self.get_menu(f"\033[1;34;40m{ccl[0]} {syma} => {cvv} {symb}\nTotal Value => {crp} USD")
            except requests.exceptions.ConnectionError:
                self.get_menu(f'\033[1;31;40mNo Connection Error!!')
            except:self.get_menu(f'\033[1;31;40m{cc} Not Valid!!')
    
    def eth_value(self, a: str):
        """
        Returns Balance Of Address In Ether Denomination.
        :param a: Address To Get Balance For
        """
        b=self.web3.eth.get_balance(self.web3.to_checksum_address(a))
        return self.web3.from_wei(b, 'ether')
    
    def ens_addr(self, a: str) -> str:
        """
        Return Ens Name Or Address For Specified Ens Name.
        :param a: Ens Name Or Address e.g `vitalik.eth | 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`
        """
        try:
            f='name'
            if '.eth' in a:f='address'
            adr=eval(f'self.web3.ens.{f}("{a}")')
            if f=='name':adr=re.search('\S+.eth',adr).group()
            return adr
        except:return a
    
    def tkn_address(self, s: str, n: str='mainnet') -> str:
        """
        Returns Token Contract Address From Dapp_Config Token Info If Available.
        :param s: Symbol Of Token To Retrieve Contract Address e.g `BNB`
        :param e: First Letter Of Token To Retrieve Contract Address e.g `BNB`
        """
        if n not in ['mainnet', 'polygon', 'goerli', 'sepolia', 'mumbai']:return
        return self.dcfg.tcd[n][[i for i in list(self.dcfg.tcd[n].keys()) if i==s.upper()][0]]
    
    def bal_main(self, a: str):
        """
        Prints Address Balance(s) To Screen From API Or Contract Call.
        :param a: Address To Get Balance(s) For
        """
        enn=''
        tca=''
        ttt=self.bt.get(self.nw)
        if not ttt:ttt='ETH'
        try:
            l=a.split()
            if len(l)==1:addr=l[0]
            elif len(l)==2:
                addr=l[0]
                if len(l[1])==42:tca=l[1]
                else:
                    tca=self.tkn_address(l[1], n=self.nw)
                    assert self.web3.to_checksum_address(tca)
            addr=self.ens_addr(l[0])
            if '.eth' in addr:
                enn=addr
                addr=l[0]
            elif '.eth' in a:enn=a
            base=self.eth_value(addr)
            if self.nw not in ['goerli','mumbai','sepolia','ganache','bsctestnet','development']:
                tot=0
                bs=''
                nw=self.nw[0].upper()+self.nw[1:]
                url=f'https://api.ethplorer.io/getAddressInfo/{addr}?showTxsCount=true&apiKey=freekey'
                if tca:url=f'https://api.ethplorer.io/getAddressInfo/{addr}?token={tca}&showETHTotals=false&showTxsCount=true&apiKey=freekey'
                bjs=self.js_resp(url).json()
                prc=bjs['ETH']['price']['rate']
                ethv=bjs['ETH']['balance']
                txc=bjs['countTxs']
                if bjs.get('tokens'):tot,bs=self.bal_sub(bjs)
                eus=float(prc)*float(ethv)
                usdt="${:,.2f}".format(tot+eus)
                eusd="${:,.2f}".format(eus)
                j=f'\033[1;34;40mAccount: {addr}\nEthereum: {ethv} ETH \033[1;32;40m({eusd} USD)\n'
                if ttt!='ETH':j=f'\033[1;34;40mAccount: {addr}\n{nw}: {base} {ttt}\nEthereum: {ethv} ETH \033[1;32;40m({eusd} USD)\n'
                if enn:j=j+f'\033[1;34;40mEnsName: {enn}\n'
                self.get_menu(bs+j+f'\033[1;34;40mTotal Value: \033[1;32;40m{usdt} USD\n\033[1;34;40mTotal Transactions: {txc}')
            else:
                if tca:c,ethv,ttt,tkn,d=self.contract_info(str(tca), chk=addr)
                self.get_menu(f'\033[1;34;40mAccount: {addr}\nBalance: {base} {ttt}')
        except:self.get_menu('e')
    
    def bal_sub(self, d: dict) -> int:
        """
        Returns Total USD Value Of All Tokens API Dictionary Response & Prints Each Iterated Token & Balance To Screen.
        :param d: Ethplorer API Response As Json Dictionary 
        """
        tot=[]
        bl=''
        for i in range(len(d['tokens'])+1):
            usdc='0'
            try:
                nam=d['tokens'][i]['tokenInfo']['name']
                sym=d['tokens'][i]['tokenInfo']['symbol']
                dec=d['tokens'][i]['tokenInfo']['decimals']
                rbal=d['tokens'][i]['rawBalance']
                bal=rbal
                if str(dec).isdigit():bal=int(rbal)/10**int(dec)
                if d['tokens'][i]['tokenInfo']['price']:
                    pri=d['tokens'][i]['tokenInfo']['price']['rate']
                    usd=float(pri)*int(bal)
                    tot.append(usd)
                    usdc="{:,.2f}".format(usd)
                bl+=f'\033[1;34;40m{nam}: {bal} \033[1;32;40m(${usdc} USD) \033[1;34;40m{sym}\033[0m\n\n'
            except:pass
        return sum(tot),bl
    
    def bal_fkey(self):
        """Loads Menu To Print Balance & Address Of Token From Authentication."""
        while True:
            try:
                a,k=self.account_auth()
                if a=='b':break
                self.bal_main(a.address)
            except:self.get_menu('e')
    
    def trx_hash(self, h: str, o=None):
        """
        Prints OR Writes Transaction Hash Info To Screen/Output File.
        :param h: Transaction Hash
        :param o: String To Specify Write Transaction Info To File Defaults To None
        """
        txr=dict(self.web3.eth.get_transaction(h))
        txr['gas']=format(self.web3.from_wei(txr['gas'], 'ether'),'f')
        txr['gasPrice']=format(self.web3.from_wei(txr['gasPrice'], 'ether'),'f')
        txr['value']=self.web3.from_wei(txr['value'], 'ether')
        txr['blockHash']=self.web3.to_hex(txr['blockHash'])
        txr['hash']=self.web3.to_hex(txr['hash'])
        txr['r']=self.web3.to_hex(txr['r'])
        txr['s']=self.web3.to_hex(txr['s'])
        if o:self._fwrite(self.tr, f'{self.node_url}\n{json.dumps(txr, indent=4, default=str)}\n\n')
        else:self.get_menu('\033[1;34;40m'+json.dumps(txr, indent=4, default=str))
    
    def block_network(self, nc: str=None):
        """
        Sets Or Loads Menu To Select & Set Specified Blockchain Network.
        :param nc: String To Specify Blockchain Network e.g `mainnet | goerli`
        """
        d={'1':'mainnet','2':'sepolia','3':'goerli',
           '4':'linea','5':'celo','6':'starknet',
           '7':'aurora','8':'near','9':'avalanche',
           '10':'palm','11':'arbitrum', '12':'optimism',
           '13':'polygon', '14':'mumbai', '15':'bsc',
		   '16':'bsctestnet', 'g':'ganache', 'd':'development'}
        try:
            if not nc:nc=self.func_menu(docs.nwl, 'Network Choice')
            if d.get(nc):self.nw=str(d[nc])
            else:self.nw='mainnet'
            self.node_url=eval(f'self.dcfg.{self.nw}')
            self.web3=Web3(Web3.HTTPProvider(self.node_url))
        except:pass
    
    def account_deposit(self):
        """Loads Menu To Create, Approve & Sign Deposit Transaction."""
        while True:
            try:
                ttt='ETH'
                acc, pk=self.account_auth()
                if acc=='b':break
                nonce=self.web3.eth.get_transaction_count(acc.address)
                dtx=self.func_menu(docs.der, 'Transfer Format', n='n')
                if not dtx:break
                dpa,amnt,tca=dtx.split()
                if tca.lower()!='eth':
                   if len(tca)!=42:
                       tca=self.tkn_address(tca, n=self.nw)
                       assert self.web3.to_checksum_address(tca)
                   c,b,ttt,n,dec=self.contract_info(tca)
                   amt=float(amnt)*(10**int(dec))
                else:amt=self.web3.to_wei(amnt, 'ether')
                assert self.web3.to_checksum_address(dpa)
                if ttt=='ETH':tx=self.transfer_eth(dpa, amt, nonce)
                else:tx=self.transfer_tkn(contract, dpa, amt, nonce)
                tc='\n\033[1;32;40mTransaction:\033[1;34;40m\n{}\n{}\n'
                td='Deposit Amount: {} {}\nFrom: {}\nTo: {}'.format(str(amnt), ttt, acc.address, dpa)
                at=tc.format(json.dumps(tx, indent=2, default=str),td)
                ap=input(f'{at}{self.at}') or 'n'
                if ap=='y':self.sign_tx(tx,pk)
            except:self.get_menu('e')
    
    def sign_tx(self, tx: dict, k: str, hs: str=None, cd: str=None):
        """
        Signs Transaction With Provided Private Key, Returns Or Prints To Screen & Writes Tx Hash & Receipt To Output File.
        :param tx: Unsigned Transaction As Type Dictionary
        :param k:  Private Key To Sign Transaction
        :param hs: Optional String If Specified Prints Transaction Hash To Screen Defaults To None
        :param cd: Optional String If Specified Returns Transaction Receipt & Hash Defaults To None
        """
        signed_tx=self.web3.eth.account.sign_tx(tx, k)
        tx_hash=self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt=self.web3.eth.wait_for_transaction_receipt(tx_hash)
        th=self.web3.to_hex(tx_receipt.transactionHash)
        if cd:return tx_receipt,th
        elif hs:print(self.hs.format(hs,th))
        else:self.get_menu(self.nh.format(th))
        self.trx_hash(th,'t')
    
    def get_contract(self, abi: list, ca: str=None, bc: str=None):
        """
        Returns Web3 Contract Instance For Specified Contract Address.
        :param abi: ABI List For Specified Contract `ca`
        :param ca:  Contract Address Defaults To None
        :param bc:  Contract ByteCode Defaults To None
        """
        if ca:return self.web3.eth.contract(abi=abi, address=ca)
        return self.web3.eth.contract(abi=abi, bytecode=bc)
    
    def contract_info(self, tca: str, chk: str=None):
        """
        Returns Web3 Contract Instance, Balance Of Contract Name For Address If Specified, Symbol, Name & Decimal Number For Contract Address.
        :param tca: Contract Address
        :param chk: Address To Get Balance Of Contract Address For Defaults To None
        """
        ethv=''
        contract=self.get_contract(self.dcfg.abi, ca=tca)
        if chk:ethv=contract.functions.balanceOf(str(chk)).call()
        dec=contract.functions.decimals().call()
        sym=contract.functions.symbol().call()
        nam=contract.functions.name().call()
        if str(dec)!='0' and chk:ethv=ethv/10**dec
        return contract,ethv,sym,nam,dec
    
    def contract_rw(self, addr: str):
        """
        Loads Menu To Interact, Call & Execute Contract Functions & Print Results.
        :param addr: Verified Smart Contract Address
        """
        abi=''
        if self.nw=='ganache':abi=self.local_abi()
        else:abi=self.remote_abi(addr, n=self.nw)
        if abi:
            contract=self.get_contract(abi, ca=addr)
            cfs=[(str(c).split('>')[0]).split(' ')[1] for c in contract.all_functions()]
            if cfs:
                dec=''
                if 'decimals()' in str(cfs):dec=contract.functions.decimals().call()
                while True:
                    self.clear_screen()
                    print(f'\n\033[1;32;40m [*]ALL CONTRACT FUNCTIONS FOR => {addr}:\033[0m\n')
                    for c in cfs:
                        if '()' in c:c=self.contract_call(contract,c,dec=dec)
                        print(f'\033[1;34;40m{c}\033[0m')
                    fnc=input(f'\n\033[1;32;40m{docs.crw}\033[0m\nInput Choice=> ')
                    if fnc=='b':break
                    elif fnc=='c':self.convert_value()
                    elif f'{fnc}(' in str(cfs):
                        v=[c for c in cfs if f'{fnc}(' in c][0]
                        self.contract_sub(v,contract,dec)
            else:self.get_menu('\033[1;31;40m*Contract Not Valid*')
        else:self.get_menu('\033[1;31;40m*Contract Abi Not Found*')
    
    def contract_sub(self, fnc: str, contract, dec: str):
        """
        Execute Private Contract Function.
        :param fnc: Function To Be Executed e.g `balanceOf`
        :param contract: Contract Instance To Execute Functions
        :param dec: Decimal Number For Contract
        """
        if '()' in fnc:self.get_menu(self.contract_call(contract,fnc,dec=dec))
        else:
            et=''
            fnc=fnc.split('(')[0]
            fd,et=self.contract_data(fnc,contract.abi)
            fo=f'{fnc}('
            for k,v in fd.items():
                if v:
                    if 'uint' in str(k):fo+=f'int("{v}"),'
                    else:fo+=f'"{v}",'
            if fo[-1]!='(':
                fp=f'{fo[:-1]})'
                if str(et) not in ['pure', 'view']:
                    acc, pk=self.account_auth()
                    if acc=='b':return
                    nonce=self.web3.eth.get_transaction_count(acc.address)
                    gas=eval(fp).estimate_gas()
                    tx=eval(fp).build_transaction({'nonce': nonce, 'gas': gas, 'gasPrice': self.web3.eth.gas_price})
                    self.sign_tx(tx,pk)
                else:self.get_menu(self.contract_call(contract,fp,dec=dec))
            else:self.get_menu('e')
    
    def contract_deploy(self, cn: str):
        """
        Verifies & Deploys Smart Contract To Current Blockchain Network & Prints Transaction Results To Screen.
        :param cn: Name Of Contract To Be Deployed
        """
        fd=list(Path(self.dcfg.scdir).rglob(f'{cn}.json'))
        if fd:fd=fd[0]
        else:call(['truffle', 'compile'], cwd=self.dcfg.scdir)
        ci=json.loads(self._fread(fd))
        abi=ci['abi']
        bc=ci['bytecode']
        acc,pk=self.account_auth()
        contract=self.get_contract(abi=abi, bc=bc)
        tx=contract.constructor().build_transaction(
              {
               'nonce': self.web3.eth.get_transaction_count(acc.address),
               'gasPrice': self.web3.eth.gas_price
              }
           )
        txr,txh=self.sign_tx(tx,pk,cd='cd')
        ca=txr.contractAddress
        cna=f'{cn}@{ca}'
        self._fwrite(self.cf, f'name: {cn}.json\nabi: {abi}\naddress: {ca}\nnetwork: {self.node_url}\n\n')
        if self.nw!='ganache':call(['truffle', 'run', 'verify', cna, '--network', self.nw], cwd=self.dcfg.scdir)
        self.trx_hash(txh,'t')
        self.get_menu(f'\n\033[1;34;40mSmart_Contract_Address: {ca}')
    
    def contract_call(self, contract, cf: str, dec: str=None):
        """
        Prints Contract Function Call & Result To Screen If Valid.
        :param contract: Contract Instance To Call Functions With
        :param cf:  Contract Function To Call e.g `balanceOf`
        :param dec: Decimal Number For Token Contract Defaults To None
        """
        try: 
            fnc=eval(f'contract.functions.{cf}.call()')
            if dec and len(str(fnc))>int(dec):fnc=fnc/(10**int(dec))
            return f'\033[1;34;40m{cf} = {fnc}\033[0m'
        except:return 'e'
    
    def convert_value(self):
        """Loads Menu To Convert To/From Wei."""
        while True:
            try:
                self.clear_screen()
                cv=input(f'\n\033[1;32;40m{docs.cwd}\n\033[0mInput Parameters=> ')
                if cv=='b':break
                cv=cv.split()
                if cv[2]=='w':
                    cs="\033[1;34;40m{} => {}"
                    if cv[1]=='t':self.get_menu(cs.format('Wei', self.web3.to_wei(float(cv[0]), 'ether')))
                    elif cv[1]=='f':self.get_menu(cs.format('Eth', self.web3.to_wei(float(cv[0]), 'ether')))
                elif str(cv[2]).isdigit():
                    if cv[1]=='t':val=float(cv[0])*10**int(cv[2])
                    else:val=float(cv[0])/10**int(cv[2])
                    self.get_menu(f"\033[1;34;40mValue => {val}")
            except:pass
    
    def remote_abi(self, a: str, n: str='mainnet'):
        """
        Returns ABI Of Verified Contract Address Using Etherscan API.
        :param a: Verified Contract Address
        :param n: Network Verified Contract Address Is Deployed On e.g `goerli`
        """
        abi=''
        try:
            cn=''
            ed={'User-Agent': 'Mozilla/5.0', 'Host':'api.etherscan.io'}
            hd={'User-Agent': 'Mozilla/5.0', 'Host':f'api-{n}.etherscan.io'}
            md={'User-Agent': 'Mozilla/5.0', 'Host':'api-testnet.polygonscan.com'}
            pd={'User-Agent': 'Mozilla/5.0', 'Host':'api.polygonscan.com'}
            if n=='mainnet':
                cn=requests.get(f'https://api.etherscan.io/api?module=contract&action=getabi&address={a}', headers=ed).text
            elif n=='mumbai':
                cn=requests.get(f'https://api-testnet.polygonscan.com/api?module=contract&action=getabi&address={a}', headers=md).text
            elif n=='polygon':
                cn=requests.get(f'https://api.polygonscan.com/api?module=contract&action=getabi&address={a}', headers=pd).text
            elif n!='ganache':
                cn=requests.get(f'https://api-{n}.etherscan.io/api?module=contract&action=getabi&address={a}', headers=hd).text
            abi=json.loads(cn)['result']
        except requests.exceptions.ConnectionError:
            print(f'\033[1;31;40mNo Connection Error!!\033[0m')
        return abi
    
    def local_abi(self):
        """Loads Prompt To Return ABI Of Locally Stored Contract."""
        abi=''
        cnt=input('\nInput Contract Name Or Pass=> ')
        if cnt:
            ci=json.loads(self._fread(Path(self.dcfg.scdir).joinpath('build','contracts',f'{cnt}.json')))
            abi=ci['abi']
        return abi
    
    def token_id(self):
        """Loads Menu To Search For Token Id Using CoinGecko API."""
        while True:
            try:
                st=self.func_menu(docs.st, 'String')
                if not st:break
                sd=self.cg.search(st)['coins']
                print('')
                for i in range(len(sd)):
                    print("Id: {},  Name: {},  Symbol: {}".format(sd[i]['id'], sd[i]['name'], sd[i]['api_symbol']))
                input('\n\n\033[1;32;40m...Hit Enter|Return Key To Continue....\033[0m\n') or None
            except:pass
    
    def eth_wallet(self):
        """Returns Tuple Containing Eth Account Object & Mnemonic String For Newly Created Account."""
        return self.web3.eth.account.create_with_mnemonic()
    
    def token_swap(self):
        """Loads Menu To Swap Tokens On Blockchain Of Choice."""
        while True:
            try:
                acc, pk=self.account_auth()
                if acc=='b':break
                td={'1': '','2': 'goerli.',
                    '3': 'polygon.','4': 'mumbai.',
                    '5': 'bsc.','6': 'optimism.',
                    '7': 'fantom.','8': 'celo.',
                    '9': 'avalanche.','10': 'arbitrum.',
                    '11': 'base.'
                    }
                self.clear_screen()
                chain=input(f'\n\033[1;32;40m{docs.tsn}\033[0m\nInput Number=> ') or '1'
                self.clear_screen()
                ld={
                    '1  ->  BuyToken        [e.g DAI Or Token Smart Contract Address]':'',
                    '2  ->  Slippage        [e.g 0.01 = 1% slippage]':'0.01',
                    '3  ->  SellToken       [e.g ETH Or Token Smart Contract Address]':'ETH',
                    '4  ->  SellAmount      [e.g Sell Specified Amount Of Sell Token]':'',
                    '5  ->  BuyAmount       [e.g Buy Specified Amount Of Buy Token]':'',
                    '6  ->  TakerAddress    [e.g Address]':acc.address
                   }
                kd={f'{k.split()[0]} ':k for k in ld.keys()}
                hd=self.function_dict(ld,kd,docs.tsa,st='s',zx=td[chain][:-1])
                bt=[x for x in (v for k,v in hd.items())]
                dt=[d for d in bt if d]
                bs='Buy'
                if bt[3]:bs='Sell'
                ff=self.web3.to_checksum_address(dt[4])
                api=self.js_resp(self.sw.format(td[str(chain)],dt[0],dt[2],bs.lower(),dt[3],dt[1],ff), h=self.dcfg.zerox).json()
                ps=dict(api)
                del(ps['data'])
                del(ps['sources'])
                apr=input(f'\n\033[1;34;40m{json.dumps(ps, indent=4)}{self.at}') or 'n'
                if apr.lower()=='y':
                    self.token_approve(api['sellTokenAddress'],acc.address,pk,api['sellAmount'],n=str(td[chain])[:-1])
                    nonce=self.web3.eth.get_transaction_count(acc.address)
                    tx={
                        'nonce': nonce,
                        'from':acc.address,
                        'to': self.web3.to_checksum_address(api['to']),
                        'data': api['data'],
                        'value': int(api['value']),
                        'gas': int(api['gas']),
                        'gasPrice': int(api['gasPrice']),
                        'chainId': api['chainId']
                        }
                    self.sign_tx(tx,pk)
            except requests.exceptions.ConnectionError:
                self.get_menu(f'\033[1;31;40mConnection Error!!')
            except Exception as e:self.get_menu(f'\033[1;31;40m{e}')
    
    def token_approve(self, t: str, o: str, k: str, a: str, n: str='mainnet'):
        """
        Creates & Signs Swap Approval Transaction.
        :param t: Token Contract Address
        :param o: Owner Address Containing Token To Swap
        :param k: Private Key Of Owner Address
        :param a: Amount Of Token To Be Swapped
        :param n: Network To Make Swap On Defaults To Ethereum Mainnet e.g `polygon | mainnet`
        """
        da=self.dcfg.exp[n]
        contract=self.web3.eth.contract(address=self.web3.to_checksum_address(t), abi=self.dcfg.abi)
        spender=self.web3.to_checksum_address(da)
        tx=contract.functions.approve(spender, int(a)).build_transaction({
            'from': o,
            'nonce': self.web3.eth.get_transaction_count(o),
        })
        self.sign_tx(tx,k,hs='Transaction Approved')
    
    def contract_data(self, fnc: str, abi: list):
        """
        Returns Contract Function Parameters As Dictionary & Function Type As String.
        :param fnc: Name Of Contract Function e.g `balanceOf`
        :param abi: ABI Of Contract Type List
        """
        doc=f" [*]{fnc}() FUNCTION PARAMETERS:"
        ld={}
        hd={}
        ex=''
        for i in range(len(abi)):
            if abi[i].get('type')=='function' and abi[i].get('name')==fnc:
                ex=abi[i]['stateMutability']
                lst=abi[i]['inputs']
                for n in range(len(lst)):
                    la=f'{n+1} -> {lst[n]["type"]} ({lst[n]["name"]})'
                    ld[la]=''
                    hd[f'{n+1} ']=la
        ld=self.function_dict(ld,hd,doc)
        return ld,ex
    
    def function_dict(self, ld: dict, hd: dict, sd: str, st: str=None, zx: str=None) -> dict:
        """
        Loads Menu To Set & Return Function Arguments & Values As Dictionary.
        :param ld: Arguments Dictionary
        :param hd: Arguments Key Dictionary
        :param sd: Banner String
        :param st: String To Specify Swap Token Menu Banner Defaults To None
        :param zx: 0x Swap Network As String Defaults To None e.g `celo`
        """
        od=dict(ld)
        while True:
            try:
                fs='Function'
                self.clear_screen()
                if st:
                    fs='Swap'
                    doc=docs.fdi+docs.fdt+self.ns.format(self.nw,self.nw_status())+f'\nSwap Network: {zx}'
                else:doc=docs.fdi+self.ns.format(self.nw,self.nw_status())
                bs=f'\n\033[1;32;40m{sd}\n{doc}\n\033[1;34;40m{fs} Parameters: {json.dumps(ld, indent=2)}'
                lda=input(f'{bs}\n\n\033[0mInput Choice=> ')
                if lda=='b':break
                elif lda=='e':self.pexit()
                elif lda=='n':self.block_network()
                elif lda=='c':self.convert_value()
                elif lda=='d':ld.update(od)
                elif len(lda)>1:
                    if lda[0]=='t' and st:
                        s=lda[2:]
                        tca=self.tkn_address(s, n=zx)
                        if not tca:
                            self.get_menu(f'\033[1;31;40m*{s} Not Found In Dapp_Config*')
                            continue
                        c,v,t,n,d=self.contract_info(tca)
                        self.get_menu(f'\033[1;34;40mAddress: {tca}\nName: {n}\nSymbol: {t}\nDecimals: {d}\nNetwork: {self.nw}')
                    elif hd.get(lda[:2]):
                        k,v=lda[:2],lda[2:]
                        ld[hd[k]]=v
            except:self.get_menu('e')
        return ld
    
    def contract_verify(self, s: str):
        """
        Verify Contract On Blockchain.
        :param s: String With Contract Name & Contract Address e.g `FeeCollector 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`
        """
        cn,adr=s.split()
        if adr and cn:
            cna=f'{cn}@{adr}'
            call(['truffle', 'run', 'verify', cna, '--network', self.nw], cwd=self.dcfg.scdir)
            self.get_menu(c=False)
    
    def transfer_eth(self, d: str, a: str, n: str) -> dict:
        """
        Returns Unsigned Transaction Dictionary For Transferral Of Ethereum.
        :param d: Deposit Address
        :param a: Exact Amount To Transfer (Converted To Wei/Decimal)
        :param n: Nonce (Amount Of Transactions Made By Address)
        """
        gas=self.web3.eth.estimate_gas({'to': d, 'value': a})
        tx={
            'nonce': n,
            'to': d,
            'value': a,
            'gas': gas,
            'gasPrice': self.web3.eth.gas_price
           }
        return tx
    
    def transfer_tkn(self, c, d: str, a: str, n: str) -> dict:
        """
        Returns Unsigned Transaction Dictionary For Transferral Of Contract Address Token.
        :param c: Eth Contract Object To Execute Token Smart Contract Functions
        :param d: Deposit Address
        :param a: Exact Amount To Transfer (Converted To Wei/Decimal)
        :param n: Nonce (Amount Of Transactions Made By Address)
        """
        gas=c.functions.transfer(d, a).estimate_gas()
        tx=c.functions.transfer(d, a).build_transaction({
            'nonce': n,
            'gas': gas,
            'gasPrice': self.web3.eth.gas_price
            })
        return tx
    
    def main(self):
        """Loads Wuddz_Dapp Main Menu."""
        while True:
            try:
                self.clear_screen()
                self.slow_print(__doc__)
                etht=input("\033[0m\nInput Choice=> ")
                if etht=='e':break
                elif etht=='d':self.func_menu(docs.ds, 'String', f='decode_bsf')
                elif etht=='p':self.crypto_price()
                elif etht=='n':self.block_network()
                elif etht=='x':
                    import exchange_api as _eapi
                    _eapi.Exchange().main()
                elif etht=='1':self.account_create()
                elif etht=='2':self.func_menu(docs.gb, 'Balance Format', n='n', f='bal_main')
                elif etht=='3':self.account_deposit()
                elif etht=='4':self.bal_fkey()
                elif etht=='5':self.func_menu(docs.ts, 'Hash', n='n', f='trx_hash')
                elif etht=='6':self.func_menu(docs.cnf, 'Contract Name', n='n', f='contract_deploy')
                elif etht=='7':self.func_menu(docs.sca, 'Contract Address', n='n', f='contract_rw')
                elif etht=='8':self.func_menu(docs.cnv, 'Verify Format', n='n', f='contract_verify')
                elif etht=='9':self.token_swap()
            except KeyboardInterrupt:break
        self.clear_screen()

def cli_main():
    """Wuddz_Dapp Entry Point Launches Wuddz_Dapp Main Menu."""
    Dapp().main()
