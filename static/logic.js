console.log("Connected")

//Initial chart placeholder

Plotly.d3.csv("Scoring.csv", function (data) {
    // Create a lookup table to sort and regroup the columns of data,
    // first by year, then by continent:
    console.log(data)
    // Create the plot:

    var x = []
    var y = []
    var goals = []
    var names = []
    for (i = 0; i < data.length; i++) {
        x.push(data[i].year);
        y.push(data[i].G);
        goals.push(data[i].G);
        names.push(data[i].playerID);
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
        yaxis: { title: 'Goals', range: [0, Math.max(y)] },
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

    Plotly.newPlot('myDiv', data, layout, { displayModeBar: false, responsive: true });
});

Plotly.d3.csv("current_nhl_data.csv", function (data) {
    // Create a lookup table to sort and regroup the columns of data,
    // first by year, then by continent:
    console.log(data)
    // Create the plot:

    var x = []
    var y = []
    var goals = []
    var names = []
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
        yaxis: { title: 'Goals', range: [0, Math.max(y)] },
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
});