function fn(num){
    document.getElementById('in').value+=`${num}`;
}
function fns(num){
    document.getElementById('in').value+=` ${num} `;
}
function fn1(){
    var wor=document.getElementById('in').value;
    const sr=wor.split(' ');
    var ans=parseFloat(sr[0]);
    for(var i=1;i<sr.length;i+=2){
        if(sr[i]=='+')
        {ans+=parseFloat(sr[i+1]);}
        if(sr[i]=='-')
        {ans-=parseFloat(sr[i+1]);}
        if(sr[i]=='*')
        {ans*=parseFloat(sr[i+1]);}
        if(sr[i]=='%')
        {ans%=parseFloat(sr[i+1]);}
        if(sr[i]=='/')
        {ans/=parseFloat(sr[i+1]);}
        if(sr[i]=='^')
        {ans**=parseFloat(sr[i+1]);}
        if(sr[i]=='√')
        {ans= Math.sqrt(ans);}
    }
    document.getElementById('demo').innerHTML=ans;
}
function fner(){
    var wor=document.getElementById('in').value;
    const rm= wor.length-1;
    if(wor[rm]==' '){
    document.getElementById('in').value= wor.substring(0,rm-2);}
    else{
    document.getElementById('in').value= wor.substring(0,rm);}

}


function clr(){
    var wor=[];
    document.getElementById('in').value=wor;
}
function fcp(){
    var fc=document.getElementById('demo').innerHTML;
    document.getElementById('demoo').innerHTML=`${fc}`;
}
function fpt(){
    var wo=document.getElementById('demoo').innerHTML;
    document.getElementById('in').value+=wo;
}
function funent()
{
    var k=document.getElementById('doneeok');
    k.addEventListener('keypress',function(ent){
        if(ent.key=='='){
            document.getElementById('doneok').click();
        }
        else if(ent.key>=0 && ent.key<=9)
        {
            fn(ent.key);
        }
        else if( ent.key == '+' || ent.key === '-'|| ent.key == '*' || ent.key == '%' || ent.key == '/' || ent.key == '^'){
            fns(ent.key);
        }
    })
}
