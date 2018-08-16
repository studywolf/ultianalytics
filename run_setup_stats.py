from stats import basic_stats, setup_stats

filename = 'Zen-stats.csv'

basic_data = basic_stats(filename)
scores = setup_stats(filename)

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 8))
for subplot_idx, key in enumerate(scores.keys()):
    print('\n----------------')
    print('Scores for setting up %ss \n' % key)
    score_dict = scores[key]
    del score_dict['Anonymous']
    if key is not 'Ratio':
        # normalize by games
        for name in score_dict.keys():
            score_dict[name] = score_dict[name] / basic_data['Games'][name]
    sorted_score_list = sorted(score_dict.items(), key=lambda kv: kv[1])

    names = []
    plt.subplot(len(scores.keys()), 1, subplot_idx+1)
    plt.grid()
    for ii in range(len(sorted_score_list)):
        names.append(sorted_score_list[ii][0])
        score = sorted_score_list[ii][1]
        print('%s: %.3f' % (names[-1].ljust(10), score))
        plt.bar(ii, score)
    plt.xticks(range(len(sorted_score_list)), names, rotation=70)
    plt.title({'Goal':'Setting up Assists',
                'Throwaway':'Setting up Throwaways',
                'Ratio':'Assist setup / Throwaway setup'
                }[key])
plt.tight_layout()
plt.show()