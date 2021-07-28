const testDB = [
    {
        question: "Q1: Life is always good.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q2: I like to observe, think and analyze to find pros and cons.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q3: I like to read and learn.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q4: I simulate a lot of different situations to see how I would react.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q5: I read or watch a lot to improve myself.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q6: I believe that people always have good intentions.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q7: I panic easily.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q8: I get irritated easily.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q9: I go-out of my own to seek adventure.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q10: I prefer to be alone.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q11: I love to daydream.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q12: I always leave the place in a mess.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q13: I am attached to conventional ways.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q14: I boast about my virtues.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q15: I try to think about the needy.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q16: I wait for others to take the lead.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q17: I feel that I'm unable to deal with things.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q18: I easily resist temptations.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q19: I break rules.",
        a : "Yes",
        b : "No",
    },
    {
        question: "Q20: I make friends easily",
        a : "Yes",
        b : "No",
    },
];
const obj=[ ];
const question = document.querySelector('.question');
const option1 = document.querySelector('#option1');
const option2 = document.querySelector('#option2');
const submit = document.querySelector('#submit');

const answers = document.querySelectorAll('.answer');

const showResult = document.querySelector('#showResult');

let questionCount = 0;


const loadQuestion = () => {

    const questionList = testDB[questionCount];
    question.innerText = questionList.question;

    option1.innerText = questionList.a;
    option2.innerText = questionList.b;         
}

loadQuestion();

const getCheckAnswer = () => {
    let answer;

    answers.forEach((curAnsElem) => {
         if(curAnsElem.checked){
            if(curAnsElem.id=="ans1")
               answer = question.innerText;      
         }
    });

    return answer;

};

const deselectAll = () => {
    answers.forEach((curAnsElem) => curAnsElem.checked = false);
}     

submit.addEventListener('click', () => {      
    const checkedAnswer = getCheckAnswer(); 
    if(checkedAnswer!=undefined) 
    obj.push(checkedAnswer);
    console.log(obj);             

    questionCount++;  //next question
    deselectAll();   //radio button deselect after next page
    if(questionCount < testDB.length){
        loadQuestion();
    }else{
         fetch('', {
            method: 'POST',
            body: JSON.stringify(obj),
            headers: {'Accept': 'application/json',
                'Content-Type': 'application/json',
               // "X-CSRFToken":  getCookie("csrftoken") 
            },
        })
            fetch('http://127.0.0.1:8000/')
                .then(data => data.json())
                .then(post => {
                console.log(post);
                });
        //console.log(ans);
        //window.location.href = "newhttp://example.com/_url";
        //showResult.classList.remove('ResultArea');
    }
});