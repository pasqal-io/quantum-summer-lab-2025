# Pasqal Theater Festival : Scheduling  Performances with Shared Actors

We are organizing the first edition of Pasqal Theater Festival and we’ll propose **20 different plays** to our public. 

We want to give the attendees the oportunity to see as many plays as possible during the weekend, so we have decided that each play will be performed **twice** during the festival. 

In order to fit all the performances whithin the weekend, we need first to decide how many venues in the city we need to book. But here’s the catch: since boocking them costs money and we have a strict budget, we cannot afford booking all the venues in the city, so we need to book the minimum number of theaters as possible. 

We already have the list of plays and we just realized that many of them share some of the 500 actors that will be performing throught the weekend.

It’s important to mention that the festival will start on Friday night and will have its last sessions on Sunday night. Also, in order to have time to setup the stage before each session, each theater can host at most 3 plays per day: one in the morning, another one in the afternoon, and one in the evening. This will also give time to the public and the actors to move from one theater to another if they want or need to.

### The Task

1. Assign each of the 20 plays to **two distinct time slots**.
2. Ensure no actor is scheduled to perform in overlapping plays at the same time.
3. Minimize the total number of time slots needed.
4. Decide how many theaters we need to book.

# Input Data

We’re sharing a CSV file representing a **500 × 20 matrix,** where

- Each **row** corresponds to an actor (A1 through A500).
- Each **column** corresponds to a play (Play1 through Play20).
- A cell value is **1** if the actor performs in that play, or **0** if they do not.

Here’s an example with 5 actors and 3 plays:

| ActorID | Play1 | Play2 | Play3 |
| --- | --- | --- | --- |
| A1 | 1 | 0 | 0 |
| A2 | 0 | 1 | 1 |
| A3 | 1 | 0 | 1 |
| A4 | 1 | 0 | 0 |
| A5 | 0 | 0 | 1 |

Here’s the full data:

[Pasqal_Festival__plays_and_actors_toy_instance.csv](Pasqal_Festival__plays_and_actors_toy_instance.csv)

If you have access to sufficient computing power, you can also try with a
beefier instance:

[Pasqal_Festival__plays_and_actors.csv](Pasqal_Festival__plays_and_actors.csv)


# What to Submit

1. An explanation of why your modeling strategy
2. How you solved the problem
3. The total number of venues we need to book and their time slots used with the related play

