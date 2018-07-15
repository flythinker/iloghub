#!/usr/bin/python3.6

from iloghub_tail.tail import LogHubTail

if __name__ == "__main__":
    tail = LogHubTail()
    tail.start_tail()


