try {
    addalert("bad call");
}
catch(e) {
    document.write ("Error Message: " + e.message);
    document.write ("<br />");
    document.write ("Error Code: ");
    document.write (e.number & 0xFFFF);
    document.write ("<br />");
    document.write ("Error Name: " + e.name);
}
