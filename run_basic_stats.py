from stats import basic_stats

filename = 'Zen-stats.csv'

# load up / read the basic stats as a sanity check
# of how we're reading in / calculating stats
basic_data = basic_stats(filename)
for key in basic_data.keys():
    data = basic_data[key]
    print('\n----------------')
    print('%s \n' % key)
    for name in sorted(data.keys()):
        print('%s %i' % (name.ljust(10), data[name]))
print('\n\n------------------------------\n\n')
