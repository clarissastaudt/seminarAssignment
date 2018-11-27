/* Toggles checkboxes for seminar priorities*/
function toggleClass() {
    if ($(this).hasClass('dontcare')) {
        $(this).removeClass('dontcare').addClass('check');
    } 
	else if ($(this).hasClass('check')) {
        $(this).removeClass('check').addClass('impossible');
    } 
	else if ($(this).hasClass('impossible')) {
        $(this).removeClass('impossible').addClass('dontcare');
    }
}

/* Shows a check sign after a successful submit */
function showValidSubmit() {
    setTimeout(function() {
        $(".sa-success").removeClass("hide");
    }, 20);
    setTimeout(function() {
        $(".sa-success").addClass('scale-out');
    }, 2000);
    setTimeout(function() {
        $(".sa-success").addClass('hide');
    }, 2500);
}

/* Writes data to database*/
function writeUserData(userId, stud, email, prios, neededSems, com) {
    firebase.database().ref(userId).set({
        student: stud,
        mail: email,
        "seminar A": prios[0],
        "seminar B": prios[1],
        "seminar C": prios[2],
		/* TODO: Add all seminars*/
        neededSeminars: parseInt(neededSems),
        comments: com
    }, 
		function(error) {
			if (error) {
				alert("Bei der Übertragung der Daten ist ein Fehler aufgetreten. Bitte versuchen Sie es nochmals.")
			} 
			else {
				/* Shows the user that the writing process was successful */
				showValidSubmit()

				/* Refreshes the page and clears all form fields */
				setTimeout(function() {
					location.reload();
				}, 2800)
			}
    	});
}

/* Converts the classes from seminar priority checkboxes to weights */
function convertToWeights(currClass) {
    if (currClass == 'check') {
        currClass = 2;
    } 
	else if (currClass == 'dontcare') {
        currClass = 1;
    } 
	else {
        currClass = 0;
    }
    return currClass;
}

/* Generates an error message if required data is still missing */
function generateErrorMessage(requiredData, requiredDataName) {
	count = 0
	missingData = []

	for (r in requiredData) {
		if (requiredData[r] == "" || typeof requiredData[r] == "undefined") {
			missingData.push(requiredDataName[count]);
		}
		count += 1
	}
	message = "Einige Angaben (" + missingData.join(", ") + ") fehlen noch. Bitte überprüfen Sie Ihre Eingaben."
}

function submitData(event) {
	/* Read in values from form*/
	firstname = $("#first_name").val()
	lastname = $("#last_name").val()
	com = $("#comments").val()
	email = $("#email").val()
	neededSems = $('input[name=neededSeminars]:checked').val()
	
	/* Create missing values for data base from given data */
	stud = firstname + " " + lastname
	userId = Math.floor((Math.random() * 1000) + 1) + firstname[0] + lastname[0]
	
	/* Comvert priorities to weights and save all values */
	prios = []
	prios.push(convertToWeights($('#sem1').attr('class')))
	prios.push(convertToWeights($('#sem2').attr('class')))
	prios.push(convertToWeights($('#sem3').attr('class')))
	/* TODO: Add all seminars*/

	requiredData = [firstname, lastname, email, neededSems]
	requiredDataName = ["Vorname", "Nachname", "E-Mail", "Benötigte Seminare"]
	
	generateErrorMessage(requiredData, requiredDataName)

	/* Check whether form values are valid and complete*/
	if (firstname && lastname && email && neededSems) {
		writeUserData(userId, stud, email, prios, neededSems, com)
	} 
	else(
		alert(message)

	)	
}		  

/* The $(document).ready function is the jQuery equivalent to a main function*/
$(document).ready(function() {
    /*
	Initialize Firebase (database)
	The necessary values can be found in your firebase account
	*/
    var config = {
		apiKey: "",
		authDomain: "seminarwahl.firebaseapp.com",
		databaseURL: "https://seminarwahl.firebaseio.com",
		projectId: "seminarwahl",
		storageBucket: "seminarwahl.appspot.com",
		messagingSenderId: ""
  	};
    firebase.initializeApp(config);

    var database = firebase.database();

	/* Change checkboxes for seminar priorities on click */
    $("#sem1").click(toggleClass)
    $("#sem2").click(toggleClass)
    $("#sem3").click(toggleClass)
	/* TODO: Add all Seminar ids*/

	/* Validate and send the gathered data to the Firebase database */
    $("#send").click(function(event) {
        event.preventDefault()
        submitData(event)
    });
});