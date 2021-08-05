#! /bin/bash

# crontab registration - run every 10 minutes this script
# 10,20,30,40,50 * * * * cd /work/geth;/bin/bash repeatedtrasfer_eth_from_knownaddr.sh
# 
# 2021.08.05 by neibc
#

# run this script only where there is no duplicated attach job
# because it tries to run sendTransaction continuously if there is no error(disconnection or something)
#

ps -ef | grep "[a]ttach" > /dev/null
if [ $? -eq 0 ]; then
echo "duplicated attach job exists"
else
#/work/geth/geth --datadir "/work/gethdata" attach >> /work/geth/joblog.txt 2> /work/geth/joblog_err.txt << EOF
nohup /work/geth/geth --datadir "/work/gethdata" attach >> /work/geth/joblog.txt 2> /work/geth/joblog_err.txt << EOF

var toacc = "0xTARGETADDRESS_FIXME";
console.log("toacc: " + toacc);
var gasprice = new BigNumber(web3.toWei('130', 'gwei'));
console.log("gas price: " + gasprice);
var gaslimit = 21000;
var cost = gasprice.mul(gaslimit);
console.log("cost price: " + cost);
var deposit = 0;
var transferval = 0;

while(true) {
        eth.accounts.forEach(function(e,i){

               deposit = eth.getBalance(eth.accounts[i]);
               transferval = eth.getBalance(eth.accounts[i]).sub(cost);

               if(transferval > 0) {
                      console.log("num:"+i);
                      console.log("addr:"+eth.accounts[i]);
                      console.log("balance:"+deposit);
                      console.log("transfer val:"+transferval);
                      console.log("Unlock account");
                      personal.unlockAccount(eth.accounts[i],"YOURPASSWORD_FIXME");
                      console.log("transfer result");
                      eth.sendTransaction({from: eth.accounts[i], to: toacc, value: transferval,gas: gaslimit, gasPrice:gasprice});
               }
        });
}
EOF

fi
