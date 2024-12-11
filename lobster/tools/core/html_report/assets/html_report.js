function buttonFilter(filter) {
    var elms = document.getElementsByTagName("div");
    var issue_elms = document.getElementsByClassName("issue");
    for (i = 0; i < elms.length; i++) {
        if (elms[i].id.startsWith("item-")) {
            console.log("elms[i].className ", elms[i].className)
            if (filter == "all") {
                elms[i].style.display = "block";
            } else if (elms[i].className == "item-" + filter) {
                elms[i].style.display = "block";
            } else {
                elms[i].style.display = "none";
            }
        }
    }
    // filter the issues list based on the issue filter button clicked
    for (i = 0; i < issue_elms.length; i++) {
        console.log("log ", issue_elms[i].className)
        if (filter == "all") {
            issue_elms[i].style.display = "list-item";
        } else if (issue_elms[i].className == "issue issue-" + filter) {
            issue_elms[i].style.display = "list-item";
        } else {
            issue_elms[i].style.display = "none";
        }
    }
    activeButton(filter);
    //call the search filering which could have been overwritten by the current filtering
    searchItem();
}


function activeButton(filter) {
    var elms = document.getElementsByTagName("button");
    console.log("the click buitton is " + filter);
    for (i = 0; i < elms.length; i++) {
        if (elms[i].className.includes("buttonActive")) {
            console.log("elem active found : " + elms[i].className);
            elms[i].className = elms[i].className.replace("buttonActive", "");
        } else if (elms[i].className.toLowerCase().includes("button" + filter.toLowerCase())) {
            console.log("elem to be activated found : " + elms[i].className);
            elms[i].className = elms[i].className + " buttonActive";
        }
    }
}


function ToggleIssues() {
    var div_issue = document.getElementById("issues-section");
    if (div_issue.style.display == "block" || div_issue.style.display == "") {
        div_issue.style.display = "none";
        document.getElementById("BtnToggleIssue").innerHTML = "Show Issues";
        document.getElementById("BtnToggleIssue").className = document.getElementById("BtnToggleIssue").className + " buttonActive";
    } else {
        div_issue.style = 'display: block; flex-direction: column; height: 200px;' +
            'overflow:auto;';
        document.getElementById("BtnToggleIssue").innerHTML = "Hide Issues";
        document.getElementById("BtnToggleIssue").className = document.getElementById("BtnToggleIssue").className.replace("buttonActive", "");
    }
}


function searchItem() {
    var input = document.getElementById('search').value
    input = input.toLowerCase();

    var divs = document.getElementsByClassName('item-name');
    for (i = 0; i < divs.length; i++) {
        var title = divs[i].parentNode.getAttribute("title");
        // get requirement name: 2nd part when we cut the long string with /svg
        var reqname = divs[i].innerHTML.toLowerCase().split("</svg>").pop();
        reqname = reqname.split(" ").pop();
        if (reqname.includes(input)) {
            // the search pattern has been found, if this elem has the title "hidden-not-matching", put it back to diplayed
            if (title) {
                if (title.startsWith("hidden-not-matching")) {
                    divs[i].parentNode.style.display = "block";
                }
            }
            divs[i].parentNode.setAttribute("title", "matching-" + input)
        } else {
            // not maching, we hide
            divs[i].parentNode.setAttribute("title", "hidden-not-matching")
            divs[i].parentNode.style.display = "none";
        }
    }
}
