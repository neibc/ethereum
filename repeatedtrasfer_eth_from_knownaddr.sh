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
#/work/geth/geth --datadir "/work/gethdata" attach >> /work/geth/autotrans_result.log 2> /work/geth/autotrans_result_err.log << EOF
nohup /work/geth/geth --datadir "/work/gethdata" attach >> /work/geth/autotrans_result.log 2> /work/geth/autotrans_result_err.log << EOF

var toacc = "YOURTARGETACCADDR";
console.log("toacc: " + toacc);
var tgasprice = new BigNumber(web3.toWei('500', 'gwei'));
var gasprice = tgasprice;
var maxgasprice = new BigNumber(web3.toWei('4000', 'gwei'));
console.log("gas price: " + gasprice);
var gaslimit = 21000;
var cost = gasprice.mul(gaslimit);
console.log("cost price: " + cost);
var deposit = 0;
var transferval = 0;
var oldprice = 1;

while(true) {
	eth.accounts.forEach(function(e,i){

		if(i>0) {
			deposit = eth.getBalance(eth.accounts[i]);

			gasprice = tgasprice;
			cost = gasprice.mul(gaslimit);
			transferval = 0;

			if(deposit.sub(maxgasprice.mul(gaslimit)) > 0) {
				console.log("*max price enabled:"+deposit);
				gasprice = maxgasprice;
				console.log("*normal cost      :"+cost);
				cost = maxgasprice.mul(gaslimit);
				console.log("*max cost         :"+cost);
				transferval = eth.getBalance(eth.accounts[i]).sub(cost);
			} else if(deposit.sub(1000000000000) > 0) {
				gasprice = deposit.dividedToIntegerBy(31533);
				console.log("gasprice:"+deposit);
				cost = gasprice.mul(21000)
				console.log("cost    :"+cost);
				transferval = eth.getBalance(eth.accounts[i]).sub(cost);
			}

			
			if(transferval > 0 && oldprice != transferval) {
				console.log("runtransfer!!:");
				console.log("num:"+i);
				console.log("fromaddr:"+eth.accounts[i]);
				console.log("toaddr:"+toacc);
				console.log("deposit:"+deposit);
				console.log("transferval:"+transferval);
				console.log("Unlock account");
				personal.unlockAccount(eth.accounts[i],"YOURPASSWORD");
				console.log("transfer result");
				eth.sendTransaction({from: eth.accounts[i], to: toacc, value: transferval,gas: gaslimit, gasPrice:gasprice});
				console.log("after sendtransaction");
				oldprice = transferval;
			}
		}

	});
}
EOF

fi
