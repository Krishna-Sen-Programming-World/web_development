arr=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'];
function fn(){
    return(Math.floor(Math.random()*16));
}
function fn1(){
    var val='#';
    for(var i=0;i<6;i++){
        val+=arr[fn()];
    }// console.log(`${val}`);
    $('.hexavalue').text(val);
    $('.fillcolor').css('background-color',val);
}   
function fn2(){
    var val='#';
    for(var i=0;i<8;i++){
        val+=arr[fn()];
    }// console.log(`${val}`);
    $('.hexavalue').text(val);
    $('.fillcolor').css('background-color',val);
}
var y=0;
function fn3()
{
    if(y==0){
        $('.three').text('Stop');
        y=setInterval(fn2,1000);
    }
    else{
        clearInterval(y);
        $('.three').text('Random');
        y=0;
    }
}