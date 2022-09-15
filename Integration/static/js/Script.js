let editor;
window.onload = function() {
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");
}


function change(id){
    let counter=0;
    for(counter=1;counter<4;counter++){
        var run_block = document.getElementById("running_zone-"+counter);
        var sample_test_label = document.getElementById(counter);
        if(counter===parseInt(id)){
            sample_test_label.style.fontWeight = "bold";
            run_block.style.display = "block";
        }
        else{
            sample_test_label.style.fontWeight = "normal";
            run_block.style.display = "none";
        }
    }
}

function Run(){
    var run_block = document.getElementById("exampleBlock");
    var score_block = document.getElementById("table");
    run_block.style.display = "block";
    score_block.style.display = "none";
    var code = editor.getSession().getValue();
   $.ajax({
       type: "POST",
       url: 'my-ajax-run/',
       data: { csrfmiddlewaretoken: '{{ csrf_token }}', code: code},
       success: function callback(response){
                    var results = response.split("-");
                    let counter = 0;
                    for(counter=0;counter<results.length;counter++){
                        var list=results[counter].split(",");
                        UpdateRunningBlock(list);
                    }
                    change(1);

           }
    });

}




function LunchTests(){
    var run_block = document.getElementById("exampleBlock");
    var score_block = document.getElementById("table");
    run_block.style.display = "none";
    score_block.style.display = "block";
    var code = editor.getSession().getValue();
    $.ajax({
       type: "POST",
       url: 'lunch_tests/',
       data: { csrfmiddlewaretoken: '{{ csrf_token }}', code: code},
       success: function callback(response){
                    var myArray = response.split(" ");
                    let counter = 0;
                    for(counter=0;counter<myArray.length;counter++){
                        var list = myArray[counter].split(",");
                        if(counter < myArray.length-1){
                            Update(list);
                        }
                        else{
                            UpdateTotal(list);
                        }
                    }
           }
    });

}

function UpdateTotal(list){
    document.getElementById("score-total").style.color = list[2];
    document.getElementById("pourcentage-total").style.color = list[2];
    document.getElementById("score-total").innerHTML = "SCORE TOTAL:"+list[0];
    document.getElementById("pourcentage-total").innerHTML = "POURCENTAGE:"+list[1]+"%";
}
function Update(list){
    document.getElementById("test"+list[0]).style.color = list[3];
    document.getElementById("score"+list[0]).style.color = list[3];
    document.getElementById("pourcentage"+list[0]).style.color = list[3];
    document.getElementById("score"+list[0]).innerHTML = list[1];
    document.getElementById("pourcentage"+list[0]).innerHTML = list[2];
}

function UpdateRunningBlock(list){
    const input_code = document.getElementById("Input-"+list[0])
    input_code.textContent = list[1];
    const output_code = document.getElementById("Your output-"+list[0]);
    output_code.textContent = list[2];
    const expected_input_code = document.getElementById("Expected output-"+list[0]);
    expected_input_code.textContent = list[3];
    const sample_test = document.getElementById(list[0]);
    sample_test.style.color = list[4];
}
