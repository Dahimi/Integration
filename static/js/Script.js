let editor;
window.onload = function() {
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");
}


function LunchTests(){
    document.getElementById("spinner").style.display = "block";
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
                    document.getElementById("spinner").style.display = "none";
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
