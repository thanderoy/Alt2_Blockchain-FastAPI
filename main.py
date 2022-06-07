import fastapi
import Alt2.blockchain as _blockchain

blockchain = _blockchain.Blockchain()
app = fastapi.FastAPI()

# endpoint to mine a block
@app.post("/mine_block/")
def mine_block(data:str):
    if not blockchain.is_chain_valid():
        return fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid"
        )
    block = blockchain.mine_block(data=data)

    return block
        

# endpoint to return entire blockv=chain
@app.get("/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return fastapi.HTTPException(
            status_code=400, detail="The blockchain is invalid"
        )
    
    chain =  blockchain.chain
    return chain
