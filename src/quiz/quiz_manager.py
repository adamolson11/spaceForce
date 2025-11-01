"""
QuizManager - Manages quiz timing, display, and result tracking
"""
import json
import time
import random
import os
from typing import Callable, Optional, Dict, List
import requests


class QuizManager:
    """
    Manages quiz lifecycle: timing, question selection, answer validation,
    and result persistence.
    """
    
    def __init__(
        self,
        questions_file: str,
        quiz_interval: float = 180.0,
        pause_callback: Optional[Callable] = None,
        resume_callback: Optional[Callable] = None,
        on_answer_callback: Optional[Callable[[bool, int], None]] = None,
        server_url: Optional[str] = None,
        demo_mode: bool = False
    ):
        """
        Initialize the QuizManager.
        
        Args:
            questions_file: Path to JSON file with quiz questions
            quiz_interval: Time in seconds between quizzes (default 180 = 3 minutes)
            pause_callback: Function to call when pausing the game for quiz
            resume_callback: Function to call when resuming the game after quiz
            on_answer_callback: Function to call when answer is submitted (receives correct: bool, coins: int)
            server_url: Optional URL to POST quiz results to
            demo_mode: If True, show first quiz after 10 seconds for quick testing
        """
        self.questions_file = questions_file
        self.quiz_interval = quiz_interval
        self.pause_callback = pause_callback
        self.resume_callback = resume_callback
        self.on_answer_callback = on_answer_callback
        self.server_url = server_url
        self.demo_mode = demo_mode
        
        # Load questions
        self.questions = self._load_questions()
        
        # Quiz state
        self.last_quiz_time = time.time()
        self.current_question = None
        self.quiz_active = False
        self.results_file = "quiz_results.json"
        self.results = self._load_results()
        
        # Demo mode: first quiz comes after 10 seconds
        if self.demo_mode:
            self.last_quiz_time = time.time() - (self.quiz_interval - 10.0)
    
    def _load_questions(self) -> List[Dict]:
        """Load questions from JSON file."""
        try:
            with open(self.questions_file, 'r') as f:
                questions = json.load(f)
            return questions
        except Exception as e:
            print(f"Error loading questions: {e}")
            return []
    
    def _load_results(self) -> List[Dict]:
        """Load quiz results from local file."""
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_results(self):
        """Save quiz results to local file."""
        try:
            with open(self.results_file, 'w') as f:
                json.dump(self.results, f, indent=2)
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def _post_result_to_server(self, result: Dict):
        """Post quiz result to server if URL is configured."""
        if not self.server_url:
            return
        
        try:
            response = requests.post(
                self.server_url,
                json=result,
                timeout=5
            )
            if response.status_code == 200:
                print("Quiz result posted to server successfully")
            else:
                print(f"Server returned status code: {response.status_code}")
        except Exception as e:
            print(f"Error posting to server: {e}")
    
    def check_and_show_quiz(self) -> bool:
        """
        Check if it's time to show a quiz. Call this from game loop.
        
        Returns:
            True if quiz is now active, False otherwise
        """
        if self.quiz_active:
            return True
        
        current_time = time.time()
        if current_time - self.last_quiz_time >= self.quiz_interval:
            self.start_quiz()
            return True
        
        return False
    
    def start_quiz(self):
        """Start a new quiz by selecting a question and pausing the game."""
        if not self.questions:
            print("No questions available!")
            return
        
        # Select a random question
        self.current_question = random.choice(self.questions)
        self.quiz_active = True
        
        # Pause the game
        if self.pause_callback:
            self.pause_callback()
        
        print(f"\n{'='*50}")
        print(f"QUIZ TIME!")
        print(f"{'='*50}")
    
    def get_current_question(self) -> Optional[Dict]:
        """Get the current quiz question."""
        return self.current_question
    
    def submit_answer(self, choice_index: int) -> bool:
        """
        Submit an answer to the current question.
        
        Args:
            choice_index: Index of the selected choice
            
        Returns:
            True if answer was correct, False otherwise
        """
        if not self.current_question or not self.quiz_active:
            return False
        
        correct = (choice_index == self.current_question['correct'])
        coins_earned = 10 if correct else 0
        
        # Record result
        result = {
            'timestamp': time.time(),
            'question_id': self.current_question['id'],
            'question': self.current_question['question'],
            'correct': correct,
            'coins_earned': coins_earned
        }
        
        self.results.append(result)
        self._save_results()
        
        # Post to server if configured
        self._post_result_to_server(result)
        
        # End quiz
        self.quiz_active = False
        self.last_quiz_time = time.time()
        self.current_question = None
        
        # Resume game
        if self.resume_callback:
            self.resume_callback()
        
        # Notify callback
        if self.on_answer_callback:
            self.on_answer_callback(correct, coins_earned)
        
        return correct
    
    def get_total_coins_earned(self) -> int:
        """Get total coins earned from all quizzes."""
        return sum(r['coins_earned'] for r in self.results)
    
    def get_quiz_stats(self) -> Dict:
        """Get quiz statistics."""
        if not self.results:
            return {
                'total_quizzes': 0,
                'correct_answers': 0,
                'accuracy': 0.0,
                'total_coins': 0
            }
        
        correct = sum(1 for r in self.results if r['correct'])
        total = len(self.results)
        
        return {
            'total_quizzes': total,
            'correct_answers': correct,
            'accuracy': (correct / total * 100) if total > 0 else 0.0,
            'total_coins': self.get_total_coins_earned()
        }
