from stats import basic_stats

filename = 'Zen-stats2.csv'

sort_by_name = False

# load up / read the basic stats as a sanity check
# of how we're reading in / calculating stats
basic_data = basic_stats(filename)
for key in basic_data.keys():
    data = basic_data[key]
    print('\n----------------')
    print('%s \n' % key)

    if sort_by_name:
        sorted_data = sorted(data.keys())
    else:
        sorted_data = sorted(data, key=data.get)

    for name in sorted_data:
        print('%s %i' % (name.ljust(10), data[name]))
print('\n\n------------------------------\n\n')
