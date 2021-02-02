# Volunteer-Scheduling
Shift scheduling for Lebanese Red Cross Volunteers using CP-SAT Solver | OR-Tools by Google, and Tkinter for a simple GUI design.

## Understand the program | Problem Statement
Shift scheduling is a messy process where all rescuers input some preferred and unwanted days.
In order to operate, shifts should include a specific number of rescuers, filling specific roles such as mission leaders, drivers, EMTs... This is why it is always a lengthy process to find a fitting combination.
With constraint and dynamic programming, we are able to fit several optimal schedules in a couple of seconds. 

## Constraints Followed
Several constraints were taken into consideration when programming this scheduler:
- One shift per rescuer per week
- One team leader per team
- Distribute rescuers equally among teams in accordance to roles (distribute mission leaders, drivers and EMTs equally)
- Set a minimum per team to avoid unwanted combinations
- At least one technical trainer per team
- At least one driver trainer per team
- At least one mission leader trainer per team
- Maximize rescuers with preferred days
- Minimize rescuers with unwanted days

## Methodology followed
The program includes some flexibility: called tolerance level.
Optimization is not always what is needed, thus the ability to change the constraints priority is included.
Increasing tolerance will yield in a less equally distributed but more satisfying team composition (in terms of number of rescuers with preferred days).
Randomness was also included to account for the large number of potential optimal solutions.

A GUI was then designed for easier implementation using tkinter.

## How to use
For an easy implementation, download and run the main.exe file.
A sample .xslx file is included.
