////////////////////////////////
// NO NETWORKING JAVASCRIPT  ///
////////////////////////////////

//make the last selected point on the markowitz curve null
last = null;
risk = 25;


//Load inputs from URL into the form.
function linkload() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    keys = urlParams.keys()
    for (const key of keys) {
        //console.log(key)
        //console.log(document.getElementsByName(key))
        input = document.getElementsByName(key)[0];
        input.value = decodeURIComponent(urlParams.get(key));
    }
    //    risk = document.getElementById("risk").value;
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
    cap = document.getElementById("capcontainer");
    if (cap.style.display == "none") {
        cap.style.display = "block";
        document.getElementById("show_hide_form").innerHTML = "Hide Form";
        document.getElementById("show_hide_form").className = "btn btn-primary";
    }
    else {
        cap.style.display = "none";
        document.getElementById("show_hide_form").innerHTML = "Show Form";
        document.getElementById("show_hide_form").className = "btn btn-outline-primary";
    }
}

function showhidetax() {
    tax = document.getElementById("taxrate");
    cap = document.getElementById("taxcap");
    if (cap.style.display == "none") {
        cap.style.display = "block";
        tax.style.display = "block";
        document.getElementById("show_hide_tax").innerHTML = "Hide Tax(coming)";
        document.getElementById("show_hide_tax").className = "btn btn-secondary";
    }
    else {
        cap.style.display = "none";
        tax.style.display = "none";
        document.getElementById("show_hide_tax").innerHTML = "Show Tax(coming)";
        document.getElementById("show_hide_tax").className = "btn btn-outline-secondary";
    }
}


////////////////////////////////
//  NETWORKING JAVASCRIPT  /////
////////////////////////////////

function scale_graphs() {
    svgs = document.getElementsByClassName("mpld3-figure");
    console.log("Scaling...")
    for (let svg of svgs) {
        console.log(svg);
        viewbox = "0 0 900 600";
        svg.setAttribute("viewBox", viewbox);
        svg.setAttribute("width", 300);
        svg.setAttribute("height", 200);
    }
}

function mplview(button) {
    graphs = document.getElementById("graphs").children
    curr = document.getElementById(button.name)
    for (i = 0; i < graphs.length; i++) {
        graphs[i].style.visibility = "hidden";
    }
    curr.style.visibility = "visible";
}


// image return
function load_graphs(data) {
    document.getElementById("message").innerHTML = "";
    document.getElementById("message-box").style.display = "none";
    var img_list = eval(data['images'])


    //console.log(data)
    $("#frontier").empty();
    $("#current").empty();
    $("#prescribed").empty();
    $("#daily").empty();
    $("#line").empty();
    $("#bell").empty();

    console.log(img_list[0]);

    $("#frontier").append(img_list[0]);
    $("#current").append(img_list[2]);
    $("#prescribed").append(img_list[1]);

    $("#daily").append(img_list[3])
    $("#line").append(img_list[4]);
    $("#bell").append(img_list[6]);

    stds = eval(data["risks"])
    means = eval(data["returns"])
    portfolios = eval(data["portfolios"])
    cap = document.getElementById("capcontainer");
    shoe = document.getElementById("show_hide_form");
    cap.style.display = "none";
    shoe.innerHTML = "Show Form";
    shoe.className = "btn btn-outline-primary";
}

function request_graphs() {
    //    document.getElementById("link").href = linkmake();
    //    document.getElementById("link").style.display = "block";
    form = {}
    $('#captable').serializeArray().map(function (x) { form[x.name] = x.value })

    document.getElementById("message").innerHTML = "Running computation...";
    document.getElementById("message-box").style.display = "block";

    $.post("/load_graphs", form, load_graphs)
        .fail(function (error) {
            document.getElementById("message").innerHTML = "Please Fill Out The Form.";
            document.getElementById("message-box").style.display = "block";


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
    if (document.getElementById("frontier").innerHTML != "") {
        form = document.getElementById('captable')
        response = form.submit()
        //console.log("response submitted")
    }
    else {
        console.log("Hit Load Graphs to Gen a Report")
    }
}


//execution
var portfolios = []
//var risk = document.getElementById("risk").value;
var means = []
var stds = []
console.log("Default risk is " + risk);
