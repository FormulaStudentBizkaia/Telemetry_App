

def createFigure1(dataDict,on,log,dato,value,onButtonTriger):
    if (on==False):
        if (onButtonTriger):
            log = log[0]
        filtered_data = dataDict[log][dataDict[log]['Time'].between(value[0], value[1])]
        figure_1 = {
            "data": [
                {
                    "x": filtered_data["Time"],
                    "y": filtered_data[dato],
                    "type": "lines",
                    "hovertemplate": "%{y:.2f}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": dato,
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"fixedrange": True},
                "colorway": ["#e30202","#302f2f", "#000000", "#15ff00", "#0062ff", "#ff00f7"],
            },
        }

        return figure_1, False
    else:
        if (onButtonTriger):
            filtered_data = dataDict[log][dataDict[log]['Time'].between(value[0], value[1])]
            figure_1 = {
                "data": [
                    {
                        "x": filtered_data["Time"],
                        "y": filtered_data[dato],
                        "type": "lines",
                        "hovertemplate": "%{y:.2f}<extra></extra>",
                    },
                ],
                "layout": {
                    "title": {
                        "text": dato,
                        "x": 0.05,
                        "xanchor": "left",
                    },
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"fixedrange": True},
                    "colorway": ["#e30202","#302f2f", "#000000", "#15ff00", "#0062ff", "#ff00f7"],
                },
            }

            return figure_1, True
        else:
            filtered_data = []
            for act in log:
                filtered_data.append(dataDict[act][dataDict[act]['Time'].between(value[0], value[1])])
            figure_1 = {
                "data": [
                    {
                        "x": cada["Time"],
                        "y": cada[dato],
                        "type": "lines",
                        "hovertemplate": "%{y:.2f}<extra></extra>",
                    }
                    for cada in filtered_data
                    ],
                "layout": {
                    "title": {
                        "text": dato,
                        "x": 0.05,
                        "xanchor": "left",
                    },
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"fixedrange": True},
                    "colorway": ["#e30202","#302f2f", "#000000", "#15ff00", "#0062ff", "#ff00f7"],
                },
            }

            return figure_1, True

def createFigure2(dataDict,on,log,dato,value,onButtonTriger, corner):
    cornerPrefix = "Wheel_" + str(corner) + "_"
    if (on==False):
        if(onButtonTriger):
            log = log[0]
        filtered_data = dataDict[log][dataDict[log]['Time'].between(value[0], value[1])]
        figure_2 = {
            "data": [
                {
                    "x": filtered_data["Time"],
                    "y": filtered_data[cornerPrefix + dato],
                    "type": "lines",
                    "hovertemplate": "%{y:.2f}<extra></extra>",
                },
            ],
            "layout": {
                "xaxis": {"fixedrange": True},
                "yaxis": {"fixedrange": True},
                "height": 300,
                "width": 450,
                "frameMargins": 0,
                "margin": {"autoexpand": False, "b": 30, "l" : 30, "r" : 10, "t" : 10},
                "colorway": ["#e30202","#302f2f", "#000000", "#15ff00", "#0062ff", "#ff00f7"],
            },
        }

        return figure_2
    else:
        if (onButtonTriger):
            filtered_data = dataDict[log][dataDict[log]['Time'].between(value[0], value[1])]
            figure_2 = {
                "data": [
                    {
                        "x": filtered_data["Time"],
                        "y": filtered_data[cornerPrefix + dato],
                        "type": "lines",
                        "hovertemplate": "%{y:.2f}<extra></extra>",
                    },
                ],
                "layout": {
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"fixedrange": True},
                    "height": 300,
                    "width": 450,
                    "frameMargins": 0,
                    "margin": {"autoexpand": False, "b": 30, "l" : 30, "r" : 10, "t" : 10},
                    "colorway": ["#e30202","#302f2f", "#000000", "#15ff00", "#0062ff", "#ff00f7"],
                },
            }

            return figure_2
        else:
            filtered_data = []
            for act in log:
                filtered_data.append(dataDict[act][dataDict[act]['Time'].between(value[0], value[1])])
            figure_2 = {
                "data": [
                    {
                        "x": cada["Time"],
                        "y": cada[cornerPrefix + dato],
                        "type": "lines",
                        "hovertemplate": "%{y:.2f}<extra></extra>",
                    }
                    for cada in filtered_data
                    ],
                "layout": {
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"fixedrange": True},
                    "height": 300,
                    "width": 450,
                    "frameMargins": 0,
                    "margin": {"autoexpand": False, "b": 30, "l" : 30, "r" : 10, "t" : 10},
                    "colorway": ["#e30202","#302f2f", "#000000", "#15ff00", "#0062ff", "#ff00f7"],
                },
            }

            return figure_2
