



@app.route('/show_windows/<string:model_name>/', methods=['GET', 'POST'])
def show_windows(model_name):
    timepoint = 0
    hub_mode = make_requested(request, session, 'hub_mode', default=GlobalConfigs.HUB_MODES[0])
    model = Model(model_name, timepoint)
    model.hub.switch_mode(hub_mode)
    windows_tables = []
    # form
    form = make_form(model, request, AppConfigs.DEFAULT_FIELD_STR, 'probe')
    # make windows_tables
    if form.validate():
        probes = form.field.data
        for probe in probes.split():
            probe_id = model.hub.probe_store.probe_id_dict[probe]
            probe_x_mat = model.hub.probe_x_mats[model.hub.probe_store.probe_id_dict[probe]]
            probe_context_df = pd.DataFrame(index=[probe_id] * len(probe_x_mat), data=probe_x_mat)
            table_df = probe_context_df.apply(
                lambda term_ids: [model.hub.train_terms.types[term_id] for term_id in term_ids])
            windows_table = table_df.to_html(index=False, header=False).replace('border="1"', 'border="0"')
            windows_tables.append(windows_table)
    return render_template('windows.html',
                           template_dict=make_template_dict(session),
                           model_name=model_name,
                           timepoint=model.timepoint,
                           form=form,
                           windows_tables=windows_tables)
