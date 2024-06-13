// const element_h = {
// 	'Q': 'quality',
// 	'C': 'correctness',
// 	'G': 'goodness',
// 	'F': 'feature',
// 	'O': 'in_own_right',
// 	'I': 'relative_to_input',
// 	'E': 'relative_to_external',
// 	'f': 'form',
// 	'c': 'content',
// 	'b': 'both'
// };

// // FIXME - do not display invalid combinations
// function updateSearch(){

// 	var h = { 
// 	    "a":0, 
// 	    "b":1, 
// 	    "c":2
// 	};
	
// 	var elements = document.getElementsByClassName('taxonomy_node');
// 	for (let i = 0; i < elements.length; i++) {
// 		let element = elements[i];
// 		let search_key = element.getAttribute("search_key");

// 		if (search_key == "Q") {
// 			// Always show the root node
// 			continue;
// 		}

// 		let hide = false;

// 		for (let i = 0; i < search_key.length; i++) {
// 		  	let c = search_key.charAt(i);
// 			for (var x in h) {
// 				var search_select = document.getElementById("select_"+x);
// 				let v = search_select.value;
// 				if (v != "."){
// 					if (search_key.includes(v) == false) {
// 						hide = true;
// 					}
// 				}
				
// 			};

// 		}

// 		if(hide) {
// 			if (element.style.display != "none"){
// 				console.log("N-" + search_key);
// 				element.style.display = 'none';
// 			};
// 		} else {
// 			element.style.display = 'block';
// 			console.log("B-" + search_key);
// 		}

// 	}
// };