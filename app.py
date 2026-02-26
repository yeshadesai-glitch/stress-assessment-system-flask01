from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "stress_project_secret"

weights={'sleep':3,'emotion':3,'energy':2,'nutrition':2,'concentration':2,'mental':2,
         'procrastination':2,'emotional_reactivity':2,'motivation':2,
         'restlessness':2,'physical':1,'social':1,'screen_time':1}

severity={1:2,2:1,3:0}

questions={
    'sleep':{
        'question':'Over the past 7 days, how would you describe your sleep?',
        'options':[
            'Poor (difficulty falling asleep/waking up tired)',
            'Average (some disturbance)',
            'Good (restful and consistent)'
        ]
    },
    'emotion':{
        'question':'Over the past 7 days, how often have you felt internally irritable, anxious, or emotionally overwhelmed?',
        'options':['Often','Sometimes','Rarely']
    },
    'energy':{
        'question':'Over the past 7 days, how would you rate your daily energy levels?',
        'options':['Low (tired most of the day)','Moderate','High']
    },
    'nutrition':{
        'question':'Over the past 7 days, how regular and balanced were your meals?',
        'options':['Irregular/frequently skipped (noticed a loss of appetite)','Mostly regular','Regular and balanced']
    },
    'concentration':{
        'question':'Over the past 7 days, how well were you able to concentrate on tasks and studies? (Did you do it willingly?)',
        'options':['Poor focus','Average focus','Good focus']
    },
    'physical':{
        'question':'Over the past 7 days, have you experienced physical discomfort often linked to stress (e.g. headaches, muscle tension, etc.)?',
        'options':['Frequently','Occasionally','Rarely / not at all']
    },
    'social':{
        'question':'Over the past 7 days, how often did you feel like avoiding social interaction?',
        'options':['Often','Sometimes','Rarely']
    },
    'mental':{
        'question':'Over the past 7 days, how often did you feel mentally "cluttered" or unable to think clearly?',
        'options':['Frequently','Occasionally','Rarely']
    },
    'procrastination':{
        'question':'Over the past 7 days, did you delay important tasks even when you knew they needed attention?',
        'options':['Yes, often','Sometimes','Rarely']
    },
    'emotional_reactivity':{
        'question':'Over the past 7 days, did you react more strongly towards others than usual due to minor issues?',
        'options':['Yes, often','Sometimes','No']
    },
    'restlessness':{
        'question':'Over the past 7 days, did you feel physically restless or unable to relax?',
        'options':['Often','Sometimes','Rarely']
    },
    'screen_time':{
        'question':'Over the past 7 days, did you resort to social media rather than prioritizing important work?',
        'options':['Frequently','Occasionally','Rarely']
    },
    'motivation':{
        'question':'Over the past 7 days, how motivated did you feel to complete responsibilities/tasks?',
        'options':['Low','Moderate','High']
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/questions')
def question_page():
    return render_template('questions.html', questions=questions)

@app.route('/result', methods=['POST'])
def result():
    stress_scores={}
    for factor in questions:
        answer=int(request.form.get(factor))
        factor_score=severity[answer]*weights[factor]
        stress_scores[factor]=factor_score

    stress_score=sum(stress_scores.values())

    if stress_score < 15:
        level="🟢 Managing Stress Well"
        explanation="Healthy HPA axis regulation. Cortisol levels appear balanced."
        advice=[
            "Maintain regular sleep timing.",
            "Stay physically active.",
            "Take structured breaks.",
            "Keep a balanced daily schedule."
        ]
    elif stress_score < 25:
        level="🟡 Early Signs of Stress"
        explanation="Mild HPA axis activation may influence sleep and focus."
        advice=[
            "Improve sleep timing.",
            "Reduce night screen use.",
            "Plan tasks in small steps.",
            "Add short daily movement."
        ]
    elif stress_score < 35:
        level="🟠 Moderate Stress Detected"
        explanation="Sustained HPA activation may affect emotional balance."
        advice=[
            "Fix sleep schedule immediately.",
            "Break large tasks into small goals.",
            "Practice slow breathing (4-4-6 pattern).",
            "Talk to a trusted adult."
        ]
    else:
        level="🔴 High Stress Level Detected ⚠️"
        explanation="Persistent cortisol elevation may disrupt biological systems."
        advice=[
            "Prioritize sleep urgently.",
            "Reduce unnecessary workload.",
            "Limit excessive screen exposure.",
            "Use grounding techniques daily.",
            "Seek guidance from a parent, teacher, or counselor."
        ]

    session['advice']=advice

    return render_template('result.html',
                           score=stress_score,
                           breakdown=json.dumps(stress_scores),
                           level=level,
                           explanation=explanation)

@app.route('/advice')
def advice_page():
    advice=session.get('advice',[])
    return render_template('advice.html', advice=advice)

if __name__ == "__main__":
    app.run(debug=True)
