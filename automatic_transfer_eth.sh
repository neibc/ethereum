#! /bin/bash

# geth attach script while running geth with light mode
# 2021.08.05 by neibc

/work/geth/geth --datadir "/work/gethdata" attach << EOF

var fromacc = "0xYOURSOURCEADDR";
var toacc = "0xYOURTARGETADDR";

console.log("fromacc: " + fromacc);
console.log("toacc: " + toacc);
var gasprice = new BigNumber(web3.toWei('35', 'gwei'));
console.log("gas price: " + gasprice);
var gaslimit = 21000;
var cost = gasprice.mul(gaslimit);
console.log("cost price: " + cost);
var deposit = eth.getBalance(fromacc);
console.log("deposit: " + deposit);
var transferval = eth.getBalance(fromacc).sub(cost);
console.log("transferval: " + transferval);

console.log("Unlock account");
personal.unlockAccount(fromacc,"YOURPASSWORD");

if(transferval > 0) {
  console.log("transfer result");
  eth.sendTransaction({from: fromacc, to: toacc, value: transferval, gas: gaslimit, gasPrice: gasprice});
} else {
  console.log("no balance");
}

EOF
