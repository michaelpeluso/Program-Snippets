# Processor-Simulation #
An simulation of serial computing, timesharing, or multitasking. Written in Python.

**A config file must be run with this document in which includes the instructions for this program. The config file has the following structure:**

* First line: indicates the total number of lines in the config file
* Second line: the unit of time used. cycle, s, ms, ns are for cycles, seconds, milliseconds, and nanoseconds respectively
* Third line: the number of tasks that will be used
* Fourth line: contains sc, ts, or mt to indicate serial computing, timesharing or multitasking respectively
* Fifth line: contains the quantum or the timeslice duration if mt or ts has been chosen - otherwise it is set to 0
* * Sixth line: may contain a request for CPU utilization for a given period of time

The amount of lines to follow is equal to the number appearing in line 3. There is one line per task indicated. Every line describes a task by four attributes: the name (label) of the task (only the 26 capital case English letters can appear), the arrival time of the task, the CPU time of the task, and the I/O time of the task. 

**All the tasks exhibit the following limited execution structure:**

CPU runs first, before I/O devices. Consider that numbers will be kept small. Thus a 32-bit integer (signed or unsigned) would be more than enough. Moreover any turnaround time would also be small enough to fit into such an integer.
