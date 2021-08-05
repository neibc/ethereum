#!/bin/bash

# check the balances of all registered accounts on geth
# 2021.08.05 by neibc

/work/geth/geth --datadir "/work/gethdata" attach << EOF

eth.accounts.forEach(function(e,i){console.log("eth.accounts["+i+"]: " + eth.accounts[i] + "\tbalance:" + web3.fromWei(eth.getBalance(eth.accounts[i]),"ether") + " Ether"
)})
EOF
