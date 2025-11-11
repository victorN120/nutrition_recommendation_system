
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class ProgressMonitor:
    def __init__(self):
        self.prediction_model = LinearRegression()

    def track_progress(self, historical_data):
        if not historical_data or len(historical_data) < 2:
            return {'status': 'insufficient_data', 'message': 'Need at least 2 data points'}

        df = pd.DataFrame(historical_data)

        progress = {
            'timeline': [],
            'trends': {},
            'achievements': [],
            'areas_for_improvement': []
        }

        # Weight trend
        if 'weight' in df.columns:
            weight_trend = self._calculate_trend(df['weight'].values)
            progress['trends']['weight'] = {
                'direction': weight_trend['direction'],
                'change': weight_trend['total_change'],
                'average_weekly_change': weight_trend['avg_weekly_change']
            }

            # Check achievements
            if abs(weight_trend['total_change']) >= 2:
                progress['achievements'].append(
                    f"Weight change: {weight_trend['total_change']:.1f} kg"
                )

        # Activity trend
        if 'active_minutes' in df.columns:
            activity_trend = self._calculate_trend(df['active_minutes'].values)
            progress['trends']['activity'] = {
                'direction': activity_trend['direction'],
                'change': activity_trend['total_change'],
                'current_avg': activity_trend['current_avg']
            }

            if activity_trend['direction'] == 'increasing':
                progress['achievements'].append(
                    f"Activity increased by {activity_trend['total_change']:.0f} minutes/day"
                )

        # Calorie adherence
        if 'calories' in df.columns and 'target_calories' in df.columns:
            adherence = self._calculate_adherence(
                df['calories'].values,
                df['target_calories'].values
            )
            progress['trends']['calorie_adherence'] = adherence

            if adherence['average_adherence'] < 80:
                progress['areas_for_improvement'].append(
                    f"Calorie adherence at {adherence['average_adherence']:.0f}% - aim for 90%+"
                )

        # Generate timeline
        progress['timeline'] = self._generate_timeline(df)

        return progress

    def predict_future_progress(self, historical_data, days_ahead=30):
        if not historical_data or len(historical_data) < 3:
            return {'status': 'insufficient_data', 'message': 'Need at least 3 data points'}

        # Predict multiple metrics in one loop
        metrics = ['weight', 'active_minutes', 'calories']
        return {metric: self._predict_metric([d[metric] for d in historical_data], days_ahead)
                for metric in metrics if all(metric in d for d in historical_data)}

    def calculate_goal_probability(self, historical_data, goal_value, goal_metric, target_days):
        if len(historical_data) < 3:
            return {'probability': 'unknown', 'message': 'Need more data'}

        values = [d.get(goal_metric, 0) for d in historical_data if goal_metric in d]
        if not values:
            return {'probability': 'unknown', 'message': f'No data for {goal_metric}'}

        prediction = self._predict_metric(values, target_days)
        current_value, predicted_value = values[-1], prediction['predicted_value']
        goal_change = goal_value - current_value
        predicted_change = predicted_value - current_value

        probability = min(100, max(0, (predicted_change / goal_change * 100) if abs(goal_change) > 0.01 else 0))

        interpretations = {
            80: 'You are on track to reach your goal!',
            50: 'You may reach your goal with consistent effort',
            0: 'Consider adjusting your plan to reach your goal'
        }
        interpretation = next((msg for threshold, msg in sorted(interpretations.items(), reverse=True)
                              if probability >= threshold), interpretations[0])

        return {
            'probability': f"{probability:.0f}%",
            'current_value': round(current_value, 1),
            'goal_value': goal_value,
            'predicted_value': round(predicted_value, 1),
            'current_trend': self._calculate_trend(np.array(values))['direction'],
            'days_to_goal': target_days,
            'interpretation': interpretation
        }

    def _calculate_trend(self, values):
        if len(values) < 2:
            return {'direction': 'stable', 'total_change': 0, 'avg_weekly_change': 0}

        total_change = values[-1] - values[0]
        avg_change_per_day = total_change / len(values)
        avg_weekly_change = avg_change_per_day * 7
        current_avg = np.mean(values[-7:]) if len(values) >= 7 else np.mean(values)

        # Determine direction
        if abs(total_change) < 0.5:
            direction = 'stable'
        elif total_change > 0:
            direction = 'increasing'
        else:
            direction = 'decreasing'

        return {
            'direction': direction,
            'total_change': round(total_change, 2),
            'avg_weekly_change': round(avg_weekly_change, 2),
            'current_avg': round(current_avg, 2)
        }

    def _calculate_adherence(self, actual_values, target_values):
        adherences = []

        for actual, target in zip(actual_values, target_values):
            if target > 0:
                adherence = (actual / target) * 100
                # Cap at 100% for over-achievement scenarios
                adherence = min(100, adherence)
                adherences.append(adherence)

        avg_adherence = np.mean(adherences) if adherences else 0

        return {
            'average_adherence': round(avg_adherence, 1),
            'consistency': round(np.std(adherences), 1) if len(adherences) > 1 else 0
        }

    def _predict_metric(self, values, days_ahead):
        X = np.array(range(len(values))).reshape(-1, 1)
        y = np.array(values)

        # Fit model
        self.prediction_model.fit(X, y)

        # Predict
        future_day = len(values) + days_ahead - 1
        predicted_value = self.prediction_model.predict([[future_day]])[0]

        # Calculate confidence (simplified using R² score)
        score = self.prediction_model.score(X, y)
        confidence = max(0, min(100, score * 100))

        return {
            'predicted_value': round(predicted_value, 2),
            'confidence': f"{confidence:.0f}%",
            'days_ahead': days_ahead
        }

    def _generate_timeline(self, df):
        if len(df) == 0:
            return []
        return [
            {'day': 1, 'event': 'Started tracking', 'data': df.iloc[0].to_dict()},
            {'day': len(df), 'event': 'Current status', 'data': df.iloc[-1].to_dict()}
        ] if len(df) > 1 else [{'day': 1, 'event': 'Started tracking', 'data': df.iloc[0].to_dict()}]

    def generate_progress_report(self, historical_data, goal_info):
        report = {
            'summary': {},
            'progress_tracking': {},
            'predictions': {},
            'goal_analysis': {},
            'recommendations': []
        }

        # Progress tracking
        progress = self.track_progress(historical_data)
        report['progress_tracking'] = progress

        # Predictions
        predictions = self.predict_future_progress(historical_data, 30)
        report['predictions'] = predictions

        # Goal analysis
        if goal_info and 'metric' in goal_info:
            goal_analysis = self.calculate_goal_probability(
                historical_data,
                goal_info.get('target_value', 0),
                goal_info.get('metric', 'weight'),
                goal_info.get('target_days', 90)
            )
            report['goal_analysis'] = goal_analysis

        # Generate recommendations
        report['recommendations'] = self._generate_progress_recommendations(
            progress,
            predictions,
            report.get('goal_analysis', {})
        )

        # Summary
        report['summary'] = {
            'days_tracked': len(historical_data),
            'achievements_count': len(progress.get('achievements', [])),
            'areas_for_improvement_count': len(progress.get('areas_for_improvement', []))
        }

        return report

    def _generate_progress_recommendations(self, progress, predictions, goal_analysis):
        recommendations = []
        trends = progress.get('trends', {})

        if trends.get('weight', {}).get('direction') == 'stable':
            recommendations.append("Consider adjusting calorie intake or activity level")

        if trends.get('activity', {}).get('direction') == 'decreasing':
            recommendations.append("Activity has decreased - schedule specific workout times")

        if 'probability' in goal_analysis:
            try:
                prob = float(goal_analysis['probability'].rstrip('%'))
                if prob < 50:
                    recommendations.append("Increase efforts to reach your goal - revise your plan")
            except ValueError:
                pass

        return recommendations if recommendations else ["Keep up the good work and stay consistent!"]
