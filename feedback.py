import json
import os
from datetime import datetime

class FeedbackManager:
    def __init__(self, feedback_file="feedback_history.json"):
        """
        Initialize FeedbackManager with a file to store feedback history.
        
        Args:
            feedback_file (str): Name of the file to store feedback history
        """
        self.feedback_file = feedback_file
        self.feedback_history = self._load_feedback_history()

    def _load_feedback_history(self):
        """
        Load feedback history from file if it exists.
        
        Returns:
            list: List of feedback entries
        """
        try:
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading feedback history: {str(e)}")
            return []

    def _save_feedback_history(self):
        """
        Save feedback history to file.
        """
        try:
            with open(self.feedback_file, 'w') as f:
                json.dump(self.feedback_history, f, indent=4)
        except Exception as e:
            print(f"Error saving feedback history: {str(e)}")

    def update_feedback(self, original_prediction, corrected_prediction):
        """
        Update feedback history with new correction.
        
        Args:
            original_prediction (str): Original model prediction
            corrected_prediction (str): User-corrected prediction
        """
        try:
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "original_prediction": original_prediction,
                "corrected_prediction": corrected_prediction
            }
            
            self.feedback_history.append(feedback_entry)
            self._save_feedback_history()
            
            # Simulate model learning from feedback
            self._simulate_learning(feedback_entry)
            
        except Exception as e:
            print(f"Error updating feedback: {str(e)}")

    def _simulate_learning(self, feedback_entry):
        """
        Simulate the model learning from feedback.
        In a real implementation, this would update the model's weights or parameters.
        
        Args:
            feedback_entry (dict): The feedback entry to learn from
        """
        try:
            print(f"Learning from feedback: Model prediction '{feedback_entry['original_prediction']}' "
                  f"corrected to '{feedback_entry['corrected_prediction']}'")
            
            # Calculate and display simple statistics
            total_corrections = len(self.feedback_history)
            correction_types = {}
            
            for entry in self.feedback_history:
                key = f"{entry['original_prediction']} → {entry['corrected_prediction']}"
                correction_types[key] = correction_types.get(key, 0) + 1
            
            print(f"\nFeedback Statistics:")
            print(f"Total corrections: {total_corrections}")
            print("Correction patterns:")
            for pattern, count in correction_types.items():
                print(f"  {pattern}: {count} times")
                
        except Exception as e:
            print(f"Error in learning simulation: {str(e)}")

    def get_feedback_statistics(self):
        """
        Get statistics about the feedback history.
        
        Returns:
            dict: Statistics about the feedback history
        """
        try:
            total_corrections = len(self.feedback_history)
            correction_types = {}
            
            for entry in self.feedback_history:
                key = f"{entry['original_prediction']} → {entry['corrected_prediction']}"
                correction_types[key] = correction_types.get(key, 0) + 1
            
            return {
                "total_corrections": total_corrections,
                "correction_patterns": correction_types
            }
            
        except Exception as e:
            print(f"Error getting feedback statistics: {str(e)}")
            return {"total_corrections": 0, "correction_patterns": {}}