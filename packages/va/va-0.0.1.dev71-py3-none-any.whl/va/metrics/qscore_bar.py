import pandas as pd
# import plotly.graph_objects as go
# import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import json


def load_qscore(input_file, new_entry):
    """

    """

    type_dict = {'ids': str, 'resolution': float, 'names': str, 'qscores': float}
    # df_nonew = pd.read_csv(input_file, dtype=type_dict).drop('Unnamed: 0', axis=1)
    df_nonew = pd.read_csv(input_file, dtype=type_dict)
    df = df_nonew.append(new_entry, ignore_index=True)
    # res_qscore = df[['resolution','qscores']].copy()
    df_without_nan = df[~df.isnull().any(axis=1)].sort_values(by='qscores').reset_index()

    return df_without_nan


def get_qscores(df, input_value):
    n = df.shape[0]
    qmin = df['qscores'].min()
    qmax = df['qscores'].max()
    large = df[df['qscores'] > input_value].shape[0]
    small = df[df['qscores'] <= input_value].shape[0]

    return (qmin, qmax), (small, large)


def match_to_newscale(original_scale, target_scale, original_value):
    original_min = original_scale[0]
    original_max = original_scale[1]

    target_min = target_scale[0]
    target_max = target_scale[1]

    target_value = ((original_value - original_min) / (original_max - original_min)) * (
                target_max - target_min) + target_min

    return target_value


def get_nearest_onethousand(new_entry, df, n):
    """
        Sort the qscore based on resolution and then
    """

    # Find the index of the nearest row to the target value
    cdf = df.sort_values(by='resolution').reset_index()
    # nearest_index = (cdf['qscores'] - new_entry['qscores']).abs().idxmin()
    nearest_index = cdf[cdf['ids'] == new_entry['ids']].index.to_list()[0]

    # Get the 1000 rows centered around the nearest index
    start = max(nearest_index - n, 0)
    end = min(nearest_index + n, len(df))
    df_nearest = cdf.iloc[start:end + 1]

    return df_nearest


def plot_bar(a, b, qmin, qmax):
    data = [range(0, 200), range(0, 200)]
    # data = [np.sort(np.random.random(200))]
    # data = [df['qscores'].sort_values(), df['qscores'].sort_values(), df['qscores'].sort_values(), df['qscores'].sort_values()]
    fig = px.imshow(data, color_continuous_scale=px.colors.sequential.RdBu)
    fig.add_trace(go.Scatter(x=[a], y=[0],
                             mode='markers',
                             marker=dict(
                                 color='LightSkyBlue',
                                 symbol='diamond-tall',
                                 size=20,
                                 line=dict(
                                     color='MediumPurple',
                                     width=2
                                 )
                             ),
                             name='markers'))
    fig.add_trace(go.Scatter(x=[b], y=[0],
                             mode='markers',
                             marker=dict(
                                 color='LightGreen',
                                 symbol='diamond-tall',
                                 size=20,
                                 line=dict(
                                     color='MediumPurple',
                                     width=2
                                 )
                             ),
                             name='markers'))
    fig.layout.coloraxis.showscale = False
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 199],
            ticktext=[qmin, qmax]
        )
    )
    # fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(showlegend=False)
    fig.write_image('/Users/zhe/Downloads/alltempmaps/q-scale.png')
    fig.show()


def plot_bar_mat(a, b, qmin, qmax):
    """
    This function here using matplotlib to produce the Q-score bar image
    """

    a /= 200
    b /= 200
    # Create a color scale from 0 to 1
    color_scale = np.linspace(0, 1, 256)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(6, 2))

    # Plot the color scale with a thinner aspect ratio
    ax.imshow([color_scale], cmap='viridis', aspect=0.05, extent=[0, 1, 0, 1])

    # Calculate the height and half-width of the diamonds
    diamond_height = 0.65
    diamond_half_width = 0.01

    # Add diamond-shaped marker for 'a'
    ax.fill(
        [a - diamond_half_width, a, a + diamond_half_width, a],
        [0.5, 0.5 + diamond_height, 0.5, 0.5 - diamond_height],
        color='red', edgecolor='black'
    )

    # Add diamond-shaped marker for 'b'
    ax.fill(
        [b - diamond_half_width, b, b + diamond_half_width, b],
        [0.5, 0.5 + diamond_height, 0.5, 0.5 - diamond_height],
        color='pink', edgecolor='black'
    )

    # add four values as annotations
    ax.annotate(f'{qmin:.2f}', (0, -0.8), color='black', ha='center', fontsize=10)
    ax.annotate(f'{qmax:.2f}', (1, -0.8), color='black', ha='center', fontsize=10)
    if a >= b:
        ax.annotate(f'{a * 100:.2f}%', (a, -0.8), color='black', ha='left', fontsize=10)
        # ax.annotate(f'{b:.2f}', (b, -0.8), color='black', ha='center', fontsize=10)
        # ax.annotate(f'{a*100:.2f}%', (a, 1.4), color='black', ha='center', fontsize=10)
        ax.annotate(f'{b * 100:.2f}%', (b, 1.4), color='black', ha='right', fontsize=10)
    else:
        ax.annotate(f'{a * 100:.2f}%', (a, -0.8), color='black', ha='right', fontsize=10)
        # ax.annotate(f'{b:.2f}', (b, -0.8), color='black', ha='center', fontsize=10)
        # ax.annotate(f'{a*100:.2f}%', (a, 1.4), color='black', ha='center', fontsize=10)
        ax.annotate(f'{b * 100:.2f}%', (b, 1.4), color='black', ha='left', fontsize=10)

    # Customize the plot
    ax.set_xlim(-0.05, 1)
    ax.set_ylim(-4.3, 1.6)
    # ax.set_xticks([0, a, b, 1])
    # ax.set_xticklabels([0, f'{a:.2f}', f'{b:.2f}', 1])
    ax.set_yticks([])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Remove the left and bottom axis lines (optional)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Add diamond-shaped marker for legend
    wa = 0.01
    ha = -2.0
    ax.fill(
        [wa - diamond_half_width, wa, wa + diamond_half_width, wa],
        [ha, ha + diamond_height, ha, ha - diamond_height],
        color='red', edgecolor='black'
    )
    ax.annotate(f'Percentile relative to all EMDB models', (wa + 3 * diamond_half_width, ha - 0.25), color='black',
                ha='left', fontsize=11)

    bwa = 0.01
    bha = -3.6
    ax.fill(
        [bwa - diamond_half_width, bwa, bwa + diamond_half_width, bwa],
        [bha, bha + diamond_height, bha, bha - diamond_height],
        color='pink', edgecolor='black'
    )
    ax.annotate(f'Percentile relative to nearest 1000 (resolution) EM models',
                (bwa + 3 * diamond_half_width, bha - 0.25), color='black', ha='left', fontsize=11)

    ax.tick_params(axis='both', which='both', length=0)
    plt.gca().set_xticklabels([])
    # Show the plot
    plt.show()


def get_json_info(jsonfile):
    """
    Function here is used to take the all json file and give the input dictionary for Q-score scale bar
    :param jsonfile: qscore json file name
    :return: dictionary like {'ids': '8117', 'resolution': 2.95, 'names': '5irx.cif', 'qscores': 0.521}
    """

    with open(jsonfile, "r") as json_file:
        jdata = json.load(json_file)
        eid = jdata.keys()[0]
        if 'resolution' in jdata[eid]:
            resolution = jdata[eid]['resolution']
        else:
            resolution = None
        if 'qscore' in jdata[eid]:
            allnames = jdata[eid]['qscore']
            if len(allnames) == 1:
                names = allnames[0]['name']
                qscores = allnames[0]['data']['averageqscore']
            else:
                names = []
                qscores = []
                for i in range(0, len(allnames)):
                    names.append(allnames[i]['name'])
                    qscores.append(allnames[i]['data']['averageqscore'])
        else:
            names = None
            qscores = None

    result = []
    if resolution and names and qscores:
        if len(names) == 1:
            result.append({'ids': eid, 'resolution': float(resolution), 'name': names[0], 'qscore': qscores[0]})
        elif len(names) > 1:
            for i in range(0, len(names)):
                result.append({'ids': eid, 'resolution': float(resolution), 'name': names[i], 'qscore': qscores[i]})
        else:
            print('Something wrong with the JSON file.')
    else:
        print('At least one of resolution, name and qscore is missing.')


    return result if result else None






if __name__ == '__main__':
    input_file = '/Users/zhe/Downloads/alltempmaps/qscores.csv'
    new_entry_dict = {'ids': '8117', 'resolution': 2.95, 'names': '5irx.cif', 'qscores': 0.521}
    df = load_qscore(input_file, new_entry_dict)
    index = df[df['ids'] == '00000'].index
    row = df.iloc[index,]
    (qmin, qmax), original_value = get_qscores(df, new_entry_dict['qscores'])
    target_value = int(match_to_newscale((0, sum(original_value)), (0, 199), original_value[0]))

    df1000 = get_nearest_onethousand(new_entry_dict, df, 500)
    (sqmin, sqmax), ovalue = get_qscores(df1000, new_entry_dict['qscores'])
    print(sqmin, sqmax)
    print(ovalue)
    target_value_40 = int(match_to_newscale((0, sum(ovalue)), (0, 199), ovalue[0]))
    print(target_value)
    print(target_value_40)
    plot_bar_mat(target_value, target_value_40, qmin, qmax)
