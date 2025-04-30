import tkinter as tk
from tkinter import messagebox, font
import time
import random
from typing import List, Optional


class TypingSpeedCalculator:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Calculator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Sample texts
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog. This sentence contains all the letters in the English alphabet.",
            "Programming is the process of creating a set of instructions that tell a computer how to perform a task. Programming can be done using a variety of computer programming languages.",
            "Python is an interpreted, high-level, general-purpose programming language. Its design philosophy emphasizes code readability with its use of significant indentation.",
            "The greatest glory in living lies not in never falling, but in rising every time we fall. The way to get started is to quit talking and begin doing.",
            "Life is what happens when you're busy making other plans. Spread love everywhere you go. Let no one ever come to you without leaving happier."
        ]
        
        # Test variables
        self.current_text = ""
        self.start_time = 0
        self.timer_running = False
        self.timer_id = None
        
        # Create UI elements
        self.setup_ui()
        
        # Start with a new test
        self.start_new_test()
    
    def setup_ui(self):
        #Set up the user interface components.
        # Custom fonts
        title_font = font.Font(family="Arial", size=16, weight="bold")
        text_font = font.Font(family="Arial", size=12)
        input_font = font.Font(family="Courier", size=12)
        result_font = font.Font(family="Arial", size=14, weight="bold")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        self.title_label = tk.Label(
            main_frame, 
            text="Typing Speed Calculator", 
            font=title_font, 
            bg="#f0f0f0", 
            fg="#333333", 
            pady=10
        )
        self.title_label.pack(fill=tk.X)
        
        # Instructions
        instructions = tk.Label(
            main_frame, 
            text="Type the text below as quickly and accurately as possible:", 
            font=text_font, 
            bg="#f0f0f0", 
            fg="#555555", 
            anchor="w", 
            pady=5
        )
        instructions.pack(fill=tk.X)
        
        # Sample text display frame
        text_frame = tk.Frame(main_frame, bg="#454545", relief=tk.SUNKEN, bd=1, padx=10, pady=10)
        text_frame.pack(fill=tk.X, pady=10)
        
        # Sample text display
        self.sample_text_display = tk.Text(
            text_frame, 
            font=text_font, 
            bg="#ffffff", 
            fg="#454545", 
            wrap=tk.WORD, 
            height=5, 
            padx=5, 
            pady=5
        )
        self.sample_text_display.pack(fill=tk.X)
        self.sample_text_display.config(state=tk.DISABLED)  # Make it read-only
        
        # Timer display
        timer_frame = tk.Frame(main_frame, bg="#f0f0f0")
        timer_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.timer_label = tk.Label(
            timer_frame, 
            text="Time: 0.0s", 
            font=text_font, 
            bg="#f0f0f0", 
            fg="#555555"
        )
        self.timer_label.pack(side=tk.LEFT)
        
        # User input frame
        input_frame = tk.Frame(main_frame, bg="#454545", relief=tk.SUNKEN, bd=1, padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        # User input label
        input_label = tk.Label(
            input_frame, 
            text="Your typing:", 
            font=text_font, 
            bg="#e0e0e0", 
            fg="#333333", 
            anchor="w"
        )
        input_label.pack(fill=tk.X)
        
        # User input text field
        self.user_input = tk.Text(
            input_frame, 
            font=input_font, 
            bg="#ffffff", 
            fg="#333333", 
            wrap=tk.WORD, 
            height=5, 
            padx=5, 
            pady=5
        )
        self.user_input.pack(fill=tk.X)
        self.user_input.bind("<KeyRelease>", self.on_key_release)
        
        # Results frame
        self.results_frame = tk.Frame(main_frame, bg="#f0f0f0", pady=10)
        self.results_frame.pack(fill=tk.X)
        
        # Results labels
        self.wpm_label = tk.Label(
            self.results_frame, 
            text="WPM: --", 
            font=result_font, 
            bg="#f0f0f0", 
            fg="#333333", 
            padx=10
        )
        self.wpm_label.pack(side=tk.LEFT)
        
        self.accuracy_label = tk.Label(
            self.results_frame, 
            text="Accuracy: --%", 
            font=result_font, 
            bg="#f0f0f0", 
            fg="#333333", 
            padx=10
        )
        self.accuracy_label.pack(side=tk.LEFT)
        
        self.errors_label = tk.Label(
            self.results_frame, 
            text="Errors: --", 
            font=result_font, 
            bg="#f0f0f0", 
            fg="#333333", 
            padx=10
        )
        self.errors_label.pack(side=tk.LEFT)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0", pady=10)
        buttons_frame.pack(fill=tk.X)
        
        # Finish button
        self.finish_button = tk.Button(
            buttons_frame, 
            text="Finish Test", 
            font=text_font, 
            command=self.finish_test, 
            bg="#4CAF50", 
            fg="white", 
            padx=10, 
            pady=5,
            state=tk.DISABLED
        )
        self.finish_button.pack(side=tk.LEFT, padx=5)
        
        # Restart button
        self.restart_button = tk.Button(
            buttons_frame, 
            text="New Test", 
            font=text_font, 
            command=self.start_new_test, 
            bg="#2196F3", 
            fg="white", 
            padx=10, 
            pady=5
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        exit_button = tk.Button(
            buttons_frame, 
            text="Exit", 
            font=text_font, 
            command=self.root.destroy, 
            bg="#f44336", 
            fg="white", 
            padx=10, 
            pady=5
        )
        exit_button.pack(side=tk.LEFT, padx=5)
    
    def select_random_text(self) -> str:
        """Select a random text from the sample texts."""
        return random.choice(self.sample_texts)
    
    def start_new_test(self):
        """Initialize and start a new typing test."""
        # Stop timer if running
        if self.timer_running:
            self.root.after_cancel(self.timer_id)
            self.timer_running = False
        
        # Reset timer display
        self.start_time = 0
        self.elapsed_time = 0
        self.timer_label.config(text="Time: 0.0s")
        
        # Reset test data
        self.current_text = self.select_random_text()
        
        # Update sample text display
        self.sample_text_display.config(state=tk.NORMAL)
        self.sample_text_display.delete("1.0", tk.END)
        self.sample_text_display.insert("1.0", self.current_text)
        self.sample_text_display.config(state=tk.DISABLED)
        
        # Clear user input
        self.user_input.delete("1.0", tk.END)
        self.user_input.focus_set()
        
        # Reset result labels
        self.wpm_label.config(text="WPM: --")
        self.accuracy_label.config(text="Accuracy: --%")
        self.errors_label.config(text="Errors: --")
        
        # Reset buttons
        self.finish_button.config(state=tk.DISABLED)
    
    def on_key_release(self, event):
        """Handle key releases in the input field."""
        # Start timer on first keystroke
        if not self.timer_running and self.user_input.get("1.0", "end-1c"):
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()
            self.finish_button.config(state=tk.NORMAL)
    
    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {self.elapsed_time:.1f}s")
            self.timer_id = self.root.after(100, self.update_timer)
    
    def finish_test(self):
        """End the test and display results."""
        if not self.timer_running:
            return
        
        # Stop timer
        self.root.after_cancel(self.timer_id)
        self.timer_running = False
        
        # Calculate results
        user_text = self.user_input.get("1.0", "end-1c")
        wpm = self.calculate_wpm(user_text)
        accuracy = self.calculate_accuracy(user_text)
        errors = self.count_errors(user_text)
        
        # Update result labels
        self.wpm_label.config(text=f"WPM: {wpm:.1f}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        self.errors_label.config(text=f"Errors: {errors}")
        
        # Show completion message
        messagebox.showinfo("Test Complete", 
                           f"Your results:\n"
                           f"- Time: {self.elapsed_time:.1f} seconds\n"
                           f"- WPM: {wpm:.1f}\n"
                           f"- Accuracy: {accuracy:.1f}%\n"
                           f"- Errors: {errors}")
    
    def calculate_wpm(self, user_text: str) -> float:
        """Calculate Words Per Minute (Net WPM)."""
        if not user_text or self.elapsed_time <= 0:
            return 0.0
        
        # Calculate uncorrected errors
        errors = self.count_errors(user_text)
        
        # A word is conventionally defined as 5 characters
        words = len(user_text) / 5
        minutes = self.elapsed_time / 60
        
        # Net WPM formula: (Total characters typed / 5 - Uncorrected errors) / Time in minutes
        net_wpm = (words - errors / 5) / minutes
        return max(0, net_wpm)  # Ensure WPM is not negative
    
    def calculate_accuracy(self, user_text: str) -> float:
        """Calculate typing accuracy as a percentage."""
        if not user_text:
            return 0.0
        
        errors = self.count_errors(user_text)
        total_chars = len(user_text)
        
        # Accuracy formula: ((Total characters - Errors) / Total characters) * 100
        if total_chars > 0:
            return max(0, ((total_chars - errors) / total_chars) * 100)
        return 0.0
    
    def count_errors(self, user_text: str) -> int:
        """Count the number of errors in the user input compared to the sample text."""
        errors = 0
        
        # Compare character by character
        for i in range(min(len(user_text), len(self.current_text))):
            if user_text[i] != self.current_text[i]:
                errors += 1
        
        # Add errors for length difference (too short or too long)
        errors += abs(len(user_text) - len(self.current_text))
        
        return errors


def main():
    """Main function to run the typing speed calculator."""
    root = tk.Tk()
    app = TypingSpeedCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()