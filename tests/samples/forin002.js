// Initialize the array.
var arr = new Array("zero","one","two");

// Add a few expando properties to the array.
arr["orange"] = "fruit";
arr["carrot"] = "vegetable";

// Iterate over the properties and elements.
var s = "";
for (var key in arr) {
    s += key + ": " + arr[key];
    s += "<br />";
}

document.write (s);

// Output:
//   0: zero
//   1: one
//   2: two
//   orange: fruit
//   carrot: vegetable
