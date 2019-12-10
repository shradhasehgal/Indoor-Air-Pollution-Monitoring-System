var deets =[[290,173], [1080, 557], [1184, 470], [1020, 427] ,[980,437], [1080, 480], [920, 290]];
var locs = ["Paarijat", "KRB", "CIE", "SH2", "Workspaces", "SPCRC", "Nilgiri"]; 

function myFunction() 
{
    var i;
    for(i=1; i<=7; i++)
    {
        $("#"+i).css({    
            "left": deets[i-1][0],
            "top": deets[i-1][1],
        });
    }
};

$(document).ready(function(){
    myFunction();
});


function loc(idx) 
{
    console.log(idx - 1);
    document.getElementById("demo").innerHTML = locs[idx - 1];
    $("#demo").css({    
        "border-style": 'solid',
    });
    
};


function noloc() 
{
    //console.log(idx - 1);
    document.getElementById("demo").innerHTML = "";
    $("#demo").css({    
        "border-style": 'none',
    });
    
};

function val(idx) 
{
    //console.log(idx - 1);
    var location = locs[idx-1];
    document.getElementById("demo").innerHTML = location;
    $("#demo").css({    
        "border-style": 'solid',
    });
    
    $("#graphs").css({    
        "display": 'block',
    });

    document.getElementById("graph").innerHTML = "Graphs for "+ location;

    for(var i=1; i<=9; i++)
    {
        var str = "img/" + location + "/" +location +"_";
        var q = "";
        if(i == 1)
            q = "CO";

        else if(i==2)
            q = "eCO2";

        else if(i == 3)
            q = "Humidity";
        
        else if(i==4)
            q = "NH3";
        
        else if(i==5)
            q = "NO2";
        
        else if(i == 6)
            q = "PM2.5";
        
        else if(i == 7)
            q = "PM10"
        
        else if(i == 8)
            q = "Temperature";
        
        else q = "VOC";

        str = str + q +".png";
        src = "url_for('static', filename= '" + str + "')"
        console.log(src)

        $("#img" + i).attr("src", str);
    }
};