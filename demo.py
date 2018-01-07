from datetime import datetime
import hashlib as hasher
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

NameList = ['Jeong Won Kim', 'Gwang Yong Lee', 'Do Hyeon Kim',
            'Ji Yeon Lee', 'Taylor.E.Cho']

app = Flask(__name__)
api = Api(app)

OWNER = {
    'owner1': {'name': 'Jeong Won Kim'},
    'owner2': {'name': 'Gwang Yong Lee'},
    'owner3': {'name': 'Do Hyeon Kim'},
    'owner4': {'name': 'Ji Yeon Lee'},
    'owner5': {'name': 'Taylor.E.Cho'},
    }

def abort_if_owner_doesnt_exist(owner_id):
    if owner_id not in OWNER:
        abort(404, message="Owner {} doesn't exist".format(owner_id))

parser = reqparse.RequestParser()
parser.add_argument('name')

# Owner.
# The delete function wasn't made.
# Because the item's history must not be deleted.
class Owner(Resource):
    def get(self, owner_id):
        abort_if_owner_doesnt_exist(owner_id)
        return OWNER[owner_id]

    def put(self, owner_id):
        args = parser.parse_args()
        name = {'name': args['name']}
        OWNER[owner_id] = name

        # append next block
        global blockchain
        global prev_block
        temp_b = next_block(prev_block, data=args['name'])
        blockchain.append(temp_b)
        prev_block = temp_b
        
        return name, 201
    
# OwnerList
# shows a list of all owners, and lets you POST to add new owners.
class OwnerList(Resource):
    def get(self):
        return OWNER
    def post(self):
        args = parser.parse_args()
        owner_id = int(max(OWNER.keys()).lstrip('owner')) +1
        owner_id = 'owner%i' %owner_id
        OWNER[owner_id] = {'name': args['name']}

        # append next block
        global blockchain
        global prev_block
        temp_b = next_block(prev_block, data=args['name'])
        blockchain.append(temp_b)
        prev_block = temp_b
        
        return OWNER[owner_id], 201

# Directory.
# Acually setup the Api resoure routing here
api.add_resource(OwnerList, '/owner')
api.add_resource(Owner, '/owner/<owner_id>')


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def __str__(self):
        return 'Block #{}'.format(self.index)

    def hash_block(self):
        sha = hasher.sha256()
        seq = (str(x) for x in (
            self.index, self.timestamp, self.data, self.previous_hash))
        sha.update(''.join(seq).encode('utf-8'))
        return sha.hexdigest()

def make_genesis_block():
    # Make the first block in a blockchain
    block = Block(index = 0,
                  timestamp = datetime.now(),
                  # The name of the graphic card must be added
                  # in this data field of the genesis block
                  data = "Geforce GTX 1080 TI",
                  previous_hash = "0")
    return block

def next_block(last_block, data = ''):
    # Return next block in a blockchain
    idx = last_block.index +1
    block = Block(index = idx,
                  timestamp = datetime.now(),
                  data = '{}{}'.format(data, idx),
                  previous_hash = last_block.hash)
    return block

# global variable.
blockchain = [make_genesis_block()]
prev_block = blockchain[0]

# ...
def setup():
    global blockchain
    global prev_block
    for i in range(len(NameList)):
        block = next_block(prev_block, data=NameList[i])
        blockchain.append(block)
        prev_block = block
        print('{} added to blockchain'.format(block))
        print('Hash: {}\n'.format(block.hash))


if __name__ == '__main__':
    setup()
    app.run(debug=True)










