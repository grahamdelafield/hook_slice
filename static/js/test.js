window.onload = function() {
    console.log("Graham's App");
    return
}

function addShot() {
    let container = document.getElementById('shot-container');

    let len = container.childElementCount + 1
    console.log(len);
    
    let template = document.querySelector('#shotrow');
    var clone = template.content.cloneNode(true);

    let holeLabel = clone.querySelector("#hole-number");
    holeLabel.innerHTML = 'Hole ' + String(len);

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

// async function setData(dataDict) {
//     let clubSelections = document.getElementsByName("club-selection");
//     let flightPaths = document.getElementsByName("flight-path");
//     let shotScale = document.getElementsByName("shot-scale");
//     let mishits = document.getElementsByName("mishit-selection");

//     let clubs = dataDict['clubs'];
//     let paths = dataDict['paths'];
//     let scales = dataDict['scales'];
//     let misses = dataDict['misses'];

//     for (i=0; i<clubSelections.length-1; i++) {
//         clubSelections[i].value = clubs[i];
//         flightPaths[i].value = paths[i];
//         shotScale[i].value = scales[i];
//         mishits[i].value = misses[i];

//     }
//     return
// }

async function submitData() {
    let currentData = await recordData();

    let firstName = document.getElementById("inputName2").value;
    let lastName = document.getElementById("inputName4").value;

    if (firstName == "" || lastName == ""){
        window.alert('No valid name...dipshit.');
        return false;
    }

    
    let month = document.getElementById("month-selector").value;
    let day = document.getElementById("day-selector").value;
    let year = document.getElementById("year-selector").value;
    
    if (month == 'Choose...' || day == 'Choose...' || year == 'Choose...'){
        window.alert("You didn't enter a date.")
        return false;
    }

    return true;

    // var data = new Object();

    // data['name'] = firstName + " " + lastName;
    // data['date'] = year + '-' + month + '-' + day;

    // data['clubs'] = currentData['clubs'];
    // data['flight paths'] = currentData['paths'];
    // data['shot scale'] = currentData['scales'];
    // data['mishits'] = currentData['misses'];

    // console.log(data);

}


