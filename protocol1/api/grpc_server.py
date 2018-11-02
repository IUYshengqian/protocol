# import sys
# sys.path.insert(0, '/home/liheng/Desktop/protocol')
from core import Contract_pb2
import grpc
import api_pb2_grpc
import Tron_pb2
import api_pb2
from pprint import pprint


class GrpcServer:
    """
    grpc:通过protocbuf协议生成grpc.py文件,调用对应的功能接口
    """

    # def __init__(self, config):
    #     self.config = config

    def generateaddress(self):
        """
        生成充币钱包地址和私钥
        :return: private key, address
        """
        empty = api_pb2.EmptyMessage()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.WalletStub(channel)
            response = stub.GenerateAddress(empty)
            # print('--------address%s' % response.address)
            # print(f'private key {response.privateKey}')
        return response

    def getaccount(self, account_address):
        """
        查询账号信息  account.address: b'TLCjmH6SqGK8twZ9XrBDWpBbfyvEXihhNS'
        :return:
        """
        # NOTE(gRPC Python Team): .close() is possible on a channel and should be
        # used in circumstances in which the with statement does not fit the needs
        # of the code.
        account = Tron_pb2.Account()
        account.address = account_address
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.WalletStub(channel)
            response = stub.GetAccount(account)
        return response

    def createtransaction(self, owner_address, to_address, amount):
        """
        创建一个转账的交易
        :return: 返回转账合约对象
        {
        "transaction" :
            {"txID":"454f156bf1256587ff6ccdbc56e64ad0c51e4f8efea5490dcbc720ee606bc7b8",
            "raw_data":
                {"contract":
                    [{"parameter":
                        {"value":
                            {"amount":1,
                             "owner_address":"41235d90e1d0a0ccfa268781f464e0252ba6112993",
                             "to_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292"
                            },
                            "type_url":"type.googleapis.com/protocol.TransferContract"
                        },
                        "type":"TransferContract"
                    }],
                    "ref_block_bytes":"267e",
                    "ref_block_hash":"9a447d222e8de9f2",
                    "expiration":1530893064000,
                    "timestamp":1530893006233
                }
            }
            ,"privateKey": "your private key"
        }
        """
        transfer = Contract_pb2.TransferContract()
        transfer.owner_address = owner_address.encode()
        transfer.to_address = to_address.encode()
        transfer.amount = amount
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.WalletStub(channel)
            response = stub.CreateTransaction2(transfer)
        return response

    def gettransactionsign(self, private_key):
        """
        对交易签名
        :return:
        """
        transsign = Tron_pb2.TransactionSign()
        transsign.privateKey = private_key
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.WalletStub(channel)
            response = stub.GetTransactionSign2(transsign)
        return response

    def broadcasttransaction(self, contract):
        """
        对签名后的transaction进行广播
        :return: 是否广播成功
        response_code {
                        SUCCESS = 0;
                        SIGERROR = 1; // error in signature
                        CONTRACT_VALIDATE_ERROR = 2;
                        CONTRACT_EXE_ERROR = 3;
                        BANDWITH_ERROR = 4;
                        DUP_TRANSACTION_ERROR = 5;
                        TAPOS_ERROR = 6;
                        TOO_BIG_TRANSACTION_ERROR = 7;
                        TRANSACTION_EXPIRATION_ERROR = 8;
                        SERVER_BUSY = 9;
                        OTHER_ERROR = 20;
                      }
        """
        transaction = Tron_pb2.Transaction()
        transaction.Contract = contract
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.WalletStub(channel)
            response = stub.BroadcastTransaction(transaction)
        return response

    def createaccount(self, from_address, account_address, ac_type):
        """
        创建账户
        :return: account 对象
        """
        accontract = Contract_pb2.AccountCreateContract()
        accontract.owner_address = from_address.encode()
        accontract.account_address = account_address.encode()
        accontract.tpye = Tron_pb2.AccountType()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.WalletStub(channel)
            response = stub.CreateAccount2(accontract)
        return response

    def getaccountinfo(self, account_address):
        """
        查询账号信息  account.address: b'TLCjmH6SqGK8twZ9XrBDWpBbfyvEXihhNS'
        :return: 返回一个包含Account信息的对象
        """

        account = Tron_pb2.Account()
        account.address = account_address.encode()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.WalletStub(channel)
            response = stub.GetAccount(account)
            print(type(response))
        return response


grpc1 = GrpcServer()
address = grpc1.generateaddress()
pprint(address)
rv = grpc1.getaccountinfo('TDCCjrC66CqCKvz55FUNa4r8x7xjrnopbv')
print(rv, '****************')
print('>>>>>>')

# rv = grpc1.createaccount('TDCCjrC66CqCKvz55FUNa4r8x7xjrnopbv', 'TGkX2DzfYNG11aV2Z3MC65Gvuexig11ctj', None)
# rv = grpc1.createtransaction('TGkX2DzfYNG11aV2Z3MC65Gvuexig11ctj', 'TTt6dZJjmk2gjCK5h739Pxjuq6gPMv7zjR', 1)
pprint(rv)
