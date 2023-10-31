"""WUDDZ-DAPP DOCS MODULE CONTAINING ALL MENU BANNERS AS VARIABLES"""

aa=""" [*]ACCOUNT AUTHENTICATION:                                                                                                     
                                                                                                                                
    Formats:
    Mnemonic     =   12-24 Word Mnemonic String
    Private Key  =   64 Character Length Hexadecimal String, Prefixed With `0x` Or Without
    Password     =   Base64 Encoded Password To Decrypt Account Data In `key-file.txt`
					 
    Mnemonic     =>  [e.g "reveal close arrive behave chaos author mother spread provide human fall possible"]
    Private Key  =>  [e.g 0x5cf948ea8ede930971f938023a08a8ac2fc984035ffac89a8e9c33c657b24e33]
    Password     =>  [e.g UElGeXBNYVBpY0R1bWhDbFhlb2Q3OFFNTUkweHZoQ2o=]
    n            =>  Choose Network
    b            =>  Back To Previous Screen
    e            =>  Exit Program
    """

tsn=""" [*]SPECIFY BLOCKCHAIN TO GET QUOTE FOR TOKEN SWAP/PURCHASE:                  
                                                                             
    1. Ethereum (Mainnet)                    6. Optimism (Optimism Mainnet)  
    2. Goerli (Ethereum Testnet)             7. Fantom (Fantom Mainnet)      
    3. Polygon (Polygon Mainnet)             8. Celo (Celo Mainnet)          
    4. Mumbai (Polygon Testnet)              9. Avalanche (Avalanche Mainnet)
    5. Binance Smart Chain (BNB Mainnet)    10. Arbitrum (Arbitrum Mainnet)  
   11. Base (Base Mainnet)
                                                                             
    Number    =>    [e.g 5 = Binance Smart Chain Default Is 1 = Ethereum]    
    """

cnf=""" [*]NAME OF CONTRACT TO COMPILE & DEPLOY:

    Name  =>  Name Of Contract [e.g  FeeCollector]
    n     =>  Choose Network
    b     =>  Back To Previous Screen
    e     =>  Exit Program
    """

tsa=""" [*]SPECIFY TOKEN SWAP/PURCHASE PARAMETERS:                       
                                                                 
    Address  =>  [e.g 0xdac17f958d2ee523a2206206994597c13d831ec7]
    Amount   =>  [e.g 1000000000000000000]"""

nwl=""" [*]CHOOSE BLOCKCHAIN NETWORK:                                                               
                                                                                             
     1    =>    Mainnet          [Ethereum Blockchain]                                       
     2    =>    Sepolia          [Ethereum Test Network]                                     
     3    =>    Goerli           [Ethereum Test Network]                                     
     4    =>    Linea            [Linea Mainnet]                                     
     5    =>    Celo             [Celo Mainnet]                                     
     6    =>    Starknet         [Starknet Mainnet]
     7    =>    Aurora           [Aurora Mainnet]
     8    =>    Near             [Near Mainnet]
     9    =>    Avalanche        [Avalanche Mainnet]
    10    =>    Palm             [Palm Mainnet]
    11    =>    Arbitrum         [Arbitrum Mainnet]
    12    =>    Optimism         [Optimism Mainnet]
    13    =>    Polygon          [Polygon Mainnet]
    14    =>    Mumbai           [Polygon Test Network]
    15    =>    BSC              [Binance Smart Chain (Mainnet)]
    16    =>    BSCTestnet       [Binance Smart Chain (Test Network)]
     g    =>    Ganache          [Truffle Local System Based Test Network e.g 127.0.0.1:7545]
     d    =>    Development      [Truffle Local System Based Test Network e.g 127.0.0.1:8545]
     b    =>    Back To Previous Screen                                                           
     e    =>    Exit Program     
    """

cwd=""" [*]CONVERT TO/FROM WEI OR SPECIFIED DECIMAL VALUE:             
                                                                
    2000000000 f w     =>    Convert 2000000000 From Wei        
    2000000000 f 12    =>    Convert 2000000000 From 12 Decimals
    2 t w              =>    Convert 2 To Wei                   
    2 t 12             =>    Convert 2 To 12 Decimals           
    b                  =>    Back To Previous Screen
    """    

sca=""" [*]SMART CONTRACT ADDRESS:

    adr  =>  Smart Contract Address To Interact With [e.g 0xdac17f958d2ee523a2206206994597c13d831ec7]
    n    =>  Choose Network
    b    =>  Back To Previous Screen
    e    =>  Exit Program
    """

cnv=""" [*]VERIFY SMART CONTRACT NAME & ADDRESS ON CURRENT NETWORK BLOCKCHAIN:
    
    Format:
    cn ca   =   String With Contract Name & Contract Address To Be Verified
    
    Format  =>  [e.g FeeCollector 0xdac17f958d2ee523a2206206994597c13d831ec7]
    n       =>  Choose Network
    b       =>  Back To Previous Screen
    e       =>  Exit Program
    """

crw=""" [*]INTERACT, EXECUTE & PRINT SMART CONTRACT FUNCTIONS:
    
    Function    =>    [e.g balanceOf]                               
    b           =>    Back To Menu                                  
    c           =>    Convert To/From Wei Or Specified Decimal Value
    """

der=""" [*]TRANSFER/DEPOSIT ERC-20 TOKENS:
    
    Format:
    Deposit Amount Token = Transfer Specified Amount Of Token To Deposit Address
    
    Examples:
    0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1 100 0xdac17f958d2ee523a2206206994597c13d831ec7
    [Transfer 100 USDT To 0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1]
    
    0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1 100 BNB
    [Transfer 100 BNB To 0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1]
    
    Deposit   =>  Deposit Address To Transfer Token To [e.g 0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1]
    Amount    =>  Amount Of Specified Currency To Transfer [e.g 0.012 | 100]
    Token     =>  Token Symbol Or Token Contract Address [e.g `BNB | 0xdac17f958d2ee523a2206206994597c13d831ec7`]
    n         =>  Choose Network
    b         =>  Back To Previous Screen
    e         =>  Exit Program
    """

fdi="""
    Formats:  
    1 value  =   Set Value For Argument '1' In Dictionary
    2 value  =   Set Value For Argument '2' In Dictionary

    value    =>  [e.g 1 0xdac17f958d2ee523a2206206994597c13d831ec7]
    b        =>  Return Current Dictionary
    c        =>  Convert To/From Wei Or Specified Decimal Value
    d        =>  Delete/Clear Dictionary Values Back To Default Values
    n        =>  Choose Network                                       
    e        =>  Exit Program                                         
"""

fdt="""    t value  =>  Print Token Info To Screen [e.g `t BNB`]
"""

ds=""" [*]DECODE BASE64 STRING:
    
    string    =>    Base64 String Output Is UTF-8 Decoded String
    b         =>    Back To Previous Screen
    e         =>    Exit Program
    """

gb=""" [*]GET ACCOUNT BALANCE(S):
    
    Formats:  
    (address)           ->  Gets All Available Balances For This Address
    (address contract)  ->  Gets Available Balance Of Contract Address Token For Address
    (address symbol)    ->  Gets Available Balance Of Symbol Token For Address
    
    Symbol    =>    [e.g USDT]
    Contract  =>    [e.g 0xbF4d5309Bc633d95B6a8fe60E6AF490F11ed2Dd1]
    Address   =>    [e.g vitalik.eth | 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045]
    n         =>    Choose Network
    b         =>    Back To Previous Screen
    e         =>    Exit Program
    """

cp=""" [*]CRYPTO PRICE & CONVERSION:                                   
                                                                 
    Amount    =  1.2 | 5 | 1004                                  
    TokenName =  Ethereum | bitcoin | binancecoin                
                                                                 
    Formats:                                                     
    Amount TokenName                                             
    Amount From(TokenName) To(TokenName)                         
                                                                 
    Examples:                                                    
    1.2 ethereum               Price Of 1.2 Ethereum In USD
    100 binancecoin bitcoin    Bitcoin Value Of 100 BNB    
                                                                 
    Format  =>  To Get Required Price/Value                
    s       =>  Search For Id Of Token                     
    b       =>  Back To Previous Screen
    e       =>  Exit Program
    """

st=""" [*]SEARCH FOR TOKEN & COPY TOKENID TO USE FOR PRICE & CONVERSION:                                                            
                                                                                                                              
    String = Name Of Token (Outputs List Matching String => "Id: TokenId,  Name: TokenName, Symbol: TokenSymbol" On Each Line)
                                                                                                                              
    String  =>  [e.g bitcoin Outputs List Matching "bitcoin" => "Id: bitcoin  Name: bitcoin Symbol: BTC "]              
    b       =>  Back To Previous Screen
    e       =>  Exit Program
    """

ts=""" [*]GET TRANSACTION HASH INFO:
        
    hash   =>   Print Transaction Hash Info
    n      =>   Choose Network
    b      =>   Back To Previous Screen
    e      =>   Exit Program
    """

exa=""" [*]{} EXCHANGE REQUIRED API AUTHENTICATION:
    
    apiKey      =>    [e.g 6dek4of7vge2z8uvxwt0qkty]            
    secret      =>    [e.g itigz23v-aezj-kua4-iasq-mxhe5o6cvdpt]
    password    =>    [e.g VTigz23vaezJKuA4IAsQmxHe5O6CvdPT]    
    """

exs=""" [*]SPECIFY EXCHANGE TO AUTHENTICATE TO:                                                
    
    Formats:
    Exchange          Authenticate To Specified Exchange
    Exchange t        Authenticate To Specified Exchange Testnet
    
    Exchange    =>    [e.g  bybit | Binance | bybit t]
    b           =>    Back To Previous Screen
    e           =>    Exit Program
    """

exov=""" [*]SPECIFY ORDER PARAMETERS:
    
    Formats:
    1 Amount     =  Specify Amount  [e.g 1 0.5 (0.5 Symbol Token Currency) | 1 10 (10 Contracts i.e $10)]
    {}
    x    =>    Execute Current Parameters
    p    =>    Fetch Current Trading/Market Info Of Symbol
    s    =>    Set Symbol
    d    =>    Clear/Delete Parameters
    b    =>    Back To Previous Screen
    e    =>    Exit Program"""

exos="""2 Price      =  Specify Price  [e.g 2 55000 | 2 61905.5 | Leave Empty To Set As Last Traded Price]
    """
    
exns="""3 StopPrice  =  Specify Stop Price  [e.g 3 33304 | 3 44500]
    4 Side       =  Specify Order Side  [e.g 4 sell | 4 buy]
    5 Type       =  Specify Order Type  [e.g 5 limit | 5 market]
    """

exws="""2 Address    =  Specify Withdraw Address  [e.g 0xdac17f958d2ee523a2206206994597c13d831ec7]
    3 Tag        =  Specify Withdraw Tag  [Optional e.g USDT]
    4 Chain      =  Specify Withdraw Chain  [Optional e.g ERC20 | BEP20]
    5 Memo       =  Specify Withdraw Memo  [Optional e.g v9d3r02m7qwqywtj5kpf83sf]
    """

exgs=""" [*]SEARCH FOR SYMBOL:
    
    Formats:  
    symbol    =  Search Available Symbols On Exchange For Symbol
    s symbol  =  Set Symbol
    
    symbol    =>    [e.g s BTC/USDT | eth/Usdt]
    b         =>    Back To Previous Screen
    e         =>    Exit Program
    """

slv=""" [*]SET LEVERAGE:

    leverage  =>  Set Leverage [e.g 10 | 25 ]
    b         =>  Back To Previous Screen
    e         =>  Exit Program
    """
