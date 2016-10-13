// '.tbl-content' consumed little space for vertical scrollbar, scrollbar width depend on browser/os/platfrom. Here calculate the scollbar width .

$("td").each(function() {
    var text= $(this).text();
  if ( text.indexOf( "http" ) > -1 ){
    $(this).text("")
    $(this).append("<a href=\""+text+"\"><button type='button'>Book!</button></a>")}    
});

$("body").prepend("<input id='searchInput' value='Type To Filter'>");

$("body").prepend("<h3>From:</h3> <h3>{{ _from }}</h3> <h3>{{ _to }}</h3>");


var maxRows = 10;
$('.dataframe').each(function() {
    var cTable = $(this);
    var cRows = cTable.find('tr:gt(0)');
    var cRowCount = cRows.length;
    
    if (cRowCount < maxRows) {
        return;
    }

    cRows.each(function(i) {
        $(this).find('td:first').text(function(j, val) {
           return (i + 1) + " - " + val;
        }); 
    });

    cRows.filter(':gt(' + (maxRows - 1) + ')').hide();


    var cPrev = cTable.siblings('.prev');
    var cNext = cTable.siblings('.next');

    cPrev.addClass('disabled');

    cPrev.click(function() {
        var cFirstVisible = cRows.index(cRows.filter(':visible'));
        
        if (cPrev.hasClass('disabled')) {
            return false;
        }
        
        cRows.hide();
        if (cFirstVisible - maxRows - 1 > 0) {
            cRows.filter(':lt(' + cFirstVisible + '):gt(' + (cFirstVisible - maxRows - 1) + ')').show();
        } else {
            cRows.filter(':lt(' + cFirstVisible + ')').show();
        }

        if (cFirstVisible - maxRows <= 0) {
            cPrev.addClass('disabled');
        }
        
        cNext.removeClass('disabled');

        return false;
    });

    cNext.click(function() {
        var cFirstVisible = cRows.index(cRows.filter(':visible'));
        
        if (cNext.hasClass('disabled')) {
            return false;
        }
        
        cRows.hide();
        cRows.filter(':lt(' + (cFirstVisible +2 * maxRows) + '):gt(' + (cFirstVisible + maxRows - 1) + ')').show();

        if (cFirstVisible + 2 * maxRows >= cRows.length) {
            cNext.addClass('disabled');
        }
        
        cPrev.removeClass('disabled');

        return false;
    });

});


$("#searchInput").keyup(function () {
    //split the current value of searchInput
    var data = this.value.split(" ");
    //create a jquery object of the rows
    var jo = $("body").find("tr");
    if (this.value == "") {
        jo.show();
        return;
    }
    //hide all the rows
    jo.hide();

    //Recusively filter the jquery object to get results.
    jo.filter(function (i, v) {
        var $t = $(this);
        for (var d = 0; d < data.length; ++d) {
            if ($t.is(":contains('" + data[d] + "')")) {
                return true;
            }
        }
        return false;
    })
    //show the rows that match.
    .show();
}).focus(function () {
    this.value = "";
    $(this).css({
        "color": "black"
    });
    $(this).unbind('focus');
}).css({
    "color": "#C0C0C0"
});