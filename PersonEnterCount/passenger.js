function incre(){
    let x= document.getElementById("values").innerHTML;    
    document.getElementById("values").innerHTML = parseInt(x)+1;
}
function decre(){
    let x= document.getElementById("values").innerHTML;
    if(x!=0)
    document.getElementById('values').innerHTML =parseInt(x)-1;
    else
    ocument.getElementById('values').innerHTML =parseInt(x);
}
function sav()
{
    let s=document.getElementById('sum').innerHTML;
    let h=document.getElementById('hist').innerHTML;
    let v= document.getElementById("values").innerHTML;  

    document.getElementById('sum').innerHTML=parseInt(s)+parseInt(v);
    document.getElementById('hist').innerHTML=`${h} + ${v}`; 
}
