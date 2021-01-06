// TODO: highlight call btn or put btn when it is selected. start w/ calls loaded by default.
// select important elements
const callBtn = document.getElementById("call-btn")
const putBtn = document.getElementById("put-btn")
const table = document.getElementById("table")
const expirationDatesDropdown = document.getElementById("w-dropdown-list-4")
const expirationDatesSelectorText = document.getElementById("exp-dates-selector")

// scroll down to sandwich when the page loads
window.onload = (event) => {
    document.getElementById("contract-editor").classList.remove("invisible-while-loading");
    setTimeout(() => {
        const scrollTarget = document.getElementsByClassName("option-row")[sandwichLocation]
        scrollTarget.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 100)
}

// modal stuff
const modal = document.getElementById("contract-editor")
const modalSubmit = document.getElementById("modal-submit")
modalSubmit.addEventListener("click", submitData)
const modalCloseButton = document.getElementById("modal-close-btn")
modalCloseButton.addEventListener("click", closeModal)
const modalCancelButton = document.getElementById("modal-cancel")
modalCancelButton.addEventListener("click", closeModal)
const modalExpirationDate = document.getElementById("editor-expiration-date")
const modalPrice = document.getElementById("editor-price")
const modalTotalCost = document.getElementById("editor-total-cost")

const modalPricePerOption = document.getElementById("editor-price-per-option")

modalPricePerOption.addEventListener("input", function () {
    const pricePerOptionFloat = parseFloat(modalPricePerOption.value).toFixed(2)
    
    if (pricePerOptionFloat > 0) {
        editorState.pricePerOption = pricePerOptionFloat *100;
    } else {
        editorState.pricePerOption = 0;
    }
    
    if (validInput(pricePerOptionFloat, editorState.contracts)) {
        totalCost = parseFloat(
			parseFloat(editorState.pricePerOption) * editorState.contracts
		).toFixed(2);
        editorState.totalCost = totalCost
        modalTotalCost.innerHTML = totalCost.toString();
    } else {
        if (isNaN(pricePerOptionFloat)) {
            modalTotalCost.innerHTML = 0
        }
    }
})

const modalContracts = document.getElementById("editor-contracts")

modalContracts.addEventListener("input", function () {
    if (parseInt(modalContracts.value, 10) > 0) {
        editorState.contracts = parseInt(modalContracts.value, 10);
    } else {
        editorState.contracts = 0;
    }

    if (validInput(editorState.pricePerOption, editorState.contracts)) {
        totalCost = parseFloat(parseFloat(editorState.pricePerOption) * editorState.contracts).toFixed(2)
        editorState.totalCost = totalCost
        modalTotalCost.innerHTML = totalCost.toString();
    }
})

// holds the values user enters in the modal
let editorState = {};
let pricePerOption;
let contracts;
let totalCost;

let sandwichLocation;
let insertedSandwich = false;
const sandwich = `<div id="sandwich-container"><div id="sandwich"><p>${stockCode}: $${sharePrice}</p></div></div>`

// import the json
const editedString = theOptions.replace(/'/g, '"').replace(/None/g, "0")
const optionsObj = JSON.parse(editedString)

const tableHeader = `
        <div class="row table-row flex-center w-row option-row">
            <div class="col table-col w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <p class="headline">Strike</p>
            </div>
            <div class="col table-col w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <p class="headline">Break Even</p>
            </div>
            <div class="col table-col w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <p class="headline">% Change</p>
            </div>
            <div class="w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <p class="headline">Change</p>
            </div>
            <div class="w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <p class="headline">Price</p>
            </div>
        </div>`

// initialize table
initializeTable();

assignExpirationDateEventListeners("CALL");

callBtn.addEventListener("click", loadCalls)
putBtn.addEventListener("click", loadPuts)

// *** Done initializing page ***

function initializeTable() {
    buildTable("CALL", 0, true)  // initialize from the Calls section for the options that expire 1st (listed at 0th index)
}

function loadCalls() {
    resetExpirationDateEventListeners();
    insertedSandwich = false;
    buildTable("CALL", 0, false)
    switchContractType("CALL")
}

function loadPuts() {
    resetExpirationDateEventListeners();
    insertedSandwich = false;
    buildTable("PUT", 0, false)
    switchContractType("PUT")
}

function switchContractType(callOrPut) {
    const expirationDateSelectors = document.getElementById("w-dropdown-list-4").children
    for (let selectorIndex = 0; selectorIndex < expirationDateSelectors.length; selectorIndex++) {
        expirationDateSelectors[selectorIndex].addEventListener("click", buildTable.bind(this, callOrPut, selectorIndex, false))
    }
}

function buildTable(callOrPut, selectorIndex, onPageLoad) {
    // generates a table based on the index of the option (selectorIndex) and isCallOrPut
    // TODO: loadSpinner();
    insertedSandwich = false;
    table.innerHTML = ""
    table.innerHTML += tableHeader

    // update dropdown text with current table
    expirationDatesSelectorText.innerHTML = optionsObj[selectorIndex].expirationDate;

    // loop to create rows in the table
    for (let j = 0; j < optionsObj[selectorIndex].options[callOrPut].length; j++) {
        const currentOptions = optionsObj[selectorIndex].options[callOrPut]

        let newRowEl;
        if (callOrPut === "CALL") {
            const call = currentOptions[j]
            newRowEl = new DOMParser().parseFromString(makeRowFromOption(call, true), "text/html").body.firstChild;
        } else if (callOrPut === "PUT") {
            const put = currentOptions[j]
            newRowEl = new DOMParser().parseFromString(makeRowFromOption(put, false), "text/html").body.firstChild;
        } else {
            throw "Neither CALL nor PUT was selected!"
        }
        table.appendChild(newRowEl)
        // check if its time to insert the price sandwich
        if (!insertedSandwich) {
            if (j < optionsObj[selectorIndex].options[callOrPut].length - 1) {
                if (currentOptions[j + 1].strike > parseInt(sharePrice, 10)) {
                    table.appendChild(new DOMParser().parseFromString(sandwich, "text/html").body.firstChild);
                    sandwichLocation = j;
                    insertedSandwich = true;
                }
            }
        }
        // prepare modal button opener
        const expiryDate = currentOptions[j].expirationDate;
        const price = currentOptions[j].lastPrice;
        const theta = currentOptions[j].theta;
        newRowEl.addEventListener("click", openModal.bind(this, expiryDate, price, theta))
    }
    if (onPageLoad) {
        // handled with window.onload at top of file now
    } else {
        const scrollTarget = document.getElementsByClassName("option-row")[sandwichLocation]
        scrollTarget.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    // TODO: stopSpinner();
}

function assignExpirationDateEventListeners(callOrPut) {
    const expirationDateSelectors = document.getElementById("w-dropdown-list-4").children
    for (let selectorIndex = 0; selectorIndex < expirationDateSelectors.length; selectorIndex++) {
        expirationDateSelectors[selectorIndex].addEventListener("click", buildTable.bind(this, callOrPut, selectorIndex, false))
        expirationDateSelectors[selectorIndex].addEventListener("click", () => {
            // this func closes the dropdown menu by simulating a click on the screen
            document.getElementById("w-dropdown-toggle-4").setAttribute("aria-expanded", false);
            document.getElementById("w-dropdown-toggle-4").classList.remove("w--open");
            document.getElementById("w-dropdown-list-4").classList.remove("w--open");
            // for (let i = 0; i < openElements.length; i++) {
            // openElements[i].classList.remove("w--open");
            // }
        })
    }
}

function resetExpirationDateEventListeners() {
    // clone and replace all the expirationDatesDropdown children
    const selectors = [];
    for (let i = 0; i < expirationDatesDropdown.children.length; i++) {
        selectors.push(expirationDatesDropdown.children[i].cloneNode(true))
    }
    // remove all the original children
    expirationDatesDropdown.innerHTML = "";
    // replace them
    for (let i = 0; i < selectors.length; i++) {
        expirationDatesDropdown.appendChild(selectors[i])
    }
}

function validInput(pricePerOption, contracts) {
    if (pricePerOption > 0 && Number.isInteger(contracts) && contracts > 0) {
        return true;
    }
    return false;
}

// *** *** Modal stuff *** ***

function openModal(expirationDate, price, theta) {
    editorState = {}; // reset the page's state
    modal.style.display = "block";
    console.log("Opening modal")

    // set values for expiration date and price
    modalExpirationDate.innerHTML = expirationDate;
    modalPrice.innerHTML = price;
    // set defaults for the inputs and total cost
    const pricePerOption = document.getElementById("editor-price-per-option");
    pricePerOption.value = price;
    modalContracts.value = 1;
    modalTotalCost.innerHTML = price;
    // set default values for editorState
    editorState.pricePerOption = price;
    editorState.contracts = 1;
    editorState.totalCost = price * 100;

    editorState.expirationDate = expirationDate;
    editorState.price = price;
    editorState.theta = theta;
}

function closeModal() {
    console.log("Closing modal...")
    modal.style.display = "none";
    editorState = {}; // reset state just in case
}

function submitData() {
    const validData = validate();
    if (validData === true) {
        const serverUrl = "http://127.0.0.1:8000/"
        const request = new Request(serverUrl, { headers: { 'X-CSRFToken': getCookie("csrftoken") } })
        fetch(request, {
            method: "POST",
            mode: "same-origin",
            body: JSON.stringify(editorState.expirationDate, editorState.contracts, editorState.theta)
        }).then(response => {
            console.log(response)
        }).catch(err => {
            console.log(err)
        });
        closeModal();
    } else {
        // TODO: inform user of err contained in validData
        document.getElementById("err-message").innerHTML = validData;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function validate() {
    if (editorState.contracts < 1 || editorState.contracts === undefined) {
        return "Must include number of contracts"
    } else if (editorState.pricePerOption < 0.01 || editorState.pricePerOption === undefined) {
        return "Must include price per option"
    } else {
        return true
    }
}

function loadSpinner() {

}

function stopSpinner() {

}

function makeRowFromOption(option, isCall) {
    let callOrPut;
    let percentChangeColor;
    let priceChangeColor;
    if (isCall) {
        callOrPut = "CALL"
    } else {
        callOrPut = "PUT"
    }
    if (option.changePercent >= 0) {
        percentChangeColor = "greenStyling"
    } else {
        percentChangeColor = "redStyling"
    }
    if (option.change >= 0) {
        priceChangeColor = "greenStyling"
    } else {
        priceChangeColor = "redStyling"
    }

    return `
        <div class="row table-row flex-center w-row option-row">
            <div class="col table-col w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <div class="transaction-type">
                    <div class="transaction-icon sent"></div>
                    <div>
                        <h6 class="currency-short-name">$${option.strike} ${callOrPut}</h6>
                    </div>
                </div>
            </div>
            <div class="col table-col w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <h6 class="currency-short-name">$${option.ask}</h6>
            </div>
            <div class="col table-col w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <h6 class="currency-short-name ${percentChangeColor}">${Math.round(option.changePercent * 100)}%</h6>
            </div>
            <div class="w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <h6 class="currency-short-name inline text-red ${priceChangeColor}">$${option.change}</h6>
            </div>
            <div class="w-col w-col-3 w-col-small-3 w-col-tiny-3">
                <h6 class="currency-short-name inline text-red">${option.ask}</h6>
            </div>
        </div>
                        `
    // unused button code
    // < a href = "#" id = "button-${option.expirationDate}" class="dropdown-link w-dropdown-link" tabindex = "0" > Buy</ >
}

// FIXME: make modal err msg more centered.