// Functional (w/ Array.map() and Array.reduce())
function func_main(data) {
	const avgs = data
		.map(i => i["points"])
		.map(p => p.reduce((a, b) => a + b) / p.length);
	const pairs = data
		.map(i => i["name"])
		.map((e, i) => [e, avgs[i]]);
	console.log(pairs);
}
