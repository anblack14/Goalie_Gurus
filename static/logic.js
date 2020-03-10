console.log("Connected")

//Initial chart placeholder

var url = "/api/data/current_scorers_data"
d3.json(url).then(function (data) {
    //filling the dropdown menu

    var subjectFilter = d3.select("#selPlayer")
    subjectFilter.selectAll("option").remove();

    data.forEach(item => {
        var fullName = `${item.lastname}, ${item.firstname} `;
        var row = subjectFilter.append("option")
        var nameList=[]
        row.append("option").text(fullName).attr("value", item.id);
    })

    //update chart on dropdown change

    //eventListener
    d3.selectAll("#selPlayer").on("change", selection);
    function selection() {
        var selectedPlayer = d3.select("#selPlayer option:checked").select("option");
        var id = selectedPlayer.attr("value");
        var name = selectedPlayer.text();
        console.log("Menu Change: ", id, name)
    };
    selection()
        ;

    var selectedid = 8448000;
    var results = data.filter(function (item) {
        return item.id == selectedid;

        var x = []
        var y = []
        var goals = []
        var names = []
        var rank = []


    });
    console.log("Player's name", results[0].lastname)
    var x = []
    var y = []
    var goals = []
    var names = []
    var rank = []

    for (i = 0; i < results.length; i++) {
        x.push(results[i].gameid);
        y.push(results[i].sumgoals);
        goals.push(results[i].sumgoals);
        names.push(results[i].lastname);
    }

    var trace1 = {
        x: x,
        y: y,
        mode: 'markers',
        type: 'scatter',
        name: 'Career Goals',
        // text: ['A-1', 'A-2', 'A-3', 'A-4', 'A-5'],
        marker: {
            color: x,
            colorscale: 'Bluered',
            // size: goals,
        },
    };
    var trace2 = {
        x: [1487],
        y: [894],
        type: 'scatter',
        name: "Wayne Gretzky Record",
        marker: { size: 6 },
        text: ["RECORD"]

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
        title: 'Career Goals',
        colorscale: 'YIGnBu',
        hovermode: 'closest',
    };


    Plotly.newPlot('myDiv', data, layout);



});


//chart -2

var url = "/api/data/historic_data"
d3.json(url).then(function (data) {

});

d3.json(url).then(function (data) {

    var x = []
    var y = []
    var goals = []
    var names = []
    var rank = []

    for (i = 0; i < data.length; i++) {
        x.push(data[i].Year);
        y.push(data[i].Goals);
        goals.push(data[i].Goals);
        names.push(data[i].Player);
    }

    var trace1 = {
        x: x,
        y: y,
        type: 'scatter',
        text: names,
        mode: 'markers',
        marker: {
            color: x,
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
        xaxis: { title: 'Year' },
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
            // console.log(d.text);
            return (d.text + ': Year= ' + d.x + ', Goals= ' + d.y.toPrecision(3));
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
            annotate_text = 'x = ' + data.points[i].x +
                'y = ' + data.points[i].y.toPrecision(4);

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



//Chart_3

var url = "/api/data/historic_data"
d3.json(url).then(function (data) {
});

d3.json(url).then(function (data) {

    var x = []
    var y = []
    var goals = []
    var names = []
    var rank = []

    for (i = 0; i < data.length; i++) {
        x.push(data[i].Year);
        y.push(data[i].Goals);
        goals.push(data[i].Goals);
        names.push(data[i].Player);
    }
    // console.log("X", x)
    // console.log("goals", goals);
    // console.log("names", names)
    var trace1 = {
        x: x,
        y: y,
        type: 'scatter',
        text: names,
        mode: 'markers',
        marker: {
            color: x,
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
        xaxis: { title: 'Year' },
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

    Plotly.newPlot('myDiv3', data, layout, { displayModeBar: false, responsive: true });

    var myPlot = document.getElementById('myDiv3'),
        hoverInfo = document.getElementById('hoverinfo2');


    myPlot.on('plotly_hover', function (data) {
        var infotext = data.points.map(function (d) {
            // console.log(d.text);
            return (d.text + ': Year= ' + d.x + ', Goals= ' + d.y.toPrecision(3));
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
            // annotate_text = 'x = ' + data.points[i].x +
            //     'y = ' + data.points[i].y.toPrecision(4);
            annotate_text = data.points.map(function (d) {
                console.log(d.text);
                return (d.text);
            });
            annotation = {
                text: annotate_text,
                x: data.points[i].x,
                y: parseFloat(data.points[i].y.toPrecision(4))
            }

            annotations = self.layout.annotations || [];
            annotations.push(annotation);
            Plotly.relayout('myDiv3', { annotations: annotations })
        }
    });

    console.log("Data completed")
});


