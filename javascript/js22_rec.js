// All functions and recursion!
function totalAcrossArray(arr, curTotal) {
	if (arr.length == 0) {
		return curTotal;
	}
	else {
		const newTotal = curTotal + arr[0];
		const remaining = arr.slice(1);
		return totalAcrossArray(remaining, newTotal);
	}
}

function avgAcrossArray(arr) {
	return totalAcrossArray(arr, 0) / arr.length;
}

function avgAllSubarrays(arr, oldList) {
	if (arr.length == 0) {
		return oldList;
	}
	else {
		const remaining = arr.slice(1);
		const newList = oldList.concat([avgAcrossArray(arr[0])]);
		return avgAllSubarrays(remaining, newList);
	}
}

function grab(arr, oldList, att) {
	if (arr.length == 0) {
		return oldList;
	}
	else {	
		const remaining = arr.slice(1);
		const newList = oldList.concat([arr[0][att]]);
		return grab(remaining, newList, att);
	}
}

/*
More readable without tail recursion
function grab(arr, att) {
	if (arr.length == 0) {
		return [];
	}
	else {
		return [arr[0][att]].concat(grab(arr.slice(1), att));
	}
}
*/

function combineArrays(arr1, arr2, oldList) {
	if (arr1.length == 0 || arr2.length == 0) {
		return oldList;
	}
	else {
		const newPair = [arr1[0], arr2[0]];
		const newList = oldList.concat([newPair]);
		const rem1 = arr1.slice(1);
		const rem2 = arr2.slice(1);
		return combineArrays(rem1, rem2, newList);
	}
}

function rec_main(data) {
	const names = grab(data, [], "name");
	const points = grab(data, [], "points");
	const avgs = avgAllSubarrays(points, []);
	const pairs = combineArrays(names, avgs, []);

	console.log(pairs);
}
