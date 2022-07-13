#!/usr/bin/env python
import sys

# Gets input from stdin and processes it and also stores
# all the votes in a string so they are properly formatted
# when tallying all the winning votes
votes = []
data = sys.stdin.readline().rstrip()
temp = " "
while data:
    temp += data + " "
    votes.append(data.split())
    data = sys.stdin.readline().rstrip()
all_votes = temp.split(" ")
# Sort through and find all of our candidates from the raw data in votes.
candidates = []
for result in votes:
    for candidate in result:
        if candidate not in candidates:
            candidates.append(candidate)

# run through the votes and count them for each round and then
# sort them in ascending order and decide whether there is a tie
# or not and display the round information, then keep going until
# a winner is decided.
voter_round = 0
eliminated = []
rounds = []
no_tie = True
no_winner = True
while no_winner:
    round_votes = []
    candidate_votes = []
    candidate_eliminated = ""
    for candidate in votes:
        try:
            if candidate[0] not in eliminated:
                round_votes.append(candidate[0])
            else:
                i = 0
                while candidate[i] in eliminated:
                    i += 1
                round_votes.append(candidate[i])
        except IndexError:
            continue

    for i in range(0, len(candidates)):
        candidate_votes.append(round_votes.count(candidates[i]))

    # Sorting in ascending order
    round_votes = sorted(round_votes, key=round_votes.count, reverse=True)
    candidate_votes = sorted(candidate_votes, reverse=True)
    candidates = sorted(candidates)
    candidates = sorted(candidates, key=round_votes.count, reverse=True)
    # If we only have one candidate left they are the winner
    # So we print out the information and the program is finished
    if len(candidates) == 1:
        print("Round {}".format(voter_round + 1))
        print("{}\t{}".format(candidates[0], temp.count(candidates[0])))
        print("Winner: {} ".format(candidates[0]))
        no_winner = False
        exit()
    if round_votes.count(candidates[0]) > (len(round_votes) / 2):
        print("Round {}".format(voter_round + 1))
        for i in range(len(candidates)):
            print("{}\t{}".format(candidates[i], candidate_votes[i]))
        print("Winner: {} ".format(candidates[0]))
        no_winner = False
        exit()
    print("Round {}".format(voter_round + 1))
    for i in range(len(candidates)):
        print("{}\t{}".format(candidates[i], candidate_votes[i]))

    # Deciding if it's a tie between the bottom two candidates
    # and deciding if it's a breakable tie or not.
    try:
        if candidate_votes[-1] == candidate_votes[-2]:
            no_tie = False
            if voter_round == 0:
                print("Unbreakable Tie")
                exit()
            for r in rounds:
                if r.count(candidates[-1]) > r.count(candidates[-2]):
                    print("Eliminated: {}".format(candidates[len(candidates) - 2]))
                    print()
                    candidate_eliminated = candidates[-2]
                    break
                elif r.count(candidates[-1]) < r.count(candidates[-2]):
                    print("Eliminated: {}".format(candidates[len(candidates) - 1]))
                    print()
                    candidate_eliminated = candidates[-1]
                    break
                else:
                    for i in range(len(candidates)):
                        print("{}\t{}".format(candidates[i], candidate_votes[i]))
                    print("Unbreakable Tie")
                    no_winner = False
                    exit()
    except IndexError:
        continue

    # Printing output of each round if there is no tie
    if no_tie:
        if len(candidates) > 2:
            print("Eliminated: {}".format(candidates[len(candidates) - 1]))
            candidate_eliminated = candidates[-1]
            print()

    # Removing the eliminated candidate, appending the last rounds votes
    # to an array if needed for comparing in the case of a tie and increasing
    # the round counter by one.
    eliminated.append(candidate_eliminated)
    no_tie = True
    candidates.remove(candidate_eliminated)
    rounds.append(round_votes)
    voter_round += 1
    
