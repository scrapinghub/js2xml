function MyObjectType(obj) {
    switch (obj.constructor) {
        case Date:
            document.write("Object is a Date.");
        case Number:
            document.write("Object is a Number.");
        case String:
            document.write("Object is a String.");
        default:
            document.write("Object is unknown.");
    }
}
