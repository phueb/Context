from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask import session
from flask import jsonify
import argparse
from itertools import chain
import socket

from ludwigviz.io import get_requested_log_dicts
from ludwigviz.io import make_log_dicts
from ludwigviz.io import get_projects_info

from ludwigviz.app_utils import make_form
from ludwigviz.app_utils import figs_to_imgs
from ludwigviz.app_utils import get_log_dicts_values
from ludwigviz.app_utils import LudwigVizEmptySubmission

from ludwigviz import config
from ludwigviz import __version__
from ludwigviz import __package__


topbar_dict = {'listing': config.RemoteDirs.research_data,
               'hostname': socket.gethostname(),
               'version': __version__,
               'title': __package__.capitalize()}

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/', methods=['GET', 'POST'])
def home():

    table_headers, rows = get_projects_info()

    return render_template('home.html',
                           topbar_dict=topbar_dict,
                           rows=rows,
                           headers=table_headers)

@app.route('/field/<string:model_name>/<string:btn_name>', methods=['GET', 'POST'])
def field(model_name, btn_name):
    # form
    form = make_form(model, request, config.Default.field_input, config.Default.valid_type)
    # autocomplete
    if valid_type == 'probe':
        session['autocomplete_list'] = list(hub.probe_store.types)
    elif valid_type == 'cat':
        session['autocomplete_list'] = list(hub.probe_store.cats)
    elif valid_type == 'term':
        session['autocomplete_list'] = list(hub.train_terms.types)
    else:
        session['autocomplete_list'] = []
    # request
    if form.validate():
        field_input = form.field.data.split()
        figs = model_btn_name_figs_fn_dict[btn_name](model, field_input)
        imgs = figs_to_imgs(*figs)
        return render_template('imgs.html',
                               topbar_dict=topbar_dict,
                               model_name=model_name,
                               timepoint=timepoint,
                               hub_mode=hub_mode,
                               imgs=imgs,
                               imgs_desc=imgs_desc)
    else:
        return render_template('field.html',
                               topbar_dict=topbar_dict,
                               model_name=model_name,
                               timepoint=timepoint,
                               hub_mode=hub_mode,
                               form=form,
                               btn_name=btn_name)



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


if __name__ == "__main__":  # pycharm does not use this
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action="store_false", default=True, dest='debug',
                        help='Use this for deployment.')
    argparse_namespace = parser.parse_args()

    app.run(port=5000, debug=argparse_namespace.debug, host='0.0.0.0')
