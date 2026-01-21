// Imperative, procedural
function proc_main(data) {
	let avgs = [];

	for (let i=0; i < data.length; i++) {
		let total = 0;
		for (let j=0; j < data[i].points.length; j++) {
			total += data[i].points[j];
		}
		let avg = total / data[i].points.length;
		avgs.push([data[i].name, avg]);
	}

	console.log(avgs);
}
