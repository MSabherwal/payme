from collections import defaultdict
from random import sample


def settle_offset(bills, offset):
    num_players = len(bills)
    base = offset // num_players
    offset -= num_players * base
    if offset >= num_players:
        # MS:TODO: is this necessary? seems definitional
        print("The offset could not be divided properly. Max remaining offset should be less than ", num_players,
              " but remaining offset was ", offset, ".")
        exit()
    for k in bills:
        bills[k] += base
    extra_cent_players = sample(list(bills), int(offset))
    for p in extra_cent_players:
        bills[p] += 1
    offset -= len(extra_cent_players)
    if offset:
        print("The offset could not be divided properly. Final offset should be 0, but was ", offset)
        exit()


def remove_zero_bills(bills):
    names = []
    for name in bills:
        if bills[name] == 0:
            names.append(name)

    for name in names:
        bills.pop(name)


def verify_bills(bills):
    balance = 0
    for name in bills:
        balance += bills[name]
    if balance == 0:
        print("Great, the net balance checks out to be 0.")
    else:

        print("Something is wrong, the net balance of the bills is off by: ", balance)
        if 0 < balance < 1:
            print('remaining balance small, ignoring')
        else:
            print('balance greater than 1c, script failure')
            exit()


def settle_bills(bills):
    settle_line_items = []
    while len(bills) > 0:
        # Sort the bills by values
        bill_list = sorted(bills.items(), key=lambda k_v: k_v[1], reverse=True)
        # print bill_list

        if len(bill_list) < 2:
            print("We have a problem, the remaining bills cannot settle: ", bill_list)
            # if remainder is <1cent, ignore

            remainder = bill_list[0][1]
            if -1 < remainder < 1:
                print("the value is small so ignoring")
                break
            return

        # Get two biggest bills to settle.
        positive_name, positive_balance = bill_list[0]
        negative_name, negative_balance = bill_list[-1]

        # Print out the transaction
        settled_balance = min(abs(positive_balance), abs(negative_balance))
        settle_line_items.append(positive_name + " <-- " + negative_name + " : " + str(settled_balance))

        # Settle the transaction
        bills[positive_name] = positive_balance - settled_balance
        bills[negative_name] = negative_balance + settled_balance

        # Remove all people that are already settled
        remove_zero_bills(bills)
    settle_line_items = sorted(settle_line_items)
    for line_item in settle_line_items:
        print(line_item)
    return


def get_bills():
    # TODO: implement
    return defaultdict(int)


def main():
    # This amount will be split amongst all players
    # NOTE: if this is non-zero, you must include zero bill players
    offset = 2600

    bills = get_bills()

    settle_offset(bills, offset)

    remove_zero_bills(bills)

    print("----- All bills: -----")

    sorted_names = sorted(list(bills))

    for name in sorted_names:
        print(name, bills[name])

    print("----- Verifying bills:")
    verify_bills(bills)

    print("----- Transactions to settle bills:")
    settle_bills(bills)


if __name__ == '__main__':
    main()