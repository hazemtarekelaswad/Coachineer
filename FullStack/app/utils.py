import ExerciseEvaluator

exercises = [
    {
        "id": ExerciseEvaluator.ExerciseType.BICEPS_CURLS.value,
        "type": ExerciseEvaluator.ExerciseType.BICEPS_CURLS,
        "name": "Biceps Curls",
        "image": "biceps_curls.jpg",
    },
    {
        "id": ExerciseEvaluator.ExerciseType.SQUATS.value,
        "type": ExerciseEvaluator.ExerciseType.SQUATS,
        "name": "Squats",
        "image": "squats.jpg",
    },
    {
        "id": ExerciseEvaluator.ExerciseType.LEG_RAISES.value,
        "type": ExerciseEvaluator.ExerciseType.LEG_RAISES,
        "name": "Leg Raises",
        "image": "leg_raises.png",
    },
    {
        "id": ExerciseEvaluator.ExerciseType.LATERAL_RAISES.value,
        "type": ExerciseEvaluator.ExerciseType.LATERAL_RAISES,
        "name": "Lateral Raises",
        "image": "lateral_raises.jpg",
    }
]


joints = [jointType.name.lower() for jointType in ExerciseEvaluator.JointType]
