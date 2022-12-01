# Ethereum Attack Reproducer

An Ethereum attack reproducer for security study.

## Attack

- [x] [Harvest Finance attack](https://medium.com/harvest-finance/harvest-flashloan-economic-attack-post-mortem-3cf900d65217)

## Setup

1. Install `Web3.py`.

```shell
pip install web3
```

2. Setup reproducing environment.

If you use [Ganache](https://github.com/trufflesuite/ganache)

```shell
ganache --fork --fork.blockNumber * --chain.time *
```

3. Initialize an account satisfying attack preconditions.

4. Run an attack in directory [attacks](attacks).
   For example:

```shell
python harvest_finance_2020.10.26.py
```

---

# References

- [Web3.py](https://web3py.readthedocs.io/en/v5/)