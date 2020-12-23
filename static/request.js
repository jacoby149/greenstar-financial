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
    risk = document.getElementById("risk").value;
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
    if (document.getElementById("graphs").innerHTML != "") {
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
