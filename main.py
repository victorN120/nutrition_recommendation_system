
import sys
import json
import numpy as np
from modules.nutrition_analyzer import NutritionAnalyzer
from modules.activity_tracker import ActivityTracker
from modules.recommendation_engine import RecommendationEngine
from modules.progress_monitor import ProgressMonitor


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


class NutritionRecommendationSystem:
    def __init__(self):
        self.nutrition_analyzer = NutritionAnalyzer()
        self.activity_tracker = ActivityTracker()
        self.recommendation_engine = RecommendationEngine()
        self.progress_monitor = ProgressMonitor()

    def run_analysis(self, user_data):
        print("\n" + "="*60)
        print("NUTRITION & EXERCISE RECOMMENDATION SYSTEM")
        print("="*60 + "\n")

        results = {
            'user_profile': user_data.get('profile', {}),
            'nutrition_analysis': {},
            'activity_analysis': {},
            'recommendations': {},
            'progress_report': {}
        }

        # 1. Analyze Nutrition
        print("[STEP 1] Analyzing dietary patterns...")
        if 'food_logs_history' in user_data:
            nutrition_analysis = self.nutrition_analyzer.analyze_dietary_pattern(
                user_data['food_logs_history']
            )
            results['nutrition_analysis'] = nutrition_analysis

            # Get nutritional gaps
            avg_nutrition = nutrition_analysis.get('average_daily', {})
            gaps = self.nutrition_analyzer.get_nutritional_gaps(avg_nutrition)
            results['nutrition_analysis']['gaps'] = gaps

            self._print_nutrition_analysis(nutrition_analysis, gaps)

        # 2. Analyze Activity
        print("\n[STEP 2] Analyzing physical activity...")
        if 'activity_logs_history' in user_data:
            activity_analysis = self.activity_tracker.analyze_activity_history(
                user_data['activity_logs_history'],
                user_data['profile'].get('weight', 70)
            )
            results['activity_analysis'] = activity_analysis

            self._print_activity_analysis(activity_analysis)

        # 3. Calculate TDEE
        profile = user_data.get('profile', {})
        if all(k in profile for k in ['weight', 'height', 'age', 'gender']):
            tdee = self.activity_tracker.calculate_tdee(
                profile['weight'],
                profile['height'],
                profile['age'],
                profile['gender'],
                results.get('activity_analysis', {}).get('activity_level', 'sedentary')
            )
            profile['tdee'] = tdee
            results['user_profile']['tdee'] = tdee
            print(f"\nYour Total Daily Energy Expenditure (TDEE): {tdee} calories")

        # 4. Generate Recommendations
        print("\n[STEP 3] Generating personalized recommendations...")
        recommendations = self.recommendation_engine.generate_recommendations(
            profile,
            results.get('nutrition_analysis', {}),
            results.get('activity_analysis', {})
        )
        results['recommendations'] = recommendations

        self._print_recommendations(recommendations)

        # 5. Track Progress (if historical data available)
        if 'progress_history' in user_data and len(user_data['progress_history']) > 0:
            print("\n[STEP 4] Analyzing progress and predicting outcomes...")
            progress_report = self.progress_monitor.generate_progress_report(
                user_data['progress_history'],
                user_data.get('goal_info', {})
            )
            results['progress_report'] = progress_report

            self._print_progress_report(progress_report)

        print("\n" + "="*60)
        print("Analysis Complete!")
        print("="*60 + "\n")

        return results

    def _print_nutrition_analysis(self, analysis, gaps):
        print("\n  Average Daily Nutrition:")
        avg = analysis.get('average_daily', {})
        for nutrient, value in avg.items():
            print(f"    • {nutrient.capitalize()}: {value:.1f}")

        print(f"\n  Dietary Pattern: {analysis.get('pattern_type', 'unknown').replace('_', ' ').title()}")

        print("\n  Adherence to Requirements:")
        adherence = analysis.get('adherence_to_requirements', {})
        for nutrient, percentage in adherence.items():
            status = "[OK]" if percentage >= 80 else "[LOW]"
            print(f"    {status} {nutrient.capitalize()}: {percentage}%")

        if gaps:
            print("\n  [WARNING] Nutritional Gaps Detected:")
            for nutrient, info in gaps.items():
                print(f"    • {nutrient.capitalize()}: {info['current']}/{info['required']} ({info['percentage']}%)")

    def _print_activity_analysis(self, analysis):
        print(f"\n  Activity Level: {analysis.get('activity_level', 'unknown').replace('_', ' ').title()}")
        print(f"  Average Daily Active Minutes: {analysis.get('average_daily_active_minutes', 0):.0f}")
        print(f"  Average Daily Calories Burned: {analysis.get('average_daily_calories_burned', 0):.0f}")
        print(f"  Weekly Active Minutes: {analysis.get('weekly_active_minutes', 0):.0f}")
        print(f"  Consistency Score: {analysis.get('consistency_score', 0)}%")

    def _print_recommendations(self, recommendations):
        # Nutrition recommendations
        print("\n  [NUTRITION] Recommendations:")
        nutrition = recommendations.get('nutrition', {})
        print(f"    • Daily Calorie Target: {nutrition.get('calorie_target', 0)} calories")

        print("    • Macronutrient Targets:")
        for macro, target in nutrition.get('macronutrient_targets', {}).items():
            print(f"      - {macro.capitalize()}: {target}")

        if nutrition.get('foods_to_increase'):
            print("    • Foods to Increase:")
            for food in nutrition.get('foods_to_increase', [])[:3]:
                print(f"      - {food.capitalize()}")

        # Exercise recommendations
        print("\n  [EXERCISE] Recommendations:")
        exercise = recommendations.get('exercise', {})
        print(f"    • Weekly Target: {exercise.get('weekly_target_minutes', 0)} minutes")
        print(f"    • Intensity: {exercise.get('intensity_level', 'moderate').replace('_', ' ').title()}")

        if exercise.get('activity_plan'):
            print("    • Weekly Activity Plan:")
            for day_plan in exercise['activity_plan'][:3]:
                if day_plan['duration'] > 0:
                    print(f"      - {day_plan['day']}: {day_plan['activity']} ({day_plan['duration']} min)")

        # Priority actions
        print("\n  [PRIORITY] Actions:")
        priorities = recommendations.get('priority_actions', [])
        if priorities:
            for i, action in enumerate(priorities, 1):
                print(f"    {i}. {action}")
        else:
            print("    • Keep maintaining your current healthy lifestyle!")

    def _print_progress_report(self, report):
        summary = report.get('summary', {})
        print(f"\n  Days Tracked: {summary.get('days_tracked', 0)}")
        print(f"  Achievements: {summary.get('achievements_count', 0)}")

        # Trends
        trends = report.get('progress_tracking', {}).get('trends', {})
        if trends:
            print("\n  Trends:")
            for metric, trend_data in trends.items():
                if isinstance(trend_data, dict) and 'direction' in trend_data:
                    direction = trend_data['direction']
                    symbol = "[UP]" if direction == "increasing" else "[DOWN]" if direction == "decreasing" else "[STABLE]"
                    print(f"    {symbol} {metric.capitalize()}: {direction}")

        # Goal analysis
        goal = report.get('goal_analysis', {})
        if 'probability' in goal:
            print(f"\n  [GOAL] Progress:")
            print(f"    • Probability of reaching goal: {goal['probability']}")
            print(f"    • {goal.get('interpretation', '')}")

        # Recommendations
        recs = report.get('recommendations', [])
        if recs:
            print("\n  [PROGRESS] Recommendations:")
            for rec in recs:
                print(f"    • {rec}")


def load_sample_data():
    return {
        'profile': {
            'age': 30,
            'weight': 75,  # kg
            'height': 170,  # cm
            'gender': 'male',
            'goal': 'weight_loss',
            'health_focus': 'general_health',
            'cultural_preference': 'western'
        },
        'food_logs_history': [
            # Day 1
            [
                {'food': 'oatmeal', 'amount': 100},
                {'food': 'banana', 'amount': 120},
                {'food': 'chicken', 'amount': 150},
                {'food': 'rice', 'amount': 200},
                {'food': 'broccoli', 'amount': 100},
                {'food': 'salmon', 'amount': 150},
                {'food': 'spinach', 'amount': 100}
            ],
            # Day 2
            [
                {'food': 'eggs', 'amount': 100},
                {'food': 'bread', 'amount': 80},
                {'food': 'chicken', 'amount': 180},
                {'food': 'pasta', 'amount': 150},
                {'food': 'broccoli', 'amount': 120},
                {'food': 'yogurt', 'amount': 150}
            ],
            # Day 3
            [
                {'food': 'yogurt', 'amount': 150},
                {'food': 'almonds', 'amount': 30},
                {'food': 'chicken', 'amount': 150},
                {'food': 'rice', 'amount': 180},
                {'food': 'beans', 'amount': 100},
                {'food': 'apple', 'amount': 150}
            ]
        ],
        'activity_logs_history': [
            # Day 1
            [
                {'activity': 'jogging', 'duration': 30},
                {'activity': 'sedentary', 'duration': 480}
            ],
            # Day 2
            [
                {'activity': 'cycling', 'duration': 40},
                {'activity': 'sedentary', 'duration': 460}
            ],
            # Day 3
            [
                {'activity': 'walking', 'duration': 45},
                {'activity': 'yoga', 'duration': 30},
                {'activity': 'sedentary', 'duration': 400}
            ]
        ],
        'progress_history': [
            {'day': 1, 'weight': 77, 'calories': 2100, 'target_calories': 2000, 'active_minutes': 30},
            {'day': 2, 'weight': 76.8, 'calories': 1950, 'target_calories': 2000, 'active_minutes': 40},
            {'day': 3, 'weight': 76.5, 'calories': 2050, 'target_calories': 2000, 'active_minutes': 75},
            {'day': 4, 'weight': 76.3, 'calories': 1980, 'target_calories': 2000, 'active_minutes': 45},
            {'day': 5, 'weight': 76.0, 'calories': 2020, 'target_calories': 2000, 'active_minutes': 50}
        ],
        'goal_info': {
            'metric': 'weight',
            'target_value': 72,
            'target_days': 60
        }
    }


def main():
    system = NutritionRecommendationSystem()

    # Load sample data
    print("Loading sample user data...")
    user_data = load_sample_data()

    # Run analysis
    results = system.run_analysis(user_data)

    # Optionally save results to file
    print("\nSaving results to 'results.json'...")
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)

    print("[SUCCESS] Results saved successfully!")
    print("\nThank you for using the Nutrition & Exercise Recommendation System!")


if __name__ == "__main__":
    main()
