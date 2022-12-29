# Formula 1 ELO system
Inspired by the 'fastest driver of all time' article Formula1 released in 2020 (https://corp.formula1.com/formula-1-and-aws-tap-into-machine-learning-and-cloud-technology-to-identify-the-fastest-driver-of-all-time/) with an algorythm developed by AWS I decided to try and come out with an idea to compare all F1 drivers in history.
ELO system looked like a good way to make something that was as bjective as possibile. Unfortunately ELO is not made to compare in a multiplayer context, luckily for me Danny Cunningham already came out with a solution for that and published his multielo library (https://github.com/djcunningham0/multielo). For any reerence on how ELO works and how it got adapted to multiplayer go check out his work, he provided a very in-depth description of the whole thing.

For what concerns my work, before commenting it there's a couple more things I'd like to point out:
- the database i used to retrieve all the data about the 72 years of F1 history can be found at https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020?resource=download Props to Vopani for the hard work that saved me
- I never used pandas and dataframes in general so there's probably a way more clever way to approach this. If anyone is willing to help me out understanding it I'd really appreciate it
- As of now the code is super ugly, I know, I'll get it cleaned up as soon as I can

Now let's move to the big elephant in the room: F1 is not as simple as you win or you lose, there are lots of factors to keep in account, how did I solve that? Very simple: I didn't. This little project is not meant to give a real, uncontestable answer, it's just for fun.

## My approach
The way I chose to approach this is that I wanted to reward both beeing better than your own teammates and rewarding you for the actual position you finished.

I have to admit I would've loved to implement an algorythm to weight the ELO gains based on the championship position of both the driver and the team (after all we all know that a Verstappen win in the 2022 RB would not be the same as a Ricciardo win in the 2021 McLaren) but I honestly don't have the brain power to do that.
Another important thing to point out is that i chose to reward both qualy and race results, but not giving them the same importance, after all points are scored on Sunday :P
The way I prioritized the ELO ranking is the following:
- teammates race comparison
- teammates qualifying comparison
- overall race
- overall qualifying
I don't know if it's the right way to do it and I don't know if the weighs I gave to the different factors is orrect, feel free to play with them and see if the results look better than what i got (more about it [later](#The-results-so-far))

## Issues

There are several things I don't like right now:
- as mentioned earlier I'd like to account for teams and drivers standings too
- the system is unfair because it *sometimes* rewards longer careers, but it's not always the case
- some results don't make much sense and I don't get why (i.e. as as good as a driver Reutmann was I don't think he's top 10?)
- current drivers always get very high positionings and again I'm a bit too stupid to understand why

## The results so far
I know what you're thinking "all nice, but give us the results already!"
So here's the top 10 of all time with their relative ELO points

![image](https://user-images.githubusercontent.com/119423921/209942503-ef05ac39-0f70-43d5-bf82-5d5165419c7a.png)

What I found out is that with smaller year ranges the results got more realistic (NB the ELO gets defaulted to 0 at the year you choose to start the comparison). So here's the top 5 drivers of each decade:
![image](https://user-images.githubusercontent.com/119423921/209942863-152a8768-9c2d-4441-b124-7bfaa3d8c881.png)

## What's the plan now?
There are some things I'd like to tackle next:
- clean up the code
- create a UI, at first just to choose the parameters that are now passed in the command line, but then I'd like to get something more interesting like following the ELO ranking of the selected driver and stuff like that
- come up with the so talked algorythm to normalize the changes based on standings
- teams ELO


If you got this far reading I want to thank you and tell you that I'd really appreciate any feedback on my work
For what the various part of the code do, please refer to the in-code comments


