//libs.js

//repeatedly makes get requests to a server, until a zero is returned.
function streamData(url, func) {
    function fetchData() {
        $.get(url, {}, cd);
    }
    //fetches data from server and runs func on the data over and over until it returns done.
    function cd(data) {
        if (func(data) == "done") return
        wait = 1000;
        setTimeout(fetchData, wait);
    }
    fetchData();
}

function getFormSubmitForUrl(url, func) {
    function formSubmit(event) {
        event.target.action = url;
        hidden = '<input type="hidden" name="clientTime" value="' + clientTime + ' >'
        event.target.innerHtml += hidden
        console.log(event.target)
        var request = new XMLHttpRequest();
        request.open('POST', url, true);
        request.onload = function () { // request successful
            // we can use server response to our request now
            event.target.reset();
            //            console.log("responseText: " + request.responseText);
            func(request.responseText);
        };
        request.onerror = function () {
            // request failed
        };
        request.send(new FormData(event.target)); // create FormData from form that triggered event
        event.preventDefault();
    }
    return formSubmit
}


// and you can attach form submit event like this for example
function attachFormSubmitEvent(formId, url, func) {
    document.getElementById(formId).addEventListener("submit", getFormSubmitForUrl(url, func));
}


//  Data is a dictionary
function postOnClick(url, func, data) {
    data['hidden_tiger'] = 5;
    var encoded_data = JSON.stringify(data);
    $.post(url, data, func);
}