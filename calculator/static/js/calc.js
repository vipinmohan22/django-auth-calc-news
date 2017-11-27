$.ajaxSetup({
    headers: {"X-CSRFToken": '{{csrf_token}}'}
});
$(document).ready(function () {
    var num1
    if (num1 == "undefined" || num1 == null) {
        var num1 = 0;
    }

    $("#0").click(function () {
        $("#result").val($("#result").val() + $("#0").val());
    });
    $("#1").click(function () {
        $("#result").val($("#result").val() + $("#1").val());
    });
    $("#2").click(function () {
        $("#result").val($("#result").val() + $("#2").val());
    });
    $("#3").click(function () {
        $("#result").val($("#result").val() + $("#3").val());
    });
    $("#4").click(function () {
        $("#result").val($("#result").val() + $("#4").val());
    });
    $("#5").click(function () {
        $("#result").val($("#result").val() + $("#5").val());
    });
    $("#6").click(function () {
        $("#result").val($("#result").val() + $("#6").val());
    });
    $("#7").click(function () {
        $("#result").val($("#result").val() + $("#7").val());
    });
    $("#8").click(function () {
        $("#result").val($("#result").val() + $("#8").val());
    });
    $("#9").click(function () {
        $("#result").val($("#result").val() + $("#9").val());
    });


    $("#c").click(function () {
        $("#result").val("");
    });
    $("#dl").click(function () {
        $("#result").val($("#result").val().slice(0, -1));
    });
    $("#sum").click(function () {
        if (valcheck($("#result").val()) == "true") {
            $("#result").val($("#result").val() + $("#sum").val());
        }
        else {
            alert("not permitted... recheck syntax");
        }

    });

    $("#sub").click(function () {
        if (valcheck($("#result").val()) == "true") {
            $("#result").val($("#result").val() + $("#sub").val());
        }
        else {
            alert("not permitted... recheck syntax");
        }
    });
    $("#mul").click(function () {
        if (valcheck($("#result").val()) == "true") {
            $("#result").val($("#result").val() + $("#mul").val());
        }
        else {
            alert("not permitted... recheck syntax");
        }
    });
    $("#div").click(function () {
        if (valcheck($("#result").val()) == "true") {
            $("#result").val($("#result").val() + $("#div").val());
        }
        else {
            alert("not permitted... recheck syntax");
        }
    });
    $("#log").click(function () {
        if (valcheck($("#result").val()) == "true") {
            $("#result").val($("#result").val() + $("#log").val());
        }
        else {
            alert("not permitted... recheck syntax");
        }

    });
    $("#equal").click(function () {
        var num = ($("#result").val()).split(/[+-/*log]+/);

        alert(num);
        var op = ($("#result").val()).replace(/[0-9]/g, ' ');
        op = op.trim();
        var op2 = op.split(' ')
        alert(op2)
        $.ajax({
            type: "GET",
            url: "/calculator/calc_op/",
            data: {
                'arr1[]': num, 'arr2[]': op2,
            },
            success: function (data) {
                $("#result").val(data)
            }
        });

    });

    function valcheck(a) {
        var b = a.slice(-1);
        if (b.match(/[+-/*log]+/) || a == "") {
            var c = "false";
            return c;
        }
        else {
            var c = "true";
            return c;
        }
    }
});
