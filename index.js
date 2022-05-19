disable();//Invokes the disable function to prevent invoking functions when a unnecessary button clicked early in the game.
let cards = ["AH","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH",
"AC","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC",
"AS","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS",
"AD","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD"];//Card's suits and values in the form of string value.  
let cards2 = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10 , 10, 10,
11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10 , 10, 10,
11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10];//Card's values in the form of integer values.
let unique = false; //this is a boolean value for prevent double winning.
document.getElementById("double").onclick = function(){//Double button can only be offered directly after the two initial cards have been dealt.
    let quantity = document.getElementById("bet").value; //When you hit the double button it checks the initial bet and substract from bank then controls if it's a negative value.
    quantity = Number(quantity);
    let bank = document.getElementById("bank").value;
    bank -= quantity;
    if(bank < 0){
        window.alert("You don't have enough money!");//Alerts when it's negative
    }
    else{//If it's not negative it updates both bank and bet sections
        document.querySelector('#double').disabled = true;
        let mybank = document.getElementById("bank").value;
        mybank = Number(mybank);
        let remainder = mybank - quantity;
        document.getElementById("bank").value = remainder;
        document.getElementById("bet").value = 2*quantity;

        let temp = document.getElementById("hit");
        if (typeof temp.onclick == "function") {//Then invokes the hit function first. In the hit function, if you will win then your unique value will become true. Thus it won't invoke stand function, because it is unnecessary and it may cause double winning.
            temp.onclick.apply(temp);
            if(unique != true){//checks whether unique is true or false.
                let temp2 = document.getElementById("stand");
                if (typeof temp2.onclick == "function") {
                    temp2.onclick.apply(temp2);
                }
            }      
        } 
    }
}
document.getElementById("reset").onclick = function(){//Resets the innerHTML values for next round. Also makes bet button functional again.
    document.getElementById("results").innerHTML = ``;
    document.getElementById("img").innerHTML = ``;
    document.getElementById("imgofcom").innerHTML = ``;
    document.getElementById("hand").value = ``;
    document.getElementById("bet").value = ``;
    document.querySelector('#betbutton').disabled = false;
}
document.getElementById("betbutton").onclick = function(){
    let quantity = document.getElementById("bet").value;//Checks the value in the bet section
    quantity = Number(quantity);
    if(Number.isInteger(quantity)){//Controls if it's a integer value
        if(quantity > 0){//Checks the value again whether it's negative or positive.
            let bank = document.getElementById("bank").value;
            bank -= quantity;
            if(bank < 0){
                window.alert("You don't have enough money!");
            }
            else{
                document.querySelector('#betbutton').disabled = true;
                let mybank = document.getElementById("bank").value;
                mybank = Number(mybank);
                let remainder = mybank - quantity;
                document.getElementById("bank").value = remainder;//Substract the bet value and updates the bank section.
                game();
            }
        }
        else{
            window.alert("You need to bet a positive value !");
        }
    }
    else{
        window.alert("Please enter a valid value !");
    } 
}
function sumup(i,boolean){//This function is responsible for adding the bet values into the bank. 
    if(boolean == true){//If the boolean value(in our code it's the 'unique' variable) equals true. It just returns the value. This prevents double winning. 
        return boolean;
    }
    else{//If the boolean is false then it updates the bank to bet that multiplied by 'i'. I, value becomes 1 when it's a draw and becomes 2 when it's a win condition. 
        let temp = document.getElementById("bet").value;
        let temp2 = document.getElementById("bank").value;
        temp = Number(temp);
        temp2 = Number(temp2);
        temp2 += (i*temp);
        document.getElementById("bank").value = temp2;
    }
}
function disable(){//This function responsible for making hit, stand and double unfunctional.
    document.querySelector('#hit').disabled = true;
    document.querySelector('#stand').disabled = true; 
    document.querySelector('#double').disabled = true; 

}
function results(total, totalcom,unique){//This function compares the dealer's hand's and your hand's values for updating results section and make the updates in bank and disables clicking the unnecessary buttons, by invoking other functions. 
    if(total > totalcom){
        sumup(2,unique);
        unique = true;
        document.getElementById("results").innerHTML = `Your hand is ${total} and Dealer's is ${totalcom}. You won!`
        disable();
    }
    else if(totalcom > total){
        document.getElementById("results").innerHTML = `Your hand is ${total} and Dealer's is ${totalcom}. You lost.`
        disable();
    }
    else{
        sumup(1,unique);
        unique = true;
        document.getElementById("results").innerHTML = `Your hand is ${total} and Dealer's is ${totalcom}. It's a draw! `
        disable();
    }
}
function reveal(randompc1, randompc2){//This function responsible for flipping the card in the dealer's hand at the initial state.
    document.getElementById("imgofcom").innerHTML = `<img class="pictures" src= ../assets/${cards[randompc1]}.png width="66" height="100" title="This card's value is(if it is an ace, it can differ):${cards2[cards.indexOf(cards[randompc1])]}"><img class="pictures" src= ..assets/${cards[randompc2]}.png width="66" height="100" title="This card's value is(if it is an ace, it can differ):${cards2[cards.indexOf(cards[randompc2])]}">`
}
function game(){
    unique = false;//Unique variable's initial value is false
    document.querySelector('#double').disabled = false; //Makes hit, stand and double buttons functional.
    document.querySelector('#hit').disabled = false;
    document.querySelector('#stand').disabled = false;
    document.querySelector('#betbutton').disabled = true;//Makes bet button unfunctional for preventing placing bet during the game.
  
    let random1 = Math.floor(Math.random()*cards.length), random2 = Math.floor(Math.random()*cards.length); //Randomly chooses your hand's initial cards' indexes. 
    let randompc1 = Math.floor(Math.random()*cards.length), randompc2 = Math.floor(Math.random()*cards.length);//Randomly chooses dealer's hand's initial cards' indexes.

    //In the below, it changes the innerHTML of those ids with images that include necessary cards' images. I named cards' png files with the same names as the cards in the array: cards.
    document.getElementById("img").innerHTML = `<img class="pictures" src= ..assets/${cards[random1]}.png width="66" height="100" title="This card's value is(if it is an ace, it can differ):${cards2[cards.indexOf(cards[random1])]}"><img class="pictures" src= ..assets/${cards[random2]}.png width="66" height="100" title="This card's value is(if it is an ace, it can differ):${cards2[cards.indexOf(cards[random2])]}">`
    document.getElementById("imgofcom").innerHTML = `<img class="pictures" src= ..assets/${cards[randompc1]}.png width="66" height="100" title="This card's value is(if it is an ace, it can differ):${cards2[cards.indexOf(cards[randompc1])]}"><img class="pictures" src= "..assets/Cardback.png" width="66" height="100" title="You should not know this card's value!">`

    //Calculates the value of cards in your and the dealer's hands.
    var total = cards2[cards.indexOf(cards[random1])] + cards2[cards.indexOf(cards[random2])];
    var totalcom = cards2[cards.indexOf(cards[randompc1])] + cards2[cards.indexOf(cards[randompc2])];

    total = Number(total);
    totalcom = Number(totalcom);

    let acecounter = 0, acecounterpc = 0;
    //Checks if the initial cards have any aces.
    if(cards[random1]== "AH"||cards[random1] == "AC" ||cards[random1]=="AD"|| cards[random1]=="AS"){
        acecounter += 1;
    }
    if(cards[random2]== "AH"||cards[random2] == "AC" ||cards[random2]=="AD"|| cards[random2]=="AS"){
        acecounter += 1;
    }
    if(cards[randompc1]== "AH"||cards[randompc1] == "AC" ||cards[randompc1]=="AD"|| cards[randompc1]=="AS"){
        acecounterpc += 1;
    }
    if(cards[randompc2]== "AH"||cards[randompc2] == "AC" ||cards[randompc2]=="AD"|| cards[randompc2]=="AS"){
        acecounterpc += 1;
    }
    //If the initial hand's value is 22 it means there's two aces and one of them must be count as 1.
    if(total == 22 ){
        total -= 10;
        acecounter -=1;
    }
    if(totalcom == 22 ){
        totalcom -= 10;
        acecounterpc -=1;
    }

    document.getElementById("hand").value = total;

    //Checks the instant win and lose conditions below.
    if(totalcom == 21 && total == 21){
        reveal(randompc1, randompc2);
        sumup(1,unique);
        unique = true;
        document.getElementById("results").innerHTML = `Both hands are Blackjack. It's a draw!`
        disable();
    }
    else if(total == 21 ){
        reveal(randompc1, randompc2);
        sumup(2,unique);
        unique = true;
        document.getElementById("results").innerHTML = `Your hand is ${total}! Blackjack!.`
        disable();
    }
    else if(totalcom == 21 ){
        disable();
        reveal(randompc1, randompc2);
        document.getElementById("results").innerHTML = `Dealer's hand is ${totalcom}! Blackjack!. You lost!`
    }

    document.getElementById("stand").onclick = function(){
        if(total > 21){//I have no idea why this is here, but i remember it fixes something :)
            reveal(randompc1,randompc2);
            document.getElementById("results").innerHTML = `Your hand is ${total}! You busted!.`      
        }
        else{
            if(totalcom < 17){//If the dealer's hand's value is less than 17, dealer must be draw cards until it is greater or equal to 17.
                reveal(randompc1, randompc2);//First it flip the card in the initial state.
                while(totalcom < 17){//Draws cards until the hand's value become greater or equal to 17.
                    let random1 = Math.floor(Math.random()*cards.length);
                    document.getElementById("imgofcom").innerHTML += `<img class="pictures" src= ..assets/${cards[random1]}.png width="66" height="100" title="This card's value is(if it is an ace, it can differ):${cards2[cards.indexOf(cards[randompc1])]}">`
                    if(cards[random1]== "AH"||cards[random1] == "AC" ||cards[random1]=="AD"|| cards[random1]=="AS"){
                        acecounterpc += 1;
                    }
                    let newquant = cards2[cards.indexOf(cards[random1])];

                    newquant= Number(newquant);

                    totalcom += newquant;
                    if(totalcom > 21){
                        if(acecounterpc > 0){
                            totalcom -= 10;
                            acecounterpc -= 1;
                        }
                    }
                }
                //Checks the instant win conditions.
                if(totalcom == 21){
                    document.getElementById("results").innerHTML = `Dealer's hand is ${totalcom}! Blackjack!. You lost.`;
                    disable();
                }
                else if(totalcom > 21){
                    if(acecounterpc == 1 || acecounterpc ==2){
                    totalcom -= 10;
                    acecounterpc -= 1;
                        if(totalcom == 21){
                        document.getElementById("results").innerHTML = `Dealer's hand is ${totalcom}! Blackjack!. You lost.`
                        disable();
                        }
                        else{
                        results(total, totalcom,unique);
                        }
                    }
                    else{
                        sumup(2,unique);
                        unique = true;
                        document.getElementById("results").innerHTML = `Dealer's hand is ${totalcom}!. You won!`
                        disable();
                    }
                }
                else if(totalcom < 21){
                    results(total, totalcom,unique);
                }
            }
            else{//If the dealer's hand's value is greater or equal to 17 it flips the card and shows the results.
                reveal(randompc1, randompc2);
                results(total, totalcom,unique);
            }
        }      
    }

    document.getElementById("hit").onclick = function(){//It's draws one card and check the conditions when it's clicked.

        document.querySelector('#double').disabled = true;
        let random1 = Math.floor(Math.random()*cards.length);

        document.getElementById("img").innerHTML += `<img class="pictures" src= ..assets/${cards[random1]}.png width="66" height="100" title="This card's value is(if it is an ace, it can differ):${cards2[cards.indexOf(cards[random1])]}">`
        if(cards[random1]== "AH"||cards[random1] == "AC" ||cards[random1]=="AD"|| cards[random1]=="AS"){
            acecounter += 1;
        }

        let newquant = cards2[cards.indexOf(cards[random1])];

        newquant = Number(newquant);

        total += newquant;

        if(total == 21){
            document.getElementById("hand").value = total;
            reveal(randompc1, randompc2);
            sumup(2,unique);
            unique = true;
            document.getElementById("results").innerHTML = `Your hand is ${total}! Blackjack!.`
            disable();
        }
        else if(total < 21){
            document.getElementById("hand").value = total;
        }
        else if(total > 21){
            if(acecounter == 1 || acecounter ==2){
                total -= 10;
                acecounter -= 1;
                document.getElementById("hand").value = total;
                if(total == 21){
                    reveal(randompc1, randompc2);
                    sumup(2,unique);
                    unique = true;
                    document.getElementById("results").innerHTML = `Your hand is ${total}! Blackjack!.`
                    disable();
                }
            }
            else{
                document.getElementById("hand").value = total;
                disable();
                reveal(randompc1, randompc2);
                document.getElementById("results").innerHTML = `Your hand is ${total}! You busted!`
            }      
        }
    }
}
/*Flaws:
The biggest flaw is deck isn't lessen when cards drawn,
Secondly, it's not a flaw but a deficiency, there's no split button.*/