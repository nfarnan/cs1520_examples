let timeoutID;
let timeout = 45000;

function setup() {
	document.getElementById("theButton").addEventListener("click", makePost);
	timeoutID = window.setTimeout(poller, timeout);
}

function makePost() {
	console.log("Sending POST request");
	const one = document.getElementById("a").value
	const two = document.getElementById("b").value
	const three = document.getElementById("c").value
	
	fetch("/new_item", {
			method: "post",
			headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
			body: `one=${one}&two=${two}&three=${three}`
		})
		.then((response) => {
			return response.json();
		})
		.then((result) => {
			updateTable(result);
			clearInput();
		})
		.catch(() => {
			console.log("Error posting new items!");
		});
}

function poller() {
	console.log("Polling for new items");
	fetch("/items")
		.then((response) => {
			return response.json();
		})
		.then(updateTable)
		.catch(() => {
			console.log("Error fetching items!");
		});
}

function updateTable(result) {
	console.log("Updating the table");
	const tab = document.getElementById("theTable");
	while (tab.rows.length > 0) {
		tab.deleteRow(0);
	}
	
	for (var i = 0; i < result.length; i++) {
		addRow(result[i]);
	}
	
	timeoutID = window.setTimeout(poller, timeout);
}

function addRow(row) {
	const tableRef = document.getElementById("theTable");
	const newRow = tableRef.insertRow();

	for (var i = 0; i < row.length; i++) {
		const newCell = newRow.insertCell();
		const newText = document.createTextNode(row[i]);
		newCell.appendChild(newText);
	}
}

function clearInput() {
	console.log("Clearing input");
	document.getElementById("a").value = "";
	document.getElementById("b").value = "";
	document.getElementById("c").value = "";
}

window.addEventListener("load", setup);
