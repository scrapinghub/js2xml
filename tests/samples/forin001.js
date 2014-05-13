// Initialize object.
a = {"a" : "Athens" , "b" : "Belgrade", "c" : "Cairo"}

// Iterate over the properties.
var s = ""
for (var key in a) {
    s += key + ": " + a[key];
    s += "<br />";
    }
document.write (s);

// Output:
// a: Athens
// b: Belgrade
// c: Cairo
