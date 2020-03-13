console.log("Connected")

//Initial chart placeholder

var url = "/api/data/current_scorers_data"
d3.json(url).then(function (data) {
    //filling the dropdown menu
    var subjectFilter = d3.select("#selPlayer")
    subjectFilter.selectAll("option").remove();
    var nameList = []

    data.forEach(item => {
        var fullName = `${item.lastname}, ${item.firstname} `;
        if (nameList.includes(fullName)) { } else {
            var row = subjectFilter.append("option")
            nameList.push(fullName)
            row.append("option").text(fullName).attr("value", item.id);
        }

    })
    //update chart on dropdown change
    var id = 8445000
    var id2 = 8447400;
    //eventListener
    d3.selectAll("#selPlayer").on("change", selection);
    function selection() {
        var selectedPlayer = d3.select("#selPlayer option:checked").select("option");
        var id = selectedPlayer.attr("value");
        var name = selectedPlayer.text();
        console.log("Menu Change: ", id, name)
        var url = "/api/data/current_scorers_data";
        d3.json(url).then(function (data) {
            console.log("Selection data connected")

            var selectedid = id;
            var G_record = 8447400;

            var results = data.filter(function (item) {
                return item.id == selectedid;

            });
            var resultsG = data.filter(function (item) {
                return item.id == G_record;

            });
            var selectedPlayer = ("Player's name", results[0].lastname);

            var x = []
            var x2 = []
            var y = []
            var y2 = []

            var goals = []
            var names = []
            var rank = []

            for (i = 0; i < results.length; i++) {
                x.push(results[i].gameid);
                y.push(results[i].sumgoals);
                goals.push(results[i].sumgoals);
                names.push(results[i].lastname);
            }

            for (i = 0; i < resultsG.length; i++) {
                x2.push(resultsG[i].gameid);
                y2.push(resultsG[i].sumgoals);

            }

            var trace1 = {
                x: x,
                y: y,
                mode: 'markers',
                type: 'scatter',
                name: ` ${selectedPlayer}`,
                // text: ['A-1', 'A-2', 'A-3', 'A-4', 'A-5'],
                marker: {
                    color: x,
                    colorscale: 'Bluered',
                    // size: goals,
                },
            };
            var trace2 = {
                x: x2,
                y: y2,
                // type: 'scatter',
                name: "Wayne Gretzky Record",
                marker: { size: 6, color: "red" },
                text: ["RECORD"],
                mode: 'lines',
                line: {
                    dash: 'dot',
                    width: 4
                }

            }


            var data = [trace1, trace2];

            var layout = {
                xaxis: {
                    title: "Games Played",
                    range: [1, 2000],
                    showline: true,
                    showgrid: false,
                },
                yaxis: {
                    title: "Career Goals",
                    range: [0, 1000]
                },
                title: `Career Goals of ${selectedPlayer} Vs. Gretzky's Record`,
                colorscale: 'YIGnBu',
                hovermode: 'closest',
            };


            Plotly.react('myDiv', data, layout, { displayModeBar: false });

        })

    };
    ;

    var selectedid = id;
    var G_record = id2;

    var results = data.filter(function (item) {
        return item.id == selectedid;

    });
    var resultsG = data.filter(function (item) {
        return item.id == G_record;

    });
    var selectedPlayer = ("Player's name", results[0].lastname);

    var x = []
    var x2 = []
    var y = []
    var y2 = []

    var goals = []
    var names = []
    var rank = []

    for (i = 0; i < results.length; i++) {
        x.push(results[i].gameid);
        y.push(results[i].sumgoals);
        goals.push(results[i].sumgoals);
        names.push(results[i].lastname);
    }

    for (i = 0; i < resultsG.length; i++) {
        x2.push(resultsG[i].gameid);
        y2.push(resultsG[i].sumgoals);

    }

    var trace1 = {
        x: x,
        y: y,
        mode: 'markers',
        type: 'scatter',
        name: ` ${selectedPlayer}`,
        // text: ['A-1', 'A-2', 'A-3', 'A-4', 'A-5'],
        marker: {
            color: x,
            colorscale: 'Bluered',
            // size: goals,
        },
    };
    var trace2 = {
        x: x2,
        y: y2,
        type: 'scatter',
        name: "Wayne Gretzky Record",
        marker: { size: 6 },
        text: ["RECORD"],
        name: "Wayne Gretzky Record",
        marker: { size: 6, color: "red" },
        text: ["RECORD"],
        mode: 'lines',
        line: {
            dash: 'dot',
            width: 4
        }
    }


    var data = [trace1, trace2];

    var layout = {
        xaxis: {
            title: "Games Played",
            range: [1, 2000]
        },
        yaxis: {
            title: "Career Goals",
            range: [0, 1000]
        },
        title: `Career Goals of ${selectedPlayer} Vs. Gretzky's Record`,
        colorscale: 'YIGnBu',
        hovermode: 'closest',
    };


    Plotly.react('myDiv', data, layout, { displayModeBar: false });



});


//chart -2

var url = "/api/data/historic_data"

d3.json(url).then(function (data) {

    var x = []
    var y = []
    var goals = []
    var names = []
    var rank = []

    for (i = 0; i < data.length; i++) {
        x.push(data[i].Season);
        y.push(data[i].Goals_Scored);
        goals.push(data[i].Goals_Scored);
        names.push(data[i].Player);
    }

    var trace1 = {
        x: x,
        y: y,
        type: 'scatter',
        text: names,
        mode: 'markers',
        marker: {
            color: y,
            colorscale: 'Bluered',
            // size: goals,
        },
        transforms: [{
            type: 'aggregate',
            groups: names,
            aggregations: [
                { target: 'y', func: 'avg', enabled: true },
                { target: 'x', func: '', enabled: true },
            ]
        }]
    };
    var config = { responsive: true }

    var data = [trace1];

    layout = {
        title: '<b>NHL Scoring Statistics</b><br>use dropdown to change statistic',
        xaxis: { title: '' },
        yaxis: {
            title: 'Goals', range: [0, Math.max(y
            )]
        },
        height: 600,
        width: 800,
        colorscale: 'YIGnBu',
        hovermode: 'closest',
        updatemenus: [{
            x: 1.15,
            y: 1.15,
            xref: 'paper',
            yref: 'paper',
            yanchor: 'top',
            active: 0,
            showactive: false,
            buttons: [{
                method: 'restyle',
                args: ['transforms[0].aggregations[0].func', 'avg'],
                label: 'Average goals per season'
            }, {
                method: 'restyle',
                args: ['transforms[0].aggregations[0].func', 'sum'],
                label: 'Total career goals'
            }, {
                method: 'restyle',
                args: ['transforms[0].aggregations[0].func', 'min'],
                label: 'Min goals/season in a career'
            }, {
                method: 'restyle',
                args: ['transforms[0].aggregations[0].func', 'max'],
                label: 'Max goals/season in a career'
            }, {
                method: 'restyle',
                args: ['transforms[0].aggregations[0].func', 'median'],
                label: 'Median goals in a  career'
            }, {
                method: 'restyle',
                args: ['transforms[0].aggregations[0].func', 'first'],
                label: 'Goals in first season'
            }, {
                method: 'restyle',
                args: ['transforms[0].aggregations[0].func', 'last'],
                label: 'Goals in last season'
            }]
        }]
    }

    Plotly.newPlot('myDiv2', data, layout, { displayModeBar: false, responsive: true });

    var myPlot = document.getElementById('myDiv2'),
        hoverInfo = document.getElementById('hoverinfo');


    myPlot.on('plotly_hover', function (data) {
        var infotext = data.points.map(function (d) {
            return (d.text + ': Starting Season= ' + d.x + ', Goals= ' + d.y.toPrecision(3));
        });

        hoverInfo.innerHTML = infotext.join('<br/>');
    })
        .on('plotly_unhover', function (data) {
            hoverInfo.innerHTML = '';
        });

    // Click function
    myPlot.on('plotly_click', function (data) {
        var pts = '';
        for (var i = 0; i < data.points.length; i++) {
            annotate_text = 'Starting Season = ' + data.points[i].x +
                ' Goals = ' + data.points[i].y.toPrecision(4);

            annotation = {
                text: annotate_text,
                x: data.points[i].x,
                y: parseFloat(data.points[i].y.toPrecision(4))
            }

            annotations = self.layout.annotations || [];
            annotations.push(annotation);
            Plotly.relayout('myDiv2', { annotations: annotations })
        }
    });
});






