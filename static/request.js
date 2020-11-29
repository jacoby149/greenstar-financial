////////////////////////////////
// NO NETWORKING JAVASCRIPT  ///
////////////////////////////////

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
    document.getElementById("std").innerHTML = "Std. : " + Math.round(std * 10000) / 100 + "%"
    document.getElementById("mean").innerHTML = "Return :" + Math.round(mean * 10000) / 100 + "%"
    document.getElementById("weight").innerHTML = "Portfolio : " + portfolio + "%"
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


//normal function returning

function norm() {
    update_vals()
    $.post("/norm", { "std": std * 100, "mu": mean * 100 }, load_norm)
}

function load_norm(data) {
    document.getElementById("norm").innerHTML = data["normal"]
}

//basic image returning

function load_basic(data) {
    console.log(data)
    document.getElementById("graphs").innerHTML = data["images"]
    stds = eval(data["risks"])
    means = eval(data["returns"])
    portfolios = eval(data["portfolios"])
    norm()
}

function basic() {
    $.post("/mark", { "risk": risk }, load_basic);
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
