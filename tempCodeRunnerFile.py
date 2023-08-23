
        
       # Monday workout (Workout Group 1)
        monday_workout_group1 = WorkoutRoutine(day='Monday', workout_group=1)
        db.session.add(monday_workout_group1)

        monday_exercises_group1 = [
            Exercise(name='Squats', sets=3, reps=12, workout_routine=monday_workout_group1),
            Exercise(name='Leg Extensions', sets=3, reps=12, workout_routine=monday_workout_group1),
            Exercise(name='Leg Curls', sets=3, reps=12, workout_routine=monday_workout_group1),
            Exercise(name='Bulgarian Split Squats', sets=3, reps=10, workout_routine=monday_workout_group1),
            Exercise(name='Calf Raises', sets=3, reps=20, workout_routine=monday_workout_group1)
        ]
        db.session.add_all(monday_exercises_group1)

        # Wednesday workout (Workout Group 1)
        wednesday_workout_group1 = WorkoutRoutine(day='Wednesday', workout_group=1)
        db.session.add(wednesday_workout_group1)

        wednesday_exercises_group1 = [
            Exercise(name='Tricep Pushdown', sets=3, reps=12, workout_routine=wednesday_workout_group1),
            Exercise(name='Lateral Raises', sets=3, reps=12, workout_routine=wednesday_workout_group1),
            Exercise(name='Shoulder Press', sets=3, reps=12, workout_routine=wednesday_workout_group1),
            Exercise(name='Dumbbell Row', sets=3, reps=12, workout_routine=wednesday_workout_group1),
            Exercise(name='Bench Press', sets=3, reps=12, workout_routine=wednesday_workout_group1)
        ]
        db.session.add_all(wednesday_exercises_group1)

        # Friday workout (Workout Group 1)
        friday_workout_group1 = WorkoutRoutine(day='Friday', workout_group=1)
        db.session.add(friday_workout_group1)

        friday_exercises_group1 = [
            Exercise(name='Squats', sets=3, reps=12, workout_routine=friday_workout_group1),
            Exercise(name='Leg Extensions', sets=3, reps=12, workout_routine=friday_workout_group1),
            Exercise(name='Leg Curls', sets=3, reps=12, workout_routine=friday_workout_group1),
            Exercise(name='Bulgarian Split Squats', sets=3, reps=10, workout_routine=friday_workout_group1),
            Exercise(name='Calf Raises', sets=3, reps=20, workout_routine=friday_workout_group1)
        ]
        db.session.add_all(friday_exercises_group1)

        db.session.commit()