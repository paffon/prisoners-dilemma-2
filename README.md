# Prisoner's Dilemma Simulation

**This Python project simulates the Prisoner's Dilemma game, a classic game theory scenario where two rational players must choose between cooperating and defecting. The code provides a flexible framework for experimenting with different strategies and analyzing the outcomes.**

## Installation

Clone the repository:

```git clone https://github.com/paffon/prisoners-dilemma-2.git```

## Install dependencies:

```pip install -r requirements.txt```

## Usage

Run the main script:

```python main.py```

## Configuration
The *main.py* file provides configuration options for the simulation, such as:
- Number of players: Set the total number of players in the tournament.
- Games between each two players: Specify how many times each pair of players will play against each other.
- Rounds per game: Determine the number of rounds in each game.
- Error rate: Set the probability of a player's action being flipped randomly.
- Survival rate: Determine the percentage of players that will survive to the next generation.
- Survival bias: Control the level of randomness in selecting survivors.
- Debug mode: Enable or disable detailed output for debugging purposes.

## Customization

You can customize the simulation by:
- Adding new strategies: Create new strategy classes in the strategies.py file.
- Modifying existing strategies: Adjust the decision-making logic within the decide method of existing strategies.
- Changing game parameters: Modify the configuration options in the main.py file.

## Visualization

The code includes visualization tools to help analyze the results of the simulation. You can visualize:
- Game outcomes: See how player scores change over time.
- Tournament history: Analyze the evolution of strategies across generations.
