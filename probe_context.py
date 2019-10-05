    def make_probe_context_fig(probe, num_context_words=20):
        """
        Returns fig showing tokens that occur most frequently before "probe"
        """
        start = time.time()

        probe_id = model.hub.probe_store.probe_id_dict[probe]
        bptt_steps = int(model.configs_dict['bptt_steps'])
        num_h_axes = 3
        num_v_axes = ((bptt_steps) // num_h_axes)
        if num_h_axes * num_v_axes < bptt_steps:
            num_v_axes += 1
        # load data
        probe_x_mat = model.hub.probe_x_mats[model.hub.probe_store.probe_id_dict[probe]]
        probe_context_df = pd.DataFrame(index=[probe_id] * len(probe_x_mat), data=probe_x_mat)
        context_dict_list = []
        for bptt_step in range(bptt_steps - 1):
            crosstab_df = pd.crosstab(probe_context_df[bptt_step], probe_context_df.index)
            context_dict = crosstab_df.sort_values(probe_id)[-num_context_words:].to_dict('index')
            context_dict = {model.hub.train_terms.types[token_id]: d[probe_id] for token_id, d in context_dict.items()}
            context_dict_list.append(context_dict)
        # add unigram freqs
        unigram_dict = dict(model.hub.train_terms.term_freq_dict.most_common(num_context_words))
        context_dict_list.insert(0, unigram_dict)
        # fig
        fig, axarr = plt.subplots(num_v_axes, num_h_axes,
                                  figsize=(FigsConfigs.MAX_FIG_WIDTH, num_v_axes * 4), dpi=FigsConfigs.DPI)
        fig.suptitle('"{}"'.format(probe))
        for ax, context_dict, bptt_step in zip_longest(
                axarr.flatten(), context_dict_list, range(bptt_steps + 1)[::-1]):
            # plot
            if not context_dict:
                ax.axis('off')
                continue
            ytlabels, token_freqs = zip(*sorted(context_dict.items(), key=itemgetter(1), reverse=True))
            mat = np.asarray(token_freqs)[:, np.newaxis]
            sns.heatmap(mat, ax=ax, square=True, annot=False,
                        annot_kws={"size": 6}, cbar_kws={"shrink": .5}, cmap='jet', fmt='d')
            # colorbar
            cbar = ax.collections[0].colorbar
            cbar.set_label('Frequency')
            # ax (needs to be below plot for axes to be labeled)
            ax.set_yticks(range(num_context_words))
            ax.set_yticklabels(ytlabels[::-1], rotation=0)  # reverse labels because default is upwards direction
            ax.set_xticklabels([])
            if bptt_step != bptt_steps:
                ax.set_title('Terms at distance t-{}'.format(bptt_step))
            else:
                ax.set_title('Unigram frequencies')
        plt.tight_layout()
        fig.subplots_adjust(top=0.9)
        print('{} completed in {:.1f} secs'.format(sys._getframe().f_code.co_name, time.time() - start))
        return fig

    def make_probe_context_alternative_fig(probe, num_context_words=20):
        """
        Returns fig showing tokens that occur most frequently before "probe" and includes unigram frequency information
        """
        start = time.time()

        probe_id = model.hub.probe_store.probe_id_dict[probe]
        x = np.arange(num_context_words)
        bptt_steps = int(model.configs_dict['bptt_steps'])
        num_h_axes = 3
        num_v_axes = ((bptt_steps) // num_h_axes)
        if num_h_axes * num_v_axes < bptt_steps:
            num_v_axes += 1
        # load data
        ytlabels, unigram_freqs = zip(*islice(model.hub.train_terms.type_freq_dict_no_oov.items(), 0, num_context_words))
        unigram_freqs_norm = np.divide(unigram_freqs, np.max(unigram_freqs).astype(np.float))
        probe_x_mat = model.hub.probe_x_mats[model.hub.probe_store.probe_id_dict[probe]]
        probe_context_df = pd.DataFrame(index=[probe_id] * len(probe_x_mat), data=probe_x_mat)
        xys = []
        for bptt_step in range(bptt_steps - 1):
            crosstab_df = pd.crosstab(probe_context_df[bptt_step], probe_context_df.index)
            context_dict = crosstab_df.sort_values(probe_id)[-num_context_words:].to_dict('index')
            context_dict = {model.hub.train_terms.types[token_id]: d[probe_id] for token_id, d in context_dict.items()}
            tups = sorted(context_dict.items(), key=lambda i: model.hub.train_terms.term_freq_dict[i[0]], reverse=True)
            y_unnorm = [tup[1] for tup in tups[:num_context_words]]
            y = np.divide(y_unnorm, np.max(y_unnorm).astype(np.float))
            distance = (bptt_steps - 1) - bptt_step
            xys.append((x, y, distance))
        # fig
        fig, ax = plt.subplots(figsize=(FigsConfigs.MAX_FIG_WIDTH, 4), dpi=FigsConfigs.DPI)
        ax.set_ylabel('Term Normalized Frequency', fontsize=FigsConfigs.AXLABEL_FONT_SIZE, labelpad=0.0)
        ax.set_xticks(x, minor=False)
        ax.set_xticklabels(ytlabels, minor=False, fontsize=FigsConfigs.AXLABEL_FONT_SIZE, rotation=90)
        ax.tick_params(axis='both', which='both', top='off', right='off')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # plot
        ax.plot(x, unigram_freqs_norm, '--', linewidth=FigsConfigs.LINEWIDTH, label='unigram frequencies',
                color='black')
        for x, y, distance in xys:
            ax.plot(x, y, '-', linewidth=FigsConfigs.LINEWIDTH, label='distance t-{}'.format(distance))
        plt.tight_layout()
        plt.legend()
        print('{} completed in {:.1f} secs'.format(sys._getframe().f_code.co_name, time.time() - start))
        return fig
