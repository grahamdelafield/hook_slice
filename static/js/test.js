window.onload = function() {
    console.log("Graham's App");
    return
}

function testAdd() {
    let container = document.getElementById('shot-container');

    let len = container.childElementCount + 1
    console.log(len);
    
    let template = document.querySelector('#productrow');
    var clone = template.content.cloneNode(true);

    let shotCounter = clone.querySelector("#shot-label");
    shotCounter.innerHTML = 'Shot ' + String(len);
    
    let shotClub = clone.querySelector("#shot-club");
    shotClub.name = "club-selection-" + String(len);

    let shotDirection = clone.querySelector("#shot-direction");
    shotDirection.name = "flight-path-" + String(len);

    let shotScale = clone.querySelector("#shot-scale");
    shotScale.name = "shot-scale-" + String(len);

    let shotMiss = clone.querySelector("#shot-mishit");
    shotMiss.name = "shot-misshit-" + String(len);
    
    container.appendChild(clone);
    console.log(container);
}

async function recordData() {
    let clubSelections = document.getElementsByName("club-selection");
    let flightPaths = document.getElementsByName("flight-path");
    let shotScale = document.getElementsByName("shot-scale");
    let mishits = document.getElementsByName("shot-misshit");



    let results = new Object();
    let clubs = [];
    let paths = [];
    let scales = [];
    let misses = [];

    for (i=0; i<clubSelections.length; i++) {
        clubs.push(clubSelections[i].value);
        paths.push(flightPaths[i].value);
        scales.push(shotScale[i].value);
        misses.push(mishits[i].value);
    }
    results['clubs'] = clubs;
    results['paths'] = paths;
    results['scales'] = scales;
    results['misses'] = misses;


    return results;
}

async function setData(dataDict) {
    let clubSelections = document.getElementsByName("club-selection");
    let flightPaths = document.getElementsByName("flight-path");
    let shotScale = document.getElementsByName("shot-scale");
    let mishits = document.getElementsByName("mishit-selection");

    let clubs = dataDict['clubs'];
    let paths = dataDict['paths'];
    let scales = dataDict['scales'];
    let misses = dataDict['misses'];

    for (i=0; i<clubSelections.length-1; i++) {
        clubSelections[i].value = clubs[i];
        flightPaths[i].value = paths[i];
        shotScale[i].value = scales[i];
        mishits[i].value = misses[i];

    }
    return
}

async function addShot() {
    let currentData = await recordData();
    var shotContainer = document.getElementById("shot-container");
    var currentShot = document.getElementsByName("running-counter");
    currentShot = currentShot.length + 1;
    shotContainer.innerHTML += "<div class='form-group row' id='shot-counter' name='running-counter'>" +
          "<label for='staticEmail' class='col-sm-1 col-form-label'>Shot " + currentShot + "</label>" +
            "<div class='col-sm-2'>" +
              "<select class='form-select' aria-label='Default select example' id='shot-"+ currentShot+"-club' name='club-selection'>" +
                    "<option selected>Club</option>" +
                    "<option value='13'>Driver</option>" +
                    "<option value='14'>3 Wood</option>" +
                    "<option value='15'>5 Wood</option>" +
                    "<option value='1'>Hybrid</option>" +
                    "<option value='2'>2 Iron</option>" +
                    "<option value='3'>3 Iron</option>" +
                    "<option value='4'>4 Iron</option>" +
                    "<option value='5'>5 Iron</option>" +
                    "<option value='6'>6 Iron</option>" +
                    "<option value='7'>7 Iron</option>" +
                    "<option value='8'>8 Iron</option>" +
                    "<option value='9'>9 Iron</option>" +
                    "<option value='10'>Pitching Wedge</option>" +
                    "<option value='11'>Sand Wedge</option>" +
                "</select>" +
            "</div>" +
            "<div class='col-sm-2'>" +
                "<select class='form-select' aria-label='Default select example' id='shot-"+ currentShot+"-direction' name='flight-path'>" +
                      "<option selected>Left/Right</option>" +
                      "<option value='1'>Left</option>" +
                      "<option value='2'>Straight</option>" +
                      "<option value='3'>Right</option>" +
                  "</select>" +
            "</div>" +
            "<div class='col-sm-2'>" +
                "<select class='form-select' aria-label='Default select example' id='shot-"+ currentShot+"-scale' name='shot-scale'>" +
                      "<option selected>Scale</option>" +
                      "<option value='0'>0</option>" +
                      "<option value='1'>+1</option>" +
                      "<option value='2'>+2</option>" +
                      "<option value='3'>+3</option>" +
                  "</select>" +
            "</div>" +
            "<div class='col-sm-2'>" +
                "<select class='form-select' aria-label='Default select example' id='shot-1-mishit' name='mishit-selection'>" +
                    "<option selected>Mishit?</option>" +
                    "<option value='0'>No</option>" +
                    "<option value='1'>Yes</option>" +
                "</select>" +
            "</div>" +
        "</div>"
    await setData(currentData);
    return false;
}

async function submitData() {
    let currentData = await recordData();

    let firstName = document.getElementById("inputName2").value;
    let lastName = document.getElementById("inputName4").value;

    if (firstName == "" || lastName == ""){
        window.alert('No valid name...dipshit.');
        return
    }

    
    let month = document.getElementById("month-selector").value;
    let day = document.getElementById("day-selector").value;
    let year = document.getElementById("year-selector").value;
    
    if (month == 'Choose...' || day == 'Choose...' || year == 'Choose...'){
        window.alert("You didn't enter a date.")
        return
    }

    var data = new Object();

    data['name'] = firstName + " " + lastName;
    data['date'] = year + '-' + month + '-' + day;

    data['clubs'] = currentData['clubs'];
    data['flight paths'] = currentData['paths'];
    data['shot scale'] = currentData['scales'];
    data['mishits'] = currentData['misses'];

    console.log(data);

}


