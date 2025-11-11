
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


class NutritionAnalyzer:
    def __init__(self):
        self.daily_requirements = {
            'calories': 2000, 'protein': 50, 'carbs': 250, 'fats': 70, 'fiber': 25
        }
        # Essential food database (per 100g) - easily extensible
        self.food_database = {
            'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fats': 0.3, 'fiber': 0.4},
            'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fats': 3.6, 'fiber': 0},
            'broccoli': {'calories': 34, 'protein': 2.8, 'carbs': 7, 'fats': 0.4, 'fiber': 2.6},
            'eggs': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fats': 11, 'fiber': 0},
            'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23, 'fats': 0.3, 'fiber': 2.6},
        }

    def analyze_food_log(self, food_log):
        totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0}

        for entry in food_log:
            food = entry.get('food', '').lower()
            amount = entry.get('amount', 0)

            if food in self.food_database:
                # Calculate nutrition based on amount (per 100g reference)
                nutrition = self.food_database[food]
                multiplier = amount / 100

                for nutrient in totals:
                    totals[nutrient] += nutrition[nutrient] * multiplier

        return totals

    def analyze_dietary_pattern(self, food_logs_history):
        daily_nutrition = []

        for daily_log in food_logs_history:
            nutrition = self.analyze_food_log(daily_log)
            daily_nutrition.append(nutrition)

        df = pd.DataFrame(daily_nutrition)

        # Calculate statistics
        avg_nutrition = df.mean().to_dict()
        pattern_analysis = {
            'average_daily': avg_nutrition,
            'adherence_to_requirements': {},
            'pattern_type': self._classify_pattern(avg_nutrition)
        }

        # Calculate adherence percentage
        for nutrient, value in avg_nutrition.items():
            if nutrient in self.daily_requirements:
                adherence = (value / self.daily_requirements[nutrient]) * 100
                pattern_analysis['adherence_to_requirements'][nutrient] = round(adherence, 1)

        return pattern_analysis

    def _classify_pattern(self, avg_nutrition):
        total_macros = avg_nutrition['protein'] + avg_nutrition['carbs'] + avg_nutrition['fats']

        if total_macros == 0:
            return 'insufficient_data'

        protein_ratio = avg_nutrition['protein'] / total_macros
        carb_ratio = avg_nutrition['carbs'] / total_macros
        fat_ratio = avg_nutrition['fats'] / total_macros

        if protein_ratio > 0.35:
            return 'high_protein'
        elif carb_ratio > 0.50:
            return 'high_carb'
        elif fat_ratio > 0.35:
            return 'high_fat'
        else:
            return 'balanced'

    def cluster_dietary_patterns(self, multiple_users_data):
        if len(multiple_users_data) < 3:
            return None, None

        features = [[d.get(n, 0) for n in ['calories', 'protein', 'carbs', 'fats', 'fiber']]
                    for d in multiple_users_data]
        kmeans = KMeans(n_clusters=min(3, len(features)), random_state=42, n_init=10)
        return kmeans.fit_predict(features), kmeans.cluster_centers_

    def get_nutritional_gaps(self, current_nutrition):
        return {
            nutrient: {
                'current': round(current := current_nutrition.get(nutrient, 0), 1),
                'required': requirement,
                'deficit': round(requirement - current, 1),
                'percentage': round((current / requirement) * 100, 1)
            }
            for nutrient, requirement in self.daily_requirements.items()
            if current_nutrition.get(nutrient, 0) < requirement * 0.8
        }
