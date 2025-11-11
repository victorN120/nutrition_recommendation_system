
import numpy as np
import pandas as pd


class ActivityTracker:
    def __init__(self):
        # MET (Metabolic Equivalent of Task) values for different activities
        self.activity_mets = {
            'walking': 3.5,
            'jogging': 7.0,
            'running': 9.8,
            'cycling': 8.0,
            'swimming': 7.0,
            'yoga': 2.5,
            'weightlifting': 6.0,
            'dancing': 4.5,
            'hiking': 6.5,
            'basketball': 8.0,
            'tennis': 7.3,
            'sedentary': 1.0,  # sitting, desk work
        }

        # Activity level thresholds (minutes per week)
        self.activity_levels = {
            'sedentary': (0, 30),
            'lightly_active': (30, 90),
            'moderately_active': (90, 150),
            'very_active': (150, 300),
            'extremely_active': (300, float('inf'))
        }

    def calculate_calories_burned(self, activity, duration_minutes, weight_kg=70):

        activity = activity.lower()

        if activity not in self.activity_mets:
            # Default to moderate activity if unknown
            met_value = 4.0
        else:
            met_value = self.activity_mets[activity]

        # Formula: Calories = MET × weight (kg) × duration (hours)
        calories = met_value * weight_kg * (duration_minutes / 60)

        return round(calories, 1)

    def analyze_activity_log(self, activity_log, weight_kg=70):
        total_calories = 0
        total_active_minutes = 0
        activities_breakdown = []

        for entry in activity_log:
            activity = entry.get('activity', '')
            duration = entry.get('duration', 0)

            if activity.lower() != 'sedentary':
                total_active_minutes += duration

            calories = self.calculate_calories_burned(activity, duration, weight_kg)
            total_calories += calories

            activities_breakdown.append({
                'activity': activity,
                'duration': duration,
                'calories_burned': calories
            })

        return {
            'total_calories_burned': round(total_calories, 1),
            'total_active_minutes': total_active_minutes,
            'activity_level': self._classify_activity_level(total_active_minutes * 7),  # weekly estimate
            'breakdown': activities_breakdown
        }

    def analyze_activity_history(self, activity_logs_history, weight_kg=70):
        daily_analyses = []

        for daily_log in activity_logs_history:
            analysis = self.analyze_activity_log(daily_log, weight_kg)
            daily_analyses.append(analysis)

        # Calculate statistics
        total_calories = sum(day['total_calories_burned'] for day in daily_analyses)
        total_minutes = sum(day['total_active_minutes'] for day in daily_analyses)

        avg_daily_calories = total_calories / len(daily_analyses)
        avg_daily_minutes = total_minutes / len(daily_analyses)
        weekly_minutes = avg_daily_minutes * 7

        return {
            'average_daily_calories_burned': round(avg_daily_calories, 1),
            'average_daily_active_minutes': round(avg_daily_minutes, 1),
            'weekly_active_minutes': round(weekly_minutes, 1),
            'activity_level': self._classify_activity_level(weekly_minutes),
            'consistency_score': self._calculate_consistency(daily_analyses)
        }

    def _classify_activity_level(self, weekly_minutes):
        for level, (min_val, max_val) in self.activity_levels.items():
            if min_val <= weekly_minutes < max_val:
                return level
        return 'sedentary'

    def _calculate_consistency(self, daily_analyses):
        active_days = sum(1 for day in daily_analyses if day['total_active_minutes'] > 20)
        consistency = (active_days / len(daily_analyses)) * 100
        return round(consistency, 1)

    def get_activity_recommendations(self, current_level, goal='health'):
        recommendations = {
            'target_weekly_minutes': 150,  # WHO recommendation
            'activities': [],
            'intensity': 'moderate'
        }

        if goal == 'weight_loss':
            recommendations['target_weekly_minutes'] = 250
            recommendations['intensity'] = 'moderate_to_vigorous'
            recommendations['activities'] = [
                {'activity': 'jogging', 'duration': 30, 'frequency': '5 days/week'},
                {'activity': 'cycling', 'duration': 45, 'frequency': '3 days/week'},
                {'activity': 'swimming', 'duration': 30, 'frequency': '2 days/week'}
            ]
        elif goal == 'fitness':
            recommendations['target_weekly_minutes'] = 200
            recommendations['intensity'] = 'vigorous'
            recommendations['activities'] = [
                {'activity': 'running', 'duration': 30, 'frequency': '4 days/week'},
                {'activity': 'weightlifting', 'duration': 45, 'frequency': '3 days/week'},
                {'activity': 'yoga', 'duration': 30, 'frequency': '2 days/week'}
            ]
        else:  # health
            recommendations['target_weekly_minutes'] = 150
            recommendations['intensity'] = 'moderate'
            recommendations['activities'] = [
                {'activity': 'walking', 'duration': 30, 'frequency': '5 days/week'},
                {'activity': 'yoga', 'duration': 30, 'frequency': '2 days/week'},
                {'activity': 'cycling', 'duration': 30, 'frequency': '2 days/week'}
            ]

        return recommendations

    def calculate_tdee(self, weight_kg, height_cm, age, gender, activity_level):
        # Calculate BMR (Basal Metabolic Rate) using Mifflin-St Jeor Equation
        if gender.lower() == 'male':
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        # Activity multipliers
        multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extremely_active': 1.9
        }

        multiplier = multipliers.get(activity_level, 1.2)
        tdee = bmr * multiplier

        return round(tdee, 0)
