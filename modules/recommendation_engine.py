
import numpy as np
from sklearn.cluster import KMeans


class RecommendationEngine:
    def __init__(self):
        # Simplified health guidelines
        self.health_guidelines = {
            'heart_disease': {'increase': ['fiber'], 'reduce': ['fats']},
            'diabetes': {'increase': ['protein', 'fiber'], 'reduce': ['carbs']},
            'general_health': {'increase': ['fiber', 'protein'], 'reduce': []}
        }

    def generate_recommendations(self, user_profile, nutrition_analysis, activity_analysis):
        recommendations = {
            'nutrition': {},
            'exercise': {},
            'lifestyle': {},
            'priority_actions': []
        }

        # Nutrition recommendations
        nutrition_recs = self._generate_nutrition_recommendations(
            user_profile,
            nutrition_analysis
        )
        recommendations['nutrition'] = nutrition_recs

        # Exercise recommendations
        exercise_recs = self._generate_exercise_recommendations(
            user_profile,
            activity_analysis
        )
        recommendations['exercise'] = exercise_recs

        # Lifestyle recommendations
        lifestyle_recs = self._generate_lifestyle_recommendations(
            user_profile,
            nutrition_analysis,
            activity_analysis
        )
        recommendations['lifestyle'] = lifestyle_recs

        # Priority actions
        recommendations['priority_actions'] = self._identify_priority_actions(
            nutrition_analysis,
            activity_analysis,
            user_profile
        )

        return recommendations

    def _generate_nutrition_recommendations(self, user_profile, nutrition_analysis):
        goal = user_profile.get('goal', 'general_health')
        tdee = user_profile.get('tdee', 2000)

        # Calorie adjustments
        calorie_adjustments = {'weight_loss': -500, 'muscle_gain': 300, 'general_health': 0}
        calorie_target = int(tdee + calorie_adjustments.get(goal, 0))

        # Macronutrient ratios
        macro_ratios = {
            'muscle_gain': {'protein': '30%', 'carbs': '45%', 'fats': '25%'},
            'weight_loss': {'protein': '30%', 'carbs': '40%', 'fats': '30%'},
            'general_health': {'protein': '20%', 'carbs': '50%', 'fats': '30%'}
        }

        # Health-based food suggestions
        health_focus = user_profile.get('health_focus', 'general_health')
        guidelines = self.health_guidelines.get(health_focus, self.health_guidelines['general_health'])

        return {
            'calorie_target': calorie_target,
            'macronutrient_targets': macro_ratios.get(goal, macro_ratios['general_health']),
            'foods_to_increase': ['chicken', 'eggs', 'broccoli', 'rice', 'banana'][:3],
            'foods_to_reduce': guidelines['reduce'],
            'meal_suggestions': 'Balanced meals with protein, carbs, and vegetables'
        }

    def _generate_exercise_recommendations(self, user_profile, activity_analysis):
        goal = user_profile.get('goal', 'general_health')
        current_level = activity_analysis.get('activity_level', 'sedentary')

        # Goal-based exercise plans
        exercise_plans = {
            'weight_loss': {'minutes': 250, 'intensity': 'moderate_to_vigorous', 'activities': ['jogging', 'cycling', 'swimming']},
            'muscle_gain': {'minutes': 180, 'intensity': 'high', 'activities': ['weightlifting', 'strength_training']},
            'general_health': {'minutes': 150, 'intensity': 'moderate', 'activities': ['walking', 'yoga', 'cycling']}
        }

        plan = exercise_plans.get(goal, exercise_plans['general_health'])

        # Generate simple weekly plan
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        activity_plan = [
            {'day': day, 'activity': plan['activities'][i % len(plan['activities'])],
             'duration': 30 if i < 5 else 0}
            for i, day in enumerate(days)
        ]

        # Adjust for beginners
        if current_level == 'sedentary':
            for activity in activity_plan:
                activity['duration'] = int(activity['duration'] * 0.6)

        return {
            'weekly_target_minutes': plan['minutes'],
            'intensity_level': plan['intensity'],
            'activity_plan': activity_plan,
            'rest_days': 2
        }

    def _generate_lifestyle_recommendations(self, user_profile, nutrition_analysis, activity_analysis):
        consistency = activity_analysis.get('consistency_score', 0)
        return {
            'hydration': 'Drink 8-10 glasses of water daily',
            'sleep': 'Aim for 7-9 hours of quality sleep',
            'stress_management': 'Practice mindfulness and take regular breaks',
            'habits_to_build': ['Build consistent exercise routine', 'Plan meals ahead', 'Track progress']
                               if consistency < 50 else ['Increase exercise intensity', 'Try new recipes', 'Set progressive goals']
        }

    def _identify_priority_actions(self, nutrition_analysis, activity_analysis, user_profile):
        priorities = []

        # Nutrition gaps
        adherence = nutrition_analysis.get('adherence_to_requirements', {})
        priorities.extend([f"Increase {nutrient} intake ({percentage}% of requirement)"
                          for nutrient, percentage in adherence.items() if percentage < 70])

        # Activity recommendations
        if activity_analysis.get('activity_level') == 'sedentary':
            priorities.append("Start with 20-30 minutes of moderate activity daily")

        if activity_analysis.get('consistency_score', 0) < 50:
            priorities.append("Focus on building consistent daily habits")

        return priorities[:3]
