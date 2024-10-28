from healthCare import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    



questions = [
    "I relapse way too easily in my drinking/smoking habit",
    "i feel sad and unhappy"
    "I have interest and joy in the aspects of my life that were of major importance to me",
    "i feel like i fall in everything i try",
    "I have difficulty in concentration and making of decisions",
    "I got constant anxiety and panic attacks",
    "I am agitated and keep moving around",
    "I am constantly looking over my show in fear",
    "I feel like the urger to move on from my negative thought is lacking",
    "I live too much in my head, creating negative ideas, thoughts that will only bring me harm",
    "I feel fatigued",
    "I feel trapped or caught",
    "Most of the times I am broke I get mad"
]
