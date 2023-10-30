from typing import TYPE_CHECKING

from bubble_aide.abc.module import PrecompileContract
from bubble_aide.utils.wrapper import contract_transaction

if TYPE_CHECKING:
    from bubble_aide import Aide


class TempPrikey(PrecompileContract):

    def __init__(self, aide: "Aide"):
        super().__init__(aide)
        self.address = self.aide.web3.subChain.temp_trivate_key.ADDRESS

    @contract_transaction()
    def bind_temp_prikey(self,
                         game_contract_address,
                         temp_address,
                         period,
                         private_key=None,
                         txn=None,
                         ):
        return self.aide.web3.subChain.temp_trivate_key.bind_temp_pri_key(game_contract_address,
                                                                          temp_address,
                                                                          period)

    @contract_transaction()
    def behalf_signature(self,
                         game_contract_address,
                         work_address,
                         period,
                         *args,
                         # private_key=None,
                         txn=None,
                         ):
        return self.aide.web3.subChain.temp_trivate_key.behalf_signature(game_contract_address,
                                                                         work_address,
                                                                         period,
                                                                         *args
                                                                         )

    @contract_transaction()
    def invalidate_temp_prikey(self,
                               game_contract_address,
                               temp_address,
                               private_key=None,
                               txn=None,
                               ):
        return self.aide.web3.subChain.temp_trivate_key.invalidate_temp_private_key(
            game_contract_address,
            temp_address)

    @contract_transaction()
    def add_line_of_credit(self,
                           game_contract_address,
                           work_address,
                           add_value,
                           private_key=None,
                           txn=None,
                           ):
        return self.aide.web3.subChain.temp_trivate_key.add_line_of_credit(game_contract_address,
                                                                           work_address,
                                                                           add_value)
