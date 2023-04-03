import ExerciseEvaluator

exercises = [
    {
        "id": ExerciseEvaluator.ExerciseType.BICEPS_CURLS.value,
        "type": ExerciseEvaluator.ExerciseType.BICEPS_CURLS,
        "name": "Biceps Curls",
        "image": "biceps_curls.jpg",
    },
    {
        "id": 1,
        "name": "Squats",
        "image": "squats.jpg",
    },
    {
        "id": 2,
        "name": "Push Ups",
        "image": "pushups.jpg",
    },
    {
        "id": 3,
        "name": "Lateral Raises",
        "image": "biceps_curls.jpg",
    },
    {
        "id": 4,
        "name": "Pull ups",
        "image": "biceps_curls.jpg",
    },
    {
        "id": 5,
        "name": "Triceps Extensions",
        "image": "biceps_curls.jpg",
    }
]


joints = [jointType.name.lower() for jointType in ExerciseEvaluator.JointType]
