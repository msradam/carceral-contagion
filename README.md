# ⚖️ Carceral Contagion ![Heroku](https://heroku-badge.herokuapp.com/?app=heroku-badge)
Simulating the infectious properties of mass incarceration through a synthetic agent-based population network, inspired by Lum et al's "The contagious
nature of imprisonment" [1].

![Screenshot](https://raw.githubusercontent.com/msradam/carceral-contagion/master/screenshot.png)

The app is live at https://carceralcontagion.herokuapp.com/.

## Instructions
Clone the repository, then run
```
python run.py
```
The app will be live at http://127.0.0.1:8521.

## Inspiration
Lum et al. [1] describes racial disparities mass incarceration in the United States as being informed by the socioeconomic issues that occur in communities
when members of the community are incarcerated. This project simulates this phenomenon by initializing a network of individuals with relationships to one 
another who have a chance of 'infecting' another individual with the possibily of being incarcerated. This is an abstraction of the complex
relationships between real persons that can result in imprisonment - such as increased poverty or the lack of parental figures - but is sufficient to illustrate
how mass incarceration is akin to an epidemic and has spiraling effects.

## Implementation
The simulation is built in Mesa, with NetworkX as the graph backend. Each individual is initiated with a randomized sex and set of relationships. The probabilities
for incarceration risks are derived from a study [2] used by Lum et al. that surveyed families of incarcerated persons. Once incarcerated, each
indvidual is assigned a sentence length based on the race of the simulated population based on median sentencing lenghts by race [1]. 

The model is based on the susceptible-infected-susceptible (SIS) model, which means that once individuals have been released they still have a chance of 'infecting' other individuals, and do not recover.

## Citations 
1. Kristian Lum, Samarth Swarup, Stephen G. Eubank, James Hawdon, The Contagious Nature of Imprisonment: An Agent-based Model to Explain Racial Disparities in Incarceration Rates, J. R. Soc. Interface 11(98):20140409, June 2014.

2. Dallaire DH. 2007. Incarcerated mothers and fathers: a comparison of risks for children and families. Family Relations 56, 440–453. (10.1111/j.1741-3729.2007.00472.x) 
