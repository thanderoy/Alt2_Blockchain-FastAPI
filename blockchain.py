import datetime
import hashlib
import json

class Blockchain:

    def __init__(self) -> None:
        self.chain = list()
        genesis_block = self.create_block(
            data="Genesis Block", proof=1, previous_hash= "0", index=1
        )
        self.chain.append(genesis_block)

    def mine_block(self, data:str) -> dict:
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self.proof_of_work(
            previous_proof, index, data
        )
        previous_hash = self.hasher(block=previous_block)
        block = self.create_block(
            data=data, proof=proof, previous_hash=previous_hash, index=index
        )
        self.chain.append(block)
        return block

    def hasher(self, block: dict) -> str:
        '''
        Hash blocks and return cyptographic hash of the block
        '''
        encoded_block = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(encoded_block).hexdigest()

    
    def to_digest(self, new_proof: int, previous_proof: int, index: str, data: str) -> bytes:
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + data

        return to_digest.encode()

    def proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        new_proof = 1
        check_proof = False

        while not check_proof:

            to_digest = self.to_digest(
                new_proof=new_proof,
                previous_proof=previous_proof, 
                index=index, 
                data=data  
            )

            hash_value = hashlib.sha256(to_digest).hexdigest()

            if hash_value[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof

    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def create_block(self, data: str, proof: int, previous_hash: str, index: int) -> dict:
        block = {
        "index": index,
        "timestamp": str(datetime.datetime.now()),
        "data": data,
        "proof": proof,
        "previous_hash": previous_hash,
        }

        return block
    
    def is_chain_valid(self) -> bool:

        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]

            if block["previous_hash"] != self.hasher(previous_block):
                return False

            previous_proof = previous_block["proof"]
            index, data, proof = (
                block["index"],
                block["data"],
                block["proof"],
            )
            hash_value = hashlib.sha256(
                self.to_digest(
                    new_proof=proof,
                    previous_proof=previous_proof,
                    index=index,
                    data=data,
                )
            ).hexdigest()

            if hash_value[:4] != "0000":
                return False

            current_block = block
            block_index +=1

        return True


blockchain = Blockchain()

bc = blockchain.chain
blockchain.mine_block('hello world')
blockchain.mine_block('hello blockchain')


valid = blockchain.is_chain_valid()
print (valid)
# blockchain.chain[1]["data"] = "Sheesh"


for count, name in enumerate(bc, 1):
    print (f'[{count}] {name}')