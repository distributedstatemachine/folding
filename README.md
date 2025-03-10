<!-- <div align="center">
    <img src="./assets/macrocosmos-black.png" alt="Alt generative-folding-tao">
</div> -->

<picture>
    <source srcset="./assets/macrocosmos-white.png"  media="(prefers-color-scheme: dark)">
    <img src="macrocosmos-white.png">
</picture>

<picture>
    <source srcset="./assets/macrocosmos-black.png"  media="(prefers-color-scheme: light)">
    <img src="macrocosmos-black.png">
</picture>

<div align="center">

# **Protein Folding Subnet 25** <!-- omit in toc -->
[![Discord Chat](https://img.shields.io/discord/308323056592486420.svg)](https://discord.gg/bittensor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

---

## The Incentivized Internet <!-- omit in toc -->

[Discord](https://discord.gg/bittensor) • [Network](https://taostats.io/) • [Research](https://bittensor.com/whitepaper)
</div>

This repository is the official codebase for Bittensor Subnet Folding (SN25), which was registered on May 20th, 2024. To learn more about the Bittensor project and the underlying mechanics, [read here.](https://docs.bittensor.com/)

**IMPORTANT**: This repo has a functional **testnet 141** as of May 13th. You should be testing your miners here before launching on main.

---

<div align="center">
    <img src="./assets/protein_tao.png" alt="Alt generative-folding-tao">
</div>

# Introduction
The protein folding subnet is Bittensors’ first venture into academic use cases, built and maintained by [Macrocosmos AI](https://www.macrocosmos.ai). While the current subnet landscape consists of mainly AI and web-scraping protocols, we believe that it is important to highlight to the world how Bittensor is flexible enough to solve almost any problem.

This subnet is designed to produce valuable academic research in Bittensor. Researchers and universities can use this subnet to solve almost any protein, on demand, for free. It is our hope that this subnet will empower researchers to conduct world-class research and publish in top journals while demonstrating that decentralized systems are an economic and efficient alternative to traditional approaches.

  
# What is Protein Folding?  
  
  Proteins are the biological molecules that "do" things, they are the molecular machines of biochemistry. Enzymes that break down food, hemoglobin that carries oxygen in blood, and actin filaments that make muscles contract are all proteins. They are made from long chains of amino acids, and the sequence of these chains is the information that is stored in DNA. However, its a large step to go from a 2D chain of amino acids to a 3D structure capable of working. 

  The process of this 2D structure folding on itself into a stable, 3D shape is called **protein folding**. For the most part, this process happens naturally and the end structure is in a much lower free energy state than the string. Like a bag of legos though, it is not enough to just know the building blocks being used, its the way they're supposed to be put together that matters. *"Form defines function"* is a common phrase in biochemsitry, and it is the quest to determine form, and thus function of proteins, that makes this process so important to understand and simulate. 

# Why is Folding a Good Subnet Idea? 
An ideal incentive mechanism defines an asymmetric workload between the validators and miners. The necessary proof of work (PoW) for the miners must require substantial effort and should be impossible to circumvent. On the other hand, the validation and rewarding process should benefit from some kind of privileged position or vantage point so that an objective score can be assigned without excess work. Put simply, **rewarding should be objective and adversarially robust**.

Protein folding is also a research topic that is of incredibly high value. Research groups all over the world dedicate their time to solving particular niches within this space. Providing a solution to attack this problem at scale is what Bittensor is meant to provide to the global community. 

# Reward Mechanism
Protein folding is a textbook example of this kind of asymmetry; the molecular dynamics simulation involves long and arduous calculations which apply the laws of physics to the system over and over again until an optimized configuration is obtained. There are no reasonable shortcuts. 

While the process of simulation is exceedingly compute-intensive, the evaluation process is actually straightforward. **The reward given to the miners is based on the ‘energy’ of their protein configuration (or shape)**. The energy value compactly represents the overall quality of their result, and this value is precisely what is decreased over the course of a molecular dynamics simulation. The energy directly corresponds to the configuration of the structure, and can be computed in closed-form. The gif below illustrates the energy minimization over a short simulation procedure.

<div align="center">
    <img src="./assets/8emf_pdb_loss.gif" alt="Alt Folded-protein" width="500" height="350">
</div>

When the simulations finally converge (ΔE/t < threshold), they produce the form of the proteins as they are observed in real physical contexts, and this form gives rise to their biological function. Thus, the miners provide utility by preparing ready-for-study proteins on demand. An example of such a protein is shown below. 

<div align="center">
    <img src="./assets/8emf_pdb_protein.gif" alt="Alt Folded-protein" width="600" height="500">
</div>

# Running the Subnet
## Requirements 
Protein folding utilizes a standardized package called [GROMACS](https://www.gromacs.org). To run, you will need:
1. A Linux-based machine 
2. Multiple high-performance CPU cores. 

Out of the box, **we do not require miners to run GPU compatible GROMACS packages**. For more information regarding recommended hardware specifications, look at [min_compute.yml](./min_compute.yml)

**IMPORTANT**: GROMACS is a large package, and take anywhere between 1h to 1.5h to download. 

## Installation
This repository requires python3.8 or higher. To install it, simply clone this repository and run the [install.sh](./install.sh) script.
```bash
git clone https://github.com/macrocosm-os/folding.git
cd folding
bash install.sh
```
This will also create a virtual environment in which the repo can be run inside of. 

The above commands will install the necessary requirements, as well as download GROMACS and add it to your `.bashrc`. To ensure that installation is complete, running `gmx` in the terminal should print
```
:-) GROMACS - gmx, 2023.1-Ubuntu_2023.1_2ubuntu1 (-:
```

If not, there is a problem with your installation, or with your `.bashrc`

## Registering on Mainnet
```
btcli subnet register --netuid 25 --wallet.name <YOUR_COLDKEY> --wallet.hotkey <YOUR_HOTKEY>
```

## Registering on Testnet
Netuids that are larger than 99 must be set explicity when registering your hotkey. Use the following command:
```
btcli subnet register --netuid 141 --wallet.name <YOUR_COLDKEY> --wallet.hotkey <YOUR_HOTKEY>
```

## Launch Commands
### Validator
There are many parameters that one can configure for a simulation. The base command-line args that are needed to run the validator are below. 
```bash
python neurons/validator.py
    --netuid <25/141>
    --subtensor.network <finney/test>
    --wallet.name <your wallet> # Must be created using the bittensor-cli
    --wallet.hotkey <your hotkey> # Must be created using the bittensor-cli
    --axon.port <your axon port> #VERY IMPORTANT: set the port to be one of the open TCP ports on your machine
```
For additional configuration, the following params are useful:
```bash
python neurons/validator.py
    --netuid <25/141>
    --subtensor.network <finney/test>
    --wallet.name <your wallet> # Must be created using the bittensor-cli
    --wallet.hotkey <your hotkey> # Must be created using the bittensor-cli
    --neuron.queue_size <number of pdb_ids to submit>
    --neuron.sample_size <number of miners per pdb_id>
    --protein.max_steps <number of steps for the simulation>
    --logging.debug # Run in debug mode, alternatively --logging.trace for trace mode
    --axon.port <your axon port> #VERY IMPORTANT: set the port to be one of the open TCP ports on your machine
```

### Miner
There are many parameters that one can configure for a simulation. The base command-line args that are needed to run the miner are below. 
```bash
python neurons/miner.py
    --netuid <25/141>
    --subtensor.network <finney/test>
    --wallet.name <your wallet> # Must be created using the bittensor-cli
    --wallet.hotkey <your hotkey> # Must be created using the bittensor-cli
    --neuron.max_workers <number of processes to run on your machine>
    --axon.port <your axon port> #VERY IMPORTANT: set the port to be one of the open TCP ports on your machine
```

Optionally, pm2 can be run for both the validator and the miner using our utility scripts found in pm2_configs. 
```bash 
pm2 start pm2_configs/miner.config.js
```
or 
```bash 
pm2 start pm2_configs/validator.config.js
```
Keep in mind that you will need to change the default parameters for either the [miner](./scripts/run_miner.sh) or the [validator](./scripts/run_validator.sh). 

## How does the Subnet Work?

In this subnet, validators create protein folding challenges for miners, who in turn run simulations based on GROMACS to obtain stable protein configurations. At a high level, each role can be broken down into parts: 

### Validation

1. Validator creates a `neuron.queue_size` number of proteins to fold.
2. These proteins get distributed to a `neuron.sample_size` number of miners (ie: 1 PDB --> sample_size batch of miners).
3. Validator is responsible for keeping track of `sample_size * queue_size` number of individual tasks it has distributed out. 
4. Validator queries and logs results for all jobs based on a timer, `neuron.update_interval`. 

For more detailed information, look at [validation.md](./documentation/validation.md)

### Mining
Miners are expected to run many parallel processes, each executing an energy minimization routine for a particular `pdb_id`. The number of protein jobs a miner can handle is determined via the `config.neuron.max_workers` parameter. 

For detailed information, read [mining.md](./documentation/mining.md).

## Notes

**Miner** simulations will output a projected time. The first two runs will be about the same length, with the third taking about an order of magnitude longer using a default number of steps = 50,000. The number of steps (`steps`) and the maximum allowed runtime (`maxh`) are easily configurable and should be employed by miners to prevent timing out. We also encourage miners to take advantage of 'early stopping' techniques so that simulations do not run past convergence.

Furthermore, we want to support the use of ML-based mining so that recent algorithmic advances (e.g. AlphaFold) can be leveraged. At present, this subnet is effectively a **specialized compute subnet** (rather than an algorithmic subnet). For now, we leave this work to motivated miners.

GROMACS itself is a rather robust package and is widely used within the research community. There are specific guides and functions if you wish to parallelize your processing or run these computations off of a GPU to speed things up.



## License

This repository is licensed under the MIT License.
```text
# The MIT License (MIT)
# Copyright © 2024 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```
