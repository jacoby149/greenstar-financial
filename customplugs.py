import matplotlib
from mpld3 import plugins



class customHover(plugins.PluginBase):
    """A Plugin to enable an HTML tooltip:
    formated text which hovers over points.
    Parameters
    ----------
    points : matplotlib Collection or Line2D object
        The figure element to apply the tooltip to
    labels : list
        The labels for each point in points, as strings of unescaped HTML.
    targets : list
        The urls that each point will open when clicked.
    hoffset, voffset : integer, optional
        The number of pixels to offset the tooltip text.  Default is
        hoffset = 0, voffset = 10
    css : str, optional
        css to be included, for styling the label html if desired
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mpld3 import fig_to_html, plugins
    >>> fig, ax = plt.subplots()
    >>> points = ax.plot(range(10), 'o')
    >>> labels = ['<h1>{title}</h1>'.format(title=i) for i in range(10)]
    >>> plugins.connect(fig, PointHTMLTooltip(points[0], labels))
    >>> fig_to_html(fig)
    """

    JAVASCRIPT = """
    mpld3.register_plugin("htmltooltip", HtmlTooltipPlugin);
    HtmlTooltipPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    HtmlTooltipPlugin.prototype.constructor = HtmlTooltipPlugin;
    HtmlTooltipPlugin.prototype.requiredProps = ["id"];
    HtmlTooltipPlugin.prototype.defaultProps = {labels:null,
                                                target:null,
                                                hoffset:0,
                                                voffset:10,
                                                targets:null};
    function HtmlTooltipPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };
    HtmlTooltipPlugin.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        var labels = this.props.labels;
        var targets = this.props.targets;
        var tooltip = d3.select("body").append("div")
            .attr("class", "mpld3-tooltip")
            .style("position", "absolute")
            .style("z-index", "10")
            .style("visibility", "hidden");
        obj.elements()
            .on("mouseover", function(d, i){
                tooltip.html(labels[i])
                    .style("visibility", "visible");
            })
            .on("mousemove", function(d, i){
                tooltip
                .style("top", d3.event.pageY + this.props.voffset + "px")
                .style("left",d3.event.pageX + this.props.hoffset + "px");
            }.bind(this))
            .on("mousedown.callout", function(d, i){
                window.open(targets[i],"_blank");
            })
            .on("mouseout", function(d, i){
                tooltip.style("visibility", "hidden");
            });
    };
    """

    def __init__(self, points, labels=None, targets=None,
                 hoffset=0, voffset=10, css=None):
        self.points = points
        self.labels = labels
        self.targets = targets
        self.voffset = voffset
        self.hoffset = hoffset
        self.css_ = css or ""
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None
        self.dict_ = {"type": "htmltooltip",
                      "id": plugins.get_id(points, suffix),
                      "labels": labels,
                      "targets": targets,
                      "hoffset": hoffset,
                      "voffset": voffset}