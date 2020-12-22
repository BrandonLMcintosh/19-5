class Game {
    constructor(name, seconds = 60){
        this.seconds = seconds;
        this.words = new Set();
        this.score = 0;
        this.name = name;
        this.timer = setInterval(this.countdown.bind(this), 1000);
        $("#wordForm").on("submit", this.submitWord.bind(this));
    }

    async countdown(){
        this.seconds -= 1;
        this.showTime();
        if(this.seconds <= 0){
            clearInterval(this.timer);
            await this.generateScore();
        }        
    }
    
    async submitWord(evt){
        evt.preventDefault()
        const word = $("#word").val();
        $("#word").val('');
        if(!word) return;
        const response = await axios.get("/get_word", {params: {word: word}});

        if(this.words.has(word)){
            return this.displayMessage("You've already guessed that word", "fail");
        }

        if(response.data.result === "not-word"){
            return this.displayMessage(`${word} is not a valid English word`, "fail");
        }else if (response.data.result === "not-on-board"){
            return this.displayMessage(`${word} is not a valid word on the Boggle board`, "fail");
        }else if (response.data.result === "ok"){
            this.score += word.length;
            this.displayScore();
            this.showWords(word);
            return this.displayMessage(`Added: ${word}`, "success");
        }
    }

    showTime(){
        $("#seconds").text(this.seconds);
    };

    showWords(word){
        this.words.add(word);
        const $words = $("#words");
        $words.empty();
        for(let word of this.words){
            $words.append(`<tr><td class="wordCell">${word}</td></tr>`);
        };
    };

    displayMessage(message, classStyle){
        $("#message").text(message).removeClass().addClass(classStyle);
    };

    async displayScore(){
        const numWords = this.words.length | 0;
        $("#score").text(this.score);
        $("#scoreNumWords").text(numWords);
        if(await isHighScore()){
            $("#highscore").text(this.score);
            $("#highscoreNumWords").text(numWords);
        };
    };

    async displayHighScore(){
        $("#wordForm").hide();
        const isHighScore = await this.isHighScore();
        if(isHighScore){
            this.displayMessage(`New Record: ${this.score}`, "success");
        }else{
            this.displayMessage(`Score: ${this.score}`, "success");
        };
    };

    async isHighScore() {
        const wordsLength = this.words.length ? this.words.length : 0;
        const response = await axios.post("/score", { score: this.score, words: wordsLength });
        return response.data.result;
    };
};

let game = new Game("boggle", 60)