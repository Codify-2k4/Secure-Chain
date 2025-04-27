import hashlib
import json
from time import time
from datetime import datetime, timezone, timedelta

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)

    def get_ist_time(self):
        return datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(self.get_ist_time()),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, action, doctor_id=None, patient_id=None, user_id=None, updated_fields=None):
        self.current_transactions.append({
            'doctor_id': doctor_id,
            'patient_id': patient_id,
            'user_id': user_id,
            'action': action,
            'timestamp': str(self.get_ist_time()),
            'updated_fields': updated_fields if action == 'patient_record_updated' else None
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"