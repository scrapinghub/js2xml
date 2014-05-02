function MyObjectType(obj) {
    switch (obj.constructor) {
        case Date:
            document.write("Object is a Date.");
            break;
        case Number:
            document.write("Object is a Number.");
            break;
        case String:
            document.write("Object is a String.");
            break;
        default:
            document.write("Object is unknown.");
    }
}
