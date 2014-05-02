var dateFormatters = {
    s   : function(d)   { return d.getSeconds() },
    ss  : function(d)   { return zeroPad(d.getSeconds()) },
    m   : function(d)   { return d.getMinutes() },
    mm  : function(d)   { return zeroPad(d.getMinutes()) },
    h   : function(d)   { return d.getHours() % 12 || 12 },
    hh  : function(d)   { return zeroPad(d.getHours() % 12 || 12) },
    H   : function(d)   { return d.getHours() },
    HH  : function(d)   { return zeroPad(d.getHours()) },
    d   : function(d)   { return d.getDate() },
    dd  : function(d)   { return zeroPad(d.getDate()) },
    ddd : function(d,o) { return o.dayNamesShort[d.getDay()] },
    dddd: function(d,o) { return o.dayNames[d.getDay()] },
    M   : function(d)   { return d.getMonth() + 1 },
    MM  : function(d)   { return zeroPad(d.getMonth() + 1) },
    MMM : function(d,o) { return o.monthNamesShort[d.getMonth()] },
    MMMM: function(d,o) { return o.monthNames[d.getMonth()] },
    yy  : function(d)   { return (d.getFullYear()+'').substring(2) },
    yyyy: function(d)   { return d.getFullYear() },
    t   : function(d)   { return d.getHours() < 12 ? 'a' : 'p' },
    tt  : function(d)   { return d.getHours() < 12 ? 'am' : 'pm' },
    T   : function(d)   { return d.getHours() < 12 ? 'A' : 'P' },
    TT  : function(d)   { return d.getHours() < 12 ? 'AM' : 'PM' },
    u   : function(d)   { return formatDate(d, "yyyy-MM-dd'T'HH:mm:ss'Z'") },
    S   : function(d)   {
        var date = d.getDate();
        if (date > 10 && date < 20) {
            return 'th';
        }
        return ['st', 'nd', 'rd'][date%10-1] || 'th';
    },
    w   : function(d, o) { // local
        return o.weekNumberCalculation(d);
    },
    W   : function(d) { // ISO
        return iso8601Week(d);
    }
};
