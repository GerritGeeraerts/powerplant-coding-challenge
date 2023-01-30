# powerplant-coding-challenge

You can read the [coding-challenge assignment](./coding-challenge.md)

Or you can read a summary in short:
Calculate how much power each of a multitude of different powerplants need to produce (a.k.a. the production-plan) when the load is given and taking into account the cost of the underlying energy sources (gas, kerosine) and the Pmin and Pmax of each powerplant.
* Do not to rely on an existing (linear-programming) solver.
* Do not spend more than 4 hours on this challenge.
* The goal of this exercise is to be a seed to discuss all kinds of interesting software engineering topics.

# comment
This is my first time that I used FastApi and the first time i started out a project with Test Driven Development aproach.
I am looking forward to some feedback :D

## To start the server with docker
Run `sudo docker-compose up -d --build` in the project root to start the server.

Run `sudo docker-compose dwon -v` in the project root to stop the server.

Open [localhost](http://localhost:8888/docs) in your browser.
