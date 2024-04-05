# Proof of Concept. Packet Splitter / Redundancy Generator.

This is a very simple proof of concept to show that Reed Solomon encoding can be used
to solve the problem listed below.

## The real problem.

- You have 10 Megabits of "real data".
- You MUST send 100 Megabits of data.
- You send 1460 byte packets.
- About 90% of your packets will be lost at random.
- You want near 100% of the time for the "real data" to make it to the other end. 

## Making the numbers "easier".

- You have 10 * 10 = 100 bytes of "real data"
- You MUST send 100 packets (so 1000 bytes in total).
- You send 10 byte packets.
- About 90% of your packets will be lost at random.
- You want near 100% of the time for the "real data" to make it to the other end.

## Defects.

As POC code to run once and throw away, lacks niceness.

1. Could use logging for debugging.
1. Could print more detail if a mismatch is found.
1. Should use argparse to accept command line arguments, instead of hardcoded values. Functions are well setup for this, but need to get user input and pass it in.


## Example Output.

```
$ python splitter.py 
Successes 1000
Failures  0
```