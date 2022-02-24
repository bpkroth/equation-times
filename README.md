# equation-times

This is a simple program to find (and count) all of the different *equation times*.

*equation times* are times where you can insert one or more operators somewhere in the digits and have have a valid equality expression.

This is something my son likes to do when reading the clock and I thought it might be fun to try and count them.

I'm sure we *could* try and do this analytically (e.g. with some complicated combinatorics), but I also thought it might be a fun exercise to code up.

## Usage

### Printing the permutations and their results

```sh
./equation-times.py | grep -v '^00:00' | grep -m1 -C 10 True
```

```txt
00:01   0==(0*(0*1))    True
00:01   0==(0*(0/1))    True
00:01   0==(0*(0+1))    True
00:01   0==(0*(0-1))    True
00:01   0==((0*0)*1)    True
00:01   0==((0/0)*1)    None
00:01   0==((0+0)*1)    True
00:01   0==((0-0)*1)    True
00:01   0==(0/(0*1))    None
00:01   0==(0/(0/1))    None
00:01   0==(0/(0+1))    True
...
```

### Counting them

```sh
./equation-times.py | awk '{ print $3 }' | sort | uniq -c
```

```txt
 129752 False
   7950 None
   6698 True
```

## Notes

- Support for seconds can be adjusted with the `with_seconds=True` parameter (see source for details).
- Additional operators and comparisons could also be added by appending to the appropriate lists (see source for details).