# steem witness failover script

Single use automatic failover for steem witness nodes with a Twilio SMS notification

### Use this at your own risk. This code is currently what I am using to maintain failover from witness node to witness node, but it requires knowledge of it's configuration and setup. I make no promises to provide assistance or updates to this code.

Requirements:

- Docker
- Your WIF Active Key
- Twilio Account (or disable that code yourself)

To get started, there are two steps

```
cp .env.example .env
```

Then edit the values in the `.env` file to the appropriate values for your account.

- **steem_account**: The account name of the witness
- **steem_node**: The steem public node used to broadcast the transaction
- **steem_wif**: The WIF active PRIVATE key of the account
- **steem_backup**: The WIF signing PUBLIC key of the backup server
- **steem_account_creation_fee**: (Preferred Witness Setting)
- **steem_maximum_block_size**: (Preferred Witness Setting)
- **steem_sbd_interest_rate**: (Preferred Witness Setting)
- **steem_witness_url**: (Preferred Witness Setting)
- **check_rate**: The number of seconds between checks.

The most confusing setting is likely:

- **threshold**: When the specified account reaches this value as `total_missed`, the update will execute and change the witness account's signing key to the key specified as `steem_backup`.

Once these environmental variables are configured, you can build and start the script with:

```
docker-compose build && docker-compose up
```

You will begin to see messages in your terminal similar to:

```
failover_1  | 'Missed = 6 | Failover if >= 8 | Next Key: SYOURNEXTPUBLICKEY'
failover_1  | 'Missed = 6 | Failover if >= 8 | Next Key: SYOURNEXTPUBLICKEY'
failover_1  | 'Missed = 6 | Failover if >= 8 | Next Key: SYOURNEXTPUBLICKEY'
```

That means it's working properly, and will trigger once the failover amount is reached.