    def make_cfreq_traj_fig(probes):
        """
        Returns fig showing cumulative frequency trajectories of "probes"
        """
        start = time.time()

        palette = iter(sns.color_palette("hls", len(probes)))
        # load data
        xys = []
        for probe in probes:
            x = range(model.num_docs)
            y = np.cumsum(model.hub.term_part_freq_dict[probe])
            if x:
                last_y, last_x = y[-1], x[-1]
            else:
                last_y, last_x = 0, 0  # in case x is empty
            xys.append((x, y, last_x, last_y, probe))
        y_thr = np.max([xy[3] for xy in xys]) / 10  # threhsold is at third from max
        # fig
        fig, ax = plt.subplots(figsize=(FigsConfigs.MAX_FIG_WIDTH, 3), dpi=FigsConfigs.DPI)
        ax.set_title(model.hub.probe_store.probe_cat_dict[probes[0]])
        ax.set_xlabel('Mini Batch', fontsize=FigsConfigs.AXLABEL_FONT_SIZE)
        ax.set_ylabel('Cumulative Frequency', fontsize=FigsConfigs.AXLABEL_FONT_SIZE)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='both', which='both', top='off', right='off')
        ax.xaxis.set_major_formatter(FuncFormatter(human_format))
        # plot
        for (x, y, last_x, last_y, probe) in xys:
            ax.plot(x, y, '-', linewidth=1.0, c=next(palette))
            if last_y > y_thr:
                plt.annotate(probe, xy=(last_x, last_y),
                             xytext=(0, 0), textcoords='offset points',
                             va='center', fontsize=FigsConfigs.LEG_FONTSIZE, bbox=dict(boxstyle='round', fc='w'))
        ax.legend(fontsize=FigsConfigs.LEG_FONTSIZE, loc='upper left')
        plt.tight_layout()
        print('{} completed in {:.1f} secs'.format(sys._getframe().f_code.co_name, time.time() - start))
        return fig

    figs = [make_cfreq_traj_fig(cat_probes)
            for cat_probes in model.hub.probe_store.cat_probe_list_dict.values()]
