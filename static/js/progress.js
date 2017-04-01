var progress_timer;

function progressBar() {

    var remove = false;

    function loadProgress(id){
        var newprogress;
        var newstatus;
        var pg;
        var selector = "#progress-" + id;
        var progress_url = "/order/" + id + "/get_progress/";
        var status_url = "/order/" + id + "/get_status/";

        // get current order status, set progress bar color, etc
        $.get(status_url, function( newstatus ) {
            switch (newstatus) {
            case "P": //in progress
                pg = "progress-bar progress-bar-success progress-bar-striped active";
                break;
            case "C": //completed
                pg = "progress-bar progress-bar-success progress-bar";
                break;
            case "F": //failed
                pg = "progress-bar progress-bar-danger progress-bar";
                break;
            case "S": //paused
                pg = "progress-bar progress-bar-info progress-bar-striped active";
                break;
            case "X": //cancelled
                pg = "progress-bar progress-bar-danger progress-bar";
                break;
            }
            $(selector).attr("class", pg);
        });

        // get current order progress
        $.get(progress_url, function( newprogress ) {
            $(selector).attr("aria-valuenow", parseFloat(newprogress)).css("width",parseFloat(newprogress)+"%");
            $(selector).html(newprogress+"%");
            if(newprogress == 100.0) {
                if(progress_type == "detail") {
                    $("#order-buttons").html("");
                }
                var parent_index = parent_order_id.indexOf(id);
                if(parent_index != -1) {
                    pg = "progress-bar progress-bar-success progress-bar";
                    $(selector).attr("class", pg);
                    parent_order_id.splice(parent_index, 1);
                    
                }
            }
        });
    }

    function loadChildren(id){
        var children;
        var child_selector = "#children-" + id + " tr:first";
        var child_id;
        try {
            child_id = parseInt(document.getElementsByClassName("child-id")[0].textContent);
        }
        catch (e) {
            child_id = "undefined";
        }
        var children_url = "/order/" + id + "/get_children/" + child_id + "/";

        // get current order children
        $.get(children_url, function( children_and_stats ) {
            children_and_stats = JSON.parse(children_and_stats);
            var children = children_and_stats["children"];
            var stats = children_and_stats["stats"];

            for(var i=0; i<children.length; i++) {
                // format output
                var fields = children[i]["fields"];
                var child_class = fields["is_successful"] ? "success" : "danger";
                var child_label = fields["is_successful"] ? "SUCCEEDED" : "FAILED";
                var date = new Date(fields["time_executed"]);
                var options = {
                    year: "numeric", month: "short",
                    day: "numeric", hour: "2-digit", minute: "2-digit"
                };
                var date_formatted = date.toLocaleTimeString("en-us", options);
                date_formatted = date_formatted.replace("AM", "a.m.");
                date_formatted = date_formatted.replace("PM", "p.m.");
                date_formatted = date_formatted.replace(" ", ". ");

                // update table with new orders
                $(child_selector).after(
                    "<tr class=\"" + child_class + "\"> \
                        <td> " + date_formatted + " EST \
                        <td class=\"child-id\"> " + children[i]["pk"] + " \
                        <td> " + fields["quantity"] + " \
                        <td> " + child_label + " \
                        <td> " + fields["price"] + " \
                    </tr>"
                );

                // update stats
                $("#stats").html("<b>Average Price:</b> " + stats["average_price"] + 
                    ", <b>Gross Sale Price:</b> " + stats["total_price"] + 
                    ", <b>Total Quantity Sold:</b> " + stats["total_quantity"]);
            }
        });
    }

    // progress_type declared on relevant template pages
    if(progress_type == "detail" && parent_order_id.length > 0) {
        loadChildren(parent_order_id[0]);
    }

    // if no more in progress orders exist, stop polling
    if (parent_order_id.length == 0) {
        clearInterval(progress_timer);
    } else {
        // otherwise update progress bars
        for (i = parent_order_id.length; i > 0; i--) {
            // update progress bar
            loadProgress(parent_order_id[i-1]);   
        }
    }
}

progressBar(); // This will run on page load
progress_timer = setInterval(function(){ progressBar() }, 2000); // get progress every 2 seconds
