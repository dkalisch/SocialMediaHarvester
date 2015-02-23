$(document).ready(function() {
	
	//reset all input fields
	$("input:text").val("");
	
	//activate all tooltips
	if ($("[rel=tooltip]").length) {
		$("input[rel=tooltip]").tooltip({
			placement:"right"
		});
		
		$("img[rel=tooltip]").tooltip({
			placement:"top"
		});
	}
});

//hide parameters of a harvester with the name 'harvesterName' when deactivated
function hideParams(harvesterName) {
	//select all 'div'-nodes of the parameters and set class from 'active' to 'inactive'
	$("#" + harvesterName + '_parameters').removeClass('active').addClass('inactive');
}

//display parameters of a harvester with the name 'harvesterName' when activated
function displayParams(harvesterName) {
	//select all 'div'-nodes of the parameters and set class from 'inactive' to 'active'
	$("#" + harvesterName + '_parameters').removeClass('inactive').addClass('active');
}

//funtion that is called when a harester icon is clicked
function harvesterClicked(elementID) {

	//get the class-attributeof the clicked element
	var elementClass = $('#' + elementID).attr("class");
	
	var form = $("form");

	//if the harvester is currently active
	if (elementClass == "harvester_icon active") {
		
		//set class from active to inactive
		$('#' + elementID).removeClass('active').addClass('inactive');
		
		//get name of the harvester
		var harvester = elementID.substr(elementID.indexOf("_") + 1);

		//set parameters class to inactive
		hideParams(harvester);
		
		//remove hidden input field which submits the harvester as selected harvester
		$("#hidden_" + harvester).remove();
		
	} else {
		
		//set class from inactive to active
		$('#' + elementID).removeClass('inactive').addClass('active');

		//get name of the harvester
		var harvester = elementID.substr(elementID.indexOf("_") + 1);

		//set parameter class to 'active'
		displayParams(harvester);
		
		//add hidden input field which submits the harvester as selected harvester
		$("<input>").attr({
			type:"hidden",
			name:"selectedHarvesters",
			value : harvester,
			id : "hidden_" + harvester
			}).appendTo(form);

	}
}

//performs a content check before the form is submitted
function checkForm(){
	console.log("checking form before submitting");
	
	//get all the selected harvesters (active icon)
	var selectedHarvesters = $("img.harvester_icon.active");
	
	//if the are selected harvesters
	if(selectedHarvesters.length > 0){
		//get required parameters (marked with a '*')
		var requiredParameters = $("div.active.param_container div label.required");
		console.log(requiredParameters);

		//iterate over required parameters
		for(i = 0; i < requiredParameters.length; i++){
			var paramValue = $(requiredParameters[i]).next();
			
				//if a parameter is empty raise an error
				if(paramValue.val() == ""){
					alert("Please fill in all requierd fields");
					return false;
				}
		}
		return true;
	}
	else{
		//if no harvester is selected raise an error
		alert("Please select a harvester!");
		return false;
	}

}


//wraps all the harvesters and parameters inside a json ----- sadly this is never used
function sendData(){
	
	console.log("sending data...");
	
	var paramContainer = $('div.param_container.active');
	
	console.log(paramContainer);
	console.log(paramContainer.length);
	
	var data = {};

	for (var i = 0; i < paramContainer.length; i++){
		
		var module = paramContainer[i];
		var moduleName = module.id.substring(0,module.id.indexOf("_"));
		console.log(moduleName);

		var param_labels = $("#" + moduleName +"_parameters div .parameter-name");

		var params = [];

		for(var k = 0; k < param_labels.length; k++){
			
			var param_name = $(param_labels[k]).text();
			
			if(param_name.indexOf("*") != -1){
				param_name = param_name.substring(0,param_name.indexOf("*"));
			}

			var param_value = $(param_labels[k]).next().val();
			
			var param = {};

			param["name"] = param_name;
			param["value"] = param_value;
			
			params.push(param);
		}
		data[moduleName] = params;
	}
	
	var json_data = JSON.stringify(data);
	console.log(json_data);
	return json_data;
}
