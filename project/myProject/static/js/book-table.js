$(document).ready(function () {
    $('.totalCost').click(function (e) { 
        e.preventDefault();
        
        var tGuest = $("[name='totalGuest']").val();
        var tTable = $("[name='totalTable']").val();
        var tEmpTable = $('#totalEmptyTable').text();
        var personPerTable = $('#personPerTable').text();
        var tableResDate = $("[name='tableResDate']").val();
        var totalCost = 0;
        alertify.set('notifier','position', 'top-right');

        if((tGuest == "" || tTable == "")){
            alertify.error("Total Guest and table can not be null!");
            return false;
        }
        else if(tableResDate == ""){
            alertify.error("Table reservation date and time can not null!");
            return false;
        }
        else if((tGuest >= "A" && tGuest <= "Z") || (tGuest >= "a" && tGuest <= "z") || (tTable >= "A" && tTable <= "Z") || (tTable >= "a" && tTable <= "z")){
            alertify.error("Total Guest and table can not be in character!");
            return false;
        }
        else if((tGuest % 1 != 0) || (tTable % 1 != 0)){
            alertify.error("Total guest or table can't be float!");
            return false;
        }
        else if(tGuest == 0 || tTable == 0){
            alertify.error("Total guest or table can not be zero!");
            return false;
        }
        else if(parseInt(tEmpTable) < parseInt(tTable)){
            alertify.error("Your total request table not here!");
            return false;
        }
        else if((parseInt(tTable) * 4) != parseInt(tGuest)){
            if((parseInt(tTable) * 4) > parseInt(tGuest)){
                totalNonePayable = (parseInt(tTable) * 4) - parseInt(tGuest);
                tmp = (parseInt(tTable) * 4) - totalNonePayable;
                totalCost = tmp * 100;
                console.log(totalCost);
            }
            else if((parseInt(tTable) * 4) < parseInt(tGuest)){
                totalNonePayable = parseInt(tGuest) - (parseInt(tTable) * 4);
                tmp = parseInt(tGuest) - totalNonePayable;
                totalCost = tmp * 100;
                console.log(totalCost)
            }
        }
        else{
            totalCost = parseInt(tGuest) * 100;
        }
        $('.totalTableResCost').html("Rs " + totalCost)
    });
});