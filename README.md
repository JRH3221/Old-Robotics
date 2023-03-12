# Robotics

All code is free for use and editing. There are multiple branches with different code programs. All code is currently from a 3 wheel omni soccer robot.

## Technical Info
The ev3 uses a linux kernal & Arm9 processor with some sort of AM1x core. It also features 64MB ram. 

This turns out to be significantly faster than spike prime processor and far more ram. 
Single operations that can be passed out to more threads, actually shouldn't be. Because it's single core, using multithreading to speed up calculations shouldn't be done. Although every isolated operation should be threaded, this can cause synchronisation issues when trying to read and write from global variables, this can be a problem when it comes to speed in micropython, but when handled correctly in languages that give more control this can be avoided. 

Although not a surprise, micropython is ridiculously slow, to the point where I think it's nearly unusable. 
For speed operations where many calculations need to be done, C is ~10x faster than micropython. 
Although java may actually be even faster as the processor runs on java bytecode, which means C is actually being compiled to bytecode and not assembly. 
This does limit optimizations to a point as bytecode cannot be directly programmed, I would've preffered trying to program in an assembly language to benchmark performance but bytecode it is. 

Micrpythons speed is a bit confusing since it is compiled to bytecode as well, but maybe it's limited as there would need to be a powerful compiler to optimize the terrible typing of python, but such a compiler can't exactly run on such slow hardware. 

This is what will change with R-Script. It should be easy with all the functions built in, as that's what it's built for, but also strongly typed so that the compiler won't have to spend a year on just figuring out what type a variable is and how much memory it needs. 
Step 1 to the compiler is to make it output micropython code, this will be a test to make sure it all works with something simple. 
Step 2 is fully fledged compiler that uses LLVM and will go straight to bytecode, original plan was to output to C then run a second compiler to get the bytecode, but that seems like it would become harder to interpret what was meant to happen in R-Script.

## New Developments 
A new Repo will be made for the compiled C version of the programming.
The repo can be found here: https://github.com/JRH3221/CType-Ev3
