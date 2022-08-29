const ClickMusic= new Audio("click.mp3");
const sadMusic=new Audio("sad.mp3");
const happyMusic=new Audio("congratulations.mp3");
const grids=document.getElementsByClassName('grids')
const gridBox=document.getElementsByClassName('gridBox');
const plc=document.getElementsByClassName('plch');
const results=document.getElementsByClassName('results');
const reset=document.getElementsByClassName('reset');
const gif=document.getElementsByClassName('gif');
const valxo=document.getElementsByClassName('valxo');
const value=['O','X'];
var z=1;var winnername='It is a draw';var flag=0;
function fnresult(){
    if(winnername=='X'||winnername=='O'){
        results[0].innerHTML="winner is "+winnername;
        gif[0].style.backgroundImage="url('win.gif')";
        happyMusic.play();
        gif[0].style.height='9rem';}
        else {results[0].innerHTML=winnername;
            sadMusic.play();
            gif[0].style.backgroundImage="url('sorry.gif')"; 
            gif[0].style.height='9rem';}
    z=10; flag=1;}
reset[0].addEventListener('click',function(){
    for(let xx=0;xx<9;xx++)
    grids[xx].innerHTML='';
    z=1;winnername='It is a draw';flag=0;
    results[0].innerHTML=`Turn for player <span class="plch">X</span>`;
    gif[0].style.height='0rem'; 
  })
function fnwhothewinneris(){
    if     ((grids[0].innerHTML==grids[1].innerHTML)&&(grids[1].innerHTML==grids[2].innerHTML)&&((grids[0].innerHTML=='X')||(grids[0].innerHTML=='O'))){winnername=grids[0].innerHTML;flag=1;fnresult();}
    else if((grids[3].innerHTML==grids[4].innerHTML)&&(grids[4].innerHTML==grids[5].innerHTML)&&((grids[3].innerHTML=='X')||(grids[3].innerHTML=='O'))){winnername=grids[3].innerHTML;flag=1;fnresult();}
    else if((grids[6].innerHTML==grids[7].innerHTML)&&(grids[7].innerHTML==grids[8].innerHTML)&&((grids[6].innerHTML=='X')||(grids[6].innerHTML=='O'))){winnername=grids[6].innerHTML;flag=1;fnresult();}
    else if((grids[0].innerHTML==grids[3].innerHTML)&&(grids[3].innerHTML==grids[6].innerHTML)&&((grids[0].innerHTML=='X')||(grids[0].innerHTML=='O'))){winnername=grids[0].innerHTML;flag=1;fnresult();}
    else if((grids[1].innerHTML==grids[4].innerHTML)&&(grids[4].innerHTML==grids[7].innerHTML)&&((grids[1].innerHTML=='X')||(grids[1].innerHTML=='O'))){winnername=grids[1].innerHTML;flag=1;fnresult();}
    else if((grids[2].innerHTML==grids[5].innerHTML)&&(grids[5].innerHTML==grids[8].innerHTML)&&((grids[2].innerHTML=='X')||(grids[2].innerHTML=='O'))){winnername=grids[2].innerHTML;flag=1;fnresult();}
    else if((grids[0].innerHTML==grids[4].innerHTML)&&(grids[4].innerHTML==grids[8].innerHTML)&&((grids[0].innerHTML=='X')||(grids[0].innerHTML=='O'))){winnername=grids[4].innerHTML;flag=1;fnresult();}
    else if((grids[2].innerHTML==grids[4].innerHTML)&&(grids[4].innerHTML==grids[6].innerHTML)&&((grids[2].innerHTML=='X')||(grids[2].innerHTML=='O'))){winnername=grids[4].innerHTML;flag=1;fnresult();}
    else if(z==10){flag=1;fnresult()}
}
function fn1(x){
    if(flag==0 && z<10){
    if(grids[x].innervalue!='X'&& grids[x].innerHTML!='O'){
        grids[x].innerHTML=value[z++%2];  
        plc[0].innerHTML=value[z%2];
        fnwhothewinneris();
    }
    ClickMusic.play();}else{z=10;fnresult();}
}