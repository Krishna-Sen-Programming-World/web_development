function fn(){
var x=document.getElementById("gsearch").value;
if(x.length!=0){
var k = `https://www.google.com/search?q=${x}`;
location.href=`${k}`;}}
function fn1(){
    var x=document.getElementById("gsearch");
    x.addEventListener('keypress', function(cli){
    if(cli.key === "Enter"){
    document.getElementById('lnk').click();}})
}
function fn2()
{
    location.href="https://www.google.com/doodles";
}