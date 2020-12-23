////////////////////////////////
// NO NETWORKING JAVASCRIPT  ///
////////////////////////////////

//make the last selected point on the markowitz curve null
last = null;


//Load inputs from URL into the form.
function linkload() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    keys = urlParams.keys()
    for (const key of keys) {
        console.log(key)
        console.log(document.getElementsByName(key))
        input = document.getElementsByName(key)[0];
        input.value = decodeURIComponent(urlParams.get(key));
    }
}

//Make a link with all of the form inputs
function linkmake() {

    //add risk to the hidden risk input value
    document.getElementById("risk").value = risk;

    inputs = document.getElementById("captable").getElementsByTagName("input");
    const urlParams = new URLSearchParams();
    for (input of inputs) {
        urlParams.set(input.name, encodeURIComponent(input.value))
    }
    //for risk slider
    return window.location + "?" + urlParams.toString()
}


function showhide() {
    cap = document.getElementById("captable")
    if (cap.style.display == "none") cap.style.display = "block";
    else cap.style.display = "none";
}

function update_vals() {
    std = stds[risk]
    mean = means[risk]
    portfolio = portfolios[risk]
    console.log(portfolios)
    document.getElementById("std").innerHTML = "Risk: " + Math.round(std * 10000) / 100 + "%"
    document.getElementById("mean").innerHTML = "Return: " + Math.round(mean * 10000) / 100 + "%"
    //document.getElementById("weight").innerHTML = "Portfolio : " + portfolio + "%"
}


////////////////////////////////
//  NETWORKING JAVASCRIPT  /////
////////////////////////////////

// image return
function load_graphs(data) {
    document.getElementById("message").innerHTML = "";
    console.log(data)
    $("#graphs").empty();
    $("#graphs").append(data["images"]);
    //document.getElementById("graphs").innerHTML = data["images"]
    stds = eval(data["risks"])
    means = eval(data["returns"])
    portfolios = eval(data["portfolios"])
    update_vals()
    cap = document.getElementById("captable");
    cap.style.display = "none";
}

function graphs() {
    document.getElementById("link").href = linkmake();
    document.getElementById("link").style.display = "block";
    form = {}
    $('#captable').serializeArray().map(function (x) { form[x.name] = x.value })

    document.getElementById("message").innerHTML = "Loading Graphs ...";
    $.post("/load_graphs", form, load_graphs)
        .fail(function (error) {
            document.getElementById("message").innerHTML = "Please Fill Out The Form.";
        });

}


//Backtesting functions

function load_backtest(data) {
    document.getElementById("backtest").innerHTML = data["backtest"]
    document.getElementById("weights").innerHTML = data["weights"]
}

function backtest() {
    $.post("/back", { "risk": risk }, load_backtest);
}

// Generate Report
function genReport() {
    if (document.getElementById("mean").innerHTML != "") {
        form = document.getElementById('captable')
        response = form.submit()
        console.log("response submitted")
    }
    else {
        console.log("Hit Load Graphs to Gen a Report")
    }
}

//execution
var portfolios = []
var risk = document.getElementById("risk").value;
var means = []
var stds = []
console.log("Default risk is " + risk);
http://localhost:5000/?risk=109&name=Jacob%2520Hoffman&birthday=12%252F28%252F1997&term=7&date-input=2020-12-23&Large+Cap+Growth=200&Large+Cap+GrowthY=0%2525&Large+Cap+GrowthX=100%2525&Large+Cap+Value=200&Large+Cap+ValueY=0%2525&Large+Cap+ValueX=100%2525&Small+Cap+Growth=200&Small+Cap+GrowthY=0%2525&Small+Cap+GrowthX=100%2525&Small+Cap+Value=200&Small+Cap+ValueY=0%2525&Small+Cap+ValueX=100%2525&Mid+Cap=200&Mid+CapY=0%2525&Mid+CapX=100%2525&International+Stock=&International+StockY=0%2525&International+StockX=100%2525&Emerging+Mkt+Stock=&Emerging+Mkt+StockY=0%2525&Emerging+Mkt+StockX=100%2525&International+Gov+Bonds=&International+Gov+BondsY=0%2525&International+Gov+BondsX=100%2525&Long+Gov+Bonds=&Long+Gov+BondsY=0%2525&Long+Gov+BondsX=100%2525&Corporate+Bonds=&Corporate+BondsY=0%2525&Corporate+BondsX=100%2525&High+Yield+Bonds=&High+Yield+BondsY=0%2525&High+Yield+BondsX=100%2525&Municipal+Bonds=&Municipal+BondsY=0%2525&Municipal+BondsX=100%2525&Foreign+Bonds=&Foreign+BondsY=0%2525&Foreign+BondsX=100%2525&Emerging+Mkt+Debt=&Emerging+Mkt+DebtY=0%2525&Emerging+Mkt+DebtX=100%2525&V.C.=&V.C.Y=0%2525&V.C.X=100%2525&Real+Estate=&Real+EstateY=0%2525&Real+EstateX=100%2525&Commodities=&CommoditiesY=0%2525&CommoditiesX=100%2525&Cash=&CashY=0%2525&CashX=100%2525