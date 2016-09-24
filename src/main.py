import os
import sys
import time
from piston.steem import Steem
from pprint import pprint
from steemtools.experimental import Transactions
from twilio.rest import TwilioRestClient

# Steem connection and witness information
node    = os.environ['steem_node']
witness = os.environ['steem_account']
wif     = os.environ['steem_wif']

# Establish the connection to steem
steem = Steem(node=node, keys=[wif])

# How many misses before we trigger the update, 0 for debugging (always trigger)
threshold = int(os.environ['threshold'])

# How often should we check for misses? (in seconds)
check_rate = int(os.environ['check_rate'])

# The signing key to swap to when the threshold is met
backup_key = os.environ['steem_backup']

# Properties to set on the witness update
props = {
    "account_creation_fee": os.environ['steem_account_creation_fee'],
    "maximum_block_size": int(os.environ['steem_maximum_block_size']),
    "sbd_interest_rate": int(os.environ['steem_sbd_interest_rate']),
}
witness_url = os.environ['steem_witness_url']

# SMS via Twilio (Paid Service)
twilio_account_sid = os.environ['twilio_account_sid']
twilio_auth_token  = os.environ['twilio_account_token']
twilio_client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
twilio_send_to = os.environ['twilio_send_to']
twilio_send_from = os.environ['twilio_send_from']
twilio_send_message = "steemd failover triggered"

# Check how many blocks a witness has missed
def check_witness():
    status = steem.rpc.get_witness_by_account(witness)
    missed = status['total_missed']
    pprint("Missed = " + str(missed) + " | Failover if >= " + str(threshold) + " | Next Key: " + backup_key)
    if missed >= threshold:
        update_witness(witness, witness_url, backup_key, props)

# Update the witness to the new signing key
def update_witness(account, url, signing_key, props):
    # Create the witness_update transaction and broadcast
    t = Transactions(steem=steem)
    tx = t.witness_update(witness, backup_key, witness_url, props, wif, sim_mode=False)
    # Send SMS Notification of Failure
    twilio_client.messages.create(to=twilio_send_to, from_=twilio_send_from, body=twilio_send_message)
    # Kill the script
    raise SystemExit

# Main Loop
if __name__ == '__main__':
    while True:
        check_witness()
        sys.stdout.flush()
        time.sleep(check_rate)
