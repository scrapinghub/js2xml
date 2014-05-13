try {
        throw new Error(200, "x equals zero");
}
catch (e) {
    document.write(e.message);
}
