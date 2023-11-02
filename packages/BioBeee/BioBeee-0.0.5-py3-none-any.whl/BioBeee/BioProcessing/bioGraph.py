
class FASTQGraphs:

    def GC_graph(self, gc_lis, type='scatter'):
        import matplotlib.pyplot as plt
        import seaborn as sns
    
        Y = [i for i in range(len(gc_lis))]
       
        if type == 'dist' or type == 'hist':
            plt.title('GC CONTENT PER SEQUENCE DISTRIBUTION', font='arial', color='#636057', fontsize=18)
            sns.distplot(gc_lis, kde=True, color='#f78181', bins=30)
            
        else:
            plt.title('GC% PER SEQUENCE READS', font='arial', color='#636057', fontsize=18)
            plt.scatter(gc_lis, Y, color='black', facecolor='#f78181')
            plt.xlabel('GC in %', font='arial', color='#636057', fontsize=12)
            plt.xlim(0, 100)
            plt.ylabel('Number of reads', font='arial', color='#636057', fontsize=12)
        return plt.show()
    
    def scoring_graph_BASE33(self, mean, data, style='default'):
        import matplotlib.pyplot as plt
        import seaborn as sns

        nt = [i for i in range(len(mean))]
        if style == 'gray':
            # (span1 0-20,  span2 20-28,  span3 28-42,  mean line color,  box color)
            colors = ('#999999', '#cccccc', '#f2f2f2', '#000000', 'white')
        elif style == 'white':
            colors = ('white', 'white', 'white', 'black', '#bfbdbd')
        elif style == 'cool':
            colors = ('#546af7', '#5ca1fa', '#add6f7', '#112ff0', '#f2f207')
        elif style == 'hot':
            colors = ('#f2b750', '#f7cb7e', '#fce4bb', '#f70505', '#f79d8d')
        elif style == 'heatmap':
            colors = ('#65c9f7', '#9ef6f7', '#f79e9e', '#0f0f0f', '#f2a1f7')
        else: 
            colors = ('#ed7272', '#ecfa82', '#82fa8c', '#ff5c33', 'yellow')

        ax = plt.subplots()[1]
        plt.title(f'SCORING GRAPH (ASCII BASED 33), length {len(mean)} bp', size=20, font='arial', color='#636057')
        plt.plot(nt, mean, c=colors[3], linewidth=1)
        sns.boxplot(data, showfliers=False, width=0.9, color=colors[4], linewidth=0.8)
        ranges = [i for i in range(0, len(mean), 5)]
        ax.grid(1)
        ax.margins(0)
        ax.axhspan(0, 20, facecolor=colors[0], alpha=0.5)
        ax.axhspan(20, 28, facecolor=colors[1], alpha=0.5)
        ax.axhspan(28, 42, facecolor=colors[2], alpha=0.5)
        ax.set_xticks(ranges)
        ax.set_xticklabels(ranges)
        plt.xlim(0, len(nt))
        plt.ylim(0, 42)

        plt.xlabel('Nucleotides (bp)', font='arial', fontsize=12, color='#636057')
        plt.ylabel('Phred Score (Q)', font='arial', fontsize=12, color='#636057')
        return plt.show()

################################## END OF THE PROGRAMS ###################################

# FASTQGraphs().GC_graph()