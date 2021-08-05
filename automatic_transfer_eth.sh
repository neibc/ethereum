#!/bin/sh

# geth attach script while running geth with light mode
# 2021.08.05 by neibc

/work/geth/geth --datadir "/work/gethdata" attach << EOF

var fromacc = "0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf"
var toacc = "0xYOURADDR"

console.log("fromacc: " + fromacc);
console.log("toacc: " + toacc);
var gasPrice = new BigNumber(web3.toWei('35', 'gwei'))
console.log("gas price: " + gasPrice);
var cost = gasPrice.mul(21000)
console.log("cost price: " + cost);
var deposit = eth.getBalance(fromacc);
console.log("deposit: " + deposit);
var transferval = eth.getBalance(fromacc).sub(cost)
console.log("transferval: " + transferval);

console.log("Unlock account");
personal.unlockAccount(fromacc,"YOURPASSWORD")

if(transferval > 0) {
  console.log("transfer result");
  eth.sendTransaction({from: fromacc, to: toacc, value: transferval});
} else {
  console.log("no balance");
}

EOF
