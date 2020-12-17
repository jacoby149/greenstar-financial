////////////////////////////////
// NO NETWORKING JAVASCRIPT  ///
////////////////////////////////

//Load inputs from URL into the form.
function linkload() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    keys = urlParams.keys()
    for (const key of keys) {
        document.getElementsByName("key").innerHTML = urlParams.get(key);
    }

}

//Make a link with all of the form inputs
function linkmake() {
    inputs = document.forms["form_name"].getElementsByTagName("input");
    const urlParams = new URLSearchParams();
    for (input of inputs) {
        urlParams.set(input.name, input.value)
    }
    return window.location + urlParams.toString
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

function setRisk() {
    console.log("adjusting risk");
    risk = $(this).val();
    console.log("risk : " + risk)
    console.log(risk + " of " + 100)
    if (portfolios.length == 0) {
        console.log("Please load graphs first ");
        return;
    }
    update_vals();
    //set variables that will post to flask to select risk level
    //display this risk level on the screen.

}

////////////////////////////////
//  NETWORKING JAVASCRIPT  /////
////////////////////////////////

// image return
function load_graphs(data) {
    console.log(data)
    document.getElementById("graphs").innerHTML = data["images"]
    stds = eval(data["risks"])
    means = eval(data["returns"])
    portfolios = eval(data["portfolios"])
    update_vals()
    cap = document.getElementById("captable");
    cap.style.display = "none";
    document.getElementById("message").innerHTML = "";

}

function graphs() {
    form = {}
    $('#captable').serializeArray().map(function (x) { form[x.name] = x.value })
    form["risk"] = risk
    console.log("FORM :" + form)
    document.getElementById("message").innerHTML = "Loading Graphs ...";
    $.post("/load_graphs", form, load_graphs);

}


//Backtesting functions

function load_backtest(data) {
    document.getElementById("backtest").innerHTML = data["backtest"]
    document.getElementById("weights").innerHTML = data["weights"]
}

function backtest() {
    $.post("/back", { "risk": risk }, load_backtest);
}

//execution
var portfolios = []
var risk = document.getElementById("risk").value;
var means = []
var stds = []
console.log("Default risk is " + risk);
$("#risk").on("change", setRisk);


// Generate Report
function genReport() {
    if (document.getElementById("mean").innerHTML != "") {
        form = document.getElementById('captable')
        form.appendChild(document.getElementById('risk'))
        response = form.submit()
        console.log("response submitted")
    }
    else {
        console.log("Hit Load Graphs to Gen a Report")
    }
}