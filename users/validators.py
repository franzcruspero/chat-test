import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from users.enums import PasswordValidationErrors


class CommonPasswordValidator:
    """
    Validate that the password isn't a simple common pattern.
    Rejects passwords based on common words, even with character substitutions.
    """
    
    def __init__(self):
        # Common password bases to check against
        self.common_bases = [
            'password', 'admin', 'welcome', 'test', 'user',
            'qwerty', 'letmein', 'guest', 'default'
        ]
        
        # L33t speak substitutions
        self.leet_substitutions = {
            'a': ['@', '4'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['$', '5']
        }
        
        # Pre-compile patterns for better performance
        self.patterns = self.compile_patterns()

    def _get_char_pattern(self, char):
        """Helper method to generate pattern for a single character"""
        if char in self.leet_substitutions:
            chars = [char] + self.leet_substitutions[char]
            return f'[{"".join(chars)}]'
        return f'[{char}{char.upper()}]'

    def _create_base_pattern(self, base):
        """Helper method to create pattern parts for a password base"""
        pattern_parts = map(self._get_char_pattern, base)
        pattern = ''.join(pattern_parts)
        
        # Recurring Patterns
        non_alpha = r'[^a-zA-Z]'
        non_alpha_start = r'^' + non_alpha + r'*'
        non_alpha_end = non_alpha + r'*$'
        
        return [
            (non_alpha_start + pattern + non_alpha_end),
            (non_alpha + pattern + non_alpha)
        ]

    def compile_patterns(self):
        """Generate regex patterns including common variations."""
        # Generate all patterns using list comprehension and flatten the result
        pattern_strings = [
            pattern 
            for base in self.common_bases
            for pattern in self._create_base_pattern(base)
        ]
        
        # Compile all patterns
        return [re.compile(p, re.IGNORECASE) for p in pattern_strings]

    def validate(self, password, user=None):
        """
        Validate that the password is not a common pattern, even with modifications.
        Always raises the same error message for consistency.
        """
        # First check: direct pattern matching
        if any(pattern.search(password) for pattern in self.patterns):
            raise ValidationError(
                PasswordValidationErrors.TOO_COMMON.value,
                code='password_too_common',
            )
        
        # Second check: exact match after stripping non-letters
        base_password = re.sub(r'[^a-zA-Z]', '', password.lower())
        if base_password in self.common_bases:
            raise ValidationError(
                PasswordValidationErrors.TOO_COMMON.value,
                code='password_too_common',
            )

    def get_help_text(self):
        return PasswordValidationErrors.HELP_TEXT.value