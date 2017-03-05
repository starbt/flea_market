
 function reply(name) {
    inputPrefix = "对@ " + name + " 说:";
   	var input = document.getElementById("comment_input");
 	input.innerHTML= inputPrefix;
 	moveEnd(input)
}

function report(){
    alert("您已经成功举报该商品！");
}

function moveEnd(obj){
    obj.focus();
    var len = obj.value.length;
    if (document.selection) {
        var sel = obj.createTextRange();
        sel.moveStart('character',len);
        sel.collapse();
        sel.select();
    } else if (typeof obj.selectionStart == 'number' && typeof obj.selectionEnd == 'number') {
        obj.selectionStart = obj.selectionEnd = len;
    }
 }