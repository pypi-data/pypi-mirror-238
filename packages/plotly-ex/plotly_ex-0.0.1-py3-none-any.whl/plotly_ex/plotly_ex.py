# make_subplots: https://plotly.com/python-api-reference/generated/plotly.subplots.make_subplots.html
# Figure: https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
# 制約1(個別のbarmode設定不可): https://community.plotly.com/t/how-to-set-barmode-for-individual-subplots/47931 https://stackoverflow.com/questions/50695971/plotly-stacked-bars-only-in-specific-subplots
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
px.defaults.template = 'plotly_dark'
from collections import defaultdict
class make_subplots_wrapper:
    """
    fig_wrapper = ex.make_subplots_wrapper()
    fig_sub_title = '実行成否'
    color_discrete_map = {'success': 'skyblue', 'error.operation-mode.nooperation': 'gray', 'error.other': 'purple'}
    fig_sub = px.bar(df_show, x='start_datetime', color='execusion_result', color_discrete_map=color_discrete_map)
    fig_sub.update_layout(xaxis={'showticklabels': False})
    fig_sub.update_xaxes(title=None)
    fig_sub.update_yaxes(tickvals=[0, 1], title_text=fig_sub_title)
    fig_wrapper.add_fig_sub(fig_sub=fig_sub, fig_sub_title=None, row=1, col=1, colspan=1, legendgroup=fig_sub_title)
    fig = fig_wrapper.build_fig(row_height=120)
    fig.update_layout(barmode='stack')
    fig.update_layout(title=f"ODU: {odu_label} ({mode})", title_font=dict(size=18), title_x=0.05)
    fig.update_layout(margin=dict(l=150))  # lは左側の余白
    fig.show()
    """
    def __init__(self, col_max:int=5) -> None:
        self.fig_sub_dict_list = []
        self.col_max = col_max

    def add_fig_sub(self, fig_sub, fig_sub_title:str=None, row:int=None, col:int=None, rowspan:int=1, colspan:int=1, secondary_y:bool=None, legendgroup:str=None) -> None:
        if row is None and col is None and rowspan == 1 and colspan == 1:
            next_index = len(self.fig_sub_dict_list)
            row, col = self._1dim_index_to_2dim_row_col(next_index)
        fig_sub_dict = {'fig_sub': fig_sub, 'fig_sub_title': fig_sub_title, 'row': row, 'col': col, 'rowspan': rowspan, 'colspan': colspan, 'secondary_y': secondary_y, 'legendgroup': legendgroup}
        self.fig_sub_dict_list.append(fig_sub_dict)
    
    def _1dim_index_to_2dim_row_col(self, index) -> tuple:
        row = (index // self.col_max) + 1
        col = (index % self.col_max) + 1
        return row, col
    
    def build_fig(self, row_height=250, shared_xaxes=False, shared_yaxes=False, font_size_default=14, coloraxis_colorscale=None, template='plotly_dark', **kwargs) -> go.Figure:
        row_max = max(fig_sub_dict["row"] + fig_sub_dict["rowspan"] - 1 for fig_sub_dict in self.fig_sub_dict_list)
        col_max = max(fig_sub_dict["col"] + fig_sub_dict["colspan"] - 1 for fig_sub_dict in self.fig_sub_dict_list)

        fig_sub_title_list = [[None for _ in range(col_max)] for _ in range(row_max)]
        specs = [[{} for _ in range(col_max)] for _ in range(row_max)]
        for fig_sub_dict in self.fig_sub_dict_list:
            row, col, rowspan, colspan = fig_sub_dict['row'], fig_sub_dict['col'], fig_sub_dict['rowspan'], fig_sub_dict['colspan']
            secondary_y = fig_sub_dict['secondary_y']
            fig_sub_title = fig_sub_dict['fig_sub_title']
            type_ = fig_sub_dict['fig_sub'].data[0].type if fig_sub_dict['fig_sub'].data and not secondary_y else 'xy'
            fig_sub_title_list[row - 1][col - 1] = fig_sub_title
            specs[row - 1][col - 1] = {'rowspan': rowspan, 'colspan': colspan, 'type': type_, 'secondary_y': secondary_y}
        fig_sub_title_list_flatten = [item for sublist in fig_sub_title_list for item in sublist]
        
        fig = make_subplots(rows=row_max, cols=col_max, shared_xaxes=shared_xaxes, shared_yaxes=shared_yaxes, subplot_titles=fig_sub_title_list_flatten, specs=specs, **kwargs) # , subplot_titles=fig_sub_title_list
        for annotation in fig['layout']['annotations']:
            annotation['font'] = {'size': font_size_default}        
        legendgroup_tracename_set = defaultdict(set) # legendが重複するのでlegendgroupごとに初出のlegendだけをshowlegend設定するための記録用set
        for fig_sub_dict in self.fig_sub_dict_list:
            row, col = fig_sub_dict['row'], fig_sub_dict['col']
            fig_sub:go.Figure = fig_sub_dict['fig_sub']
            secondary_y = fig_sub_dict['secondary_y']
            legendgroup = fig_sub_dict['legendgroup']
            fig_sub.for_each_trace(lambda trace: trace.update(showlegend=False) if hasattr(trace, 'showlegend') and trace.name in legendgroup_tracename_set[legendgroup] else None) \
                   .for_each_trace(lambda trace: trace.update(legendgroup=legendgroup) if hasattr(trace, 'legendgroup') else None) \
                   .for_each_trace(lambda trace: trace.update(legendgrouptitle_text=legendgroup) if hasattr(trace, 'legendgroup') else None) \
                   .for_each_trace(lambda trace: legendgroup_tracename_set[legendgroup].add(trace.name)) \
                   .for_each_trace(lambda trace: trace.update(bingroup=None) if isinstance(trace, go.Histogram) else None) # histogramのbingroupは解除する(必要があれば引数で制御可能にするがfacetもあるし不要だと思う)
            # fig_sub.update_layout(title_text='title!') # no work
            for trace in fig_sub.select_traces():
                fig.add_trace(trace, row=row, col=col, secondary_y=secondary_y)
            for shape in fig_sub.select_shapes():
                fig.add_shape(shape, row=row, col=col)
            for annotation in fig_sub.select_annotations():
                fig.add_annotation(annotation, row=row, col=col)
            for xaxes in fig_sub.select_xaxes():
                xaxes_added = {key: value for key, value in xaxes.to_plotly_json().items() if key not in ['anchor', 'domain']} # anchorは関連するyのIDかなんか、domainは描画範囲っぽい
                fig.update_xaxes(xaxes_added, row=row, col=col)
            for yaxes in fig_sub.select_yaxes():
                yaxes_added = {key: value for key, value in yaxes.to_plotly_json().items() if key not in ['anchor', 'domain']}
                fig.update_yaxes(yaxes_added, row=row, col=col, secondary_y=secondary_y)
        fig.update_layout(height=row_height*row_max)
        fig.update_layout(coloraxis_autocolorscale=False, coloraxis_colorscale=coloraxis_colorscale) if coloraxis_colorscale else None
        fig.update_layout(template=template) if template else None
        fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)')) if template == 'plotly_dark' else None
        return fig
