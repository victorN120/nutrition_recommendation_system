# Nutrition and Exercise Recommendation Engine

A personalized nutrition and fitness recommendation system that analyzes dietary habits and physical activity to provide actionable recommendations for disease prevention and healthy living.

## Overview

This system demonstrates the implementation of a modular health recommendation engine that:
- Analyzes dietary patterns using clustering algorithms
- Tracks and evaluates physical activity levels
- Generates personalized nutrition and exercise recommendations
- Predicts future progress using machine learning
- Monitors user progress toward health goals

## Features

### 1. Nutrition Analysis
- Food database with nutritional information
- Dietary pattern classification (high protein, high carb, balanced, etc.)
- Nutritional gap detection
- Adherence tracking to daily requirements
- K-means clustering for dietary pattern grouping

### 2. Activity Tracking
- MET (Metabolic Equivalent of Task) based calorie calculations
- Activity level classification
- TDEE (Total Daily Energy Expenditure) calculation
- Consistency scoring
- Multiple activity type support

### 3. Recommendation Engine
- Personalized nutrition plans based on goals
- Exercise recommendations with weekly schedules
- Cultural dietary preference consideration
- Disease prevention guidelines integration
- Priority action identification

### 4. Progress Monitoring
- Historical data analysis
- Linear regression for future predictions
- Goal probability calculations
- Trend identification
- Progress report generation

## Project Structure

```
nutrition_recommendation_system/
├── modules/
│   ├── __init__.py
│   ├── nutrition_analyzer.py      # Dietary analysis and pattern detection
│   ├── activity_tracker.py        # Physical activity tracking
│   ├── recommendation_engine.py   # Recommendation generation
│   └── progress_monitor.py        # Progress tracking and prediction
├── main.py                         # Main pipeline and CLI interface
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Requirements

- Python 3.7+
- numpy
- pandas
- scikit-learn

## Installation

1. Clone or download this project

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the System

Simply run the main script:
```bash
python main.py
```

The system will:
1. Load sample user data
2. Analyze dietary patterns
3. Analyze activity levels
4. Generate personalized recommendations
5. Predict progress toward goals
6. Save results to `results.json`

### Using Custom Data

You can modify the `load_sample_data()` function in `main.py` to use your own data:

```python
user_data = {
    'profile': {
        'age': 30,
        'weight': 75,  # kg
        'height': 170,  # cm
        'gender': 'male',
        'goal': 'weight_loss',  # 'weight_loss', 'muscle_gain', 'general_health'
        'health_focus': 'general_health',  # 'heart_disease', 'diabetes', 'obesity', 'general_health'
        'cultural_preference': 'western'  # 'mediterranean', 'asian', 'vegetarian', 'western'
    },
    'food_logs_history': [
        # Daily food logs
        [
            {'food': 'chicken', 'amount': 150},  # amount in grams
            {'food': 'rice', 'amount': 200},
            # ... more foods
        ],
        # ... more days
    ],
    'activity_logs_history': [
        # Daily activity logs
        [
            {'activity': 'jogging', 'duration': 30},  # duration in minutes
            {'activity': 'sedentary', 'duration': 480},
            # ... more activities
        ],
        # ... more days
    ],
    'progress_history': [
        # Daily progress tracking
        {'day': 1, 'weight': 77, 'calories': 2100, 'target_calories': 2000, 'active_minutes': 30},
        # ... more days
    ],
    'goal_info': {
        'metric': 'weight',
        'target_value': 72,
        'target_days': 60
    }
}
```

## Skills Demonstrated

### AI/ML Implementation
- **K-means Clustering**: Groups users with similar dietary patterns
- **Linear Regression**: Predicts future progress based on historical data
- **Pattern Recognition**: Classifies dietary patterns and activity levels
- **Goal Tracking**: Calculates probability of reaching health goals

### Critical Thinking
- Considers nutrition science principles (macronutrient ratios, calorie balance)
- Accommodates cultural dietary preferences
- Balances restriction with sustainability
- Applies disease prevention guidelines

### Problem Solving
- Handles incomplete food logs gracefully
- Adapts to varying activity levels
- Manages dietary restrictions
- Provides progressive overload for beginners

### Modular Structure
- **Nutrition Analyzer**: Separate module for dietary analysis
- **Activity Tracker**: Independent physical activity tracking
- **Recommendation Engine**: Centralized recommendation logic
- **Progress Monitor**: Standalone progress tracking and predictions

### Clear Architecture
The system follows a clear pipeline:
```
User Input → Pattern Analysis → Goal Setting → Personalized Recommendations
```

## Available Foods

The system includes a database of common foods:
- Grains: rice, bread, pasta, oatmeal
- Proteins: chicken, salmon, eggs, beans
- Dairy: milk, yogurt
- Vegetables: broccoli, spinach
- Fruits: apple, banana
- Nuts: almonds

You can extend this by adding more foods to the `food_database` in `nutrition_analyzer.py`.

## Available Activities

Supported activities with MET values:
- walking, jogging, running
- cycling, swimming
- yoga, weightlifting
- dancing, hiking
- basketball, tennis
- sedentary (desk work)

## Sample Output

```
============================================================
NUTRITION & EXERCISE RECOMMENDATION SYSTEM
============================================================

[STEP 1] Analyzing dietary patterns...

  Average Daily Nutrition:
    • Calories: 1103.6
    • Protein: 96.5
    • Carbs: 119.4
    • Fats: 26.3
    • Fiber: 13.9

  Dietary Pattern: High Protein

  Adherence to Requirements:
    [LOW] Calories: 55.2%
    [OK] Protein: 193.1%

...

[NUTRITION] Recommendations:
    • Daily Calorie Target: 2668 calories
    • Macronutrient Targets:
      - Protein: 30%
      - Carbs: 40%
      - Fats: 30%

[EXERCISE] Recommendations:
    • Weekly Target: 250 minutes
    • Intensity: Moderate To Vigorous
```

## Future Enhancements

- Add more foods to the database
- Implement meal planning features
- Add data visualization with matplotlib
- Create a web interface
- Implement user authentication
- Add more sophisticated ML models (Random Forest, Neural Networks)
- Include micronutrient tracking
- Add recipe suggestions
- Implement social features for motivation

## Assignment Requirements Met

- ✓ AI/ML: K-means clustering for dietary patterns, linear regression for predictions
- ✓ Critical Thinking: Nutrition science, cultural preferences, sustainability
- ✓ Problem Solving: Handles incomplete data, varying activity levels, restrictions
- ✓ Modular Structure: 4 separate modules with clear responsibilities
- ✓ Clear Architecture: Pipeline from inputs to recommendations

## License

This project is created for educational purposes as a coding assignment.

## Author

Created as a coding assignment demonstrating nutrition and exercise recommendation system implementation.
