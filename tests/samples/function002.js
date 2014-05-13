function AddFive(x) {
    return x + 5;
}

function AddTen(x) {
    return x + 10;
}

var condition = false;

var MyFunc;
if (condition) {
    MyFunc = AddFive;
}
else {
    MyFunc = AddTen;
}

var result = MyFunc(123);
// Output: 133
