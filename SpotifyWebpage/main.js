function fn11(){
    $('#startplay').css('display','none');
    $('#stopplay').css('display','block');
}
var ch1;
var ch2;
function fn22(){
    $('#startplay').css('display','block');
    $('#stopplay').css('display','none');
}
var counterfortune=0;
function fn55(k){
    counterfortune=k;
    if(k==1){
        $('.logo1').css('display','block');
        $('#head1').css('display','none');
        $('.logo2').css('display','none');
        $('#head2').css('display','block');
        $('.logo3').css('display','none');
        $('#head3').css('display','block');
        $('.logo4').css('display','none');
        $('#head4').css('display','block');
    }
    if(k==2){
        $('.logo2').css('display','block');
        $('#head2').css('display','none');
        $('.logo1').css('display','none');
        $('#head1').css('display','block');
        $('.logo3').css('display','none');
        $('#head3').css('display','block');
        $('.logo4').css('display','none');
        $('#head4').css('display','block');
    }
    if(k==3){
        $('.logo3').css('display','block');
        $('#head3').css('display','none');
        $('.logo1').css('display','none');
        $('#head1').css('display','block');
        $('.logo2').css('display','none');
        $('#head2').css('display','block');
        $('.logo4').css('display','none');
        $('#head4').css('display','block');
    }
    if(k==4){
        $('.logo4').css('display','block');
        $('#head4').css('display','none');
        $('.logo1').css('display','none');
        $('#head1').css('display','block');
        $('.logo2').css('display','none');
        $('#head2').css('display','block');
        $('.logo3').css('display','none');
        $('#head3').css('display','block');
    }

    fnch(counterfortune);
}
function fn44(){
    ++counterfortune;
    if(counterfortune==5){
        counterfortune=1}
        fn55(counterfortune);
        fnch();
}
function fn33(){
    --counterfortune;
    if(counterfortune==0||counterfortune==-1){
        counterfortune=4}
        fn55(counterfortune);
        fnch();
}
function fnch()
{
    if(counterfortune==1)
    document.getElementById('changed').setAttribute('src','{Demon Slayer} Gurenge - Lisa (First Take) - English lyrics _ Romaji.mp3');
    if(counterfortune==2)
    document.getElementById('changed').setAttribute('src','Legends Never Die (ft. Against The Current) _ Worlds 2017 - League of Legends.mp3');
    if(counterfortune==3)
    document.getElementById('changed').setAttribute('src','Unstoppable - Sia (Lyric Video).mp3');
    if(counterfortune==4)
    document.getElementById('changed').setAttribute('src','Goku - Migatte no Gokui - Ultra instinto - KA KA KACHI DAZE SONG.mp3');
    document.getElementById('changed').play();
}