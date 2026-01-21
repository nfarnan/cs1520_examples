// Make heavy use of selectively commenting out lines and refreshing to see 
// the effects of strict mode

"use strict";

console.log("Errors to guard typos");
var myVar = 12;
// ReferenceError
//mVar = 13;
console.log(myVar);
//console.log(mVar);

console.log("Illegal assignments");
// TypeError
//var NaN = 13;
//true.false = "TypeError";
//"This".willbe = "A TypeError";

console.log("No duplicate function arguments");
/*function foo(a, b, a, a) {
	console.log(a);
	console.log(b);
	console.log(a);
	console.log(a);
}  // SyntaxError
foo(1, 2, 3, 4);
*/
