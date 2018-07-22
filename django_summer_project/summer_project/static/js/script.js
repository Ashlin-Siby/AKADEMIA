$(document).ready(function(){
    
    $("#stud").click(function(){
        $("#studLogin").addClass("displayIt");
        $("#teach").addClass("dontDisplay");
        $("#admin").addClass("dontDisplay");
        $("#stud").addClass("dontDisplay");
    });

      $("#teach").click(function(){
        $("#teachLogin").addClass("displayIt");
        $("#teach").addClass("dontDisplay");
        $("#admin").addClass("dontDisplay");
        $("#stud").addClass("dontDisplay");
    });

       $("#admin").click(function(){
        $("#adminLogin").addClass("displayIt");
        $("#teach").addClass("dontDisplay");
        $("#admin").addClass("dontDisplay");
        $("#stud").addClass("dontDisplay");
    }); 

});